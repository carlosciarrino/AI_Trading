# CONTESTO PROGETTO AI_TRADING

Ultimo aggiornamento: 2026-10-22 16:50
Autore: Carlo + Chat (decisione congiunta)
Regola: questo file si aggiorna SOLO a mano, in chat, quando cambia una decisione.
Nessuno script automatico deve scriverci dentro.

## 1. Cos'e' il progetto

Sistema di trading automatico su MT4 (Wine su Linux) con:
- un EA MQL4 che esegue ordini e scrive file di stato,
- agenti Python (tmux) che analizzano mercato e generano segnali,
- una dashboard web che mostra stato conto, ordini aperti, PNL, controllo agenti.

Obiettivo: azienda digitale semplice, intuitiva, aggiornabile facilmente.
"Come l'acqua": si adatta, non si rompe, non ci fa perdere tempo.

## 2. Chi fa cosa

- Carlo: idee, obiettivi, decisioni finali, verifica in MT4.
- Chat: progetta, decide la strategia tecnica, prepara i comandi per Kilo,
  ricerca soluzioni online (in piu' lingue, non solo italiano).
- Kilo: esegue. Non interpreta. Non decide. Se ha dubbi, si ferma e chiede.

## 3. Architettura attuale (deciso, non si discute)

- Un solo EA per grafico MT4.
- L'EA di trading si chiama AI_BRIDGE_EA.mq4 e risiede in:
  /home/carlo/Scrivania/XM MT4/MQL4/Experts/AI_BRIDGE_EA.mq4
- La telemetria (account.json) sta DENTRO AI_BRIDGE_EA, non in un EA separato.
- account.json viene scritto in: /home/carlo/Scrivania/XM MT4/MQL4/Files/account.json
- Gli agenti Python girano in tmux sessioni separate (14 sessioni).
- La dashboard web gira come servizio systemd user "web-app" (porta 5000).
- Il server controllo remoto gira come servizio systemd user "controllo-remoto".
- Registro pendenze: docs/PENDENZE.md (vedi D18).
- Mappa progetto: docs/ORGANIGRAMMA.md + docs/MAPPA_PROGETTO.md (vedi D19).

## 3b. Segnali dell'orchestratore e pesi

| Segnale      | Fonte file                 | Peso  | Range score    |
|--------------|----------------------------|-------|----------------|
| news         | news_context.txt           | 0.20  | -0.3 / 0 / +0.3|
| social       | social_context.txt         | 0.20  | -0.2 / 0 / +0.2|
| cycle        | cycles_context.txt         | 0.15  | -0.2 / 0 / +0.2|
| volume       | volume_context.txt         | 0.25  | variabile (-0.3/0/+0.3)|
| experience   | trading_memory.md          | 0.20  | -0.2 / 0 / +0.2|
|--------------|----------------------------|-------|----------------|
| SOMMA PESI   |                            | 1.00  |                |

Segnale technical (technical_context.txt): calcolato ma **PESO 0** (solo log, per validazione futura).

Soglie decisionali:
- final_score > +0.10  ->  BUY
- final_score < -0.10  ->  SELL
- altrimenti           ->  HOLD

Punteggio attuale: variabile (0.04-0.17). HOLD o BUY/SELL.

Riferimento codice: /home/carlo/AI_Trading/orchestrator.py, funzione get_signal().

## 3c. Contratto orchestratore <-> EA

Formato comando accettato da AI_BRIDGE_EA.mq4 (funzione ExecuteCommand):
  buy  [lots] [sl_price] [tp_price]
  sell [lots] [sl_price] [tp_price]
  close <ticket>   (minuscolo, NON "CLOSE")

Ciclo file comando:
- orchestratore scrive "AI_BRIDGE_CMD.txt"
- EA legge, esegue, FileDelete(CMD_FILE) one-shot
- EA scrive esito in "AI_BRIDGE_RES.txt" (OK: aperto <ticket>... / ERR: ...)
- orchestratore LEGGE AI_BRIDGE_RES.txt e logga esito reale in decision_log.jsonl

Ciclo file SL modification (O8):
- orchestratore scrive "sl_commands.json" con array di comandi
- EA legge, applica OrderModify, cancella one-shot.

Ciclo file parametri EA (P049):
- EA scrive "ea_params.json" con MaxOrders, LotSize, StopLoss, TakeProfit.
- orchestratore legge MaxOrders da ea_params.json (modificabile da MT4).
- Fallback: max_orders.txt.

Ciclo file volume (P048):
- EA scrive "volume_data.json" (Tick Volume reale) ogni 5s.
- volume_agent legge, calcola divergenza prezzo-volume, scrive volume_context.txt.
- technical_agent legge per OBV.

Path:
- MT4_FILES = ~/Scrivania/XM MT4/MQL4/Files
- AI_BRIDGE_CMD.txt, AI_BRIDGE_RES.txt, orders.json, account.json,
  sl_commands.json, open_time.json, volume_data.json, ea_params.json, max_orders.txt

## 3d. Logica post-apertura O8

L'orchestratore esegue 4 controlli ad ogni ciclo (ogni 5 min, anche fuori orario):

1. **check_time_stop**: chiude ordini aperti da >24h.
2. **check_break_even**: se ordine in profitto >= 20 pip, sposta SL a
   entry +2 pip (BUY) / entry -2 pip (SELL). Scrive sl_commands.json.
3. **check_friday_profit (C1)**: venerdi 15:00 UTC, chiude ordini con PNL > 0.
4. **check_friday_close (C2)**: venerdi 20:00 UTC, chiude tutti gli ordini.

Parametri:
- BREAK_EVEN_PIP = 20
- BREAK_EVEN_OFFSET_PIP = 2
- FRIDAY_PROFIT_HOUR_UTC = 15
- FRIDAY_CLOSE_HOUR_UTC = 20
- MAIN_LOOP_SLEEP = 300 (5 min)

## 3e. Controllo remoto

- File: controllo_remoto/server.py
- Servizio systemd user: controllo-remoto (attivo, PID 1045)
- Funzione: da definire (P050).

## 4. Stato attuale

### Cosa funziona
- MT4 su Wine, terminal.exe attivo.
- Agenti tmux attivi (14 sessioni).
- Servizi systemd user attivi: web-app, controllo-remoto.
- GitHub carlosciarrino/AI_Trading: integro, sincronizzato con origin/main.
- AI_BRIDGE_EA.mq4 v3.5-volume: FUNZIONANTE in MT4.
  Scrive account.json, orders.json, volume_data.json, ea_params.json.
  Compila 0 errori, 0 warning.
- orchestrator.py: legge AI_BRIDGE_RES.txt, O8 attivo, MaxOrders da ea_params.json.
- news_agent.py v2 (O10): Investing.com RSS, sentiment, news_context.txt ogni 10 min.
- social_agent.py v2 (P041): sentiment + volume + intensita + storico.
- volume_agent.py v2 (P048): legge volume_data.json, divergenza prezzo-volume.
- technical_agent.py (P042): EMA, RSI, ADX, OBV (OBV da volume_data.json). Peso 0.
- reflection_agent.py (P031-bis): trading_memory.md, deterministico (no LLM).
- config.json: password broker rimossa (O11). Permessi 600.
- account.json: scritto ogni 5s. Conto demo 450000065, ~100074 EUR.
- docs/PENDENZE.md: registro pendenze (aggiornato).
- docs/ORGANIGRAMMA.md + docs/MAPPA_PROGETTO.md: mappe del progetto.
- docs/VIBE_TRADING_SKILLS.md: catalogo 90 skill.
- docs/CONFRONTO_ESTERNO.md: confronto TradingAgents + Quant-Agent.
- docs/RICERCA_COMMERCIALE.md: fonti commerciali (Palanca, Rizzo, MuseSpark).

### Cosa e' rotto o incompleto
- Vedi docs/PENDENZE.md per l'elenco completo e aggiornato delle pendenze.
- In sintesi: supervisor falso positivo (P001), agenti muti (P004), loop sell
  (P005), verifica O8/O7b-bis in produzione (P007/P008), 7 agenti dormienti
  archiviati (P024), 2 ordini aperti (test MaxOrders=1).

### Backup attivi (D3)
- AI_BRIDGE_EA.mq4.pre_volume, .pre_volume_master
- orchestrator.py.pre_*, volume_agent.py.pre_p048, technical_agent.py.pre_obv
- config.json.pre_o11, social_agent.py.pre_p041, reflection_agent.py.pre_*
- docs/archive/2026-10/ (32 cartelle + 56 .py + 40 file vari DEPRECATED)

## 5. Decisioni prese (non si ridiscutono)

D1. Un solo EA per grafico. Telemetria dentro l'EA di trading.
D2. La v3.3 e' il sorgente di riferimento. Ogni modifica parte da li' e
    aggiunge SOLO righe. Se una modifica rimuove righe, e' FAIL.
D3. Ogni modifica a un file di produzione richiede backup con md5sum
    prima/dopo. Il backup non si cancella finche' la modifica non e'
    confermata su demo per almeno 24h.
D4. Kilo non decide mai. Esegue, e se ha dubbi si ferma.
D5. I comandi a Kilo hanno intestazione fissa (5 righe).
D6. La chat non incolla codice in mezzo al testo: comandi in blocchi separati.
D7. La chat dichiara, prima di ogni comando a Kilo, cosa contiene il file
    target e cosa cambia. Carlo autorizza solo dopo aver letto.
D8. La ricerca online va fatta in almeno 3 lingue e 4 fonti minime.
D9. Il ripristino di AI_BRIDGE_EA.mq4 v3.3 e la patch a v3.4 sono fatti
    DIRETTAMENTE dalla chat, non da Kilo.
D10. Solo Carlo e la Chat decidono modifiche a backup PC e a GitHub.
D11. La dashboard legge da account.json la telemetria conto.
D12. IN PRODUZIONE l'orchestratore opera SOLO durante i mercati Londra e NY.
D13. Ogni decisione dell'orchestratore va loggata in decision_log.jsonl.
D14. MetaEditor va CHIUSO prima di modificare AI_BRIDGE_EA.mq4 da terminale.
D15. Quando Carlo deve modificare un file, la chat fornisce in un UNICO
    messaggio: comando di apertura + contenuto completo da incollare.
D16. Per modificare un file a mano, Carlo preferisce SEMPRE il file
    completo (sostituzione totale), mai istruzioni puntuali.
D17. Nelle regole di calcolo delle operazioni sono SEMPRE inclusi take
    profit, stop loss, commissioni e spread.
D18. Ogni questione in sospeso emersa durante una sessione va registrata
    IMMEDIATAMENTE in docs/PENDENZE.md.
D19. Ogni chat nuova DEVE leggere prima: docs/ORGANIGRAMMA.md +
    docs/MAPPA_PROGETTO.md + CONTESTO.md + HANDOFF.md + docs/PENDENZE.md.
D20. La chat NON PRESUME di conoscere il contenuto del progetto. Non ha
    accesso autonomo al filesystem. Chiede il censimento o lo esegue.
D21. Una soluzione non e' "ok" finche' non e' attiva, verificata e produce
     output. Non basta che il file esista. Va aggiunta a start_all.sh,
     avviata in tmux, schedulata in cron (se periodica), e testata con un
     ciclo manuale. Solo allora si dice "fatto". Regola nata dall'incidente
     2026-10-24 (agenti di ricerca creati ma mai attivati).
## 6. Ricerca agenti (una tantum, periodica)

Cercare su GitHub, forum, repo specializzati chi ha costruito agenti di
comunicazione tra agenti. Non fermarsi ai primi risultati. Verificare
codice, stelle, manutenzione, licenza. Obiettivo: prendere il meglio.

Progetti identificati (docs/CONFRONTO_ESTERNO.md):
- TradingAgents (Tauric Research): multi-agente con dibattito.
- Quant-Agent-Trader: self-evolution con diario trading.
- Vibe-Trading (HKUDS): 90 skill, shadow account, swarm (docs/VIBE_TRADING_SKILLS.md).

## 7. Prossimo passo (uno solo)

P044: risk manager separato con size dinamica (da Quant-Agent/Vibe-Trading).
Oppure P033: dibattito bull/bear borderline (da TradingAgents).

## 8. Come si aggiorna questo file

Solo in chat, solo a mano, solo quando Carlo dice "aggiorna CONTESTO.md".

## 9. Prossimi obiettivi in coda (non attivi, solo promemoria)

- O4: fix auto-sync Git. FATTO 2026-10-14.
- O5: pulizia file storici. FATTO 2026-10-14.
- O6: ricerca agenti. IN CORSO.
- O7: verificare flusso decisione trading. IN CORSO.
- O7a: decision_log.jsonl. FATTO 2026-10-14.
- O7b: fix orchestrator.py. FATTO 2026-10-14.
- O7b-bis: orchestratore legge AI_BRIDGE_RES.txt. FATTO 2026-10-15.
- O7c: diagnosi 4 segnali. CHIUSO 2026-10-14.
- O8: logica post-apertura. FATTO 2026-10-15. Verifica in corso.
- O9: orario London+NY in config.json. Da fare in produzione.
- O10: news redesign. FATTO 2026-10-15.
- O11: password broker fuori da config.json. FATTO 2026-10-15.
- O12: bonifica progetto. FATTO 2026-10-16.
- O13: organigramma + mappa progetto. FATTO 2026-10-16.
- P041: social_agent v2. FATTO 2026-10-19.
- P042: technical_agent. FATTO 2026-10-22.
- P048: volume_agent v2. FATTO 2026-10-19.
- P049: MaxOrders da MT4. FATTO 2026-10-22.
- Pendenze: vedi docs/PENDENZE.md.
