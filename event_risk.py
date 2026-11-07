#!/usr/bin/env python3
"""event_risk.py - Blocca il trading se ci sono eventi macro imminenti."""
import json, os, time
from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup

OUTPUT_JSON = "/home/carlo/AI_Trading/event_risk.json"

# Fonte: ForexFactory (feed XML pubblico)
FF_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

def fetch_events():
    try:
        r = requests.get(FF_URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.content, "xml")
        events = []
        for item in soup.find_all("event"):
            try:
                # Formato data: "11-07-2026" e ora "8:30am"
                date_str = item.find("date").text.strip()
                time_str = item.find("time").text.strip()
                currency = item.find("country").text.strip()
                impact = item.find("impact").text.strip().lower()
                title = item.find("title").text.strip()
                
                if impact != "high" or currency not in ("USD", "EUR"):
                    continue
                    
                # Parsing data e ora (semplificato, assumiamo formato US)
                # Esempio: "11-07-2026" -> 2026-11-07
                dt_str = f"{date_str} {time_str}"
                # Prova formati comuni
                for fmt in ("%m-%d-%Y %I:%M%p", "%m-%d-%Y %H:%M"):
                    try:
                        dt = datetime.strptime(dt_str, fmt).replace(tzinfo=timezone.utc)
                        break
                    except ValueError:
                        dt = None
                        
                if dt:
                    events.append({
                        "title": title,
                        "currency": currency,
                        "time_utc": dt.isoformat(),
                        "impact": impact
                    })
            except Exception:
                continue
        return events
    except Exception as e:
        print(f"[event_risk] Errore fetch: {e}", flush=True)
        return []

def main():
    events = fetch_events()
    now = datetime.now(timezone.utc)
    
    # Blocca se un evento High è entro 2 ore prima o 1 ora dopo
    block = False
    next_event = None
    for e in events:
        try:
            ev_time = datetime.fromisoformat(e["time_utc"])
            delta = (ev_time - now).total_seconds() / 60.0  # minuti
            # Blocco: da 120 min prima a 60 min dopo
            if -60 <= delta <= 120:
                block = True
                if next_event is None or delta < next_event["delta"]:
                    next_event = {"title": e["title"], "delta": delta, "time": e["time_utc"]}
        except Exception:
            continue
            
    result = {
        "timestamp": now.isoformat(),
        "block": block,
        "reason": f"Evento imminente: {next_event['title']} tra {next_event['delta']:.0f} min" if next_event else "Nessun evento imminente",
        "events": events
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
        
    print(f"[event_risk] Block: {block} | {result['reason']}", flush=True)

if __name__ == "__main__":
    main()
