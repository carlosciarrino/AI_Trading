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

### [P001] Supervisor falso positivo su news_agent (e altri) [CHIUSA 2026-10-24]
- Data: 2026-10-15
- Priorita': media
- Contesto: supervisor_agent.py controllava solo esistenza sessione tmux.
- Azione: RISOLTA. supervisor_agent.py v3-bis (md5 a074dba2...): check con
  `ps -eo comm,args` filtrando comm in (python3, python) e script in args.
  Esclude il wrapper bash. Testato: tutti i 14 agenti -> active, has_issue
  False, zero duplicate session. Backup: supervisor_agent.py.pre_p001_v2.

### [P002] experiences.json cresce senza rotazione
- Data: 2026-10-15
- Priorita': media
- Contesto: 84 record storici. Il segnale experience legge gli ultimi 3,
  ma il file cresce all'infinito. Rallenta la lettura, sporca il repo se
  non ignorato.
- Azione: tenere ultimi 20-30 record, archiviare i vecchi in
  docs/archive/experiences_YYYYMM.json.

### [P003] Wrapper zombie tmux PID 1263886 [CHIUSA 2026-10-24]
- Data: 2026-10-15
- Priorita': bassa
- Contesto: si sospettava uno zombie tmux.
- Azione: SMENTITO. Verifica 2026-10-24: tutti i processi agenti sono
  `Ss+`/`Sl+` (sleeping in foreground, normale per tmux detached). Nessuno
  zombie. PID 1263886 e' il server tmux del 14/10, vivo e funzionante.

### [P004] 8 agenti su 11 con log vuoti [CHIUSA 2026-10-24]
- Data: 2026-10-15
- Priorita': media
- Contesto: si sospettavano agenti muti.
- Azione: RISOLTA parzialmente. Verifica 2026-10-24: solo cycle_agent era
  rotto (sessione tmux con bash invece di python3). Riavviato 20:04 con
  python3; cycles_context.txt aggiornato 20:05. Gli altri agenti scrivono
  i context file (news, social, volume, technical freschi). Log vuoti
  perche' Python bufferizza stdout: vedi P067. Monitoraggio 24h: se
  cycles_context.txt resta fermo al 24/10, yfinance fallisce.

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

### [P007] Verifica O8 con ordine reale [CHIUSA 2026-10-24, verifica finale lunedì]
- Data: 2026-10-15
- Priorita': alta
- Contesto: O8 (break-even, C1 venerdi profitto, C2 venerdi chiusura) e'
  stato scritto e testato solo staticamente (py_compile). Mai eseguito con
  ordine vero.
- Azione: al primo BUY/SELL reale, monitorare:
  - check_break_even scrive sl_commands.json quando profitto >= 20 pip;
  - EA applica nuovo SL (log MT4);
  - C1 e C2 funzionano al primo venerdi (2026-10-16 e successivi).
- Nota 2026-10-24: orchestrator.py patchato (md5 d4ea2900..., 586 righe). Aggiunti [BRIDGE] raw/status su stdout, write_decision in send_close_command (ok/err/timeout). Backup: orchestrator.py.pre_p007 (md5 33dd1ac8...). Verifica finale: lunedì con ordine reale, guardare [O8]/[BE]/[BRIDGE] in ai_workforce.log e action_taken:close in decision_log.jsonl.

### [P008] Verifica O7b-bis con ordine reale [CHIUSA 2026-10-24, verifica finale lunedì]
- Data: 2026-10-15
- Priorita': alta
- Contesto: O7b-bis (orchestratore legge AI_BRIDGE_RES.txt) testato solo
  con unit test (mock file). Mai testato con ordine reale post-patch.
- Azione: al primo BUY/SELL reale, verificare decision_log.jsonl registra
  ticket reale (non null) se EA risponde OK.
- Nota 2026-10-24: O7b-bis gia' funzionante (campo error in decision_log.jsonl). read_bridge_result ora logga [BRIDGE] raw su stdout. Verifica finale: lunedì con ordine reale, guardare campo error in decision_log.jsonl.

### [P009] .gitignore esclude *.json (anche config utili)
- Data: 2026-10-15
- Priorita': bassa
- Contesto: pattern *.json in .gitignore esclude config.json, ma anche
  configs/system_config.json (se non gia' committato prima) e altri file
  di config utili. Da valutare eccezioni.
- Azione: aggiungere !configs/*.json o simile, se serve.

### [P010] social_agent.log fermo [DA RICONTROLLARE 2026-10-24]
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

### [P021] Doppio mt4_shared: uno in progetto (inutile), uno in home (usato)
- Data: 2026-10-16
- Priorita': media
- Contesto: esistevano due mt4_shared.
  - /home/carlo/AI_Trading/mt4_shared/ → file vecchi di maggio, nessuno lo
    usava. Spostato in docs/archive/2026-10/mt4_shared_DEPRECATED.
  - /home/carlo/mt4_shared/ → symlink orders.json a Scrivania, usato da
    experience_agent, kronos_agent, nzt_agent, tools/stato_sistema.py.
- Azione: aggiornare agenti per usare direttamente Scrivania/XM MT4/MQL4/Files/
  invece del symlink. Rimuovere symlink dopo migrazione.

### [P022] agents_night_shift.sh non in cron [CHIUSA 2026-10-24, obsoleto]
- Data: 2026-10-16
- Priorita': bassa
- Contesto: agents_night_shift.sh avvia 5 agenti di ricerca notturni
  (github_researcher, skill_researcher, strategy_tester_agent, news_critical,
  ai_researcher_agent) + audit_agent. Ma non è in crontab. Gli agenti che
  avvia sono ora in archive/2026-10/py_files_DEPRECATED/.
- Azione: decidere se riattivare. Se sì, aggiornare percorso script
  (da archive/) e aggiungere a crontab (2:00).

- Nota 2026-10-24: script referenziava 6 .py inesistenti (github_researcher, skill_researcher, strategy_tester_agent, news_critical, ai_researcher_agent, audit_agent). Tutti MISS. Script archiviato in docs/archive/2026-10/agents_night_shift.sh.OBSOLETO. Nessun cron aggiunto: scouting_agent.py gia' in cron 6:00 e funzionante.
### [P023] docs/STATO_SISTEMA.md auto-generato: ora sappiamo da chi
- Data: 2026-10-16
- Priorita': bassa
- Contesto: RISOLTO il mistero P006. Il file è generato da
  tools/stato_sistema.py. Ma quel file è ora in
  docs/archive/2026-10/tools_DEPRECATED/. Quindi STATO_SISTEMA.md non si
  aggiornerà più. Verificare se serve.
- Azione: se utile, ripristinare tools/stato_sistema.py in root e
  aggiungere a crontab. Altrimenti dismettere STATO_SISTEMA.md.

### [P024] 7 agenti dormienti archiviati (decisione rimandata)
- Data: 2026-10-16
- Priorita': media
- Contesto: ai_researcher_agent, ai_tester_agent, audit_agent,
  indicator_tester_agent, strategy_tester_agent, tool_updater_agent,
  youtube_agent sono ora in docs/archive/2026-10/py_files_DEPRECATED/.
  Utili potenzialmente per O6 (ricerca agenti) e progetto Media.
- Azione: decidere caso per caso se riattivare. Probabile:
  - ai_researcher_agent + ai_tester_agent → utili per O6.
  - indicator_tester_agent → utile per validare segnali.
  - audit_agent → utile ma duplica supervisor.
  - youtube_agent, tool_updater_agent → progetto Media.
  - strategy_tester_agent → progetto Media.

### [P031] Memoria con riflessione (da TradingAgents)
- Data: 2026-10-16
- Priorita': ALTA
- Contesto: TradingAgents ha reflection.py che genera 2-4 frasi di lezione
  specifica per ogni decisione chiusa, reiniettate nei prompt futuri.
  Il nostro experiences.json ha lezione sempre identica. Il segnale experience
  legge solo PNL, non lezioni.
- Azione: aggiungere riflessione a experience_agent.py (o nuovo reflection_agent.py).
  Usa Ollama per generare lezioni. Reinietta in orchestrator (get_signal).
- Complessita': media. ~100 righe.

### [P032] Rotazione experiences.json (chiude P002)
- Data: 2026-10-16
- Priorita': ALTA
- Contesto: experiences.json ha 84 record, nessuna rotazione, cresce all'infinito.
- Azione: tenere ultimi 30, archiviare in docs/archive/experiences/YYYY-MM.json.
- Complessita': bassa. ~20 righe.

### [P033] Dibattito bull/bear borderline (da TradingAgents)
- Data: 2026-10-16
- Priorita': ALTA
- Contesto: TradingAgents fa dibattere bull vs bear prima di decidere. Noi
  decidiamo con 1 orchestratore lineare, nessun contraddittorio.
- Azione: quando final_score e' tra 0.08 e 0.12 (zona grigia), lancia 2 prompt
  (bull, bear) via Ollama, arbitro decide. Solo in zona grigia, per costi.
- Complessita': media-alta. Prompt ben scritti.

### [P034] Risk manager separato con size dinamica (da Quant-Agent)
- Data: 2026-10-16
- Priorita': ALTA
- Contesto: Quant-Agent ha risk budget dinamico (volatilita', drawdown,
  sentiment). TradingAgents ha 3 risk analyst che dibattono. Noi abbiamo solo
  break-even e time-stop.
- Azione: agente che calcola size in base a ATR + drawdown corrente. Regola
  LEVERAGE_MAX e size massima. Non bypassabile.
- Complessita': alta.

### [P035] Hypothesis library (da Quant-Agent)
- Data: 2026-10-16
- Priorita': MEDIA
- Contesto: Quant-Agent ha configs/hypotheses/*.json con win rate, sample size,
  stato proposed/verified/deprecated. Ogni ipotesi e' validata con event study.
- Azione: creare configs/hypotheses/ con prime 3-5 ipotesi (es. "news negativo
  + social negativo -> SELL"). Validatore notturno con backtest.
- Complessita': alta.

### [P036] Multi-vendor dati (da TradingAgents)
- Data: 2026-10-16
- Priorita': MEDIA
- Contesto: TradingAgents ha Yahoo + FRED + Alpha Vantage + Polymarket + Reddit.
  Noi abbiamo solo Investing.com RSS + Google News RSS + yfinance.
- Azione: aggiungere FRED (macro), Alpha Vantage (fallback), Reddit (sentiment).
- Complessita': media.

### [P037] Settlement point-in-time (da TradingAgents)
- Data: 2026-10-16
- Priorita': MEDIA
- Contesto: TradingAgents misura alpha vs benchmark (SPY) dopo N giorni, con
  point-in-time corretto. Noi no.
- Azione: dopo N giorni, misura PNL reale e alpha vs DXY (benchmark EURUSD).
- Complessita': media.

### [P038] Multi-provider LLM (da TradingAgents)
- Data: 2026-10-16
- Priorita': BASSA
- Contesto: TradingAgents usa GPT/Gemini/Claude/Grok/Ollama. Noi solo Ollama
  qwen2.5:0.5b (modello piccolissimo).
- Azione: valutare se usare modelli piu' grandi (anche solo Ollama con qwen3 o
  llama3). Rischio costi se API a pagamento.
- Complessita': media.

### [P039] MCP services (da Quant-Agent)
- Data: 2026-10-16
- Priorita': BASSA
- Contesto: Quant-Agent ha 5 MCP server per math/search/trade/price/memory.
  Overkill per il nostro sistema attuale.
- Azione: rimandare. Valutare solo se cresciamo molto.
- Complessita': alta.

### [P040] Arena web / dashboard React (da Quant-Agent)
- Data: 2026-10-16
- Priorita': BASSA
- Contesto: Quant-Agent ha dashboard React (leaderboard, live).
- Azione: la nostra Flask funziona. Non serve. Rimandare.
- Complessita': alta.
---

### [P067] cycle_agent.py non flusha stdout
- Data: 2026-10-24
- Priorita': bassa
- Contesto: cycle_agent.log resta 0 byte anche quando cycles_context.txt
  viene aggiornato. Python bufferizza stdout quando non e' tty.
- Azione: aggiungere flush=True ai print di cycle_agent.py.

### [P068] supervisor matcha python3 -c "script.py"
- Data: 2026-10-24
- Priorita': bassa
- Contesto: agent_alive() matcha qualunque python3 con <script>.py negli
  args, incluso `python3 -c "...script.py..."`. Non accade in produzione,
  ma e' un falso positivo potenziale.
- Azione: aggiungere `and " -c " not in args` alla condizione.

### [P069] restart_log.json 4 record falsi
- Data: 2026-10-24
- Priorita': bassa
- Contesto: il supervisor v3 (pgrep, poi scartato) ha scritto 4 record
  "restart" alle 20:08 per agenti mai riavviati (duplicate session).
  Backup: restart_log.json.pre_p001_falsi.
- Azione: verificare che la pulizia (record < 2026-10-24T20:08) sia
  andata a buon fine.

### [P070] open_time.json non pulito dei ticket chiusi
- Data: 2026-10-24
- Priorita': bassa
- Contesto: open_time.json contiene 9 ticket tutti chiusi. check_time_stop
  fa del solo quando chiude per >24h. Se l'ordine chiude per TP/SL/C1/C2,
  il ticket resta per sempre. Accumulo infinito.
- Azione: in check_time_stop (o check separato), rimuovere i ticket non
  piu' presenti in orders.json come open.

### [P071] check_break_even puo' riscrivere SL
- Data: 2026-10-24
- Priorita': bassa
- Contesto: se orders.json non e' aggiornato dall'EA (ogni 5s) e il ciclo
  orchestratore (5 min) legge il vecchio SL, riscrive sl_commands.json.
  Al massimo 1 riscrittura extra, non loop.
- Azione: tracciare ultimo SL inviato per ticket, non riscrivere se
  identico.

## Chiuse

### [P016] tools/ e' archivio fossile
- Data apertura: 2026-10-16
- [CHIUSA 2026-10-16] 75 file spostati in docs/archive/2026-10/tools_DEPRECATED/.

### [P018] .engram/index.md obsoleto
- Data apertura: 2026-10-16
- [CHIUSA 2026-10-16] .engram/ spostato in docs/archive/2026-10/engram_DEPRECATED/.

### [P019] tests/ non aggiornati
- Data apertura: 2026-10-16
- [CHIUSA 2026-10-16] spostati in docs/archive/2026-10/tests_DEPRECATED/.

### [P020] tools/position_manager.py duplica O8
- Data apertura: 2026-10-16
- [CHIUSA 2026-10-16] in docs/archive/2026-10/tools_DEPRECATED/.

### [P049] MaxOrders da MT4 a orchestratore
- Data: 2026-10-22
- Priorita': ALTA
- Contesto: orchestratore aveva MAX_OPEN_ORDERS hardcoded. Non modificabile
  senza toccare codice.
- Azione: RISOLTA 2026-10-22. EA scrive ea_params.json con MaxOrders.
  Orchestratore legge da lì. Modifica da MT4, nessun codice.

### [P050] controllo_remoto: funzione da definire
- Data: 2026-10-22
- Priorita': media
- Contesto: servizio controllo-remoto attivo (PID 1045, 3 giorni) ma non
  documentato in CONTESTO.md. Cosa fa? Come si usa?
- Azione: leggere controllo_remoto/server.py e documentare.

### [P051] 2 ordini aperti (test MaxOrders)
- Data: 2026-10-22
- Priorita': alta
- Contesto: 420485 (BUY) e 433116 (BUY) aperti. MaxOrders=1. Orchestratore
  blocca nuove aperture. Rischio doppio.
- Azione: monitorare break-even e time-stop. Decidere se chiudere 433116.

### [P052] Video Instagram da analizzare
- Data: 2026-10-22
- Priorita': bassa
- Contesto: Carlo ha incollato 10 link di reel Instagram (Palanca, Rizzo,
  ai_swarm_solutions, gabriaprile, coco.satoru, rianmedeiros, Dori).
  Non posso aprirli direttamente. Serve testo o sintesi.
- Azione: quando Carlo incolla i testi, analizzare per trading/commerciale.
(nessuna per ora)

### [P053] P033: dibattito borderline (rinviato)
- Data: 2026-10-22
- Priorita': bassa
- Contesto: implementato e poi rimosso (produceva rumore, non segnale).
  L'idea (dibattito bull/bear quando score e' borderline) resta valida.
  Ma richiede LLM veloce (Ollama lento su i3) o euristiche migliori.
- Azione: rivalutare quando hardware migliore (Gemma 4 12B) o quando
  avremo piu' dati per calibrare le soglie.

### [P059] Studio Harness2 (google-research/harness2)
- Data: 2026-10-24
- Priorita': media (futuro)
- Contesto: framework che auto-migliora l'harness di un agente (Propose-Probe-Compose).
  Trovato da scouting_agent. Non per trading immediato, ma concetto utile
  per migliorare il sistema nel tempo.
- Azione: leggere paper/codice quando avremo piu' dati e stabilita'.

### [P060] Studio replica-skill (Jakeschincariol/replica-skill)
- Data: 2026-10-24
- Priorita': bassa (commerciale)
- Contesto: skill per clonare app (reverse-engineer, rebuild, bug-fix).
  Trovata da scouting_agent. Utile solo per il progetto commerciale (se
  dovremo replicare UI/funzionalita' di app esistenti).
- Azione: valutare quando parte il progetto commerciale.

### [P061] Test Decima-small (decision model)
- Data: 2026-10-24
- Priorita': alta
- Contesto: decision model open source (122M parametri, CPU, ~20 ms).
  Potrebbe sostituire le regole fisse (trend, risk) con decisioni probabilistiche.
- Azione: scaricare Decima-small, testarlo su "trend bull/bear", valutare
  integrazione in orchestrator.py.

### [P062] Studio TimesFM (Mistral) - previsione serie storiche
- Data: 2026-10-24
- Priorita': bassa
- Contesto: modello decoder-only per zero-shot forecasting. Utile per
  previsioni di volume/volatilità, non per direzione prezzo. Richiede dati
  puliti e test statistici. Non integrare ora.
- Azione: rivalutare solo se in futuro vorremo prevedere volume/volatilità.

### [P063] Gettrade.ai - NON USARE (sospetto)
- Data: 2026-10-24
- Priorita': nessuna (da evitare)
- Contesto: servizio che analizza screenshot di grafici e dà "segnali".
  Recensioni indipendenti lo definiscono inaffidabile: sviluppatori anonimi,
  paywall, follower social comprati. Probabile wrapper di modello generico.
- Azione: NON integrare. Il nostro sistema è trasparente e tracciato.

### [P064] Test Limite 1B Violetto (Paradigma)
- Data: 2026-10-24
- Priorita': media
- Contesto: modello 1B open source (Apache 2.0), specializzato in matematica,
  senza "personalità da assistente". Gira su CPU. Potrebbe essere usato come
  calcolatore per position sizing/risk o validazione logica.
- Azione: testare quando avremo tempo. Non è un modello di trading.

### [P065] Decima-small testato - SCARTATO
- Data: 2026-10-24
- Priorita': nessuna (scartato)
- Contesto: testato Decima-small (122M, decision model). Classifica
  "Fed raises rates" come "aziendale" (84.8% confidenza) invece di "macro".
  Sbaglia con sicurezza. Inutile per notizie finanziarie.
- Azione: scartato. Il filtro trend deterministico (P055) e' meglio.
  venv_decima (144 MB) puo' essere cancellato.
