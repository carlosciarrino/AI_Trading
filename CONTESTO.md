# CONTESTO PROGETTO AI_TRADING

Ultimo aggiornamento: 2026-10-15 21:20
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
  Motivo: MT4 accetta un solo EA per grafico. Due EA = confusione.
- account.json viene scritto in:
  /home/carlo/Scrivania/XM MT4/MQL4/Files/account.json
- AccountWriter.mq4 resta in cartella ma NON viene caricato su nessun grafico.
- Gli agenti Python girano in tmux sessione "ai_workforce".
- La dashboard web gira come servizio systemd user "web-app".
- Registro pendenze: docs/PENDENZE.md (vedi D18).

## 3b. Segnali dell'orchestratore e pesi

L'orchestratore legge 5 file di contesto, assegna uno score a ciascuno,
moltiplica per un peso, somma e divide per la somma dei pesi.

| Segnale      | Fonte file                 | Peso  | Range score    |
|--------------|----------------------------|-------|----------------|
| news         | news_context.txt           | 0.20  | -0.3 / 0 / +0.3|
| social       | social_context.txt         | 0.20  | -0.2 / 0 / +0.2|
| cycle        | cycles_context.txt         | 0.15  | -0.2 / 0 / +0.2|
| volume       | volume_context.txt         | 0.25  | variabile      |
| experience   | experiences.json           | 0.20  | -0.2 / 0 / +0.2|
|--------------|----------------------------|-------|----------------|
| SOMMA PESI   |                            | 1.00  |                |

Soglie decisionali:
- final_score > +0.10  ->  BUY
- final_score < -0.10  ->  SELL
- altrimenti           ->  HOLD

TUTTI I 5 SEGNALI SONO ATTIVI (post O10, 2026-10-15).

Punteggio attuale: -0.02 (news +0.06, social -0.04, experience -0.04,
cycle e volume 0). Risultato: HOLD.

Riferimento codice: /home/carlo/AI_Trading/orchestrator.py, funzione
get_signal().

## 3c. Contratto orchestratore <-> EA (confermato 2026-10-14, esteso 2026-10-15)

Formato comando accettato da AI_BRIDGE_EA.mq4 (funzione ExecuteCommand):
  buy  [lots] [sl_price] [tp_price]
  sell [lots] [sl_price] [tp_price]
  close <ticket>

Ciclo file comando:
- orchestratore scrive "AI_BRIDGE_CMD.txt"
- EA legge, esegue, FileDelete(CMD_FILE) one-shot
- EA scrive esito in "AI_BRIDGE_RES.txt" (OK: aperto <ticket>... / ERR: ...)
- orchestratore LEGGE AI_BRIDGE_RES.txt (fix O7b-bis, 2026-10-15) e logga
  esito reale in decision_log.jsonl (ticket reale o errore o timeout)

Ciclo file SL modification (O8, 2026-10-15):
- orchestratore scrive "sl_commands.json" con array di comandi:
  [{"ticket": <int>, "new_sl": <float>}, ...]
- EA legge (ApplySLModifications, gia' esistente), applica OrderModify,
  cancella il file one-shot.

Path:
- MT4_FILES = ~/Scrivania/XM MT4/MQL4/Files
- AI_BRIDGE_CMD.txt, AI_BRIDGE_RES.txt, orders.json, account.json,
  sl_commands.json

## 3d. Logica post-apertura O8 (2026-10-15)

L'orchestratore esegue 4 controlli ad ogni ciclo (ogni 5 min, anche fuori orario):

1. **check_time_stop**: chiude ordini aperti da >24h.
2. **check_break_even**: se ordine in profitto >= 20 pip, sposta SL a
   entry +2 pip (BUY) / entry -2 pip (SELL). Scrive sl_commands.json.
3. **check_friday_profit (C1)**: venerdi 15:00 UTC, chiude ordini con PNL > 0
   (salva-profitto prima del weekend).
4. **check_friday_close (C2)**: venerdi 20:00 UTC, chiude tutti gli ordini
   aperti (protegge da gap weekend).

Parametri:
- BREAK_EVEN_PIP = 20
- BREAK_EVEN_OFFSET_PIP = 2
- FRIDAY_PROFIT_HOUR_UTC = 15
- FRIDAY_CLOSE_HOUR_UTC = 20
- MAIN_LOOP_SLEEP = 300 (5 min)

Motivazione C1/C2: evitare che un ordine positivo diventi negativo per gap
weekend. Caso reale 2026-10-15: ordine chiuso +2 centesimi, commissione 6
centesimi -> netto -4 centesimi.

## 4. Stato attuale

### Cosa funziona
- MT4 su Wine, terminal.exe attivo.
- Agenti tmux attivi (12 sessioni).
- Servizi systemd user attivi: web-app, controllo-remoto, ai-trading-agenti.
- File condivisi MT4 presenti in /home/carlo/Scrivania/XM MT4/MQL4/Files/:
  orders.json, open_time.json, account.json.
- GitHub carlosciarrino/AI_Trading: integro, sincronizzato con origin/main.
- AI_BRIDGE_EA.mq4 v3.5-bis: FUNZIONANTE in MT4.
  Compila 0 errori, 0 warning. Test end-to-end superato 2026-10-14 23:41.
  md5 .mq4 = c728dfa14c3246268dedd260a0542418
  md5 .ex4 = e9df7b1d225b52b9e756d3df72c19f27
- orchestrator.py O7b-bis: legge AI_BRIDGE_RES.txt dopo ogni comando.
- orchestrator.py O10: news RIATTIVATO.
- orchestrator.py O8: logica post-apertura (break-even, venerdi C1+C2).
  md5 orchestrator.py = 76b3b3eecb734c7f4d5a2b9b33e979e9
- news_agent.py v2 (O10): Investing.com RSS, sentiment, news_context.txt
  ogni 10 min. md5 = d5b5c99630b8ac0512a9b9440a4edc46
- config.json: password broker rimossa (O11). Permessi 600.
  md5 = 65985576e9a14f20c2b2437c11b52a92
- account.json: scritto ogni 5s. Conto demo 450000065, ~100066 EUR.
- docs/PENDENZE.md: registro pendenze (11 voci aperte al 2026-10-15).

### Cosa e' rotto o incompleto
- Vedi docs/PENDENZE.md per l'elenco completo e aggiornato delle pendenze.
- In sintesi: supervisor falso positivo, experiences.json senza rotazione,
  wrapper zombie, agenti muti, loop sell, verifica O8/O7b-bis in produzione.

### Backup attivi (D3)
- AI_BRIDGE_EA.mq4.pre_v3.5bis, .ex4.pre_v3.5bis
- orders.json.pre_v3.5bis
- orchestrator.py.pre_o7b_bis, .pre_o10, .pre_o8
- config.json.pre_o11
- news_agent.py.pre_o10
- supervisor_agent.py.pre_rewrite, .pre_venvfix
- start_all.sh.pre_venvfix, agents_night_shift.sh.pre_venvfix
- CONTESTO.md.pre_o10, .pre_o11, .pre_o8
- HANDOFF.md.pre_o10, .pre_o11, .pre_o8

## 5. Decisioni prese (non si ridiscutono)

D1. Un solo EA per grafico. Telemetria dentro l'EA di trading.
D2. La v3.3 e' il sorgente di riferimento. Ogni modifica parte da li' e
    aggiunge SOLO righe. Se una modifica rimuove righe, e' FAIL.
D3. Ogni modifica a un file di produzione richiede backup con md5sum
    prima/dopo. Il backup non si cancella finche' la modifica non e'
    confermata su demo per almeno 24h.
D4. Kilo non decide mai. Esegue, e se ha dubbi si ferma.
D5. I comandi a Kilo hanno intestazione fissa (5 righe): ID, file target,
    cosa fare, cosa NON fare, dove salvare evidenza.
D6. La chat non incolla codice in mezzo al testo: i comandi a Kilo e i
    comandi al terminale Linux sono sempre in blocchi separati, etichettati
    fuori dal blocco.
D7. La chat dichiara, prima di ogni comando a Kilo, cosa contiene il file
    target e cosa cambia. Carlo autorizza solo dopo aver letto.
D8. La ricerca online va fatta in almeno 3 lingue (italiano, inglese,
    cinese) e su almeno 4 fonti (GitHub, forum specializzati, Reddit/HN,
    repo minori). Non ci si ferma ai primi 3 risultati.
D9. Il ripristino di AI_BRIDGE_EA.mq4 v3.3 e la patch a v3.4 sono fatti
    DIRETTAMENTE dalla chat, non da Kilo. Kilo non tocca questo file.
D10. Solo Carlo e la Chat decidono modifiche a backup PC e a GitHub.
     Kilo non ha voce in capitolo su questo.
D11. La dashboard legge da account.json la telemetria conto. Non da
     orders.json per il saldo. orders.json serve solo per ordini aperti.
D12. IN PRODUZIONE l'orchestratore deve operare SOLO durante i mercati
     Londra (8-17 UTC) e New York (13-22 UTC). Non deve operare di notte.
     Attualmente config.json ha session: 'all' per fare test. Va cambiato
     a 'london_newyork' prima della messa in produzione.
D13. Ogni decisione dell'orchestratore (anche HOLD) va loggata in
     decision_log.jsonl con score, pesi, punteggio finale, azione presa.
     Nessuna decisione senza tracciabilita'.
D14. MetaEditor va CHIUSO prima di modificare AI_BRIDGE_EA.mq4 da
     terminale. Se aperto, sovrascrive il file su disco con la copia in
     memoria. Regola nata dall'incidente 2026-10-14.
D15. Quando Carlo deve modificare un file, la chat fornisce in un UNICO
     messaggio: comando di apertura + contenuto completo da incollare.
     Mai spezzare in due messaggi. Motivo: evitare che il file resti
     aperto e vulnerabile a imprevisti mentre si aspetta il secondo
     messaggio.
D16. Per modificare un file a mano, Carlo preferisce SEMPRE il file
     completo (sostituzione totale), mai istruzioni puntuali (es. "cambia
     riga 5, 20, 40"). Motivo: meno errori (spazi, parentesi), recupero
     piu' semplice, tempo/token risparmiati. Dopo ogni modifica, sempre
     un controllo di routine (grep, md5, wc) commisurato alla modifica.
D17. Nelle regole di calcolo delle operazioni sono SEMPRE inclusi take
     profit, stop loss, commissioni e spread. L'azienda opera con parametri
     ideali. Nessun calcolo "lordo" senza costi reali. Il PNL letto da
     orders.json e' netto (OrderProfit + OrderCommission + OrderSwap).
D18. Ogni questione in sospeso (bug minore, pulizia, debito tecnico)
     emersa durante una sessione va registrata IMMEDIATAMENTE in
     docs/PENDENZE.md, anche se non critica e anche se rinviata. Formato:
     ID [P###], data, priorita', contesto, azione. Nessuna pendenza persa.
     Quando chiusa, si marca [CHIUSA YYYY-MM-DD] e si sposta in fondo.

## 6. Ricerca agenti (una tantum, periodica)

Cercare su GitHub, forum, repo specializzati chi ha costruito agenti di
comunicazione tra agenti, come li ha costruiti, con quali pattern.
Non fermarsi ai primi risultati. Verificare codice, stelle, manutenzione,
licenza. Obiettivo: prendere il meglio e applicarlo a tutti i progetti,
non solo al trading. Questa ricerca si fa una volta, poi si aggiorna
periodicamente.

Per il progetto trading: cercare al 100% dei risultati, ma limitato al
settore trading/algo trading/MT4/MT5/bot/EA/signal/dashboard.
Lingue minime: italiano, inglese, cinese, russo, spagnolo.

Quando passeremo al progetto commerciale: stessa regola, settore
commerciale.

## 7. Prossimo passo (uno solo)

Verifica O8 in produzione. Attendere primo ordine reale e controllare:
- check_break_even scrive sl_commands.json quando profitto >= 20 pip;
- EA applica il nuovo SL;
- check_friday_profit/C1 e check_friday_close/C2 funzionano venerdi.

In assenza di ordini reali (HOLD attuale), testare con ordine manuale
via AI_BRIDGE_CMD.txt.

## 8. Come si aggiorna questo file

Solo in chat, solo a mano, solo quando Carlo dice "aggiorna CONTESTO.md".
Nessuna scrittura automatica. Nessun commit automatico.

## 9. Prossimi obiettivi in coda (non attivi, solo promemoria)

- O4: fix auto-sync Git. FATTO 2026-10-14.
- O5: pulizia file storici. FATTO 2026-10-14.
- O6: ricerca agenti (vedi sezione 6).
- O7: verificare flusso decisione trading orchestratore -> MT4. IN CORSO.
- O7a: decision_log.jsonl. FATTO 2026-10-14.
- O7b: fix orchestrator.py. FATTO 2026-10-14.
- O7b-bis: orchestratore legge AI_BRIDGE_RES.txt. FATTO 2026-10-15.
- O7c: diagnosi 4 segnali. CHIUSO 2026-10-14.
- O8: logica post-apertura. FATTO 2026-10-15. Verifica in corso.
- O9: orario London+NY in config.json (D12). Da fare in produzione.
- O10: news redesign. FATTO 2026-10-15.
- O11: password broker fuori da config.json. FATTO 2026-10-15.
- Pendenze: vedi docs/PENDENZE.md (11 voci aperte al 2026-10-15).
