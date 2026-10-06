# AI_BRIDGE V3 — Handoff Completo

Ultimo aggiornamento: 2026-10-06

## 🔧 Fix 2026-10-06 (sera)

- **Orchestratore:** risolto bug ordini infiniti. `MAX_OPEN_ORDERS = 3`, `time.sleep = 3600`. Lock esclusivo in `/tmp/orchestrator.lock`.
- **File comando:** `AI_BRIDGE_CMD.txt` svuotato (0 byte).
- **Solo orchestratore** scrive ordini (confermato via grep).
- **Dashboard:** multi-progetto (Home, Trading, Media, E-commerce, Verifier).
- **Verifier:** 3/3 file PASS (position_manager, orchestrator, web_app).
- **Auto-Researcher:** attivo, cron 5:00, report Telegram.

## 🎯 Visione

Azienda digitale multi-progetto. Ogni progetto è un'azienda indipendente. Tu sei CEO, intervieni solo su direzioni strategiche e problemi gravi.

**Principio:** come acqua — si adatta a qualsiasi ambiente, non dipende da AI/agenti specifici.

## 🏢 Progetti attivi

1. **Forex Trading** (in produzione demo) — conto FP Markets 450000065, server FPTrading-demo
2. **Media Company** (video automatici) — da avviare
3. **E-commerce** (dropshipping/affiliazione) — futuro
4. **Piattaforma scommesse** (multilingua) — futuro

## 🔧 Infrastruttura attuale

### Agenti attivi (tmux)
- `ai_workforce` — orchestratore trading (ogni ora)
- `position_manager` — break-even/trailing stop (60s)
- `verifier` — test automatici post-modifica (60s)
- `watchdog` — controllo sistema (5 minuti)
- `reconciliation` — riconciliazione ordini (60s)
- `telegram` — bot comandi
- `dashboard` — web app Flask

### File monitorati da Verifier
- `tools/position_manager.py` → `tests/test_position_manager.py` (2/2 PASS)
- `orchestrator.py` → `tests/test_orchestrator.py` (4/4 PASS)
- `web_app.py` → `tests/test_dashboard.py` (5/5 PASS)

### EA MT4
- File: `~/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.mq4`
- Versione: 3.3 con `ApplySLModifications()`
- Legge comandi: `AI_BRIDGE_CMD.txt`
- Scrive stato: `orders.json`
- Legge SL commands: `sl_commands.json`
- Timer: 5 secondi

### File condivisi
- `~/mt4_shared/orders.json` → symlink a `~/Scrivania/XM MT4/MQL4/Files/orders.json`
- `~/mt4_shared/sl_commands.json` → comandi SL dal Position Manager

## 📌 Decisioni chiave approvate

1. **Comando unico:** ogni interazione = 1 comando aggregato.
2. **File unico:** per modifiche, sempre file completo con `nano`, mai `sed` o `cat` lunghi.
3. **Zero costi:** solo tool gratuiti e open-source.
4. **Modularità:** ogni componente sostituibile senza toccare gli altri.
5. **Test automatici:** ogni modifica passa da Verifier prima di essere considerata valida.
6. **CEO role:** utente interviene solo su direzioni strategiche.
7. **Memoria:** Engram/Neuragram + copia-incolla manuale a inizio chat web.

## 🚧 Problemi aperti

1. **Memoria tra chat web:** DeepSeek web non ha accesso filesystem. Soluzione: incollare `.engram/index.md` a inizio chat.
2. **DeepSeek Harness + Ollama:** da testare come alternativa con accesso filesystem.
3. **Microfono Linux:** da risolvere (Voice In su Chrome come test rapido).
4. **Backup:** hard disk esterno da acquistare.

## 🎯 Prossimi passi immediati

1. **Creare `tools/auto_researcher.py`** — agente ricerca automatica GitHub/HF/Reddit/Twitter per tool/skill nuovi.
2. **Dashboard multi-progetto** — tab per passare da Trading a Media a E-commerce.
3. **Test DeepSeek Harness + Ollama** — se funziona, memoria automatica.
4. **Avviare progetto Media Company** — MVP: 1 video/giorno YouTube Shorts.
5. **Integrare MiroFish** — simulazione predittiva per contenuti e trading.

## 📊 Stato conto Forex

- Balance: €100.046,61
- Equity: €100.048,89
- Operazioni aperte: 1 (ticket 35483, sell @ 1.12455, SL 1.12475, TP 1.11432)
- Operazioni chiuse: 2 TP colpiti (+€12,93)
- Break-even: funzionante (testato)
- Trailing stop: configurato (20 pip)

## 🛠️ Comandi chiave

```bash
# Riavvia orchestratore
tmux kill-session -t ai_workforce 2>/dev/null
tmux new-session -d -s ai_workforce "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && while true; do python3 orchestrator.py; sleep 3600; done"

# Dashboard
tmux kill-session -t dashboard 2>/dev/null
tmux new-session -d -s dashboard "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 web_app.py"

# Verifier
tmux kill-session -t verifier 2>/dev/null
tmux new-session -d -s verifier "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 tools/verifier.py 2>&1 | tee -a ~/verifier.log"

# Test manuale
cd ~/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 tests/test_dashboard.py
