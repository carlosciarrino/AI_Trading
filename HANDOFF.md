# HANDOFF - Sessione 2026-10-14 / 2026-10-15

Diario operativo. Da leggere INSIEME a CONTESTO.md.

---

## Sessione 2026-10-14 (ore 21:00-22:15)

Autore: Carlo + Chat.
Scopo: diario operativo della sessione.

### 1. Punto di partenza della sessione

- AI_BRIDGE_EA in MT4: rotto (v3.4 sbagliata di Kilo #3, o v3.3 parziale).
- orders.json: 121 KB, accumulo infinito di campi chiusi.
- Dashboard: versione ridotta, saldo hardcoded.
- supervisor: processo zombie, venv path sbagliato.
- Git cron: commit con messaggio letterale "auto-sync $(date)".
- 190 MB di file storico inutile in MT4 Files.
- 3 venv diversi puntati da file diversi, 2 inesistenti.
- orchestratore: operativo ma con 4 bug (path, regex, limiti, soglia).

### 2. Cosa e' stato fatto (in ordine)

O1 - Dashboard unificata riscritta da zero (web_app.py, 535 righe). Legge
account.json, orders.json, calcola PNL giorno/settimana, controllo agenti
tmux. Promossa a servizio systemd user "web-app", porta 5000.

O2 - Fix accumulo orders.json. Nuova versione AI_BRIDGE_EA v3.5. Logica
aggiunta: se un oggetto e' gia' "closed", viene copiato invariato (no
riappende campi). File ora stabile.

O3 - Supervisor v2 riscritto. Legge tmux, riavvia critici fermi, aggiorna
audit_status.json ogni 300s. Venv canonico: AI_Trading_Agents/venv.

O4 - Fix crontab Git. Da apici singoli a doppi: 'auto-sync $(date)' ->
"auto-sync $(date)". Ora i commit hanno timestamp reali.

O5 - Pulizia. orders_backup_20261002_2335.json (190 MB) -> gzip in
/home/carlo/Archivio_MT4/. test.mq4/test.ex4 rimossi da MT4 Experts.

O7a - decision_log.jsonl. Orchestratore ora scrive una riga JSON per ogni
decisione (score, pesi, punteggio, azione). Tracciabilita' completa.

O7b - Fix orchestrator.py: path ordini corretto (era ~/mt4_shared/, non
esiste). count_open_orders legge da account.json. Regex volume corretto.
MAX_OPEN_ORDERS = 1. Soglia decisionale da ±0.01 a ±0.10.

### 3. Cosa e' cambiato sul sistema

FILE MT4:
- /home/carlo/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.mq4 (v3.5)
- /home/carlo/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.ex4 (v3.5)
- Backup v3.4 in AI_BRIDGE_EA_v3.4.mq4/.ex4

FILE AI_Trading:
- web_app.py (dashboard unificata)
- supervisor_agent.py (supervisor v2)
- orchestrator.py (fix O7b)
- start_all.sh, agents_night_shift.sh (venv corretto)
- decision_log.jsonl (nuovo)
- CONTESTO.md (nuovo, 172 righe)
- HANDOFF.md (questo file)

SERVIZI:
- web-app: systemd user, attivo
- supervisor: tmux, attivo (PID nuovo)
- orchestratore ai_workforce: tmux, attivo in HOLD

### 4. Stato attuale dei processi

- Orchestratore: attivo, in HOLD. Punteggio attuale -0.04 < soglia 0.10.
- Supervisor: attivo, watchdog. Ultimo audit_status.json aggiornato.
- Dashboard: attiva su porta 5000.
- MT4: 0 ordini aperti. Account 100066.12 EUR.
- 12 sessioni tmux attive.

### 5. Cosa NON e' stato fatto (aperto)

O7c - 4 segnali su 5 sono sempre 0: news, social, cycle, volume.
O7d - Logica post-apertura (break-even, rivalutazione, chiusura venerdi').
O6 - Ricerca agenti (GitHub, forum, repo). Settore trading.
O9 - Orario di mercato London+NY in config.json (D12). Solo in produzione.

### 6. Prossimo passo esatto

O7c - Indagare perche' 4 agenti su 5 danno score 0.

### 7. Come verificare che il sistema e' come lo abbiamo lasciato

  tmux ls | grep -E "ai_workforce|supervisor"
  systemctl --user is-active web-app
  tail -3 /home/carlo/AI_Trading/decision_log.jsonl
  cat /home/carlo/Scrivania/XM MT4/MQL4/Files/account.json

### 8. Puntatori

- CONTESTO.md: stato stabile, decisioni.
- HANDOFF.md: questo file.
- decision_log.jsonl: storico decisioni orchestratore.

---

## Sessione 2026-10-14 sera - O7c diagnosi 4 segnali (ore 22:00-23:15)

Scopo: O7c - indagare perche' 4 segnali su 5 davano sempre score 0.

### Scoperte

- **news**: `news_context.txt` ORFANO. Nessun processo attivo lo scrive.
  `news_agent.py` scrive solo `/tmp/news_score.txt` (numero, sempre 0.0).
  Segnale SOSPESO in `orchestrator.py`. Cantiere O10.
- **social**: FIXATO. `social_agent.py` patchato con `sentiment_score()`
  (keyword EN). Contributo: -0.2.
- **cycle**: FIXATO. `cycle_agent.py` patchato: `df.columns.get_level_values(0)`.
  Segnale ATTIVO.
- **volume**: regex orchestratore accetta `score` o `Punteggio`. Score 0.00.
- **experience**: -0.2 (3 PERDITE recenti). Funziona.
- **final_score**: -0.08. Signal: HOLD.

### Contratto orchestratore <-> EA chiarito

- Formato comando: `buy|sell lots sl tp` oppure `close <ticket>`.
- `AI_BRIDGE_RES.txt` contiene esito (`OK: aperto ...` / `ERR: ...`).
- Orchestratore NON legge `AI_BRIDGE_RES.txt` (fino a O7b-bis).

### Da fare prossima sessione

1. Test end-to-end. FATTO 2026-10-14 notte.
2. Fix `orders.json` dedup (v3.5-bis). FATTO 2026-10-14 notte.
3. Orchestratore legge `AI_BRIDGE_RES.txt`. FATTO 2026-10-15.
4. Cantiere O10: news redesign. FATTO 2026-10-15.
5. Pulizia processi tmux zombie.

---

## Sessione 2026-10-14 notte - Fix orders.json dedup (v3.5-bis) (ore 23:00-23:45)

Scopo: fixare bug doppio "status"/"pnl" in orders.json.

### Fatto

- Diagnosi: dedup v3.5 non rimuoveva "status":"open" e "pnl":0 prima di
  appendere "status":"closed" e pnl reale.
- Patch v3.5-bis: blocco objClean rimuove i campi vecchi prima di appendere.
- Applicata via script Python.
- Prima applicazione fallita: MetaEditor sovrascrive file su disco con
  copia in memoria. Soluzione: chiudere MetaEditor prima della patch (D14).
- File intermedio rotto (455 righe, graffe sbilanciate) -> ripristinato.
- Compilata: 0 errori, 0 warning.
- md5 .mq4 = c728dfa14c3246268dedd260a0542418
- md5 .ex4 = e9df7b1d225b52b9e756d3df72c19f27

### Test end-to-end superato

1. orders.json -> "[]" in 15 sec.
2. buy 0.01 0 0 -> "OK: aperto 253699".
3. orders.json: 1 record, 1 status":"open".
4. close 253699 -> "OK: chiuso 253699".
5. orders.json: 1 record, 1 status":"closed", 1 pnl (-0.04).

---

## Sessione 2026-10-15 - O7b-bis + O11 + pulizia backup (ore 18:30-19:30)

Autore: Carlo + Chat.
Scopo: O7b-bis (orchestratore legge esito EA); O11 (password); pulizia.

### 1. Punto di partenza

- orchestrator.py (277 righe, md5 6c6d6f90...) non leggeva AI_BRIDGE_RES.txt.
- config.json conteneva broker.password in chiaro (mai su Git).
- Numerosi backup vecchi accumulati (25 file, ~240 KB).

### 2. Cosa e' stato fatto

**O7b-bis** - patch orchestrator.py, 4 modifiche:

1. Nuova funzione `read_bridge_result(timeout=8)`.
2. `write_decision(... error=None)`: nuovo campo opzionale `error`.
3. Main loop: dopo write CMD, cancella RES vecchio, attende, legge esito.
4. Chiusura 24h: stessa logica.

**md5 orchestrator.py post-patch**: 4f567d0d6009cbb8d01effc9344a4aad.
Righe: 330.

**O11** - password broker rimossa da config.json:

- Verificato: nessun file usa `broker.password`.
- Rimossa, permessi 600. md5 config.json post: 65985576e9a14f20c2b2437c11b52a92.

**Pulizia backup**: rimossi 25 file. Tenuti i principali.
**.gitignore**: aggiunti pattern `*.pre_*` e `.pre_*`.
**Regole nuove**: D14, D15, D16.

### 3. Test O7b-bis superato

Test unitario `read_bridge_result()`: 3 casi OK/ERR/timeout. Tutti passati.

### 4. Commit Git

`9fd95ce contesto: O7b-bis ... + pulizia backup`.

### 5. Da fare prossima sessione

- O10: news redesign.
- O8: logica post-apertura.

---

## Sessione 2026-10-15 sera - O10 news redesign (ore 20:30-21:00)

Autore: Carlo + Chat.
Scopo: riprogettare news_agent.py, riattivare segnale news.

### 1. Punto di partenza

- news_agent.py fermo al 2026-09-05. Scriveva solo /tmp/news_score.txt
  (numero). Non scriveva news_context.txt.
- news_context.txt orfano dal 2026-09-05 (formato vecchio, senza Sentiment).
- orchestrator.py forzava scores['news'] = 0.0 (SOSPESO).
- Segnale news contribuiva 0 al final_score.

### 2. Cosa e' stato fatto

**news_agent.py v2** (file completo, 113 righe):

- Legge RSS Investing.com IT (https://it.investing.com/rss/news.rss).
- Filtra titoli con keyword macro (IT+EN): fed, bce, tassi, inflazione,
  pil, lavoro, euro, dollaro, guerra, dazi, ecc.
- Sentiment EN+IT (positivo/negativo/neutro).
- Scrive news_context.txt nel formato:
  "Ultime notizie macro (aggiornate <data>):" + N titoli + "Sentiment: ...".
- Max 15 titoli (macro prima, poi altri). Loop ogni 10 min.
- md5 news_agent.py = d5b5c99630b8ac0512a9b9440a4edc46
- Backup: news_agent.py.pre_o10 (md5 25e6108b4c679526c99faf3d736ec5b4)

**orchestrator.py O10** (patch chirurgica, no file completo):

- Rimosso force-to-zero `scores['news'] = 0.0`.
- Aggiunto: legge `Sentiment:` da news_context.txt, assegna +0.3/0/-0.3.
- md5 orchestrator.py = b99adeb9775958108ee3b99ec501ffae
- Backup: orchestrator.py.pre_o10 (md5 4f567d0d6009cbb8d01effc9344a4aad)

### 3. Test superato

news_agent.py v2 eseguito una volta:
- Output: "news: 10 titoli (4 macro), sentiment=positivo".
- news_context.txt generato, formato corretto, Sentiment presente.

news_agent in tmux riavviato (sessione creata 20:43:52).

orchestrator.py riavviato:
- Punteggio combinato: -0.020 (prima -0.04/-0.08).
- decision_log.jsonl: `news: 0.3`, final_score -0.02, HOLD.

### 4. Calcolo

- news +0.3 × 0.20 = +0.06
- social -0.2 × 0.20 = -0.04
- experience -0.2 × 0.20 = -0.04
- cycle, volume = 0
- final_score = -0.02

### 5. Da fare prossima sessione

- **O8**: logica post-apertura (prossimo passo).
- Verifica O7b-bis in produzione al primo BUY reale.
- Bug noto supervisor (falso positivo su news_agent).
- 8 agenti con log vuoti.

### 6. Riepilogo finale sessione 2026-10-15

**Obiettivi completati:**
- O7b-bis: orchestratore legge AI_BRIDGE_RES.txt.
- O11: password broker rimossa da config.json.
- O10: news redesign + riattivazione segnale.
- Pulizia backup (25 file).
- Regole D14, D15, D16.
- Documenti aggiornati (2 commit Git).

**Stato sistema:**
- 5/5 segnali attivi. Punteggio attuale -0.02. HOLD.
- EA v3.5-bis funzionante.
- Agenti vivi (12 sessioni).
- Conto demo: saldo ~100066 EUR, 0 ordini aperti.

**Prossimo:**
- O8: logica post-apertura (break-even, rivalutazione, chiusura venerdi').
- Verifica O7b-bis con ordine reale.
- Bug supervisor.
