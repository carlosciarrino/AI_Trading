import os, subprocess, json, tempfile, logging, requests
import whisper

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def download_audio(url):
    """Scarica l'audio da YouTube/Instagram/TikTok usando yt-dlp."""
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            audio_file = f.name
        cmd = [
            "yt-dlp", "--cookies-from-browser", "brave", "--js-runtimes", "deno",
            "--cookies-from-browser", "brave",
            "-x", "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", audio_file,
            url
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"Audio scaricato: {audio_file}")
        return audio_file
    except Exception as e:
        logger.error(f"Errore download audio: {e}")
        return None

def transcribe_audio(audio_file, model_size="tiny"):
    """Trascrive l'audio con Whisper."""
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_file)
        os.unlink(audio_file)
        logger.info(f"Trascrizione completata ({len(result['text'])} caratteri)")
        return result['text']
    except Exception as e:
        logger.error(f"Errore trascrizione: {e}")
        return None

def extract_rules(text):
    """Estrae le regole della strategia dal testo con Ollama."""
    prompt = f"""
Sei un esperto di trading. Estrai le regole di una strategia in formato JSON. I campi devono essere: "entry", "exit", "sl", "tp". Usa condizioni semplici come "close > SMA(20)".
Formato JSON:
{{
  "name": "nome_strategia",
  "timeframe": "15min",
  "entry": "condizione di entrata",
  "exit": "condizione di uscita",
  "sl": "regola stop loss",
  "tp": "regola take profit",
  "filters": "filtri aggiuntivi"
}}

Testo:
{text[:3000]}
"""
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
            timeout=60
        )
        result = resp.json().get("response", "")
        # Estrai JSON
        import re
        match = re.search(r'\{.*\}', result, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        logger.error(f"Errore estrazione regole: {e}")
        return None

def analyze_video(url):
    """Pipeline completa: scarica audio → trascrive → estrae regole."""
    logger.info(f"📹 Analisi video: {url}")
    
    # 1. Scarica audio
    audio_file = download_audio(url)
    if not audio_file:
        return "Errore: impossibile scaricare l'audio. Verifica il link."
    
    # 2. Trascrivi
    transcript = transcribe_audio(audio_file, model_size="tiny")
    if not transcript:
        return "Errore: trascrizione fallita."
    
    # 3. Estrai regole
    rules = extract_rules(transcript)
    if not rules:
        return "Impossibile estrarre regole dalla trascrizione."
    
    # 4. Genera backtest (usa strategy_tester)
    from tools.strategy_tester import generate_backtest_code
    code = generate_backtest_code(rules)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(["python3", tmp], capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
    except Exception as e:
        output = f"Errore esecuzione: {e}"
    os.unlink(tmp)
    return f"📊 Regole estratte:\n{json.dumps(rules, indent=2)}\n\n📈 Backtest:\n{output}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(analyze_video(sys.argv[1]))
    else:
        print("Usa: python3 video_analyzer.py <link_video>")
