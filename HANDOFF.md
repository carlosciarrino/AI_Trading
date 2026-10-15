# HANDOFF - Sessione 2026-10-14 / 2026-10-15

Diario operativo. Da leggere INSIEME a CONTESTO.md.

---

## Sessione 2026-10-14 (ore 21:00-22:15)

Autore: Carlo + Chat.
Scopo: diario operativo della sessione.

### 1. Punto di partenza

- AI_BRIDGE_EA in MT4: rotto (v3.4 sbagliata di Kilo #3, o v3.3 parziale).
- orders.json: 121 KB, accumulo infinito di campi chiusi.
- Dashboard: versione ridotta, saldo hardcoded.
- supervisor: processo zombie, venv path sbagliato.
- Git cron: commit con messaggio letterale "auto-sync $(date)".
- 190 MB di file storico inutile in MT4 Files.
- 3 venv diversi, 2 inesistenti.
- orchestratore: operativo ma con 4 bug (path, regex, limiti, soglia).

### 2. Fatto

O1 - Dashboard unificata (web_app.py, 535 righe). Servizio web-app, porta 5000.
O2 - Fix accumulo orders.json. AI_BRIDGE_EA v3.5.
O3 - Supervisor v2. Legge tmux, riavvia critici, audit_status.json ogni 300s.
O4 - Fix crontab Git. 'auto-sync $(date)' -> "auto-sync $(date)".
O5 - Pulizia. 190 MB archiviati, test.mq4/.ex4 rimossi.
O7a - decision_log.jsonl. Tracciabilita' decisioni.
O7b - Fix orchestrator.py: path, regex volume, MAX_OPEN_ORDERS=1,
soglia da ±0.01 a ±0.10.

### 3. Da fare (aperto alla fine sessione)

O7c - 4 segnali su 5 sono sempre 0.
O7d - Logica post-apertura.
O6 - Ricerca agenti.
O9 - Orario London+NY.

---

## Sessione 2026-10-14 sera - O7c diagnosi 4 segnali (ore 22:00-23:15)

Scopo: O7c - indagare perche' 4 segnali su 5 davano sempre score 0.

### Scoperte

- **news**: ORFANO. news_agent scrive solo /tmp/news_score.txt. SOSPESO.
- **social**: FIXATO. sentiment_score() aggiunto. ATTIVO (-0.2).
- **cycle**: FIXATO. MultiIndex yfinance appiattito. ATTIVO.
- **volume**: regex orchestratore corretto. Score 0.00.
- **experience**: -0.2 (3 PERDITE recenti).
- **final_score**: -0.08. HOLD.

### Contratto orchestratore <-> EA chiarito

- Formato: `buy|sell lots sl tp` o `close <ticket>`.
- AI_BRIDGE_RES.txt contiene esito.
- Orchestratore NON legge AI_BRIDGE_RES.txt (fino O7b-bis).

### Da fare

1. Test end-to-end. FATTO 2026-10-14 notte.
2. Fix orders.json dedup. FATTO 2026-10-14 notte.
3. Orchestratore legge AI_BRIDGE_RES.txt. FATTO 2026-10-15.
4. O10 news redesign. FATTO 2026-10-15.

---

## Sessione 2026-10-14 notte - Fix orders.json dedup v3.5-bis (ore 23:00-23:45)

Scopo: fixare bug doppio status/pnl in orders.json.

### Fatto

- Diagnosi: dedup v3.5 non rimuoveva status:open/pnl:0 prima di appendere
  status:closed/pnl reale.
- Patch v3.5-bis: blocco objClean rimuove campi vecchi.
- Applicata via script Python.
- Prima applicazione fallita: MetaEditor sovrascrive file su disco con
  copia in memoria. Soluzione: chiudere MetaEditor prima (D14).
- File intermedio rotto (455 righe) -> ripristinato.
- Compilata: 0 errori, 0 warning.
- md5 .mq4 = c728dfa14c3246268dedd260a0542418
- md5 .ex4 = e9df7b1d225b52b9e756d3df72c19f27

### Test end-to-end superato

1. orders.json -> "[]" in 15 sec.
2. buy 0.01 0 0 -> "OK: aperto 253699 lotto 0.01".
3. orders.json: 1 record, 1 status":"open".
4. close 253699 -> "OK: chiuso 253699".
5. orders.json: 1 record, 1 status":"closed", 1 pnl (-0.04).
6. account.json: open_orders 0.

---

## Sessione 2026-10-15 - O7b-bis + O11 + pulizia (ore 18:30-19:30)

Autore: Carlo + Chat.

### 1. Fatto

**O7b-bis** - patch orchestrator.py:
1. `read_bridge_result(timeout=8)`.
2. `write_decision(... error=None)`.
3. Main loop legge esito EA dopo ogni comando.
4. Chiusura 24h idem.
- md5 orchestrator.py = 4f567d0d6009cbb8d01effc9344a4aad

**O11** - password broker rimossa da config.json:
- Nessun file usa broker.password.
- Permessi 600. md5 config.json = 65985576e9a14f20c2b2437c11b52a92.
- Backup: config.json.pre_o11.

**Pulizia**: rimossi 25 backup vecchi.
**.gitignore**: pattern *.pre_* e .pre_*.
**Regole**: D14, D15, D16.
**Commit Git**: `9fd95ce contesto: O7b-bis ...`.

### 2. Da fare

- O10: news redesign.
- O8: logica post-apertura.

---

## Sessione 2026-10-15 sera - O10 news redesign (ore 20:30-21:00)

Autore: Carlo + Chat.

### 1. Punto di partenza

- news_agent.py fermo 2026-09-05. Scriveva solo /tmp/news_score.txt.
- news_context.txt orfano.
- orchestrator.py forzava scores['news'] = 0.0.

### 2. Fatto

**news_agent.py v2** (113 righe):
- RSS Investing.com IT.
- Filtro keyword macro (IT+EN).
- Sentiment EN+IT.
- news_context.txt: "Ultime notizie macro (aggiornate <data>):" + N titoli
  + "Sentiment: ...". Loop 10 min.
- md5 news_agent.py = d5b5c99630b8ac0512a9b9440a4edc46
- Backup: news_agent.py.pre_o10.

**orchestrator.py O10**:
- Rimosso force-to-zero news.
- Legge "Sentiment:" da news_context.txt, +0.3/0/-0.3.
- md5 orchestrator.py = b99adeb9775958108ee3b99ec501ffae

### 3. Test

- news_agent v2: "news: 10 titoli (4 macro), sentiment=positivo".
- orchestrator: `news: 0.3`, final_score -0.02, HOLD.

### 4. Da fare

- O8: logica post-apertura.

---

## Sessione 2026-10-15 notte - O8 logica post-apertura (ore 21:00-21:30)

Autore: Carlo + Chat.

### 1. Punto di partenza

- orchestrator.py aveva solo check_time_stop (chiusura 24h).
- open_time.json e sl_commands.json inesistenti.
- experiences.json: 84 record storici.

### 2. Progettazione

4 funzioni:
- **check_time_stop**: chiude ordini >24h.
- **check_break_even**: profitto >= 20 pip -> sposta SL a entry ±2 pip.
- **check_friday_profit (C1)**: venerdi 15:00 UTC, chiude ordini con PNL > 0.
- **check_friday_close (C2)**: venerdi 20:00 UTC, chiude tutto.

Motivazione C1/C2: caso reale 2026-10-15, ordine +2 cent, commissione 6
cent -> netto -4 cent.

Parametri: BREAK_EVEN_PIP=20, BREAK_EVEN_OFFSET_PIP=2,
FRIDAY_PROFIT_HOUR_UTC=15, FRIDAY_CLOSE_HOUR_UTC=20, MAIN_LOOP_SLEEP=300.

### 3. Cosa e' stato fatto

- orchestrator.py riscritto in 5 blocchi (nano).
- Nuove funzioni: get_open_order, send_close_command, get_current_price,
  check_break_even, write_sl_command, check_friday_profit,
  check_friday_close.
- Main loop: chiama 4 check + sleep 300.
- md5 orchestrator.py = 76b3b3eecb734c7f4d5a2b9b33e979e9
- Righe: 489 (prima 330).
- Backup: orchestrator.py.pre_o8.

### 4. Verifica

- SINTASSI OK. 15 funzioni. Costanti O8. time.sleep(3600) rimosso.
- Orchestratore: `Punteggio: -0.020`, HOLD.
- Traceback nel log: residui vecchio processo, non bug.

### 5. Decisione nuova

**D17**: TP, SL, commissioni, spread sempre inclusi. PNL netto.

### 6. Commit Git

`df60d62 O8: logica post-apertura ... + D17`.

---

## Sessione 2026-10-15 notte - PENDENZE.md + D18 (ore 21:15-21:30)

Autore: Carlo + Chat.
Scopo: creare registro delle questioni in sospeso.

### 1. Motivazione

Carlo: "I grandi problemi spesso sono formati da un insieme di tanti
piccoli problemi." Le questioni non critiche emerse durante le sessioni
(bug minori, pulizie, debiti tecnici) si perdevano. Serve un registro.

### 2. Fatto

**docs/PENDENZE.md** creato con 11 voci aperte:

- P001: supervisor falso positivo (media)
- P002: experiences.json senza rotazione (media)
- P003: wrapper zombie tmux PID 1263886 (bassa)
- P004: 8 agenti su 11 con log vuoti (media)
- P005: loop sell non diagnosticato (bassa)
- P006: docs/STATO_SISTEMA.md auto-generato, chi lo scrive? (bassa)
- P007: verifica O8 con ordine reale (alta)
- P008: verifica O7b-bis con ordine reale (alta)
- P009: .gitignore esclude *.json (bassa)
- P010: social_agent.log fermo (bassa)
- P011: agenti esterni in MT4 Navigator (bassa)

Formato: ID [P###], data, priorita', contesto, azione.
- md5 docs/PENDENZE.md = 4a9203d3c724b45820249cf72c4437c3

**D18** aggiunta a CONTESTO.md: ogni questione in sospeso va registrata
IMMEDIATAMENTE in docs/PENDENZE.md, anche se rinviata. Quando chiusa, si
marca [CHIUSA YYYY-MM-DD] e si sposta in fondo.

### 3. Riepilogo sessione 2026-10-15

**Obiettivi completati:**
- O7b-bis: orchestratore legge AI_BRIDGE_RES.txt.
- O11: password broker rimossa.
- O10: news redesign + riattivazione segnale.
- O8: logica post-apertura (break-even, C1, C2).
- PENDENZE.md + D18 (registro pendenze).
- Pulizia backup, regole D14/D15/D16/D17/D18.
- Documenti aggiornati.

**Commit Git (5):**
- 9fd95ce contesto: O7b-bis + HANDOFF + pulizia
- 744db1b contesto: O11 + D15/D16
- 7a47e12 O10: news_agent v2 + riattivazione
- df60d62 O8: logica post-apertura + D17
- (prossimo) PENDENZE.md + D18

**Stato sistema:**
- 5/5 segnali attivi. Score -0.02. HOLD.
- EA v3.5-bis funzionante.
- Agenti vivi.
- Conto demo: ~100066 EUR, 0 ordini aperti.
- 11 pendenze aperte.

**Prossimo:**
- Verifica O8 con ordine reale (P007, alta priorita').
- Verifica O7b-bis con ordine reale (P008, alta).
- Pulizia experiences.json (P002).
- Bug supervisor (P001).
