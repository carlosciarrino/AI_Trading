# AI_BRIDGE V2 — PROMPT DI CONTINUITÀ

## Modalità di lavoro

**CAVEMAN MODE FULL**

- Risposte brevi.
- Nessuna teoria inutile.
- Nessuna proposta non richiesta.
- Ogni risposta deve produrre un avanzamento concreto.
- Se serve modificare un file:
  - fornire file completo;
  - mai patch;
  - mai frammenti;
  - includere compilazione;
  - includere test;
  - includere commit Git.

## Repository

Repository:

~/AI_Trading

Branch corrente:

feature/fast-track

Git locale.

Nessun remoto GitHub configurato.

## Regole

- Repository = fonte di verità.
- Nessuna API inventata.
- Nessuna dipendenza inventata.
- Nessun refactoring fuori milestone.
- Verificare solo file coinvolti.

## Stato

Completate:

- M01 Bootstrap
- M02 Runtime Controller
- M03 Application Layer
- M04 System Builder
- M05 Orchestrator
- M06 Market Engine
- M07 Decision Engine
- M08 Risk Engine
- M09 Memory Engine
- M10 Learning Engine
- M11 Diagnostics CLI
- M12 System Inspector
- M13 Continuity Dossier
- M14 Handoff Prompt
- M15 Project Progress

Milestone corrente:

M16 — System Diagnostics

## Stato repository

Esistono:

core_v2/application.py
core_v2/system_inspector.py
diagnostics_v2.py

Non esiste:

core_v2/system_diagnostics.py

## Decisioni confermate

- Nessuna API precedente definita.
- Nessuna implementazione precedente.
- Nessun pseudocodice.
- API minima da progettare coerentemente con repository.

## Obiettivo

Creare:

core_v2/system_diagnostics.py

Usare:

- SystemInspector
- nessuna logica di presentazione
- riutilizzabile da CLI, Dashboard, API

Integrare in:

core_v2/application.py

CLI continua a usare solo application.py.

## Metodo

Ogni risposta deve produrre:

- codice completo;
- compilazione;
- test;
- commit Git.

Mai interrompere flusso con discussioni lunghe.

## Primo passo

Leggere solo file necessari.

Implementare M16.

Compilare.

Testare.

Commit.

Passare subito a milestone successiva.
