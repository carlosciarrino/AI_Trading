import os, json, time, requests
from datetime import datetime

BASE = os.path.expanduser("~/AI_Trading")
REPORT_FILE = os.path.join(BASE, "report_giornaliero.txt")
TELEGRAM_BOT_TOKEN = ""  # inserisci se hai
TELEGRAM_CHAT_ID = ""    # inserisci se hai

def read_file(path, default="Nessun dato"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return default

def build_report():
    lines = []
    lines.append(f"=== REPORT GIORNALIERO - {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
    
    # YouTube
    yt = read_file(os.path.join(BASE, "youtube_context.txt"))
    lines.append("[YOUTUBE]")
    lines.append(yt[:200] + "..." if len(yt)>200 else yt)
    lines.append("")
    
    # Indicator tester
    ind = read_file(os.path.join(BASE, "report_indicatori.txt"))
    lines.append("[INDICATORI]")
    lines.append(ind[:200] + "..." if len(ind)>200 else ind)
    lines.append("")
    
    # Skill Researcher (se esiste)
    skill = read_file(os.path.join(BASE, "skill_context.txt"))
    lines.append("[SKILL RESEARCH]")
    lines.append(skill[:200] + "..." if len(skill)>200 else skill)
    lines.append("")
    
    # Strategy Tester (se esiste)
    strat = read_file(os.path.join(BASE, "report_strategia.txt"))
    lines.append("[STRATEGY TEST]")
    lines.append(strat[:200] + "..." if len(strat)>200 else strat)
    lines.append("")
    
    # Riepilogo rapido
    lines.append("=== RIEPILOGO ===")
    lines.append(f"YouTube sentiment: {extract_sentiment(yt)}")
    lines.append(f"Indicatori win rate: {extract_winrate(ind)}")
    lines.append(f"Skill: {extract_skill(skill)}")
    
    return "\n".join(lines)

def extract_sentiment(text):
    if "positivo" in text.lower(): return "POSITIVO"
    if "negativo" in text.lower(): return "NEGATIVO"
    if "neutro" in text.lower(): return "NEUTRO"
    return "N/D"

def extract_winrate(text):
    for line in text.split("\n"):
        if "Win Rate" in line:
            return line.split(":")[-1].strip()
    return "N/D"

def extract_skill(text):
    for line in text.split("\n"):
        if "trovati" in line or "scoperti" in line:
            return line.strip()
    return "N/D"

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

def main():
    report = build_report()
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print(f"Report salvato: {REPORT_FILE}")
    send_telegram(report[:4000])  # limite telegram

if __name__ == "__main__":
    main()
