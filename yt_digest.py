import os
import subprocess
import sys
import time
import json
import requests
from datetime import datetime

# ===== CONFIG =====
BASE_DIR = os.path.expanduser("~/AI_Trading")
LINK_FILE = os.path.join(BASE_DIR, "video_link.txt")
REPORT_FILE = os.path.join(BASE_DIR, "report_video.txt")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
# =================

def read_link():
    """Legge il primo link dal file video_link.txt."""
    try:
        with open(LINK_FILE, "r") as f:
            link = f.read().strip().splitlines()[0]
        return link if link else None
    except:
        return None

def download_video(link):
    """Scarica audio con yt-dlp e salva come audio.m4a."""
    temp_dir = os.path.join(BASE_DIR, "temp_video")
    os.makedirs(temp_dir, exist_ok=True)
    
    audio_file = os.path.join(temp_dir, "audio.m4a")
    cmd = [
        "yt-dlp",
        "--no-warnings",          # <-- aggiunto per silenziare avvisi Python
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "m4a",
        "--output", audio_file,
        link
    ]
    
    print(f"Download in corso da: {link}", flush=True)
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(audio_file):
            return audio_file
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Errore yt-dlp: {e.stderr.decode()}", flush=True)
        return None

def transcribe_audio(audio_path):
    """Trascrive l'audio con whisper (modello tiny)."""
    try:
        import whisper
        print("Caricamento modello whisper tiny...", flush=True)
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Errore whisper: {e}", flush=True)
        return ""

def analyze_with_ollama(text):
    """Invia la trascrizione a Ollama per analisi."""
    if not text:
        return "Nessuna trascrizione disponibile."
    
    prompt = f"""Sei un analista finanziario. Analizza il seguente testo estratto da un video di trading/forex.

Testo:
\"{text[:3000]}\"

Rispondi in italiano con una struttura chiara:
1. **Strategia principale** – descrivi la strategia proposta (entry, exit, stop loss, take profit, timeframe, indicatori, pattern).
2. **Sentiment** – positivo, negativo, neutro.
3. **Pattern candlestick** – eventuali pattern citati.
4. **Consigli pratici** – cosa suggerisce il video.
5. **Rischio** – eventuali avvertenze.

Sii conciso ma preciso.
"""
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 512}
        }, timeout=300)
        r.raise_for_status()
        return r.json()["response"].strip()
    except Exception as e:
        return f"Errore AI: {e}"

def generate_report(video_link, transcription, analysis):
    """Crea report completo."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""REPORT VIDEO - {now}
========================================
LINK ANALIZZATO: {video_link}

--- TRASCRIZIONE (estratto) ---
{transcription[:500]}{'...' if len(transcription)>500 else ''}

--- ANALISI AI ---
{analysis}
========================================
"""
    return report

def cleanup(temp_dir):
    """Rimuove cartella temporanea."""
    try:
        import shutil
        shutil.rmtree(temp_dir)
    except:
        pass

def main():
    print("=== YT-DIGEST AGENT ===", flush=True)
    link = read_link()
    if not link:
        print("Nessun link trovato in video_link.txt. Inserisci un link e riprova.", flush=True)
        return
    
    # 1. Download
    audio_path = download_video(link)
    if not audio_path:
        print("Download fallito.", flush=True)
        return
    
    # 2. Trascrizione
    print("Trascrizione in corso (richiede ~1-2 min)...", flush=True)
    transcription = transcribe_audio(audio_path)
    if not transcription:
        print("Trascrizione vuota o fallita.", flush=True)
        cleanup(os.path.dirname(audio_path))
        return
    
    print(f"Trascrizione ottenuta ({len(transcription)} caratteri).", flush=True)
    
    # 3. Analisi
    print("Analisi con Ollama in corso...", flush=True)
    analysis = analyze_with_ollama(transcription)
    
    # 4. Report
    report = generate_report(link, transcription, analysis)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"Report salvato in: {REPORT_FILE}", flush=True)
    
    # 5. Pulizia
    cleanup(os.path.dirname(audio_path))
    print("=== FATTO ===", flush=True)

if __name__ == "__main__":
    main()
