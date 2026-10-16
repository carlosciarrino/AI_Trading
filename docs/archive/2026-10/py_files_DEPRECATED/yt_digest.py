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

# Carica SpaCy una volta
try:
    import spacy
    nlp = spacy.load("it_core_news_sm")
except:
    nlp = None

def is_night():
    h = datetime.now().hour
    return h >= 22 or h < 6

def read_link():
    try:
        with open(LINK_FILE, "r") as f:
            link = f.read().strip().splitlines()[0]
        return link if link else None
    except:
        return None

def download_video(link):
    temp_dir = os.path.join(BASE_DIR, "temp_video")
    os.makedirs(temp_dir, exist_ok=True)
    audio_file = os.path.join(temp_dir, "audio.m4a")
    cmd = [
        "yt-dlp",
        "--no-warnings",
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
        return None
    except subprocess.CalledProcessError as e:
        print(f"Errore yt-dlp: {e.stderr.decode()}", flush=True)
        return None

def transcribe_audio(audio_path):
    try:
        import whisper
        print("Caricamento whisper tiny...", flush=True)
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Errore whisper: {e}", flush=True)
        return ""

def extract_patterns(text):
    """Usa SpaCy per estrarre pattern candlestick menzionati."""
    if nlp is None:
        return "SpaCy non disponibile"
    doc = nlp(text.lower())
    # Pattern noti
    patterns = {
        "doji": ["doji", "doj"],
        "hammer": ["hammer", "martello"],
        "shooting star": ["shooting", "stella cadente"],
        "engulfing": ["engulfing", "inglobamento"],
        "three white soldiers": ["tre soldati", "3 soldati", "tre candele bianche"],
        "three black crows": ["tre corvi", "3 corvi", "tre candele nere"],
        "morning star": ["morning star", "stella mattutina"],
        "evening star": ["evening star", "stella serale"],
        "harami": ["harami"],
        "piercing": ["piercing", "foratura"],
        "dark cloud": ["dark cloud", "nuvola scura"]
    }
    found = []
    for pattern, keywords in patterns.items():
        for kw in keywords:
            if kw in doc.text:
                found.append(pattern)
                break
    return ", ".join(found) if found else "Nessun pattern riconosciuto"

def analyze_with_ollama(text, patterns):
    prompt = f"""Sei un analista finanziario. Analizza il seguente testo estratto da un video di trading/forex.

Testo:
\"{text[:3000]}\"

Pattern candlestick rilevati automaticamente: {patterns}

Rispondi in italiano con:
1. **Strategia principale** – entry, exit, stop loss, take profit, timeframe, indicatori.
2. **Sentiment** – positivo/negativo/neutro.
3. **Pattern candlestick** – conferma o integra quelli rilevati.
4. **Consigli pratici** – cosa suggerisce il video.
5. **Rischio** – eventuali avvertenze.
Sii conciso.
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

def generate_report(link, transcription, patterns, analysis):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""REPORT VIDEO - {now}
========================================
LINK: {link}

--- TRASCRIZIONE (estratto) ---
{transcription[:500]}{'...' if len(transcription)>500 else ''}

--- PATTERN RILEVATI (SpaCy) ---
{patterns}

--- ANALISI AI ---
{analysis}
========================================
"""

def cleanup(temp_dir):
    try:
        import shutil
        shutil.rmtree(temp_dir)
    except:
        pass

def main():
    print("=== YT-DIGEST AGENT (notturno) ===", flush=True)
    if not is_night():
        print("Orario diurno. Attendo la notte (22-06).", flush=True)
        return

    link = read_link()
    if not link:
        print("Nessun link in video_link.txt", flush=True)
        return

    audio_path = download_video(link)
    if not audio_path:
        print("Download fallito.", flush=True)
        return

    print("Trascrizione in corso...", flush=True)
    transcription = transcribe_audio(audio_path)
    if not transcription:
        print("Trascrizione vuota.", flush=True)
        cleanup(os.path.dirname(audio_path))
        return

    print(f"Trascrizione: {len(transcription)} caratteri.", flush=True)

    print("Estrazione pattern con SpaCy...", flush=True)
    patterns = extract_patterns(transcription)

    print("Analisi con Ollama...", flush=True)
    analysis = analyze_with_ollama(transcription, patterns)

    report = generate_report(link, transcription, patterns, analysis)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report salvato: {REPORT_FILE}", flush=True)
    cleanup(os.path.dirname(audio_path))
    print("=== FATTO ===", flush=True)

if __name__ == "__main__":
    main()
