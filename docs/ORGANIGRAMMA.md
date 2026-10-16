# ORGANIGRAMMA PROGETTO AI_TRADING

Ultimo aggiornamento: 2026-10-16 23:00
Autore: Carlo + Chat

Mappa visiva del progetto. Ogni nuova chat legge QUESTO file + MAPPA_PROGETTO.md
+ CONTESTO.md. Nessuna memoria umana richiesta.

---

## 1. STRUTTURA CARTELLE

/home/carlo/AI_Trading/
├── .git/                    (126 MB, storia Git)
├── Kronos/                  (26 MB, repo esterno per kronos_agent)
├── controllo_remoto/        (server.py, systemd user "controllo-remoto")
├── docs/                    (documenti + archivio)
│   ├── CONTESTO.md          -> vedi /home/carlo/AI_Trading/CONTESTO.md
│   ├── HANDOFF.md           -> vedi /home/carlo/AI_Trading/HANDOFF.md
│   ├── PENDENZE.md          (20 voci aperte)
│   ├── ORGANIGRAMMA.md      (questo file)
│   ├── MAPPA_PROGETTO.md    (ruolo componenti)
│   ├── STATO_SISTEMA.md     (auto-generato da tools/stato_sistema.py)
│   ├── kilo3_evidence/, kilo4_evidence/
│   ├── research/            (documenti da ricerca agenti)
│   └── archive/2026-10/     (32 cartelle + 56 file .py + 40 file vari DEPRECATED)
├── signals/                 (usata da signal_observer_agent)
│   ├── signals.json         (fermo al 2026-09-06)
│   ├── report.json
│   └── verified_signals.json
├── *.py                     (13 file attivi)
├── *.md                     (3 file attivi)
├── *.json, *.txt            (config + contesto)
├── *.sh                     (start_all.sh, agents_night_shift.sh)
└── AI_BRIDGE_EA*.mq4        (EA MQL4)

---

## 2. COMPONENTI ATTIVI

### 2.1 Orchestratore

- **File**: orchestrator.py (18020 byte, ott 16 22:04)
- **md5**: 76b3b3eecb734c7f4d5a2b9b33e979e9
- **Sessione tmux**: ai_workforce
- **Ruolo**: legge 5 file di contesto, calcola score, decide BUY/SELL/HOLD,
  invia comandi a EA via AI_BRIDGE_CMD.txt, legge esito da AI_BRIDGE_RES.txt,
  logga in decision_log.jsonl.
- **Logica post-apertura**: check_time_stop, check_break_even,
  check_friday_profit (C1), check_friday_close (C2).
- **Ciclo**: 300 secondi (MAIN_LOOP_SLEEP).

### 2.2 Agenti di segnale (5)

| Agente | File | Contesto scritto | Segnale |
|---|---|---|---|
| news_agent | news_agent.py | news_context.txt | +0.3/0/-0.3 |
| social_agent | social_agent.py | social_context.txt | +0.2/0/-0.2 |
| cycle_agent | cycle_agent.py | cycles_context.txt | +0.2/0/-0.2 |
| volume_agent | volume_agent.py | volume_context.txt | variabile |
| experience_agent | experience_agent.py | experiences.json (lettura) | -0.2/0/+0.2 |

### 2.3 Agenti dormienti/muti (4)

| Agente | File | Nota |
|---|---|---|
| kronos_agent | kronos_agent.py | legge ~/mt4_shared/orders.json |
| market_anomaly | market_anomaly_agent.py | log vuoto (P004) |
| nzt_agent | nzt_agent.py | legge ~/mt4_shared/orders.json |
| signal_observer | signal_observer_agent.py | usa signals/, log vuoto |
| strategy_validator | strategy_validator.py | log vuoto |

### 2.4 Supervisor

- **File**: supervisor_agent.py (5421 byte, ott 14 21:37)
- **Sessione tmux**: supervisor
- **Ruolo**: legge tmux, riavvia agenti critici fermi, aggiorna
  audit_status.json ogni 300s.
- **BUG NOTO (P001)**: controlla solo nome sessione tmux, non processo figlio.

### 2.5 Dashboard

- **File**: web_app.py (22748 byte, ott 14 20:56)
- **Servizio systemd user**: web-app (attivo, porta 5000)
- **URL**: http://100.77.33.7:5000
- **Pagine**: /, /trading, /agents, /verifier, /media, /ecommerce

### 2.6 Controllo remoto

- **File**: controllo_remoto/server.py
- **Servizio systemd user**: controllo-remoto (attivo, PID 1045, 3 giorni)

### 2.7 EA MT4

- **File**: /home/carlo/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.mq4
- **Versione**: v3.5-bis
- **md5 .mq4**: c728dfa14c3246268dedd260a0542418
- **md5 .ex4**: e9df7b1d225b52b9e756d3df72c19f27
- **Ruolo**: esegue ordini, scrive account.json e orders.json,
  legge AI_BRIDGE_CMD.txt, scrive AI_BRIDGE_RES.txt, legge sl_commands.json.
- **Timer**: 5 secondi.

---

## 3. FILE DI CONTESTO (usati dall'orchestratore)

| File | Scritto da | Letto da | Frequenza |
|---|---|---|---|
| news_context.txt | news_agent | orchestrator | 10 min |
| social_context.txt | social_agent | orchestrator | 10 min |
| cycles_context.txt | cycle_agent | orchestrator | 15 min? |
| volume_context.txt | volume_agent | orchestrator | 1 min? |
| experiences.json | experience_agent | orchestrator | evento |

---

## 4. FILE DI COMUNICAZIONE CON MT4

| File | Chi scrive | Chi legge | Note |
|---|---|---|---|
| AI_BRIDGE_CMD.txt | orchestrator | EA | one-shot, EA cancella |
| AI_BRIDGE_RES.txt | EA | orchestrator | esito OK/ERR |
| orders.json | EA | orchestrator, agenti | stato ordini |
| account.json | EA | orchestrator, web_app | stato conto |
| sl_commands.json | orchestrator | EA | break-even SL |
| open_time.json | orchestrator | orchestrator | timestamp apertura |

---

## 5. SERVIZI SYSTEMD USER

- web-app.service (attivo, porta 5000)
- controllo-remoto.service (attivo, PID 1045)

---

## 6. SESSIONI TMUX ATTIVE

ai_workforce, supervisor, news_agent, social_agent, cycle_agent,
volume_agent, experience_agent, kronos_agent, nzt_agent, market_anomaly,
signal_observer, strategy_validator.

---

## 7. CRON ATTIVI

- 0 * * * * auto-sync Git (commit + push orari)

**Sospesi 2026-10-16**: 7 job tools/ (skill_scout, strategy_tester_agent,
auto_reflect, generate_dashboard, daily_reporter, youtube_scout,
auto_researcher).

---

## 8. DOCUMENTI CHIAVE

- CONTESTO.md — decisioni D1-D20 + stato
- HANDOFF.md — diario sessioni
- docs/PENDENZE.md — 20 voci aperte
- docs/ORGANIGRAMMA.md — questo file
- docs/MAPPA_PROGETTO.md — ruolo componenti
- decision_log.jsonl — storico decisioni orchestratore

---

## 9. ARCHIVIO

docs/archive/2026-10/ contiene il vecchio mondo (fino al 2026-10-16):
- 32 cartelle DEPRECATED (tools, core, data, docs_v2, ecc.)
- 56 file .py DEPRECATED (adaptive_ai, audit_agent, ecc.)
- 11 documenti .md DEPRECATED
- 21 backup .pre_* DEPRECATED
- 40 file vari DEPRECATED

Nessuno di questi è attivo. Recuperabili se serve.
