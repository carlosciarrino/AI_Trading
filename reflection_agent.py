#!/usr/bin/env python3
"""reflection_agent.py v2 - Memory log in markdown (formato TradingAgents).

Scrive in trading_memory.md append-only, con separatore HTML.
Legge decision_log.jsonl per contesto. Genera lezioni via Ollama.
"""
import json, os, time, requests
from datetime import datetime

MEMORY_PATH = os.path.expanduser("~/AI_Trading/trading_memory.md")
DECISION_LOG = os.path.expanduser("~/AI_Trading/decision_log.jsonl")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
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


def load_memory():
    """Legge trading_memory.md, ritorna lista di entry (dict)."""
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH) as f:
        content = f.read()
    entries = []
    for block in content.split(SEPARATOR):
        block = block.strip()
        if not block:
            continue
        # Parse tag [date | ticket | action | pending]
        if block.startswith("["):
            end_tag = block.find("]")
            if end_tag > 0:
                tag = block[1:end_tag]
                rest = block[end_tag+1:].strip()
                entries.append({"tag": tag, "body": rest, "raw": block})
    return entries


def save_memory(entries):
    """Riscrive il file con le entry aggiornate."""
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
    pnl = exp.get("pnl", 0)
    azione = exp.get("azione", "?")
    prezzo = exp.get("prezzo", 0)
    esito = exp.get("esito", "?")
    ticket = exp.get("ticket", "?")

    ctx_str = ""
    if ctx:
        ctx_str = (
            f"\nContesto:\n"
            f"- scores: {ctx.get('scores', {})}\n"
            f"- final_score: {ctx.get('final_score', '?')}\n"
            f"- signal: {ctx.get('signal', '?')}\n"
        )

    prompt = (
        f"Decisione: {azione} a prezzo {prezzo}, ticket {ticket}.\n"
        f"Esito: {esito}, PNL: {pnl:+.2f} EUR.\n"
        f"{ctx_str}\n"
        f"Scrivi 2-4 frasi di lezione specifica."
    )

    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": SYSTEM_PROMPT + "\n\n" + prompt,
                  "stream": False, "options": {"temperature": 0.3}},
            timeout=180,
        )
        r.raise_for_status()
        text = r.json().get("response", "").strip()
        return text[:600]
    except Exception as e:
        print(f"[reflection] Errore Ollama: {e}", flush=True)
        return None


def process_pending():
    """Trova decisioni chiuse non ancora riflesse, genera lezione."""
    # Carica decision_log per contesto
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

    # Carica orders.json per PNL reali
    orders = []
    try:
        with open(os.path.expanduser("~/Scrivania/XM MT4/MQL4/Files/orders.json")) as f:
            orders = json.load(f)
    except Exception:
        pass

    closed = [o for o in orders if o.get("status") == "closed"]

    # Leggi memoria esistente
    entries = load_memory()
    already = set()
    for e in entries:
        # tag = "date | ticket | action | pending" o "date | ticket | action | +x% | ..."
        parts = [p.strip() for p in e["tag"].split("|")]
        if len(parts) >= 2:
            already.add(parts[1])

    generated = 0
    for op in closed[-10:]:  # ultimi 10
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
