# AI_BRIDGE - Manuale del Progetto

## Ultimo aggiornamento: 2026-08-27

---

## 1. Obiettivo dell'Azienda
Azienda digitale autonoma per il trading sul Forex (EUR/USD). L'obiettivo è generare profitto tramite agenti intelligenti che analizzano dati di mercato, notizie macro, sentiment social e cicli storici. NO sistemi a regole fisse. NO scalping. L'AI deve decidere.

---

## 2. Regole Ferree (Convenzioni)
- UTENTE: NON programmatore, vieta modifiche parziali al codice.
- Ogni modifica richiede: Comando per aprire `nano` -> Svuotare tutto (`Ctrl+K`) -> Incollare file COMPLETO -> Salva ed esci.
- Prima di modificare, fare backup: `cp file.py _backups/file_backup.py`.
- MAI usare `echo >>` o `cat >` per modificare file.
- Ogni nuova AI deve LEGGERE questo file prima di procedere.
- Il percorso MT4 è: `/home/carlo/Scrivania/XM MT4/MQL4/Files`.
- Broker: FP Markets (Demo) - Login: 4976414, Server: FPTradingLLC-Demo.

---

## 3. Elenco AGENTI (Tutti devono essere attivi)
1. **Orchestratore (ai_workforce)**: Prende decisioni di trading tramite AI e gestisce il flusso dati.
2. **Dashboard (dashboard)**: Mostra lo stato dell'azienda all'utente.
3. **Sentinella (sentinel)**: Monitora la sicurezza e ferma il sistema in caso di anomalie.
4. **Agente Notizie (news_agent)**: Analizza notizie macro (guerre, crisi, tassi).
5. **Agente Social (social_agent)**: Analizza sentiment da social e news trending.
6. **Agente Cicli (cycle_agent)**: Analizza cicli storici e stagionalità del mercato.
7. **Agente Esperienza (experience_agent)**: Impara dagli errori passati e aggiorna la memoria.
8. **Strategy Tester (strategy_tester_agent)**: Testa nuove strategie su dati storici.
9. **GitHub Researcher (github_researcher)**: Cerca progetti utili su GitHub.
10. **Skill Researcher (skill_researcher)**: Cerca nuove competenze, framework o strategie online.
11. **News Critical (news_critical)**: Analizza condizioni socio-politiche globali.
12. **AI Researcher (ai_researcher_agent)**: Cerca nuove intelligenze artificiali disponibili.
13. **AI Tester (ai_tester_agent)**: Testa le nuove AI su compiti reali per verificarne l'affidabilità.

---

## 4. Log di Decisioni e Test (Storico)
- **2026-08-27**: Aperto 50 operazioni per errore. Risolto con EA che cancella file subito e limite MAX 1 operazione.
- **2026-08-27**: Bug Pandas risolto. Uso `float(df["Close"].iloc[-1])`.
- **2026-08-27**: Dashboard riscritta (V4) con Organigramma, Auto-Refresh e Controllo Agent.

---

## 5. Prossimi Passi
1. Aggiungere gli agenti `ai_researcher_agent` e `ai_tester_agent` alla dashboard.
2. Testare i nuovi modelli AI open-source (Meta Muse Glimmer, Nvidia Nemotron 3.5 Lightning).
3. Preparare pacchetto USB (con `install.sh` e `start.sh`).

---
