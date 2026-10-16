# MAPPA PROGETTO AI_TRADING

Ultimo aggiornamento: 2026-10-16 23:05
Autore: Carlo + Chat

Ruolo e stato di ogni componente. Da leggere INSIEME a ORGANIGRAMMA.md
e CONTESTO.md.

Legenda stato:
- ATTIVO = in uso oggi
- DORMIENTE = esiste, non usato, recuperabile
- OBSOLETO = archiviato, non usato
- PENDENZA = problema noto, vedi PENDENZE.md

---

## 1. FILE PYTHON IN ROOT (13)

### 1.1 Orchestratore
- **orchestrator.py** (18020 byte, md5 76b3b3ee...)
  - STATO: ATTIVO
  - RUOLO: cervello del sistema. Legge 5 segnali, decide, invia comandi.
  - DIPENDE DA: news_context.txt, social_context.txt, cycles_context.txt,
    volume_context.txt, experiences.json, account.json, orders.json.
  - SCRIVE: decision_log.jsonl, AI_BRIDGE_CMD.txt, sl_commands.json,
    open_time.json.

### 1.2 Agenti di segnale (5)
- **news_agent.py** (3946 byte) — ATTIVO. Scrive news_context.txt (10 min).
- **social_agent.py** (1538 byte) — ATTIVO. Scrive social_context.txt (10 min).
- **cycle_agent.py** (920 byte) — ATTIVO. Scrive cycles_context.txt.
- **volume_agent.py** (1364 byte) — ATTIVO. Scrive volume_context.txt.
- **experience_agent.py** (1952 byte) — ATTIVO. Aggiorna experiences.json.

### 1.3 Agenti dormienti/muti (4)
- **kronos_agent.py** (1067 byte) — DORMIENTE. Legge ~/mt4_shared/orders.json.
  Log vuoto (P004).
- **market_anomaly_agent.py** (5194 byte) — DORMIENTE. Log vuoto (P004).
- **nzt_agent.py** (1935 byte) — DORMIENTE. Legge ~/mt4_shared/orders.json.
  Log vuoto (P004).
- **signal_observer_agent.py** (3451 byte) — DORMIENTE. Usa signals/.
  Legge signals.json (fermo al 2026-09-06). Log vuoto (P004).

### 1.4 Supervisor e altri
- **supervisor_agent.py** (5421 byte) — ATTIVO. Watchdog.
  BUG NOTO (P001): controlla solo nome sessione tmux, non processo figlio.
- **strategy_validator.py** (2480 byte) — DORMIENTE. Log vuoto (P004).
- **web_app.py** (22748 byte) — ATTIVO. Dashboard Flask, servizio systemd.

---

## 2. FILE DI CONTESTO

| File | Scritto da | Letto da | Frequenza | Stato |
|---|---|---|---|---|
| news_context.txt | news_agent | orchestrator | 10 min | ATTIVO |
| social_context.txt | social_agent | orchestrator | 10 min | ATTIVO |
| cycles_context.txt | cycle_agent | orchestrator | ~10 min | ATTIVO |
| volume_context.txt | volume_agent | orchestrator | ~1 min | ATTIVO |
| experiences.json | experience_agent | orchestrator | evento | ATTIVO |

---

## 3. FILE DI COMUNICAZIONE MT4

| File | Chi scrive | Chi legge | Note | Stato |
|---|---|---|---|---|
| AI_BRIDGE_CMD.txt | orchestrator | EA MT4 | one-shot | ATTIVO |
| AI_BRIDGE_RES.txt | EA MT4 | orchestrator | esito | ATTIVO |
| orders.json | EA MT4 | orchestrator, agenti | ordini | ATTIVO |
| account.json | EA MT4 | orchestrator, web_app | conto | ATTIVO |
| sl_commands.json | orchestrator | EA MT4 | SL break-even | ATTIVO |
| open_time.json | orchestrator | orchestrator | timestamp | ATTIVO |

---

## 4. EA MT4

- **File**: /home/carlo/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.mq4
- **Versione**: v3.5-bis
- **Stato**: ATTIVO
- **md5 .mq4**: c728dfa14c3246268dedd260a0542418
- **md5 .ex4**: e9df7b1d225b52b9e756d3df72c19f27
- **WINEPREFIX**: /home/carlo/.wine_trading_finale
- **Conto**: FPTrading-Demo login 450000065

---

## 5. SERVIZI SYSTEMD USER

| Servizio | Stato | Note |
|---|---|---|
| web-app.service | ATTIVO | porta 5000 |
| controllo-remoto.service | ATTIVO | server.py, PID 1045 |

---

## 6. SESSIONI TMUX (12)

| Sessione | Script | Stato |
|---|---|---|
| ai_workforce | orchestrator.py | ATTIVO |
| supervisor | supervisor_agent.py | ATTIVO |
| news_agent | news_agent.py | ATTIVO |
| social_agent | social_agent.py | ATTIVO |
| cycle_agent | cycle_agent.py | ATTIVO |
| volume_agent | volume_agent.py | ATTIVO |
| experience_agent | experience_agent.py | ATTIVO |
| kronos_agent | kronos_agent.py | DORMIENTE (log vuoto) |
| nzt_agent | nzt_agent.py | DORMIENTE (log vuoto) |
| market_anomaly | market_anomaly_agent.py | DORMIENTE (log vuoto) |
| signal_observer | signal_observer_agent.py | DORMIENTE (log vuoto) |
| strategy_validator | strategy_validator.py | DORMIENTE (log vuoto) |

---

## 7. CARTELLE ATTIVE

| Cartella | Ruolo | Stato |
|---|---|---|
| .git/ | Storia Git | ATTIVO |
| Kronos/ | Repo esterno per kronos_agent | ATTIVO |
| controllo_remoto/ | Server controllo remoto | ATTIVO |
| docs/ | Documenti + archivio | ATTIVO |
| signals/ | Segnali per signal_observer | ATTIVO |

---

## 8. CARTELLE ARCHIVIATE (docs/archive/2026-10/)

Tutte DEPRECATED, non attive:
architecture, assets, _backups, backups, backup_v2_initial, config, configs,
config_v2, core, core_v2, data, data_v2, docs_v2, emergency_backup, engram,
examples, legacy, logs, logs_v2, mt4, mt4_shared, nodes, recovery_notes,
research, sandbox, scripts, static, strategies, tests, tests_v2, tools.

**py_files_DEPRECATED**: 56 file .py (adaptive_ai, audit_agent, backtest_*,
daily_reporter, dashboard_remote, decision, diagnostics_v2, feedback_loop,
fusion_engine, github_researcher, indicator_tester_agent, learning_engine,
main, main_v2, market_classifier, market_regime, memory_engine, multidigest,
news_critical, news, optimize, optimizer, orchestrator_backup,
orchestrator_simple, performance_tracker, prompts, reset_runtime,
risk_manager, run_backtest_*, sentinel, skill_researcher,
strategy_tester_agent, sync_agent, tool_updater_agent, web_app_backup,
web_app_min, youtube_agent, yt_digest, +14 test_*).

**md_files_DEPRECATED**: 11 documenti (AGENTS, AI_BRIDGE_V2_CONTINUITY_PROMPT,
FAILED_ATTEMPTS, HANDOFF_NEW_CHAT, KILO, MANUALE_PROGETTO, OBIETTIVI_PROGETTO,
PROJECT_RULES, README, RIASSUNTO, STATUTO).

**misc_files_DEPRECATED**: 21 backup .pre_*, 40 file vari (.txt, .json, .csv,
.html, .zip, .tar.gz, .mqh), 5 script setup, 3 file deploy.

---

## 9. FILE DI CONFIGURAZIONE

| File | Ruolo | Stato |
|---|---|---|
| config.json | Config orchestratore | ATTIVO (permessi 600) |
| requirements.txt | Dipendenze Python | ATTIVO |
| runtime.txt | Versione Python | ATTIVO |
| .gitignore | Esclusioni Git | ATTIVO |
| start_all.sh | Avvio agenti tmux | ATTIVO |
| agents_night_shift.sh | Agenti notturni | DORMIENTE (non in cron) |

---

## 10. DOCUMENTI CHIAVE

| File | Ruolo |
|---|---|
| CONTESTO.md | Decisioni D1-D20, stato sistema |
| HANDOFF.md | Diario sessioni |
| docs/PENDENZE.md | 20 voci aperte |
| docs/ORGANIGRAMMA.md | Struttura visiva |
| docs/MAPPA_PROGETTO.md | Questo file |
| docs/STATO_SISTEMA.md | Auto-generato da tools/stato_sistema.py |
| APERTURA_CHAT.md | Pacchetto per nuova chat |
| decision_log.jsonl | Storico decisioni orchestratore |

---

## 11. COME USARE QUESTA MAPPA

**Per una chat nuova**:
1. Leggere ORGANIGRAMMA.md (struttura).
2. Leggere MAPPA_PROGETTO.md (questo file, ruoli).
3. Leggere CONTESTO.md (decisioni).
4. Leggere HANDOFF.md (ultima sessione).
5. Leggere PENDENZE.md (problemi aperti).

**Prima di modificare un file**:
- Verificare se è ATTIVO o DEPRECATED.
- Se DEPRECATED, chiedere a Carlo se va recuperato o ignorato.
- Se ATTIVO, seguire D3 (backup + md5).

**Prima di aggiungere un file**:
- Capire dove va (root? docs? signals?).
- Se è un agente, metterlo in root con suffisso `_agent.py`.
- Se è un documento, metterlo in `docs/`.
- Se è contesto, metterlo in root con suffisso `_context.txt`.
