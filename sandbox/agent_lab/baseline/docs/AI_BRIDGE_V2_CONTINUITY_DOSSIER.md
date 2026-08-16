# AI_BRIDGE V2 — CONTINUITY DOSSIER
Versione: 1.0
Stato: Documento Ufficiale di Continuità
Aggiornamento: 2026-07-25

---

# SCOPO DEL DOCUMENTO

Questo documento rappresenta la memoria tecnica ufficiale di AI_BRIDGE V2.

Non è una semplice documentazione.

È il riferimento tecnico che permette a qualsiasi sviluppatore o nuova sessione di comprendere completamente il progetto senza dover ricostruire settimane di lavoro.

Ogni modifica architetturale importante dovrà essere riportata in questo documento.

Questo documento ha priorità rispetto alle ricostruzioni effettuate da una nuova chat.

---

# OBIETTIVO DEL PROGETTO

AI_BRIDGE V2 è un Trading Operating System professionale.

Non è un Expert Advisor.

Non è un semplice bot.

È un sistema operativo modulare dedicato al trading algoritmico.

Il progetto è costruito per essere:

- modulare
- estendibile
- osservabile
- mantenibile
- professionale

---

# FILOSOFIA PROGETTUALE

Ogni componente possiede una sola responsabilità.

La logica è distribuita nei vari Engine.

Nessun Engine deve svolgere il lavoro di un altro.

L'architettura è più importante della velocità di sviluppo.

Prima si costruiscono fondamenta solide.

Successivamente vengono aggiunte nuove funzionalità.

---

# PRINCIPI ARCHITETTURALI

• Python Standard Library.

• Type Hints obbligatori.

• Dataclass dove appropriate.

• API stabili.

• Nessuna duplicazione.

• Nessuna dipendenza circolare.

• Nessuna logica nel layer di presentazione.

• Ogni Engine deve poter essere testato indipendentemente.

---

# STRUTTURA GENERALE

Il progetto è composto da Engine indipendenti.

Ogni Engine ha una responsabilità precisa.

La comunicazione avviene attraverso AIComponents.

L'Orchestrator coordina il ciclo operativo.

---

# COMPONENTI PRINCIPALI

Bootstrap

Runtime Controller

Application

System Builder

Orchestrator

Market Engine

Decision Engine

Risk Engine

Execution Engine

Memory Engine

Learning Engine

Monitoring Engine

Recovery Engine

Event Engine

System Inspector

Diagnostics CLI

---

# STATO ATTUALE

Completati:

- Bootstrap
- Runtime
- Application
- System Builder
- Orchestrator
- Memory Engine
- Learning Engine
- Execution Summary
- Learning Summary
- Runtime Statistics
- Decision History
- Pipeline Summary
- Diagnostics CLI
- System Inspector

---

# SYSTEM INSPECTOR

Responsabilità:

Fornire una vista tecnica dello stato corrente del sistema.

Espone:

- snapshot()
- runtime_state()
- memory_snapshot()
- last_pipeline_record()
- recent_pipeline_records()
- orchestrator_statistics()

Non contiene logica di presentazione.

---

# COMPONENTE SUCCESSIVO

SystemDiagnostics

Responsabilità:

Centralizzare tutte le informazioni diagnostiche del sistema.

Utilizzerà SystemInspector come sorgente dei dati.

Non conterrà logica di stampa.

Sarà riutilizzabile dalla CLI e da eventuali dashboard future.

---

# REGOLE DI SVILUPPO

Ogni nuovo modulo deve rispettare:

- responsabilità unica
- type hints
- dataclass quando necessarie
- docstring
- Python Standard Library

---

# REGOLE DI CONSEGNA

Quando un file viene modificato, la consegna deve contenere nello stesso messaggio:

1. comando nano

2. file completo

3. compilazione

4. test

5. commit Git

Mai patch parziali.

Mai frammenti.

Mai file lasciati aperti.

---

# PASSAGGIO DI CONSEGNE

Una nuova chat deve:

1.

Leggere completamente questo documento.

2.

Considerarlo la fonte autorevole del progetto.

3.

Non ricostruire l'architettura.

4.

Non cercare file inesistenti.

5.

Non modificare moduli già stabili senza motivazione.

6.

Proseguire esclusivamente dalla milestone corrente.

---

# STATO DEL REPOSITORY

Repository:

~/AI_Trading

Branch di lavoro:

feature/diagnostics-cli

Repository pulito.

---

# PROSSIMA MILESTONE

Realizzazione di:

core_v2/system_diagnostics.py

Successiva integrazione con:

- diagnostics_v2.py

- application.py

---

Questo documento dovrà essere aggiornato dopo ogni milestone importante.
