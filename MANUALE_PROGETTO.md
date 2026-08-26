# AI_BRIDGE - Manuale del Progetto

## Ultimo aggiornamento: 2026-08-28

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
*(...elenco aggiornato...)*

---

## 4. Log di Decisioni e Test (Storico)
- **2026-08-27**: Aperto 50 operazioni per errore. Risolto con EA che cancella file subito e limite MAX 1 operazione.
- **2026-08-27**: Bug Pandas risolto. Uso `float(df["Close"].iloc[-1])`.
- **2026-08-27**: Dashboard riscritta (V4) con Organigramma, Auto-Refresh e Controllo Agent.
- **2026-08-28**: Implementazione sistema di Diagnostica della Catena (Sentinella potenziata).
    - **Fonte**: Integrazione del progetto open-source **Argus** (https://github.com/mylesndavid/argus) per il monitoraggio del comportamento degli agenti.
    - **Obiettivo**: Rilevare "stalli silenziosi" dove l'agente è vivo ma non produce output, eliminando i falsi positivi nel controllo di sistema.

---

## 5. Prossimi Passi
1. Integrare la Sentinella con il sistema diagnostico Argus.
2. Aggiungere un test automatico che verifichi che ogni agente produca un output entro un tempo massimo (es. 10 minuti).
3. Configurare Alert Telegram se la catena si rompe.
