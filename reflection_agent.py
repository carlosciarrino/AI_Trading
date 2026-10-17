#!/usr/bin/env python3
"""reflection_agent.py v3 - Memory log markdown + pulizia output tinyllama."""
import json, os, time, requests
from datetime import datetime

MEMORY_PATH = os.path.expanduser("~/AI_Trading/trading_memory.md")
DECISION_LOG = os.path.expanduser("~/AI_Trading/decision_log.jsonl")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama:latest"
SEPARATOR = "\n\n<!-- ENTRY_END -->\n\n"

SYSTEM_PROMPT = (
    "Sei un analista di trading che rivede una propria decisione passata "
    "ora che conosce l'esito. Scrivi esattamente 2-4 frasi di prosa semplice "
    "(no elenchi, no titoli, no markdown).\n\n"
    "Copri in ordine:\n"
    "1. Cosa mostra il PNL sulla decisione (cita il valore).\n"
    "2. Quale parte della tesi e' stata confermata o smentita.\n"
    "3. Una lezione concreta da applicare alla prossima analisi simile.\n\n"
    "Sii specifico e conciso."
)


def check_ram(min_mb=500):
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    kb = int(line.split()[1])
                    mb = kb // 1024
                    if mb < min_mb:
                        print(f"[reflection] RAM bassa ({mb} MB < {min_mb}). Salto.", flush=True)
                        return False
                    return True
    except Exception:
        return True
    return True


def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH) as f:
        content = f.read()
    entries = []
    for block in content.split(SEPARATOR):
        block = block.strip()
        if not block:
            continue
        if block.startswith("["):
            end_tag = block.find("]")
            if end_tag > 0:
                tag = block[1:end_tag]
                rest = block[end_tag+1:].strip()
                entries.append({"tag": tag, "body": rest, "raw": block})
    return entries


def save_memory(entries):
    with open(MEMORY_PATH, "w") as f:
        for e in entries:
            f.write(e["raw"] + SEPARATOR)


def load_decision_context(ticket):
    try:
        with open(DECISION_LOG) as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("ticket") == str(ticket):
                    return d
    except Exception:
        pass
    return None


def ask_reflection(exp, ctx):
    """Genera lezione deterministica, senza LLM."""
    pnl = exp.get("pnl", 0)
    azione = exp.get("azione", "?")
    prezzo = exp.get("prezzo", 0)
    esito = exp.get("esito", "?")

    lezione = f"Decisione {azione} a {prezzo}. PNL {pnl:+.2f} EUR ({esito}). "

    if ctx:
        scores = ctx.get("scores", {})
        signal = ctx.get("signal", "?")
        final = ctx.get("final_score", 0)
        # Identifica segnali che hanno contribuito
        contributi = [f"{k}={v:+.2f}" for k, v in scores.items() if abs(v) > 0.1]
        lezione += f"Segnale {signal} (score {final:+.2f}, contributi: {', '.join(contributi)}). "

    if pnl < 0:
        lezione += "La direzione era sbagliata o lo spread/commissioni hanno eroso il margine. "
        lezione += "Lezione: verificare che il segnale sia forte (score > 0.15) prima di aprire."
    elif pnl > 0:
        lezione += "La direzione era corretta. "
        lezione += "Lezione: replicare quando gli stessi segnali si ripresentano."
    else:
        lezione += "Risultato neutro. Lezione: evitare aperture con segnale debole."

    return lezione[:800]


def process_pending():
    if not check_ram(500):
        return

    ctx_map = {}
    try:
        with open(DECISION_LOG) as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("ticket"):
                    ctx_map[str(d["ticket"])] = d
    except Exception:
        pass

    orders = []
    try:
        with open(os.path.expanduser("~/Scrivania/XM MT4/MQL4/Files/orders.json")) as f:
            orders = json.load(f)
    except Exception:
        pass

    closed = [o for o in orders if o.get("status") == "closed"]

    entries = load_memory()
    already = set()
    for e in entries:
        parts = [p.strip() for p in e["tag"].split("|")]
        if len(parts) >= 2:
            already.add(parts[1])

    # P031-bis: forza rigenerazione se la lezione e' di bassa qualita'
    bad_words = ["impresa", "Ligne", "riferirsi a tali eventi", "condividendo l'errore",
                 "smerta", "Confermato che la decisione di acquistare"]
    bad_tickets = set()
    for e in entries:
        body = e.get("body", "").lower()
        if any(w.lower() in body for w in bad_words):
            parts = [p.strip() for p in e["tag"].split("|")]
            if len(parts) >= 2:
                bad_tickets.add(parts[1])
    already = already - bad_tickets
    entries = [e for e in entries if not any(w.lower() in e.get("body", "").lower() for w in bad_words)
               and e.get("body", "").count("ha causato") < 2]

    generated = 0
    for op in closed[-10:]:
        ticket = str(op.get("ticket", "?"))
        if ticket in already:
            continue

        exp = {
            "ticket": ticket,
            "azione": op.get("action", "?"),
            "prezzo": op.get("price", 0),
            "pnl": op.get("pnl", 0),
            "esito": "PROFITTO" if op.get("pnl", 0) > 0 else "PERDITA",
        }
        ctx = ctx_map.get(ticket)
        lezione = ask_reflection(exp, ctx)
        if lezione:
            date = datetime.now().strftime("%Y-%m-%d")
            pnl_pct = f"{exp['pnl']:+.2f}EUR"
            tag = f"[{date} | {ticket} | {exp['azione']} | {pnl_pct} | resolved:{date}]"
            body = f"DECISION:\n{exp['azione']} @ {exp['prezzo']}\nREFLECTION:\n{lezione}"
            entries.append({"tag": tag[1:-1], "body": body, "raw": tag + "\n" + body})
            generated += 1
            print(f"[reflection] Lezione per {ticket}: {lezione[:80]}...", flush=True)
        else:
            print(f"[reflection] Skip {ticket} (Ollama timeout)", flush=True)

    if generated:
        save_memory(entries)
        print(f"[reflection] {generated} lezioni scritte in trading_memory.md", flush=True)
    else:
        print("[reflection] Nessuna nuova lezione", flush=True)


if __name__ == "__main__":
    while True:
        try:
            process_pending()
        except Exception as e:
            print(f"[reflection] Errore: {e}", flush=True)
        time.sleep(1800)  # 30 min
