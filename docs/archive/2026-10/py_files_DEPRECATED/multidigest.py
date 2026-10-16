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

# Percorso assoluto di panoscribe (se installato)
PANOSCRIBE_BIN = "/home/carlo/AI_Trading_Agents_py311/bin/panoscribe"
PANOSCRIBE_AVAILABLE = os.path.exists(PANOSCRIBE_BIN)

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

def analyze_with_panoscribe(link):
    """Usa panoscribe con --no-ocr per trascrivere solo audio."""
    temp_dir = os.path.join(BASE_DIR, "temp_video")
    os.makedirs(temp_dir, exist_ok=True)
    output_json = os.path.join(temp_dir, "panoscribe_output.json")
    
    cmd = [
        PANOSCRIBE_BIN,
        "transcribe", link,
        "--format", "json",
        "--output", output_json,
        "--no-ocr",          # disabilita OCR (risolve errore latino)
        "--model", "tiny"    # più veloce per test, togli per qualità
    ]
    try:
        subprocess.run(cmd, check=True, timeout=600)
        if os.path.exists(output_json):
            with open(output_json, "r") as f:
                data = json.load(f)
            # Estrai il testo dalla chiave "text" (trascrizione completa)
            transcription = data.get("text", "")
            return transcription.strip()
    except Exception as e:
        print(f"Errore panoscribe: {e}")
    return None

def analyze_with_fallback(link):
    """Metodo fallback: yt-dlp + whisper."""
    # Usa il vecchio codice (yt-dlp + whisper)
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
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not os.path.exists(audio_file):
            return None
        # Whisper
        import whisper
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        print(f"Errore fallback: {e}")
    finally:
        # pulizia
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
            pass
    return None

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
STRUMENTO: panoscribe (no-ocr)

--- TRASCRIZIONE COMPLETA ---
{transcription}

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

    transcription = None
    if PANOSCRIBE_AVAILABLE:
        print("Analisi con panoscribe...", flush=True)
        transcription = analyze_with_panoscribe(link)
    if not transcription:
        print("Fallback con yt-dlp+whisper...", flush=True)
        transcription = analyze_with_fallback(link)

    if not transcription:
        print("Trascrizione fallita.", flush=True)
        return

    print(f"Trascrizione ottenuta ({len(transcription)} caratteri).", flush=True)
    patterns = extract_patterns(transcription)
    analysis = analyze_with_ollama(transcription, patterns)

    report = generate_report(link, transcription, patterns, analysis)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report salvato: {REPORT_FILE}", flush=True)
    cleanup(os.path.join(BASE_DIR, "temp_video"))
    print("=== FATTO ===", flush=True)

if __name__ == "__main__":
    main()
