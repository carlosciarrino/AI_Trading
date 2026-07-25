# AI_BRIDGE V2 — PROJECT INDEX

Versione: 1.0

Ultimo aggiornamento: 2026-07-25

---

# SCOPO

Questo documento rappresenta il punto di ingresso ufficiale del progetto.

Qualsiasi sviluppatore o nuova sessione di lavoro deve iniziare da qui.

Non iniziare mai direttamente dal codice.

Seguire sempre l'ordine di lettura riportato in questo documento.

---

# DOCUMENTI UFFICIALI

Ordine di lettura obbligatorio:

1.

docs/AI_BRIDGE_V2_CONTINUITY_DOSSIER.md

Contiene:

- visione del progetto
- architettura
- filosofia progettuale
- componenti
- roadmap
- pipeline
- regole tecniche

---

2.

docs/PROJECT_PROGRESS.md

Contiene:

- stato delle milestone
- attività completate
- attività future
- milestone corrente

---

3.

docs/HANDOFF_PROMPT.md

Contiene:

- protocollo operativo
- regole di consegna
- modalità di sviluppo

---

# REPOSITORY

Repository

~/AI_Trading

Branch principale

main

Branch di sviluppo corrente

feature/diagnostics-cli

---

# STATO ATTUALE

Sistema stabile.

Repository pulito.

Documentazione di continuità completata.

Architettura consolidata.

---

# MILESTONE CORRENTE

M16

System Diagnostics

File da realizzare

core_v2/system_diagnostics.py

Obiettivo

Centralizzare la diagnostica del sistema utilizzando
SystemInspector come sorgente dati.

Il modulo non dovrà contenere logica di presentazione.

Dovrà poter essere utilizzato da:

- Diagnostics CLI
- Dashboard future
- API future

---

# FILE PRINCIPALI DEL PROGETTO

core_v2/application.py

core_v2/system_builder.py

core_v2/orchestrator.py

core_v2/runtime_controller.py

core_v2/memory_engine.py

core_v2/learning_engine.py

core_v2/system_inspector.py

diagnostics_v2.py

main_v2.py

---

# REGOLE OPERATIVE

Prima leggere la documentazione.

Poi verificare la milestone corrente.

Successivamente modificare esclusivamente i file coinvolti.

Aggiornare PROJECT_PROGRESS.md al termine della milestone.

Aggiornare AI_BRIDGE_V2_CONTINUITY_DOSSIER.md solo se viene modificata l'architettura.

---

# OBIETTIVO

Garantire la continuità dello sviluppo senza dover ricostruire il progetto a ogni nuova sessione.

Questo documento rappresenta il punto di ingresso ufficiale di AI_BRIDGE V2.
