# AI_BRIDGE - MANUALE COMPLETO DEL PROGETTO

## Ultimo aggiornamento: 2026-08-29

---

## 1. IDENTITÀ DELL'UTENTE
- **Non programmatore.** NON modificare MAI pezzi di codice.
- Ogni modifica richiede: Comando nano -> Svuotare tutto (Ctrl+K) -> Incollare file COMPLETO -> Salva.
- Prima di ogni modifica, fare backup: `cp file.py _backups/file_backup.py`.
- Il progetto è un'**azienda digitale autonoma** per trading Forex (EUR/USD). Deve lavorare da sola, generare profitto e proteggersi dai rischi.

---

## 2. OBIETTIVO AZIENDALE
- Profitto tramite **agenti intelligenti** che analizzano dati di mercato, notizie, social, cicli storici.
- **NO sistemi a regole fisse.** L'AI deve decidere (modello `qwen2.5:0.5b` via Ollama).
- **NO scalping.** Si opera su timeframe 15min con sessioni selezionabili (Londra, New York, Tokyo).

---

## 3. REGOLE FERREE DI COLLABORAZIONE
- MAI usare `cat >` o `echo >>` per scrivere file. Usare SEMPRE `nano`.
- Non usare MAI comandi lunghi nel terminale: uno alla volta.
- Ogni nuovo agente deve essere creato, avviato e documentato immediatamente.
- Ogni nuova intelligenza artificiale o chat deve LEGGERE questo file prima di procedere.

---

## 4. ARCHITETTURA TECNICA (File principali)
- **`web_app.py`**: Dashboard (Flask). Contiene 4 sezioni: Dashboard, Trading, Agenti, Configura. Ha il pulsante "STOP TUTTO" e il pulsante "Leggi Report".
- **`orchestrator.py`**: Prende decisioni tramite AI, gestisce orari di trading (configurabili), invia ordini al bridge.
- **`AI_BRIDGE_EA.mq4`**: Expert Advisor su MT4. Legge `AI_BRIDGE_CMD.txt`, piazza ordini, scrive `AI_BRIDGE_RES.txt`. Ha limite massimo operazioni e parametri configurabili.
- **`sentinel.py`**: Sentinella avanzata. Controlla che l'orchestratore sia vivo e produttivo. Se blocchi, uccide tutto.
- **`strategy_tester_agent.py`**: Legge `strategia_da_testare.txt` (il link), chiede all'AI di analizzare e salva `report_strategia.txt`.

---

## 5. ELENCO AGENTI (Tutti devono essere attivi in `tmux ls`)
| Nome Sessione | Nome Agente | Ruolo |
| :--- | :--- | :--- |
| `ai_workforce` | Orchestratore | Prende decisioni di trading tramite AI e gestisce il flusso dati. |
| `dashboard` | Dashboard | Mostra lo stato dell'azienda all'utente. |
| `sentinel` | Sentinella | Monitora la sicurezza e ferma il sistema in caso di anomalie. |
| `news_agent` | Agente Notizie | Analizza notizie macro (guerre, crisi, tassi). |
| `social_agent` | Agente Social | Analizza sentiment da social e news trending. |
| `cycle_agent` | Agente Cicli | Analizza cicli storici e stagionalità del mercato. |
| `experience_agent` | Agente Esperienza | Impara dagli errori passati e aggiorna la memoria. |
| `strategy_tester_agent` | Strategy Tester | Analizza link e testa strategie su dati storici. |
| `github_researcher` | GitHub Researcher | Cerca progetti utili su GitHub. |
| `skill_researcher` | Skill Researcher | Cerca nuove competenze, framework o strategie online. |
| `news_critical` | News Critical | Analizza condizioni socio-politiche globali. |
| `ai_researcher_agent` | AI Researcher | Cerca nuove intelligenze artificiali disponibili. |
| `ai_tester_agent` | AI Tester | Testa le nuove AI su compiti reali. |
| `sync_agent` | Sync Agent | Sincronizza il progetto su GitHub e USB. |

---

## 6. CONFIGURAZIONI CRITICHE
- **Percorso MT4 (File di comunicazione):** `/home/carlo/Scrivania/XM MT4/MQL4/Files`
  - `AI_BRIDGE_CMD.txt` (comando da Python a MT4)
  - `AI_BRIDGE_RES.txt` (risposta da MT4 a Python)
- **Broker:** FP Markets (Demo)
  - Login: `4976414`
  - Password: `100607Mattia$` (Solo conto demo, non condividere pubblicamente)
  - Server: `FPTradingLLC-Demo`
- **Modello AI:** `qwen2.5:0.5b` (via Ollama locale)
- **Limite operazioni:** Massimo 1 operazione aperta alla volta.

---

## 7. STATO ATTUALE (29/08/2026)
- Tutti gli agenti sopra elencati sono operativi e in esecuzione.
- Il bot ha aperto e chiuso un'operazione in negativo dopo 2-3 giorni (problema time-stop).
- La dashboard è completa con selezione sessioni di trading.
- L'EA è stato aggiornato con parametri configurabili (lotti, SL, TP).

---

## 8. PROSSIMI PASSI (PIANO OPERATIVO APPROVATO)
1. **Integrare OmniRoute** (router AI open-source) per sostituire Ollama e gestire i token gratuiti di vari provider. Endpoint: `http://localhost:20128/v1`.
2. **Creare Agente YouTube/Instagram** (base: progetto `yt-digest`) per monitorare video e notizie utili.
3. **Creare Agente Test Indicatori** (base: progetto `forex-trader`) per testare indicatori come conferma, eseguendo backtest notturni.
4. **Implementare Time-Stop**: Chiudere automaticamente un'operazione se resta aperta per più di 24 ore.

---

## 9. COME AVVIARE IL SISTEMA (Dopo un riavvio completo)
Nel terminale, eseguire questi comandi UNO ALLA VOLTA:
```bash
tmux kill-server 2>/dev/null
