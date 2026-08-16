# AI_BRIDGE V2 — PROMPT DI CONTINUITÀ

## Modalità di lavoro

**CAVEMAN MODE FULL**

* Risposte brevi.
* Nessuna teoria inutile.
* Nessuna proposta non richiesta.
* Ogni risposta deve produrre un avanzamento concreto.
* Se serve modificare un file:

  * fornire **file completo**;
  * mai patch;
  * mai frammenti;
  * includere compilazione;
  * includere test;
  * includere commit Git.

---

# Repository

```text
~/AI_Trading
```

Branch corrente:

```text
feature/fast-track
```

Git locale.

Nessun remoto GitHub ancora configurato.

---

# Regole fondamentali

Il repository è la fonte di verità.

La memoria della chat non prevale mai sul codice.

Prima di modificare:

1. verificare solo i file coinvolti;
2. evitare analisi dell'intero progetto;
3. nessun refactoring fuori milestone;
4. nessuna API inventata;
5. nessuna dipendenza inventata.

---

# Stato progetto

Milestone completate:

* M01 Bootstrap
* M02 Runtime Controller
* M03 Application Layer
* M04 System Builder
* M05 Orchestrator
* M06 Market Engine
* M07 Decision Engine
* M08 Risk Engine
* M09 Memory Engine
* M10 Learning Engine
* M11 Diagnostics CLI
* M12 System Inspector
* M13 Continuity Dossier
* M14 Handoff Prompt
* M15 Project Progress

Milestone corrente:

**M16 — System Diagnostics**

---

# Stato reale verificato

Esistono:

```text
core_v2/application.py
core_v2/system_inspector.py
diagnostics_v2.py
```

Non esiste:

```text
core_v2/system_diagnostics.py
```

`diagnostics_v2.py` usa esclusivamente funzioni pubbliche di `core_v2.application`.

`SystemInspector` espone già API di sola lettura sullo stato del sistema.

---

# Decisioni progettuali confermate

Dalle verifiche del repository e delle chat precedenti risulta che:

* non è mai stata definita un'API pubblica per `SystemDiagnostics`;
* non è mai stato scritto il file;
* non esiste pseudocodice;
* non esiste implementazione nascosta.

Quindi la nuova chat dovrà progettare **l'API minima**, coerente con l'architettura esistente, senza inventare dipendenze.

---

# Obiettivo immediato

Completare M16.

Realizzare:

```text
core_v2/system_diagnostics.py
```

Requisiti:

* usare `SystemInspector`;
* nessuna logica di presentazione;
* raccogliere dati diagnostici;
* essere riutilizzabile da:

  * `diagnostics_v2.py`;
  * Dashboard future;
  * API future.

Successivamente integrare il modulo in:

```text
core_v2/application.py
```

Lasciando la CLI dipendente solo dalle API pubbliche dell'application layer.

---

# Metodo operativo

Ogni risposta deve terminare con:

* codice completo;
* compilazione;
* test;
* commit Git.

Mai interrompere il flusso con discussioni lunghe.

Produrre almeno un avanzamento verificabile per sessione.

---

# Primo passo nella nuova chat

Leggere esclusivamente i file necessari alla M16.

Implementare direttamente `core_v2/system_diagnostics.py`.

Aggiornare `core_v2/application.py`.

Compilare.

Testare.

Commit.

Passare immediatamente alla milestone successiva.

---

# Regola di continuità

Ogni modifica significativa del flusso di lavoro, delle milestone o dell'architettura deve essere riportata anche nel prompt di handoff.

File di riferimento:

```text
docs/HANDOFF_PROMPT.md
```

Il file deve rappresentare sempre lo stato corrente del progetto e consentire di riprendere lo sviluppo da una nuova chat senza ricostruire il contesto.

Ad ogni milestone completata:

* aggiornare `docs/HANDOFF_PROMPT.md`;
* aggiornare `docs/PROJECT_PROGRESS.md`;
* eseguire commit Git.


## AGENTIC WORKFORCE RULE — MANDATORY

AI_BRIDGE development follows an enterprise-style dynamic workforce model.

### Mandatory procedure

Before implementing new functionality internally:

1. SEARCH existing free/open-source solutions.
2. QUALIFY candidate repositories.
3. CHECK license and provenance.
4. RUN security inspection.
5. RUN sandbox validation.
6. RUN modification test.
7. RUN recovery/rollback test.
8. RUN benchmark.
9. COMPARE candidate against internal implementation cost.
10. REUSE, ADAPT, or REJECT based on evidence.

Do not reinvent functionality when suitable existing work is available.

External agents are temporary specialists, not permanent project dependencies.

Supervisor dynamically creates the workforce required by current task.

Agent count is workload-dependent.

Every agent receives explicit:
- ROLE
- MISSION
- INPUTS
- CHECKLIST
- FORBIDDEN ACTIONS
- REQUIRED EVIDENCE
- PASS CONDITIONS
- FAIL CONDITIONS
- ESCALATION CONDITIONS
- OUTPUT SCHEMA

Unchecked work cannot be marked PASS.

Missing evidence cannot be treated as successful validation.

External repositories remain isolated until all required gates pass.

core_v2 remains protected.

Production integration requires controlled promotion.

### Owner / Supervisor / Agent model

OWNER:
- defines objectives;
- makes strategic decisions;
- approves/rejects major changes.

SUPERVISOR:
- decomposes work;
- recruits/selects agents;
- assigns contracts;
- validates evidence;
- controls gates;
- coordinates integration.

SPECIALIST AGENTS:
- execute bounded tasks;
- report machine-verifiable evidence;
- never redefine project objectives.

### Economic principle

Every unnecessary manual operation has a cost.

Prefer:
- automation;
- parallel work;
- reusable open-source components;
- existing tested solutions;
- machine-readable evidence;
- compact decision reports.

Avoid:
- repetitive manual inspection;
- raw repository dumps into chat;
- repeated diagnostics;
- rebuilding existing functionality without justification;
- fixed agent architecture;
- unnecessary token consumption.

### Chat rule

Chat is a meeting room.

Chat must contain only:
- decisions;
- strategic evaluation;
- blockers;
- compact evidence;
- approval requests;
- milestone results.

Repository artifacts contain project memory.

Agents perform operational work outside chat.

This rule is mandatory for future AI_BRIDGE development.
