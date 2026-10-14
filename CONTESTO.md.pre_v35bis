# CONTESTO PROGETTO AI_TRADING

Ultimo aggiornamento: 2026-10-14 20:25
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
  E' un riferimento, non un pezzo attivo del sistema.
- Gli agenti Python girano in tmux sessione "ai_workforce".
- La dashboard web gira come servizio systemd user "web-app".

## 3b. Segnali dell'orchestratore e pesi

L'orchestratore legge 5 file di contesto, assegna uno score a ciascuno,
moltiplica per un peso, somma e divide per la somma dei pesi.

| Segnale      | Fonte file                 | Peso  | Range score    |
|--------------|----------------------------|-------|----------------|
| news         | news_context.txt           | 0.20  | -0.3 / 0 / +0.3|
| social       | social_context.txt         | 0.20  | -0.2 / 0 / +0.2|
| cycle        | cycles_context.txt         | 0.15  | -0.2 / 0 / +0.2|
| volume       | volume_context.txt         | 0.25  | variabile      |
| experience   | experiences.json           | 0.20  | -0.2 / 0       |
|--------------|----------------------------|-------|----------------|
| SOMMA PESI   |                            | 1.00  |                |

Soglie decisionali (post O7b):
- final_score > +0.10  ->  BUY
- final_score < -0.10  ->  SELL
- altrimenti           ->  HOLD

Punteggio attuale: -0.04 (solo experience contribuisce con -0.2).
Risultato: HOLD.

Riferimento codice: /home/carlo/AI_Trading/orchestrator.py, funzione
get_signal().

## 3c. Contratto orchestratore <-> EA (confermato 2026-10-14)

Formato comando accettato da AI_BRIDGE_EA.mq4 (funzione ExecuteCommand):
  buy  [lots] [sl_price] [tp_price]
  sell [lots] [sl_price] [tp_price]
  close <ticket>

Ciclo file comando:
- orchestratore scrive "AI_BRIDGE_CMD.txt"
- EA legge, esegue, FileDelete(CMD_FILE) one-shot
- EA scrive esito in "AI_BRIDGE_RES.txt" (OK: aperto <ticket>... / ERR: ...)
- orchestratore NON legge AI_BRIDGE_RES.txt (debolezza, da fixare)

Path:
- MT4_FILES = ~/Scrivania/XM MT4/MQL4/Files
- AI_BRIDGE_CMD.txt, AI_BRIDGE_RES.txt, orders.json, account.json

## 4. Stato attuale

### Cosa funziona
- MT4 su Wine, terminal.exe attivo.
- Agenti tmux attivi (12 finestre).
- Servizi systemd user attivi: web-app, controllo-remoto, ai-trading-agenti.
- File condivisi MT4 presenti in /home/carlo/Scrivania/XM MT4/MQL4/Files/:
  orders.json, open_time.json, sl_commands.json, account.json.
- GitHub carlosciarrino/AI_Trading: integro, sincronizzato con origin/main.
- Cartelle backup PC: intatte, non toccate da Kilo.
- AI_BRIDGE_EA.mq4 v3.5: FUNZIONANTE in MT4. v3.4 + fix accumulo.
  Compila 0 errori, 0 warning.
  md5 .mq4 = 7bd03880a822babf63770b92671bf62f
  md5 .ex4 = 2c5ca83375d568aef8f1abfd62baa5e3
- account.json: scritto ogni 5s con balance, equity, margin, free_margin,
  profit, open_orders, currency, leverage, login, server, timestamp.
  Conto demo: FPTrading-Demo login 450000065, saldo 100066.75 EUR.

### Cosa e' rotto o incompleto
- orders.json: bug accumulo RISOLTO in v3.5. File stabile, no crescita
  a parita' di ordini. Backup del file gonfio in MQL4/Files/orders.json.pre_v3.5fix.
- orders_backup_20261002_2335.json: 200 MB, file storico enorme in
  MQL4/Files/. Va archiviato o rimosso.
- supervisor: RISCRITTO v2 il 2026-10-14. Legge stato agenti da tmux,
  riavvia critici fermi, aggiorna audit_status.json ogni 300s. Venv
  canonico: /home/carlo/AI_Trading_Agents/venv. Log: /home/carlo/supervisor.log.
- web_app: RISCRITTO unificato il 2026-10-14. Legge account.json e
  orders.json da MT4, mostra saldo/equity/margin/free_margin/profit,
  PNL giorno/settimana, ordini aperti/chiusi, controllo agenti tmux
  (start/stop/restart individuale). Pagine: /, /trading, /agents,
  /verifier, /media, /ecommerce. API: /api/account, /api/orders,
  /api/pnl, /api/agent/<name>/<action>. Servizio systemd user web-app
  attivo, porta 5000.
- loop sell: non diagnosticato.
- test.mq4 in MT4 Experts: residuo di Kilo, da rimuovere.
- Script auto-sync Git: bug nel messaggio commit, scrive "$(date)" come
  stringa invece di espanderlo. RISOLTO 2026-10-14.
- orchestrator.py: path ordini CORRETTO in O7b. count_open_orders legge
  da account.json (campo open_orders). check_time_stop ora funziona.
- orchestrator.py: regex volume CORRETTO in O7b. Score volume ora legge
  il valore vero da volume_context.txt.
- orchestrator.py: MAX_OPEN_ORDERS allineato a 1 in O7b (letto da
  account.json).
- orchestrator.py: soglia decisionale ALZATA da ±0.01 a ±0.10 in O7b.
  Il sistema ora non apre su segnali deboli.
- news_context.txt: ORFANO. Nessun agente attivo lo scrive. Residuo storico.
  news_agent.py attuale scrive solo /tmp/news_score.txt (numero). Segnale
  news SOSPESO in orchestrator.py (forzato a 0.0). Da riprogettare in O10.
- social_agent.py: PATCHATO 2026-10-14. Aggiunta funzione sentiment_score()
  (keyword list EN, positivo/negativo/neutro). File social_context.txt ora
  contiene riga "Sentiment: negativo|positivo|neutro". Orchestratore legge
  correttamente. Segnale ATTIVO.
- cycle_agent.py: PATCHATO 2026-10-14. Fix MultiIndex yfinance
  (df.columns.get_level_values(0)). cycles_context.txt ora contiene 12 righe
  "Mese N: media prezzo X.XXXXX". Orchestratore legge correttamente. Segnale
  ATTIVO (ottobre media 1.08960 -> range 1.08-1.10 -> 0.0).
- orchestrator.py: NON legge AI_BRIDGE_RES.txt. Logga action_taken ma non
  verifica esito. decision_log.jsonl puo' riportare ticket:null anche se
  l'ordine e' stato rifiutato dall'EA (es. "ERR: limite operazioni raggiunto").
  Da fixare.
- orders.json: record con doppio "status" (open + closed). Bug residuo v3.5
  nella dedup (cerca "status":"closed" esatto). Da fixare in v3.5-bis.
- 8 agenti su 11 non scrivono log attivi: social_agent, news_agent,
  cycle_agent, market_anomaly, kronos_agent, nzt_agent, signal_observer,
  strategy_validator. Da indagare se fanno qualcosa o sono muti.
- orchestrator.py: nessuna storia dietro l'ordine nel log (risolto
  parzialmente con decision_log.jsonl in O7a).
- orchestrator.py: nessuna logica post-apertura (break-even, rivalutazione
  giornaliera, chiusura venerdi'). Da implementare.

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

O7c: indagare perche' 4 segnali su 5 sono sempre 0:
- news: news_context.txt fermo al 2026-09-05 (news_agent rotto o muto).
- social: social_context.txt aggiornato ma non contiene 'positivo'/'negativo'.
- cycle: cycles_context.txt non matcha il pattern 'mese N' atteso.
- volume: ora regex corretto, ma il file contiene 'score 0.00'.

O7d: logica post-apertura (break-even, rivalutazione giornaliera,
chiusura venerdi'). Vedi O8.

## 8. Come si aggiorna questo file

Solo in chat, solo a mano, solo quando Carlo dice "aggiorna CONTESTO.md".
Nessuna scrittura automatica. Nessun commit automatico.
Se una decisione cambia, si aggiorna qui, e la vecchia versione resta nel
diario Git con messaggio "contesto: <cosa e' cambiato>".

## 9. Prossimi obiettivi in coda (non attivi, solo promemoria)

- O4: fix script auto-sync Git ($(date) non espanso). FATTO 2026-10-14.
- O5: pulizia file storici. FATTO 2026-10-14 (190 MB liberati).
- O6: ricerca agenti (vedi sezione 6).
- O7: verificare flusso decisione trading orchestratore -> MT4. IN CORSO.
- O8: logica post-apertura (break-even, rivalutazione giornaliera,
  chiusura venerdi'). Da progettare.
- O9: attivare orario di mercato London+NY in config.json (D12). Da
  fare in fase di produzione.
