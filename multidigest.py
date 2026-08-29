import os
import subprocess
import sys
import time
import json
import requests
from datetime import datetime
from urllib.parse import urlparse

BASE_DIR = os.path.expanduser("~/AI_Trading")
LINK_FILE = os.path.join(BASE_DIR, "video_link.txt")
REPORT_FILE = os.path.join(BASE_DIR, "report_multivideo.txt")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"

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
    
    # Usa cookie dal browser (es. firefox, chrome)
    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--cookies-from-browser", "firefox",   # Cambia in "chrome" se usi Chrome
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "m4a",
        "--output", audio_file,
        link
    ]
    
    print(f"Download da: {link}", flush=True)
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(audio_file):
            return audio_file
        # Fallback: cerca qualsiasi .m4a
        for f in os.listdir(temp_dir):
            if f.endswith(".m4a"):
                return os.path.join(temp_dir, f)
        return None
    except subprocess.CalledProcessError as e:
        print(f"Errore yt-dlp: {e.stderr.decode()}", flush=True)
        # Tentativo senza cookie (solo YouTube)
        cmd_no_cookie = [c for c in cmd if "--cookies-from-browser" not in c]
        try:
            subprocess.run(cmd_no_cookie, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for f in os.listdir(temp_dir):
                if f.endswith(".m4a"):
                    return os.path.join(temp_dir, f)
        except:
            pass
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
    if nlp is None:
        return "SpaCy non disponibile"
    doc = nlp(text.lower())
    patterns = {
        "doji": ["doji", "doj"],
        "hammer": ["hammer", "martello"],
        "shooting star": ["shooting", "stella cadente"],
        "engulfing": ["engulfing", "inglobamento"],
        "three white soldiers": ["tre soldati", "3 soldati"],
        "three black crows": ["tre corvi", "3 corvi"],
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
    return ", ".join(found) if found else "Nessun pattern"

def analyze_with_ollama(text, patterns):
    prompt = f"""Analizza il seguente testo da video trading/forex.

Testo:
\"{text[:3000]}\"

Pattern rilevati: {patterns}

Rispondi in italiano:
1. Strategia principale (entry, exit, SL, TP, timeframe, indicatori)
2. Sentiment (positivo/negativo/neutro)
3. Pattern candlestick confermati
4. Consigli pratici
5. Rischio
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
    return f"""REPORT MULTI-VIDEO - {now}
========================================
LINK: {link}
PIATTAFORMA: {urlparse(link).netloc}

--- TRASCRIZIONE (estratto) ---
{transcription[:500]}{'...' if len(transcription)>500 else ''}

--- PATTERN (SpaCy) ---
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
    print("=== MULTI-DIGEST AGENT (notturno) ===", flush=True)
    if not is_night():
        print("Orario diurno. Attendo notte (22-06).", flush=True)
        return

    link = read_link()
    if not link:
        print("Nessun link in video_link.txt", flush=True)
        return

    audio_path = download_video(link)
    if not audio_path:
        print("Download fallito. Verifica cookie o link.", flush=True)
        return

    print("Trascrizione...", flush=True)
    transcription = transcribe_audio(audio_path)
    if not transcription:
        print("Trascrizione vuota.", flush=True)
        cleanup(os.path.dirname(audio_path))
        return

    print(f"Trascrizione: {len(transcription)} caratteri.", flush=True)
    patterns = extract_patterns(transcription)
    analysis = analyze_with_ollama(transcription, patterns)

    report = generate_report(link, transcription, patterns, analysis)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report salvato: {REPORT_FILE}", flush=True)
    cleanup(os.path.dirname(audio_path))
    print("=== FATTO ===", flush=True)

if __name__ == "__main__":
    main()
