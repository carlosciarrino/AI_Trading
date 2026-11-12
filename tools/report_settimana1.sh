#!/bin/bash
cd /home/carlo/Progetti/AI_Trading
echo "=== REPORT SETTIMANA 1 (12-16 nov 2026) ==="
echo ""
echo "--- Conto finale ---"
cat "/home/carlo/Scrivania/XM MT4/MQL4/Files/account.json" | python3 -m json.tool
echo ""
echo "--- Decisioni: conteggio per azione ---"
python3 - <<'PY'
import json
from collections import Counter
c = Counter(); tickets = []
for line in open("decision_log.jsonl"):
    try: d = json.loads(line)
    except: continue
    c[d.get("action_taken","?")] += 1
    if d.get("ticket"): tickets.append((d.get("timestamp","")[:19], d.get("signal"), d.get("ticket")))
print("Azioni:", dict(c))
print("\nTicket aperti (ultimi 20):")
for t in tickets[-20:]: print(" ", t)
PY
echo ""
echo "--- Ordini chiusi (orders.json) ---"
cat "/home/carlo/Scrivania/XM MT4/MQL4/Files/orders.json" | python3 -c "
import sys, json
o = json.load(sys.stdin)
closed = [x for x in o if x.get('status')=='closed']
print(f'Chiusi totali: {len(closed)}')
pnl = sum(x.get('pnl',0) for x in closed)
print(f'PNL totale storico: {pnl:.2f}')
print('Ultimi 10 chiusi:')
for x in closed[-10:]:
    print(f\"  {x.get('action'):5s} {x.get('lots')} @ {x.get('price')} -> {x.get('close_price')} PNL={x.get('pnl')}\")
"
echo ""
echo "--- Alert supervisore ---"
cat docs/ALERT.md 2>/dev/null || echo "(nessun alert)"
echo ""
echo "--- Riepilogo log errori ---"
grep -iE "error|traceback|exception|failed" /home/carlo/ai_workforce.log /home/carlo/supervisor.log /home/carlo/news_agent.log 2>/dev/null | tail -20 || echo "(nessun errore)"
