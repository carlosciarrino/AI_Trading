# PENDENZE - Questioni in sospeso

Registro delle questioni non critiche emerse durante le sessioni e rinviate.
Aggiornato in chat, a mano, subito quando emerge una pendenza (D18).

Formato voce:
- ID univoco [P###]
- Data di apertura
- Priorita': alta / media / bassa
- Contesto: cosa e' emerso, perche' non e' critico ora
- Azione proposta: cosa fare quando si affronta

Quando una pendenza e' chiusa, si marca [CHIUSA 2026-XX-XX] e si sposta in
fondo, in sezione "Chiuse".

---

## Aperte

### [P001] Supervisor falso positivo su news_agent (e altri)
- Data: 2026-10-15
- Priorita': media
- Contesto: supervisor_agent.py controlla solo esistenza sessione tmux per
  nome. Se una sessione e' chiusa ma il supervisor la vede in audit_status,
  dice "active" -> falso positivo. Osservato con news_agent il 2026-10-15.
- Azione: far controllare anche il processo figlio (ps --ppid <pane_pid>).

### [P002] experiences.json cresce senza rotazione
- Data: 2026-10-15
- Priorita': media
- Contesto: 84 record storici. Il segnale experience legge gli ultimi 3,
  ma il file cresce all'infinito. Rallenta la lettura, sporca il repo se
  non ignorato.
- Azione: tenere ultimi 20-30 record, archiviare i vecchi in
  docs/archive/experiences_YYYYMM.json.

### [P003] Wrapper zombie tmux PID 1263886
- Data: 2026-10-15
- Priorita': bassa
- Contesto: `tmux new-session -d -s ai_workforce ...` dal 14/10, rimasto
  appeso dopo l'avvio iniziale. Non fa danno, sporca pgrep.
- Azione: kill dopo aver verificato che l'orchestratore attuale e' il
  processo figlio, non il wrapper.

### [P004] 8 agenti su 11 con log vuoti
- Data: 2026-10-15
- Priorita': media
- Contesto: social_agent, news_agent, cycle_agent, market_anomaly,
  kronos_agent, nzt_agent, signal_observer, strategy_validator hanno log
  da 0 byte. Non significa morti (processi vivi) ma non scrivono nulla.
  Solo cycle_agent e experience_agent scrivono log.
- Azione: verificare per ciascuno se scrive su file di contesto (allora
  il log vuoto e' ok) o se e' muto (allora inutile).

### [P005] Loop sell non diagnosticato
- Data: 2026-10-14
- Priorita': bassa
- Contesto: in passato si sono verificati ordini sell ricorrenti (decine
  di sell consecutivi, vedi experiences.json). Causa sconosciuta.
- Azione: analizzare storico decision_log.jsonl per pattern sell anomali.

### [P006] docs/STATO_SISTEMA.md auto-generato: chi lo scrive?
- Data: 2026-10-15
- Priorita': bassa
- Contesto: file aggiornato ogni ora, allineato con cron auto-sync Git.
  Contiene TMUX, servizi, processi, Git log. Utile. Ma nessuno script
  nei *.py o *.sh lo menziona. Forse cron esterno, systemd timer, o
  altro path.
- Azione: cercare in /etc/cron.d/, crontab -l, systemd --user list-timers,
  ~/.config/systemd/user/. Documentare in CONTESTO.md sez. 3.

### [P007] Verifica O8 con ordine reale
- Data: 2026-10-15
- Priorita': alta
- Contesto: O8 (break-even, C1 venerdi profitto, C2 venerdi chiusura) e'
  stato scritto e testato solo staticamente (py_compile). Mai eseguito con
  ordine vero.
- Azione: al primo BUY/SELL reale, monitorare:
  - check_break_even scrive sl_commands.json quando profitto >= 20 pip;
  - EA applica nuovo SL (log MT4);
  - C1 e C2 funzionano al primo venerdi (2026-10-16 e successivi).

### [P008] Verifica O7b-bis con ordine reale
- Data: 2026-10-15
- Priorita': alta
- Contesto: O7b-bis (orchestratore legge AI_BRIDGE_RES.txt) testato solo
  con unit test (mock file). Mai testato con ordine reale post-patch.
- Azione: al primo BUY/SELL reale, verificare decision_log.jsonl registra
  ticket reale (non null) se EA risponde OK.

### [P009] .gitignore esclude *.json (anche config utili)
- Data: 2026-10-15
- Priorita': bassa
- Contesto: pattern *.json in .gitignore esclude config.json, ma anche
  configs/system_config.json (se non gia' committato prima) e altri file
  di config utili. Da valutare eccezioni.
- Azione: aggiungere !configs/*.json o simile, se serve.

### [P010] social_agent.log fermo
- Data: 2026-10-15
- Priorita': bassa
- Contesto: social_agent.log 290 byte, ultimo aggiornamento 14/10 22:42.
  social_context.txt si aggiorna (23:03 ieri), quindi l'agente e' vivo.
  Forse log non piu' scritto.
- Azione: verificare se e' un residuo o se log e' disabilitato.

### [P011] Agenti esterni (youtube_agent, chatgpt-agent) in MT4 Navigator
- Data: 2026-10-15
- Priorita': bassa
- Contesto: nel Navigator MT4 compaiono EA non nostri: AccountWriter,
  Aurus_*, youtube_agent. Non attivi sui grafici. Ma youtube_agent.py
  esiste in AI_Trading (legge config.json). Da chiarire se in uso.
- Azione: verificare se youtube_agent.py e' attivo, chi lo lancia,
  se serve.

### [P012] Bug CLOSE maiuscolo vs close minuscolo
- Data: 2026-10-16
- Priorita': alta
- Contesto: orchestrator.py scriveva `CLOSE <ticket>` (maiuscolo). EA accetta
  solo `close` (minuscolo). Risultato: `ERR: comando sconosciuto`, C2 e
  check_time_stop non potevano chiudere ordini.
- Azione: RISOLTA 2026-10-16. `f.write(f"CLOSE {ticket}\n")` ->
  `f.write(f"close {ticket}\n")`. md5 orchestrator.py = 8dd00dab8ab706d8ff50b5e83b47369b.

### [P013] Nessun blocco apertura venerdi sera
- Data: 2026-10-16
- Priorita': alta
- Contesto: l'orchestratore ha aperto SELL 319798 alle 20:09 UTC di venerdi.
  C1 (15:00) era gia' passato, C2 (20:00) e' scattato dopo. Ordine rimasto
  aperto nel weekend per il bug P012 + mercato chiuso (ERR 132).
- Azione: RISOLTA 2026-10-16. Aggiunto blocco in main: se venerdi e
  hour >= 19 UTC, non aprire nuovi ordini.

### [P014] check_friday_close ritenta ogni 5 min se fallisce
- Data: 2026-10-16
- Priorita': bassa
- Contesto: se close fallisce (es. mercato chiuso ERR 132), C2 ritenta ogni
  5 min fino a fine ora. Rumoroso nei log. Inutile.
- Azione: aggiungere flag o throttle: dopo un fallimento nella stessa ora,
  non ritentare.

### [P015] Ordine 319798 aperto nel weekend
- Data: 2026-10-16
- Priorita': alta
- Contesto: SELL 319798 aperto 20:09 UTC 16/10 (1.12358, SL 1.12688,
  TP 1.11931). Chiusura fallita (P012 + mercato chiuso). PNL -0.39.
  Passa il weekend aperto. Rischio gap domenica sera.
- Azione: domenica sera/lunedi mattina: verificare stato. Se ancora aperto
  e in perdita, valutare chiusura manuale. Se ha colpito SL/TP, chiuso.

### [P016] tools/ e' archivio fossile (75+ file, vecchio mondo)
- Data: 2026-10-16
- Priorita': media
- Contesto: tools/ contiene position_manager, verifier, watchdog,
  reconciliation, telegram_bot, workforce_*, agent_*, strategy_*.
  Quasi tutti ago/set 2026. Nessuno gira in tmux. E' il vecchio sistema,
  sostituito da orchestrator.py + *_agent.py + supervisor_agent.py.
- Azione: archiviare in docs/archive/tools_2026-10/ (mv, non rm). Alcuni
  script (telegram_bot, auto_researcher) potrebbero tornare utili.

### [P017] mt4_shared/ residuo storico
- Data: 2026-10-16
- Priorita': bassa
- Contesto: mt4_shared/ contiene symlink orders.json -> Scrivania, piu'
  open_time.json (2002 byte, ott 14) e sl_commands.json (109 byte, ott 6).
  L'orchestratore attuale usa direttamente ~/Scrivania/XM MT4/MQL4/Files/.
- Azione: verificare se qualcuno legge ancora da mt4_shared/. Se no,
  rimuovere symlink e file.

### [P018] .engram/index.md obsoleto (2026-10-07)
- Data: 2026-10-16
- Priorita': media
- Contesto: .engram/index.md descrive il vecchio mondo (position_manager,
  verifier, watchdog, MAX_OPEN_ORDERS=3, EA v3.3). Ora e' CONTESTO.md +
  HANDOFF.md + PENDENZE.md a fare quel lavoro.
- Azione: dismettere .engram/ o aggiornare index.md con rimando a
  CONTESTO.md. Verificare se .engram/experience/ e .engram/session/
  contengono dati utili.

### [P019] tests/ non aggiornati e non eseguiti
- Data: 2026-10-16
- Priorita': media
- Contesto: tests/ ha 3 file (test_dashboard, test_orchestrator,
  test_position_manager), ultimo aggiornamento 2026-10-06. Nessun verifier
  attivo. Non girano.
- Azione: valutare se riattivare test automatici (verifier) o dismettere.
  I test sono utili per non rompere il codice.

### [P020] tools/position_manager.py duplica O8
- Data: 2026-10-16
- Priorita': media
- Contesto: tools/position_manager.py (3823 byte, ott 6) fa break-even e
  trailing stop, esattamente come O8 in orchestrator.py. Ma non gira.
  Rischio: se riattivato, conflitto con O8.
- Azione: verificare contenuto. Archiviare con P016.

---

## Chiuse

(nessuna per ora)
