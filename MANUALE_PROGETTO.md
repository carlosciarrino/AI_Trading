# AI_BRIDGE - Manuale del Progetto

## Ultimo aggiornamento: 2026-08-27

---

## 1. Obiettivo dell'Azienda
Azienda digitale autonoma per il trading sul Forex (EUR/USD). L'obiettivo è generare profitto tramite agenti intelligenti che analizzano dati di mercato, notizie macro, sentiment social e cicli storici. NO sistemi a regole fisse. NO scalping. L'AI deve decidere.

---

## 2. Regole Ferree (Convenzioni)
- UTENTE: NON programmatore, vieta modifiche parziali al codice.
- Ogni modifica richiede: Comando per aprire `nano` -> Svuotare tutto (`Ctrl+K`) -> Incollare file COMPLETO -> Salva ed esci.
- Prima di modificare, fare backup: `cp file.py _backups/file_backup.py` (usare mkdir se serve).
- MAI usare `echo >>` o `cat >` per modificare file.
- Ogni nuova AI deve LEGGERE questo file prima di procedere.
- Il percorso MT4 è: `/home/carlo/Scrivania/XM MT4/MQL4/Files`.
- Broker: FP Markets (Demo) - Login: 4976414, Server: FPTradingLLC-Demo.

---

## 3. Elenco AGENTI (Tutti devono essere attivi)
1. **Market Data Agent** (Orchestratore): Scarica prezzi via yfinance.
2. **AI Decision Agent**: Usa modello `qwen2.5:0.5b` per decidere (BUY/SELL/HOLD). Legge 3 file contesto.
3. **Risk Manager Agent**: Limite duro: MAX 1 OPERAZIONE APERTA. Se superato, STOP.
4. **Bridge Agent (EA)**: Comunica con MT4. Scrive in `AI_BRIDGE_CMD.txt` e legge `AI_BRIDGE_RES.txt`.
5. **Sentinel Agent** (Sentinella): Controlla ogni 10 secondi. Se trova anomalie (troppi ordini, processi morti, Traceback), UCCIDE tutto.
6. **News Agent**: Legge RSS BBC/Reuters. Cerca parole chiave (guerra, crisi, ecc.). Scrive `news_context.txt`.
7. **Social Agent**: Legge Google News. Scrive `social_context.txt`.
8. **Cycle Agent**: Analizza stagionalità (5 anni). Scrive `cycles_context.txt`.
9. **Strategy Tester Agent**: **NON ATTIVO. DA INSERIRE.** Deve testare le strategie su dati storici prima che vengano usate.
10. **GitHub Researcher Agent**: Cerca su GitHub progetti/skill da integrare.
11. **Dashboard Agent**: Mostra tutto all'utente su web app.

---

## 4. Log di Decisioni e Test (Storico)
- **2026-08-27**: Aperto 50 operazioni per errore (bug loop EA). Risolto con EA che cancella file subito e limite MAX 1 operazione.
- **2026-08-27**: Bug Pandas (iat) risolto. Uso `float(df["Close"].iloc[-1])`.
- **2026-08-27**: Dashboard riscritta (V4) con Organigramma, Auto-Refresh e Controllo Agent.

---

## 5. Prossimi Passi
1. Creare e attivare **Strategy Tester Agent**.
2. Creare e attivare **GitHub Researcher Agent**.
3. Preparare pacchetto USB (con `install.sh` e `start.sh`).

---
