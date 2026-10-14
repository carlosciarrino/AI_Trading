# HANDOFF - Sessione 2026-10-14

Sessione: 14 ottobre 2026, ore 21:00-22:15
Autore: Carlo + Chat
Scopo: diario operativo della sessione. Da leggere INSIEME a CONTESTO.md.

## 1. Punto di partenza della sessione

- AI_BRIDGE_EA in MT4: rotto (v3.4 sbagliata di Kilo #3, o v3.3 parziale).
- orders.json: 121 KB, accumulo infinito di campi chiusi.
- Dashboard: versione ridotta, saldo hardcoded.
- supervisor: processo zombie, venv path sbagliato.
- Git cron: commit con messaggio letterale "auto-sync $(date)".
- 190 MB di file storico inutile in MT4 Files.
- 3 venv diversi puntati da file diversi, 2 inesistenti.
- orchestratore: operativo ma con 4 bug (path, regex, limiti, soglia).

## 2. Cosa e' stato fatto (in ordine)

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

## 3. Cosa e' cambiato sul sistema

FILE MT4:
- /home/carlo/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.mq4 (v3.5)
- /home/carlo/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.ex4 (v3.5)
- Backup v3.4 in AI_BRIDGE_EA.v3.4.mq4/.ex4

FILE AI_Trading:
- web_app.py (dashboard unificata)
- supervisor_agent.py (supervisor v2)
- orchestrator.py (fix O7b)
- start_all.sh, agents_night_shift.sh (venv corretto)
- decision_log.jsonl (nuovo)
- CONTESTO.md (nuovo, 172 righe)
- HANDOFF.md (questo file)
- APERTURA_CHAT.md (da creare subito dopo)

SERVIZI:
- web-app: systemd user, attivo
- supervisor: tmux, attivo (PID nuovo)
- orchestratore ai_workforce: tmux, attivo in HOLD

## 4. Stato attuale dei processi

- Orchestratore: attivo, in HOLD. Punteggio attuale -0.04 < soglia 0.10.
  Non aprira' nulla finche' i segnali non si rafforzano.
- Supervisor: attivo, watchdog. Ultimo audit_status.json aggiornato.
- Dashboard: attiva su porta 5000. Pagine /, /trading, /agents, /verifier ok.
- MT4: 0 ordini aperti. Account 100066.12 EUR.
- 12 sessioni tmux attive (ai_workforce, cycle_agent, experience_agent,
  kronos_agent, market_anomaly, news_agent, nzt_agent, signal_observer,
  social_agent, strategy_validator, supervisor, volume_agent).

## 5. Cosa NON e' stato fatto (aperto)

O7c - 4 segnali su 5 sono sempre 0: news, social, cycle, volume.
  - news_context.txt fermo al 2026-09-05 (40 giorni).
  - social_context.txt aggiornato ma non contiene 'positivo'/'negativo'.
  - cycles_context.txt non matcha il pattern 'mese N'.
  - volume_context.txt contiene 'score 0.00'.

O7d - Logica post-apertura: break-even, rivalutazione giornaliera,
  chiusura venerdi'. Vedi O8.

O6 - Ricerca agenti (GitHub, forum, repo). Settore trading.

O9 - Orario di mercato London+NY in config.json (D12). Solo in produzione.

## 6. Prossimo passo esatto

O7c - Indagare perche' 4 agenti su 5 danno score 0.

Azioni concrete:
1. Leggere news_context.txt, social_context.txt, cycles_context.txt,
   volume_context.txt: contenuto esatto.
2. Capire chi li scrive (quale agente).
3. Verificare se l'agente e' attivo (tmux, log).
4. Confrontare il formato atteso dall'orchestratore vs il formato scritto.
5. Fixare: o l'agente (scrive nel formato giusto) o l'orchestratore
   (legge il formato scritto).

## 7. Come verificare che il sistema e' come lo abbiamo lasciato

Da terminale Linux:

  tmux ls | grep -E "ai_workforce|supervisor"
  systemctl --user is-active web-app
  tail -3 /home/carlo/AI_Trading/decision_log.jsonl
  cat /home/carlo/Scrivania/XM MT4/MQL4/Files/account.json
  cat /home/carlo/AI_Trading/CONTESTO.md | head -20

Atteso:
- ai_workforce e supervisor attive
- web-app active
- decision_log.jsonl cresce di 1 riga ogni ora (HOLD o BUY/SELL)
- account.json aggiornato (open_orders coerente)

## 8. Puntatori

- CONTESTO.md: stato stabile, decisioni D1-D13.
- HANDOFF.md: questo file, diario operativo.
- APERTURA_CHAT.md: pacchetto per nuova chat.
- decision_log.jsonl: storico decisioni orchestratore.
- docs/kilo3_evidence/, docs/kilo4_evidence/: evidenze Kilo.
- Backup vari: .pre_o7a, .pre_o7b, .pre_venvfix, .pre_dashboard, ecc.

---

## Sessione 2026-10-14 sera - O7c diagnosi 4 segnali

Sessione: 14 ottobre 2026, sera (22:00-23:15 circa).
Scopo: O7c - indagare perche' 4 segnali su 5 davano sempre score 0.

### Scoperte

- **news**: `news_context.txt` ORFANO. Nessun processo attivo lo scrive.
  `news_agent.py` attuale scrive solo `/tmp/news_score.txt` (numero, sempre
  0.0). Fetch a Investing.com RSS funziona (HTTP 200, RSS valido), ma
  keyword-list italiane non trovate nei titoli. Segnale SOSPESO in
  `orchestrator.py` (forzato a 0.0). Cantiere O10.
- **social**: FIXATO. `social_agent.py` patchato con `sentiment_score()`
  (keyword list EN, positivo/negativo/neutro). `social_context.txt` ora
  contiene riga `Sentiment: negativo`. Orchestratore legge correttamente.
  Contributo: -0.2.
- **cycle**: FIXATO. `cycle_agent.py` patchato: `df.columns.get_level_values(0)`
  per appiattire MultiIndex yfinance. `cycles_context.txt` ora contiene 12
  righe `Mese N: media prezzo X.XXXXX`. Mese 10 = 1.08960 -> range neutro
  (1.08-1.10) -> score 0.0. Nessun impatto su final_score attuale.
- **volume**: regex orchestratore accetta ora `score` o `Punteggio`
  (case-insensitive). Valore reale 0.00 (volume ratio 1.00, corretto).
- **experience**: -0.2 (3 PERDITE recenti in `experiences.json`). Funziona.
- **final_score**: -0.08. Signal: HOLD.

### Contratto orchestratore <-> EA chiarito

- Formato comando: `buy|sell lots sl tp` oppure `close <ticket>`.
- `AI_BRIDGE_CMD.txt` consumato one-shot (EA cancella dopo lettura).
- `AI_BRIDGE_RES.txt` contiene esito (`OK: aperto ...` / `ERR: ...`).
- Orchestratore NON legge `AI_BRIDGE_RES.txt`. Logga `action_taken` senza
  verificare esito.
- Bug `orders.json`: record con doppio `status` (`open` + `closed`). Dedup
  v3.5 cerca `"status":"closed"` esatto e non scatta nel caso osservato.

### Backup creati (NON cancellare per 24h, D3)

- `orchestrator.py.pre_o7c` (pre-fix O7c)
- `orchestrator.py.pre_o7c_news_suspend` (pre-sospensione news)
- `social_agent.py.pre_s1` (coincide con file patchato - backup poco utile)
- `cycle_agent.py.pre_h` (pre-patch cycle)
- `CONTESTO.md.pre_o7c`, `HANDOFF.md.pre_o7c`

### Da fare prossima sessione

1. Test end-to-end orchestratore -> MT4 con comando manuale (buy/sell a
   prezzi plausibili). Verificare catena: AI_BRIDGE_CMD.txt -> EA ->
   AI_BRIDGE_RES.txt -> orders.json -> account.json -> dashboard.
2. Fix `orders.json` dedup (v3.5-bis).
3. Orchestratore legge `AI_BRIDGE_RES.txt` per tracciare esito reale.
4. Cantiere O10: riprogettare `news_agent.py` (file di testo vs numero).
5. Pulizia processi tmux zombie (es. wrapper 1263886).

### Decisioni nuove proposte

- **O10**: news redesign.
- **O11**: password broker fuori da `config.json` (file in chiaro,
  potenzialmente su GitHub).
