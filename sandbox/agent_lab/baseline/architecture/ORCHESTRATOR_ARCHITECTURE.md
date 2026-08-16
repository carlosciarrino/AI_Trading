# AI_BRIDGE V2 — Orchestrator Architecture

## Scopo del documento

Questo documento definisce il ruolo architetturale dell'Orchestrator in AI_BRIDGE V2.

L'Orchestrator è il coordinatore del sistema.
Non contiene logica decisionale di trading e non sostituisce gli engine specializzati.

La sua responsabilità è garantire che i componenti del sistema collaborino secondo un flusso ordinato e prevedibile.

---

# Principio fondamentale

L'Orchestrator è un coordinatore, non un motore.

Responsabilità:

- inizializzazione componenti;
- gestione ciclo operativo;
- coordinamento chiamate;
- gestione stato generale del sistema;
- collegamento tra engine.

Non deve contenere:

- strategie di trading;
- indicatori di mercato;
- calcoli rischio;
- logiche broker;
- apprendimento.

---

# Posizione nell'architettura

Pipeline:

Market Engine
↓
Decision Engine
↓
Risk Engine
↓
Execution Engine
↓
Monitoring Engine
↓
Memory Engine
↓
Learning Engine

L'Orchestrator coordina il flusso senza assumere la responsabilità delle singole fasi.

---

# Ciclo operativo

Il ciclo principale previsto:

1. Avvio sistema
2. Caricamento configurazione
3. Inizializzazione engine
4. Raccolta dati mercato
5. Generazione decisione
6. Valutazione rischio
7. Eventuale esecuzione
8. Monitoraggio risultato
9. Aggiornamento memoria
10. Processo di apprendimento futuro

---

# Regole di progettazione

## Dipendenze esplicite

Ogni engine deve ricevere le proprie dipendenze tramite parametri.

Nessun componente deve cercare autonomamente altri moduli globali.

---

## Nessuna duplicazione

Ogni responsabilità deve avere un solo proprietario.

Se una logica appartiene a un engine, non deve essere replicata nell'Orchestrator.

---

## Evoluzione futura

L'Orchestrator dovrà permettere:

- sostituzione degli engine;
- aggiunta nuovi broker;
- evoluzione del sistema learning;
- esecuzione multi-strategia.

---

# Stato attuale

Questo documento descrive l'architettura prevista.

L'integrazione completa degli engine sarà sviluppata nella fase successiva:
Pipeline Integration.
