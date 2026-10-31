import yfinance as yf
import json, time, os, requests
from datetime import datetime, timezone, timedelta
import risk_manager

CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
MAX_OPEN_ORDERS = 1
MT4_FILES = os.path.expanduser("~/Scrivania/XM MT4/MQL4/Files")
MAX_ORDERS_FILE = os.path.join(MT4_FILES, "max_orders.txt")
EA_PARAMS_FILE = os.path.join(MT4_FILES, "ea_params.json")
ORDERS_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/orders.json"
OPEN_TIME_FILE = "/home/carlo/Scrivania/XM MT4/MQL4/Files/open_time.json"
ACCOUNT_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/account.json"
SL_COMMANDS_FILE = "/home/carlo/Scrivania/XM MT4/MQL4/Files/sl_commands.json"
LOCK_FILE = "/tmp/orchestrator.lock"
DECISION_LOG = "/home/carlo/AI_Trading/decision_log.jsonl"

# O8 - parametri logica post-apertura
BREAK_EVEN_PIP = 20
BREAK_EVEN_OFFSET_PIP = 2
FRIDAY_PROFIT_HOUR_UTC = 15
FRIDAY_CLOSE_HOUR_UTC = 20
MAIN_LOOP_SLEEP = 300


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_max_orders():
    try:
        with open(EA_PARAMS_FILE) as f:
            data = json.load(f)
            return int(data.get("MaxOrders", MAX_OPEN_ORDERS))
    except:
        pass
    try:
        with open(MAX_ORDERS_FILE) as f:
            return int(f.read().strip())
    except:
        return MAX_OPEN_ORDERS


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


def get_technical_trend():
    """Legge technical_context.txt e ritorna 'bull', 'bear', 'neutral' o None."""
    try:
        with open('/home/carlo/AI_Trading/technical_context.txt') as f:
            text = f.read().lower()
        # Match piu' robusto: cerca 'bear=true' o 'bull=true' ovunque nella riga Trend
        if 'bear=true' in text:
            return 'bear'
        if 'bull=true' in text:
            return 'bull'
        return 'neutral'
    except:
        return None


def get_rsi():
    try:
        with open('/home/carlo/AI_Trading/technical_context.txt') as f:
            text = f.read().lower()
        import re
        match = re.search(r'rsi[\s:]+([0-9.]+)', text)
        if match:
            return float(match.group(1))
    except Exception as e:
        print(f"[RSI] Errore lettura: {e}", flush=True)
    return None

def send_close_command(ticket, reason_log):
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
        # P007: traccia chiusura O8 in decision_log
        write_decision({}, action_taken="close", ticket=ticket, reason=reason_log)
    elif status == "err":
        print(f"[O8] Chiusura {ticket} fallita ({reason_log}): {payload.get('error')}", flush=True)
        # P007: traccia errore chiusura
        write_decision({}, action_taken="none", ticket=ticket,
                       reason=reason_log + "_err",
                       error=payload.get("error"))
    else:
        print(f"[O8] Chiusura {ticket} timeout EA ({reason_log})", flush=True)
        # P007: traccia timeout
        write_decision({}, action_taken="none", ticket=ticket,
                       reason=reason_log + "_timeout",
                       error="timeout_ea")


def get_signal():
    scores = {}
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
            if 'sentiment: positivo' in text:
                scores['social'] = 0.2
            elif 'sentiment: negativo' in text:
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
            match = re.search(r'(?:punteggio|score)[:\s]+(-?\d+\.\d+)', text)
            if match:
                scores['volume'] = float(match.group(1))
            else:
                scores['volume'] = 0.0
    except:
        scores['volume'] = 0.0
    try:
        with open('/home/carlo/AI_Trading/trading_memory.md', 'r') as f:
            content = f.read()
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

        # Pattern: 3 BUY loss consecutivi -> blocca BUY
        import json as _json
        try:
            with open('/home/carlo/Scrivania/XM MT4/MQL4/Files/orders.json') as _f:
                _orders = _json.load(_f)
            _closed = [o for o in _orders if o.get('status') == 'closed']
            _recent = _closed[-3:] if len(_closed) >= 3 else _closed
            if len(_recent) == 3 and all(o.get('action') == 'buy' and float(o.get('pnl', 0)) < 0 for o in _recent):
                scores['experience'] = -0.5
        except Exception:
            pass
    except:
        scores['experience'] = 0.0
    weights = {
        'news': 0.1,
        'social': 0.15,
        'cycle': 0.15,
        'volume': 0.30,
        'experience': 0.30,
    }
    total = 0.0
    weight_sum = 0.0
    for key in weights:
        total += scores.get(key, 0.0) * weights[key]
        weight_sum += weights[key]
    final_score = total / weight_sum if weight_sum > 0 else 0.0
    print(f"Punteggio combinato: {final_score:.3f}", flush=True)
    # P007: diagnostica scores su stdout
    print(f"[SCORES] {scores}", flush=True)
    if final_score > 0.08:
        signal = "BUY"
    elif final_score < -0.08:
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
        try:
            del open_times[str(ticket)]
            with open(OPEN_TIME_FILE, "w") as f:
                json.dump(open_times, f)
        except Exception:
            pass


def get_current_price():
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


def get_atr():
    """Scarica ATR da yfinance (15m)."""
    try:
        df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
        if df.empty:
            return None
        df['ATR'] = df['High'].rolling(14).max() - df['Low'].rolling(14).min()
        atr = df['ATR'].iloc[-1]
        if hasattr(atr, 'iloc'):
            atr = float(atr.iloc[0])
        else:
            atr = float(atr)
        return atr
    except Exception as e:
        print(f"[BE] Errore get_atr: {e}", flush=True)
        return None


def check_break_even():
    order = get_open_order()
    if not order:
        return
    ticket = order.get('ticket')
    action = order.get('action')
    entry = order.get('price')
    current_sl = order.get('sl')
    if not all([ticket, action, entry, current_sl is not None]):
        return
    entry = float(entry)
    current_sl = float(current_sl)
    current_price = get_current_price()
    if current_price is None:
        return
    pip = 0.0001
    offset = BREAK_EVEN_OFFSET_PIP * pip

    # P056: soglia dinamica = max(20, ATR * 2)
    atr = get_atr()
    if atr is None:
        atr = 0.0010  # fallback 10 pip
    soglia_pip = max(20, (atr / pip) * 2.0)
    print(f"[BE] Soglia dinamica: {soglia_pip:.0f} pip (ATR {atr/pip:.1f} pip)", flush=True)

    if action == "buy":
        profit_pips = (current_price - entry) / pip
        if profit_pips >= soglia_pip and current_sl < entry:
            new_sl = round(entry + offset, 5)
            write_sl_command(ticket, new_sl)
    elif action == "sell":
        profit_pips = (entry - current_price) / pip
        if profit_pips >= soglia_pip and current_sl > entry:
            new_sl = round(entry - offset, 5)
            write_sl_command(ticket, new_sl)


def write_sl_command(ticket, new_sl):
    try:
        cmd = {"ticket": int(ticket), "new_sl": float(new_sl)}
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


def check_trailing_stop():
    """Trailing stop dinamico: sposta lo SL in direzione favorevole se il prezzo supera una soglia."""
    order = get_open_order()
    if not order:
        return
    ticket = order.get('ticket')
    action = order.get('action')
    entry = order.get('price')
    current_sl = order.get('sl')
    
    if not all([ticket, action, entry, current_sl is not None]):
        return
        
    entry = float(entry)
    current_sl = float(current_sl)
    current_price = get_current_price()
    if current_price is None:
        return
        
    pip = 0.0001
    atr = get_atr()
    if atr is None:
        atr = 0.0010
        
    # Distanza di trailing (es. 1.5 * ATR)
    trail_distance = atr * 1.5
    
    if action == "buy":
        # Se il prezzo è salito oltre entry + trail_distance, sposta lo SL
        if current_price - entry > trail_distance:
            new_sl = round(current_price - trail_distance, 5)
            # Sposta solo se il nuovo SL è migliore del vecchio (più alto)
            if new_sl > current_sl:
                write_sl_command(ticket, new_sl)
                print(f"[TRAILING] BUY {ticket}: SL spostato a {new_sl} (prezzo {current_price:.5f})", flush=True)
                
    elif action == "sell":
        # Se il prezzo è sceso oltre entry - trail_distance, sposta lo SL
        if entry - current_price > trail_distance:
            new_sl = round(current_price + trail_distance, 5)
            # Sposta solo se il nuovo SL è migliore del vecchio (più basso)
            if new_sl < current_sl:
                write_sl_command(ticket, new_sl)
                print(f"[TRAILING] SELL {ticket}: SL spostato a {new_sl} (prezzo {current_price:.5f})", flush=True)


def check_friday_profit():
    now = datetime.now(timezone.utc)
    if now.weekday() != 4:
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
    now = datetime.now(timezone.utc)
    if now.weekday() != 4:
        return
    if now.hour != FRIDAY_CLOSE_HOUR_UTC:
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
    # Chiudi solo se in profitto o perdita contenuta (< 5 EUR)
    if pnl > -5.0:
        print(f"[O8] C2 venerdi: chiusura ordine {ticket} (PNL {pnl:+.2f}).", flush=True)
        send_close_command(ticket, "friday_close_all")
    else:
        print(f"[O8] C2 venerdi: ordine {ticket} in perdita ({pnl:+.2f}). Lascio aperto.", flush=True)


def read_bridge_result(timeout=8):
    res_path = os.path.join(MT4_FILES, "AI_BRIDGE_RES.txt")
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(res_path):
            try:
                if time.time() - os.path.getmtime(res_path) < timeout:
                    with open(res_path) as f:
                        content = f.read().strip()
                    # P007: diagnostica bridge su stdout
                    print(f"[BRIDGE] raw={content}", flush=True)
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
            check_time_stop()
            check_break_even()
            check_trailing_stop()
            check_friday_profit()
            check_friday_close()

            if not is_trading_hours(session):
                print(f"Fuori orario. UTC: {datetime.now(timezone.utc).hour}", flush=True)
                time.sleep(MAIN_LOOP_SLEEP)
                continue

            open_count = count_open_orders()
            max_orders = get_max_orders()
            if open_count >= max_orders:
                print(f"Limite operazioni raggiunto ({open_count}/{max_orders}).", flush=True)
                time.sleep(MAIN_LOOP_SLEEP)
                continue

            signal, detail = get_signal()
            print(f"Segnale AI: {signal}", flush=True)

            now_utc = datetime.now(timezone.utc)
            if signal in ("BUY", "SELL") and now_utc.weekday() == 4 and now_utc.hour >= 19:
                print("[P013] Venerdi dopo 19:00 UTC: apertura bloccata.", flush=True)
                write_decision(detail, action_taken="none", reason="p013_friday_late")
                time.sleep(MAIN_LOOP_SLEEP)
                continue

            # P055: filtro trend (blocca controtendenza)
            tech = get_technical_trend()
            if tech == "bear" and signal == "BUY":
                print("[P055] Trend bear, BUY bloccato.", flush=True)
                write_decision(detail, action_taken="none", reason="p055_trend_bear")
                time.sleep(MAIN_LOOP_SLEEP)
                continue
            if tech == "bull" and signal == "SELL":
                print("[P055] Trend bull, SELL bloccato.", flush=True)
                write_decision(detail, action_taken="none", reason="p055_trend_bull")
                time.sleep(MAIN_LOOP_SLEEP)
                continue

            rsi = get_rsi()
            if rsi is not None:
                if signal == "BUY" and rsi > 70:
                    print(f"[RSI] Ipercomprato (RSI {rsi:.1f}), BUY bloccato.", flush=True)
                    write_decision(detail, action_taken="none", reason=f"rsi_overbought_{rsi:.1f}")
                    time.sleep(MAIN_LOOP_SLEEP)
                    continue
                if signal == "SELL" and rsi < 30:
                    print(f"[RSI] Ipervenduto (RSI {rsi:.1f}), SELL bloccato.", flush=True)
                    write_decision(detail, action_taken="none", reason=f"rsi_oversold_{rsi:.1f}")
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

                    # P044: size dinamico da risk_manager
                    risk = risk_manager.get_risk_decision(float(atr))
                    if risk["halt"]:
                        print(f"[RISK] Halt: {risk['reason']}", flush=True)
                        write_decision(detail, action_taken="none", reason=f"risk_halt: {risk['reason']}")
                        time.sleep(MAIN_LOOP_SLEEP)
                        continue
                    lots = risk["lots"]
                    if lots <= 0:
                        lots = 0.01

                    cmd = f"{action} {lots} {sl} {tp}"
                    print(f"Ordine {action} {lots} inviato con SL={sl} TP={tp}", flush=True)
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
                # P007: diagnostica esito bridge su stdout
                print(f"[BRIDGE] status={status} payload={payload}", flush=True)
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
