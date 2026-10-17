import yfinance as yf
import json, time, os, requests
from datetime import datetime, timezone, timedelta

CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
MAX_OPEN_ORDERS = 1
MT4_FILES = os.path.expanduser("~/Scrivania/XM MT4/MQL4/Files")
ORDERS_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/orders.json"
OPEN_TIME_FILE = "/home/carlo/Scrivania/XM MT4/MQL4/Files/open_time.json"
ACCOUNT_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/account.json"
SL_COMMANDS_FILE = "/home/carlo/Scrivania/XM MT4/MQL4/Files/sl_commands.json"
LOCK_FILE = "/tmp/orchestrator.lock"
DECISION_LOG = "/home/carlo/AI_Trading/decision_log.jsonl"

# O8 - parametri logica post-apertura
BREAK_EVEN_PIP = 20       # attivazione: profitto >= 20 pip
BREAK_EVEN_OFFSET_PIP = 2 # SL spostato a entry +/- 2 pip
FRIDAY_PROFIT_HOUR_UTC = 15  # C1: venerdi 15:00 UTC, chiudi se PNL > 0
FRIDAY_CLOSE_HOUR_UTC = 20   # C2: venerdi 20:00 UTC, chiudi tutto
MAIN_LOOP_SLEEP = 300        # 5 minuti


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def is_trading_hours(session):
    now_utc = datetime.now(timezone.utc).hour
    if session == "all":
        return True
    if session == "london":
        return 8 <= now_utc < 17
    if session == "newyork":
        return 13 <= now_utc < 22
    if session == "tokyo":
        return 0 <= now_utc < 9
    if session == "london_newyork":
        return (8 <= now_utc < 17) or (13 <= now_utc < 22)
    return True


def count_open_orders():
    try:
        with open(ACCOUNT_JSON) as f:
            acc = json.load(f)
        n = int(acc.get("open_orders", 0))
        print(f"[DEBUG] Ordini aperti (account.json): {n}", flush=True)
        return n
    except Exception as e:
        print(f"[DEBUG] Errore lettura account.json: {e}", flush=True)
        return 0


def get_open_order():
    """Ritorna il primo ordine aperto da orders.json, o None.
    Formato tipico: {"action":"buy","lots":0.01,"price":1.11664,"sl":1.11614,
    "tp":1.11764,"time":...,"status":"open","ticket":"253699","pnl":0}
    """
    try:
        with open(ORDERS_JSON) as f:
            orders = json.load(f)
        for o in orders:
            if o.get("status") == "open":
                return o
        return None
    except Exception as e:
        print(f"[DEBUG] Errore lettura orders.json: {e}", flush=True)
        return None


def send_close_command(ticket, reason_log):
    """Invia comando CLOSE <ticket> all'EA e legge esito. Logga su stdout."""
    cmd_path = os.path.join(MT4_FILES, "AI_BRIDGE_CMD.txt")
    res_path = os.path.join(MT4_FILES, "AI_BRIDGE_RES.txt")
    if os.path.exists(res_path):
        try:
            os.remove(res_path)
        except Exception:
            pass
    with open(cmd_path, "w") as f:
        f.write(f"close {ticket}\n")
    status, payload = read_bridge_result(timeout=8)
    if status == "ok":
        print(f"[O8] Chiusura {ticket} confermata ({reason_log})", flush=True)
    elif status == "err":
        print(f"[O8] Chiusura {ticket} fallita ({reason_log}): {payload.get('error')}", flush=True)
    else:
        print(f"[O8] Chiusura {ticket} timeout EA ({reason_log})", flush=True)

def get_signal():
    scores = {}
    # O10 (2026-10-15): news RIATTIVATO. news_agent v2 scrive news_context.txt
    # fresco (ogni 10 min) con riga "Sentiment: positivo|negativo|neutro".
    try:
        with open('/home/carlo/AI_Trading/news_context.txt', 'r') as f:
            text = f.read().lower()
            if 'sentiment: positivo' in text:
                scores['news'] = 0.3
            elif 'sentiment: negativo' in text:
                scores['news'] = -0.3
            else:
                scores['news'] = 0.0
    except:
        scores['news'] = 0.0
    try:
        with open('/home/carlo/AI_Trading/social_context.txt', 'r') as f:
            text = f.read().lower()
            if 'positivo' in text:
                scores['social'] = 0.2
            elif 'negativo' in text:
                scores['social'] = -0.2
            else:
                scores['social'] = 0.0
    except:
        scores['social'] = 0.0
    try:
        with open('/home/carlo/AI_Trading/cycles_context.txt', 'r') as f:
            text = f.read().lower()
            import re
            month = datetime.now().month
            lines = text.split('\n')
            for line in lines:
                if f"mese {month}" in line:
                    match = re.search(r'(\d+\.\d+)', line)
                    if match:
                        avg = float(match.group(1))
                        if avg > 1.10:
                            scores['cycle'] = 0.2
                        elif avg < 1.08:
                            scores['cycle'] = -0.2
                        else:
                            scores['cycle'] = 0.0
                        break
            else:
                scores['cycle'] = 0.0
    except:
        scores['cycle'] = 0.0
    try:
        with open('/home/carlo/AI_Trading/volume_context.txt', 'r') as f:
            text = f.read().lower()
            import re
            match = re.search(r'(?:score|punteggio)[:\s]+(-?\d+\.\d+)', text)
            if match:
                scores['volume'] = float(match.group(1))
            else:
                scores['volume'] = 0.0
    except:
        scores['volume'] = 0.0
    try:
        # P031-bis: legge trading_memory.md (markdown append-only)
        memory_path = '/home/carlo/AI_Trading/trading_memory.md'
        if os.path.exists(memory_path):
            with open(memory_path) as f:
                content = f.read()
            # Conta REFLECTION: e cerca parole chiave
            reflections = content.split('REFLECTION:')
            recent = reflections[-3:] if len(reflections) >= 3 else reflections
            text = ' '.join(recent).lower()
            pos = sum(1 for w in ['positivo', 'successo', 'corretto', 'confermato', 'profitto'] if w in text)
            neg = sum(1 for w in ['negativo', 'fallito', 'smentito', 'perdita', 'errore'] if w in text)
            if neg > pos:
                scores['experience'] = -0.2
            elif pos > neg:
                scores['experience'] = 0.2
            else:
                scores['experience'] = 0.0
        else:
            scores['experience'] = 0.0
    except:
        scores['experience'] = 0.0

    weights = {
        'news': 0.2,
        'social': 0.2,
        'cycle': 0.15,
        'volume': 0.25,
        'experience': 0.2,
    }
    total = 0.0
    weight_sum = 0.0
    for key in weights:
        total += scores.get(key, 0.0) * weights[key]
        weight_sum += weights[key]
    final_score = total / weight_sum if weight_sum > 0 else 0.0
    print(f"Punteggio combinato: {final_score:.3f}", flush=True)
    if final_score > 0.10:
        signal = "BUY"
    elif final_score < -0.10:
        signal = "SELL"
    else:
        signal = "HOLD"
    detail = {
        "scores": dict(scores),
        "weights": dict(weights),
        "final_score": round(final_score, 4),
        "signal": signal,
    }
    return signal, detail

def check_time_stop():
    """Chiude ordini aperti da piu' di 24h."""
    order = get_open_order()
    if not order:
        return
    ticket = order.get('ticket')
    if not ticket:
        return
    try:
        with open(OPEN_TIME_FILE) as f:
            open_times = json.load(f)
    except Exception:
        open_times = {}
    open_time = open_times.get(str(ticket))
    if not open_time:
        open_times[str(ticket)] = time.time()
        with open(OPEN_TIME_FILE, "w") as f:
            json.dump(open_times, f)
        return
    open_dt = datetime.fromtimestamp(open_time)
    if datetime.now() - open_dt > timedelta(hours=24):
        print(f"[O8] Ordine {ticket} aperto da >24h. Chiusura.", flush=True)
        send_close_command(ticket, "time_stop_24h")
        # Rimuovi da open_times
        try:
            del open_times[str(ticket)]
            with open(OPEN_TIME_FILE, "w") as f:
                json.dump(open_times, f)
        except Exception:
            pass


def get_current_price():
    """Scarica prezzo corrente EURUSD (Close ultima candela 15m)."""
    try:
        df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
        if df.empty:
            return None
        price = df['Close'].iloc[-1]
        if hasattr(price, 'iloc'):
            price = float(price.iloc[0])
        else:
            price = float(price)
        return price
    except Exception as e:
        print(f"[O8] Errore get_current_price: {e}", flush=True)
        return None


def check_break_even():
    """Se ordine in profitto >= BREAK_EVEN_PIP, sposta SL a entry+offset.
    Scrive sl_commands.json, l'EA lo applica al timer successivo.
    """
    order = get_open_order()
    if not order:
        return
    ticket = order.get('ticket')
    action = order.get('action')  # buy|sell
    entry = order.get('price')
    current_sl = order.get('sl')
    if not all([ticket, action, entry, current_sl is not None]):
        return
    entry = float(entry)
    current_sl = float(current_sl)
    current_price = get_current_price()
    if current_price is None:
        return
    pip = 0.0001  # 1 pip EURUSD = 0.0001
    offset = BREAK_EVEN_OFFSET_PIP * pip

    if action == "buy":
        profit_pips = (current_price - entry) / pip
        # Attiva se profitto >= soglia e SL ancora sotto entry
        if profit_pips >= BREAK_EVEN_PIP and current_sl < entry:
            new_sl = round(entry + offset, 5)
            write_sl_command(ticket, new_sl)
    elif action == "sell":
        profit_pips = (entry - current_price) / pip
        if profit_pips >= BREAK_EVEN_PIP and current_sl > entry:
            new_sl = round(entry - offset, 5)
            write_sl_command(ticket, new_sl)


def write_sl_command(ticket, new_sl):
    """Scrive sl_commands.json. L'EA legge e applica, poi cancella il file."""
    try:
        cmd = {"ticket": int(ticket), "new_sl": float(new_sl)}
        # L'EA legge un array di comandi (anche se ne scriviamo uno solo)
        existing = []
        if os.path.exists(SL_COMMANDS_FILE):
            try:
                with open(SL_COMMANDS_FILE) as f:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = [existing]
            except Exception:
                existing = []
        existing.append(cmd)
        with open(SL_COMMANDS_FILE, "w") as f:
            json.dump(existing, f)
        print(f"[O8] SL command scritto: ticket={ticket} new_sl={new_sl}", flush=True)
    except Exception as e:
        print(f"[O8] Errore write_sl_command: {e}", flush=True)


def check_friday_profit():
    """C1: venerdi 15:00 UTC. Chiudi ordini con PNL > 0 (salva-profitto)."""
    now = datetime.now(timezone.utc)
    if now.weekday() != 4:  # 4 = venerdi
        return
    if now.hour != FRIDAY_PROFIT_HOUR_UTC:
        return
    order = get_open_order()
    if not order:
        return
    ticket = order.get('ticket')
    pnl = order.get('pnl', 0)
    try:
        pnl = float(pnl)
    except Exception:
        pnl = 0.0
    if pnl > 0:
        print(f"[O8] C1 venerdi: ordine {ticket} PNL={pnl} > 0. Chiusura.", flush=True)
        send_close_command(ticket, "friday_profit")


def check_friday_close():
    """C2: venerdi 20:00 UTC. Chiudi tutti gli ordini aperti."""
    now = datetime.now(timezone.utc)
    if now.weekday() != 4:
        return
    if now.hour != FRIDAY_CLOSE_HOUR_UTC:
        return
    order = get_open_order()
    if not order:
        return
    ticket = order.get('ticket')
    print(f"[O8] C2 venerdi: chiusura forzata ordine {ticket}.", flush=True)
    send_close_command(ticket, "friday_close_all")

def read_bridge_result(timeout=8):
    """Legge AI_BRIDGE_RES.txt dopo invio comando. Ritorna (status, payload)."""
    res_path = os.path.join(MT4_FILES, "AI_BRIDGE_RES.txt")
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(res_path):
            try:
                if time.time() - os.path.getmtime(res_path) < timeout:
                    with open(res_path) as f:
                        content = f.read().strip()
                    if content.startswith("OK:"):
                        parts = content.split()
                        ticket = None
                        for p in parts:
                            if p.isdigit():
                                ticket = p
                                break
                        return ("ok", {"ticket": ticket, "raw": content})
                    elif content.startswith("ERR:"):
                        return ("err", {"error": content, "raw": content})
            except Exception as e:
                return ("err", {"error": f"read_exception: {e}"})
        time.sleep(0.5)
    return ("timeout", {"error": "timeout_ea"})


def write_decision(detail, action_taken, ticket=None, reason=None, error=None):
    import json as _json
    entry = {
        "timestamp": datetime.now().isoformat(),
        "scores": detail.get("scores", {}),
        "weights": detail.get("weights", {}),
        "final_score": detail.get("final_score", 0.0),
        "signal": detail.get("signal", "HOLD"),
        "action_taken": action_taken,
        "ticket": ticket,
        "reason": reason,
    }
    if error is not None:
        entry["error"] = error
    try:
        with open(DECISION_LOG, "a") as f:
            f.write(_json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Errore write_decision: {e}", flush=True)

def main():
    # Lock esclusivo
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE) as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print(f"[LOCK] Orchestratore già attivo (PID {pid}). Esco.", flush=True)
            return
        except (ProcessLookupError, ValueError):
            os.remove(LOCK_FILE)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    try:
        config = load_config()
        session = config.get("session", "all")
        print(f"Orchestratore avviato. Sessione: {session}", flush=True)

        while True:
            # O8: logica post-apertura (sempre attiva, anche fuori orario)
            check_time_stop()
            check_break_even()
            check_friday_profit()
            check_friday_close()

            if not is_trading_hours(session):
                print(f"Fuori orario. UTC: {datetime.now(timezone.utc).hour}", flush=True)
                time.sleep(MAIN_LOOP_SLEEP)
                continue

            open_count = count_open_orders()
            if open_count >= MAX_OPEN_ORDERS:
                print("Limite operazioni raggiunto.", flush=True)
                time.sleep(MAIN_LOOP_SLEEP)
                continue

            signal, detail = get_signal()
            print(f"Segnale AI: {signal}", flush=True)

            # P013 (2026-10-16): non aprire nuovi ordini il venerdi dopo le 19:00 UTC
            now_utc = datetime.now(timezone.utc)
            if signal in ("BUY", "SELL") and now_utc.weekday() == 4 and now_utc.hour >= 19:
                print("[P013] Venerdi dopo 19:00 UTC: apertura bloccata.", flush=True)
                write_decision(detail, action_taken="none", reason="p013_friday_late")
                time.sleep(MAIN_LOOP_SLEEP)
                continue

            if signal in ("BUY", "SELL"):
                action = "buy" if signal == "BUY" else "sell"
                try:
                    df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
                    if df.empty:
                        raise ValueError("Nessun dato scaricato")
                    df['ATR'] = df['High'].rolling(14).max() - df['Low'].rolling(14).min()
                    atr = df['ATR'].iloc[-1]
                    sl_distance = atr * 1.0
                    tp_distance = atr * 1.5
                    price = df['Close'].iloc[-1]
                    if signal == "BUY":
                        sl = price - sl_distance
                        tp = price + tp_distance
                    else:
                        sl = price + sl_distance
                        tp = price - tp_distance
                    if hasattr(sl, 'iloc'):
                        sl = float(sl.iloc[0])
                    else:
                        sl = float(sl)
                    if hasattr(tp, 'iloc'):
                        tp = float(tp.iloc[0])
                    else:
                        tp = float(tp)
                    sl = round(sl, 5)
                    tp = round(tp, 5)
                    cmd = f"{action} 0.01 {sl} {tp}"
                    print(f"Ordine {action} inviato con SL={sl} TP={tp}", flush=True)
                except Exception as e:
                    print(f"Errore calcolo ATR, uso default: {e}", flush=True)
                    cmd = action

                cmd_path = os.path.join(MT4_FILES, "AI_BRIDGE_CMD.txt")
                res_path = os.path.join(MT4_FILES, "AI_BRIDGE_RES.txt")
                if os.path.exists(res_path):
                    try:
                        os.remove(res_path)
                    except Exception:
                        pass
                with open(cmd_path, "w") as f:
                    f.write(f"{cmd}\n")
                status, payload = read_bridge_result(timeout=8)
                if status == "ok":
                    write_decision(detail, action_taken=action,
                                   ticket=payload.get("ticket"),
                                   reason="ea_ok")
                elif status == "err":
                    write_decision(detail, action_taken="none",
                                   reason="ea_err",
                                   error=payload.get("error"))
                else:
                    write_decision(detail, action_taken="none",
                                   reason="timeout_ea",
                                   error="timeout_ea")
            else:
                print("HOLD", flush=True)
                write_decision(detail, action_taken="none", reason="score_neutro")

            time.sleep(MAIN_LOOP_SLEEP)
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)


if __name__ == "__main__":
    main()


