# AI_BRIDGE V2 — Pipeline Integration Architecture

## Scopo

Definire il primo ciclo operativo integrato di AI_BRIDGE V2.

Questo documento descrive il collegamento tra gli engine senza modificare le responsabilità interne dei singoli moduli.

---

# Pipeline principale

Market Engine
↓
Decision Engine
↓
Risk Engine
↓
Execution Engine
↓
Memory Engine
↓
Learning Engine

---

# Pipeline di controllo

Monitoring Engine
↓
Recovery Engine

Il sistema di controllo osserva il ciclo operativo senza sostituirlo.

---

# Ruolo Orchestrator

L'Orchestrator coordina il ciclo.

Non contiene:

- strategie trading;
- calcoli rischio;
- logiche broker.

Gestisce solamente ordine e comunicazione.

---

# Primo ciclo operativo

1. Aggiornamento mercato
2. Generazione decisione
3. Validazione rischio
4. Eventuale esecuzione
5. Memorizzazione risultato
6. Analisi apprendimento
7. Controllo salute sistema

---

# Stato attuale

Tutti gli engine baseline sono presenti.

La fase successiva implementerà il collegamento operativo mantenendo interfacce stabili.
