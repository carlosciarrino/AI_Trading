#!/bin/bash
# check_test.sh - Monitoraggio test 2 settimane AI_Trading
# Uso: ./tools/check_test.sh
cd /home/carlo/Progetti/AI_Trading

echo "================================================"
echo " CHECK TEST AI_TRADING - $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================"

echo ""
echo "--- 1. SERVIZIO ---"
systemctl is-active ai-workforce.service
sudo systemctl status ai-workforce.service --no-pager 2>/dev/null | grep -E "Active:|Main PID:" | head -2

echo ""
echo "--- 2. SESSIONI TMUX ---"
tmux ls 2>/dev/null | wc -l
tmux ls 2>/dev/null | awk -F: '{print "  " $1}'

echo ""
echo "--- 3. CONT0 DEMO (account.json) ---"
cat "/home/carlo/Scrivania/XM MT4/MQL4/Files/account.json" 2>/dev/null | python3 -m json.tool 2>/dev/null | grep -E "balance|equity|margin|profit|open_orders|timestamp"

echo ""
echo "--- 4. AUDIT STATUS (supervisore) ---"
cat audit_status.json 2>/dev/null | python3 -m json.tool 2>/dev/null | grep -E "timestamp|balance|equity|ok|reason|has_issue" | head -10

echo ""
echo "--- 5. FINANCIAL GUARD (supervisore) ---"
tail -5 /home/carlo/supervisor.log 2>/dev/null

echo ""
echo "--- 6. ULTIME 5 DECISIONI ---"
tail -5 decision_log.jsonl 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line)
        print(f\"  {d.get('timestamp','?')[:19]} | {d.get('signal','?'):5s} | {d.get('action_taken','?'):10s} | ticket={d.get('ticket')} | {d.get('reason','?')}\")
    except: pass
"

echo ""
echo "--- 7. FORECAST ---"
cat forecast.json 2>/dev/null | python3 -m json.tool 2>/dev/null

echo ""
echo "--- 8. TRIGGERS ---"
cat triggers.json 2>/dev/null | python3 -m json.tool 2>/dev/null

echo ""
echo "--- 9. ALERT (se esiste) ---"
if [ -f docs/ALERT.md ]; then cat docs/ALERT.md; else echo "(nessun alert)"; fi

echo ""
echo "--- 10. LOG ORCHESTRATORE (ultime 10) ---"
tail -10 /home/carlo/ai_workforce.log 2>/dev/null

echo ""
echo "--- 11. LOG NEWS (ultime 3) ---"
tail -3 /home/carlo/news_agent.log 2>/dev/null

echo ""
echo "================================================"
