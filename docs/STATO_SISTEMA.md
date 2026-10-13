# STATO SISTEMA AI_TRADING

## 1. Stato rilevato (auto)
Timestamp: 2026-10-13 23:58:34
TMUX: ai_workforce: 1 windows (created Tue Oct 13 16:36:06 2026)
cycle_agent: 1 windows (created Tue Oct 13 16:36:06 2026)
experience_agent: 1 windows (created Tue Oct 13 16:36:06 2026)
kronos_agent: 1 windows (created Tue Oct 13 16:36:06 2026)
market_anomaly: 1 windows (created Tue Oct 13 16:36:06 2026)
news_agent: 1 windows (created Tue Oct 13 16:36:06 2026)
nzt_agent: 1 windows (created Tue Oct 13 16:36:06 2026)
signal_observer: 1 windows (created Tue Oct 13 16:36:06 2026)
social_agent: 1 windows (created Tue Oct 13 16:36:06 2026)
strategy_validator: 1 windows (created Tue Oct 13 16:36:06 2026)
supervisor: 1 windows (created Tue Oct 13 16:36:06 2026)
volume_agent: 1 windows (created Tue Oct 13 16:36:06 2026)
Servizi systemd user: web-app: active; controllo-remoto: active; ai-trading-agenti: active
Processi Windows: terminal.exe: carlo       2366  0.0  0.0   9984  2392 ?        S    16:36   0:00 bash -c wineserver -k; export WINEPREFIX="/home/carlo/.wine_trading_finale"; export WINEDEBUG=-all; cd "/home/carlo/Scrivania/XM MT4" && wine terminal.exe /portable
carlo       2369 15.6  0.9 1464320 118804 ?      Sl   16:36  69:13 terminal.exe /portable; metaeditor.exe: carlo      11929  2.1  1.5 1427060 191404 ?      Sl   17:24   8:28 Z:\home\carlo\Scrivania\XM MT4\metaeditor.exe /portable
File condivisi MT4: orders.json: presente (397 bytes); open_time.json: presente (1973 bytes); sl_commands.json: presente (109 bytes)
IP Tailscale: 100.77.33.7
Git: commit 957b8b5: auto-sync $(date)

## 2. Diario azioni

- 13 October 2026 - 2d37cfd: test 1e primo
- 13 October 2026 - 9e608d4: test 1e secondo
- 13 October 2026 - b4e0d28: test 1e terzo
- 13 October 2026 - b29cde3: test 1f
- 13 October 2026 - 92921f6: auto-sync $(date)
- 13 October 2026 - 33d8e26: auto-sync $(date)
- 13 October 2026 - 8f5967a: auto-sync $(date)
- 13 October 2026 - 81849dc: auto-sync $(date)
- 13 October 2026 - 957b8b5: auto-sync $(date)

## 3. Problemi noti

- EA UpdateOrdersFile accumula ordini nel file senza cancellazione
- supervisor venv rotto (percorso venv non corretto o mancante)
- web_app ridotto (funzionalità limitate rispetto alla versione completa)
- saldo non letto da MT4 (EA non invia o script non legge correttamente)
- loop sell non diagnosticato (possibile bug nella logica di chiusura)

## 4. Prossimo passo

- recuperare dashboard da web_app_backup.py per ripristinare funzionalità complete
- correggere supervisor verificando percorso venv e riavviando servizi
- aggiungere account.json scritto dall'EA per sincronizzare conto di trading
