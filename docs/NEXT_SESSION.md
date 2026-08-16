# AI_BRIDGE V2 — NEXT SESSION HANDOFF

Versione: 2.0
Data: 2026-08-14
Repository: ~/AI_Trading
Branch: feature/fast-track
HEAD: aa29a6f

==================================================
REGOLA ASSOLUTA
==================================================

Repository = unica fonte di verità.

CAVEMAN ULTRA:
- output diretto;
- niente spiegazioni inutili;
- niente richieste ripetitive;
- niente controlli già conclusi;
- ogni risposta deve produrre avanzamento concreto;
- quando utente scrive "approvato" o "procediamo": eseguire immediatamente prossimo passo;
- mai dire "attendo", "procederò", "nel prossimo messaggio";
- quando si modifica un file: comando terminale completo + contenuto completo;
- evitare apertura manuale di file quando automazione possibile;
- comandi combinati quando sicuri;
- file grandi: generazione automatica tramite heredoc/script, non copia manuale a blocchi;
- non inventare API;
- niente refactoring fuori milestone;
- repository reale prevale su memoria.

==================================================
OBIETTIVO PROGETTO
==================================================

AI_BRIDGE V2 = Trading Operating System modulare integrato con MT4.

Architettura:
- Python standard library;
- engine modulari;
- orchestrazione centrale;
- pipeline condivisa tramite PipelineContext;
- diagnostics;
- monitoring;
- memory;
- learning;
- recovery;
- execution;
- runtime control.

==================================================
STATO REALE AL PASSAGGIO
==================================================

Sistema stabile.

Bootstrap funzionante.

Compilazione core_v2 verificata.

Diagnostics CLI funzionante.

Monitoring Evolution implementata.

Developer Snapshot automation implementata.

tools/dev.py dispone di:
- verify
- finish

Ultimo commit:

aa29a6f Restore verify command

Commit precedenti rilevanti:

5a11083 Add developer snapshot automation
ff3e71b Add development automation helper
4d5d3eb Add development automation helper
0f78424 Evolve monitoring engine with runtime health evaluation
a8cc611 Update project index for milestone M17
f100fa4 Complete milestone M16 system diagnostics
1882f95 Add centralized system diagnostics
83e6b39 Update handoff prompt with continuity rule

==================================================
MILESTONE
==================================================

M16 — System Diagnostics
COMPLETATA.

M17 — Monitoring Evolution
IMPLEMENTATA.

M16.5 — Continuity Automation
IN CORSO / CONSOLIDAMENTO.

Scopo M16.5:

Eliminare necessità di leggere manualmente repository a ogni nuova chat.

==================================================
M16.5 — IMPLEMENTATO
==================================================

Creato:

tools/build_developer_snapshot.py

Genera:

docs/DEVELOPER_SNAPSHOT.md

Comando:

python3 tools/build_developer_snapshot.py

Snapshot contiene automaticamente:
- file core_v2;
- classi pubbliche;
- dataclass;
- funzioni pubbliche;
- metodi pubblici;
- firme;
- import;
- dipendenze core_v2;
- branch;
- ultimo commit;
- milestone rilevata.

Creato/ripristinato comando:

python3 tools/dev.py verify

verify esegue:
- py_compile core_v2;
- main_v2.py;
- diagnostics_v2.py --report;
- git diff --stat;
- git status.

finish esegue:
- verifica;
- staging;
- commit.

Comando usato:

python3 tools/dev.py finish "Restore verify command"

Risultato:

aa29a6f Restore verify command

==================================================
ULTIMO TEST CONFERMATO
==================================================

Comando:

python3 tools/dev.py finish "Restore verify command"

Risultati:

py_compile OK.

main_v2.py OK.

Bootstrap:

AI_BRIDGE V2 bootstrap completed successfully.

diagnostics_v2.py --report OK.

Runtime............ RUNNING
Cycles............. 0
Memory Records..... 0
Last Decision...... NONE

No pipeline executed.

Learning:
Samples 0
BUY 0
SELL 0
HOLD 0

Execution:
Approved 0
Rejected 0
Executed 0
Not Executed 0

Nessun errore.

==================================================
MONITORING EVOLUTION
==================================================

M17 ha modificato:

core_v2/monitoring_engine.py
core_v2/system_builder.py

Commit:

0f78424 Evolve monitoring engine with runtime health evaluation

MonitoringEngine API pubblica consolidata:

evaluate()
last_report()
reset()

SystemDiagnostics API:

snapshot()
runtime_state()
memory_snapshot()
last_pipeline_record()
recent_pipeline_records()
orchestrator_statistics()

==================================================
ARCHITETTURA CORE
==================================================

core_v2 contiene:

application.py
bootstrap.py
config.py
constants.py
decision_engine.py
event_engine.py
exceptions.py
execution_engine.py
learning_engine.py
market_engine.py
memory_engine.py
monitoring_engine.py
orchestrator.py
pipeline_context.py
recovery_engine.py
risk_engine.py
runtime_controller.py
system_builder.py
system_diagnostics.py
system_inspector.py
telemetry.py
utils.py

Componenti principali:

MarketEngine
DecisionEngine
RiskEngine
ExecutionEngine
MemoryEngine
LearningEngine
MonitoringEngine
RecoveryEngine
EventEngine
Orchestrator
RuntimeController

AIComponents contiene:

runtime
orchestrator
market
decision
risk
execution
monitoring
recovery
memory
learning
events

==================================================
SYSTEM BUILDER
==================================================

core_v2/system_builder.py

Responsabilità:
- creare engine;
- collegare dipendenze;
- costruire AIComponents;
- collegare Orchestrator.

Compatibility layer callbacks ancora presente.

Orchestrator riceve AIComponents tramite:

attach_components()

==================================================
MEMORY
==================================================

MemoryRecord
MemorySnapshot
MemoryEngine

API rilevante:

store()
last_record()
snapshot()
clear()
size
records()
recent()

Memory integrata nel pipeline orchestrator.

==================================================
DIAGNOSTICS
==================================================

SystemInspector produce SystemSnapshot.

Snapshot include:
- runtime_state;
- cycle_count;
- memory_records.

SystemDiagnostics centralizza accesso diagnostico senza presentation logic.

diagnostics_v2.py è CLI presentation layer.

Uso corretto:

python3 diagnostics_v2.py --report

NON:

python3 diagnostics_v2.py report

==================================================
TOOLS
==================================================

tools/dev.py

Comandi disponibili:

python3 tools/dev.py verify

python3 tools/dev.py finish "Commit message"

tools/build_developer_snapshot.py

Comando:

python3 tools/build_developer_snapshot.py

==================================================
PROCEDURA NUOVE CHAT
==================================================

NON chiedere subito cat di file singoli.

Prima leggere:

docs/PROJECT_INDEX.md
docs/PROJECT_MANIFEST.md
docs/NEXT_SESSION.md
docs/DEVELOPMENT_PROTOCOL.md
docs/PROJECT_PROGRESS.md
docs/DEVELOPER_SNAPSHOT.md

Poi usare Developer Snapshot come contesto tecnico.

Repository = fonte definitiva.

Se snapshot aggiornato:
NON richiedere nuovamente cat dei file già rappresentati.

Richiedere file aggiuntivi solo se:
- reale errore;
- snapshot insufficiente;
- file nuovo non indicizzato;
- impossibilità concreta di determinare API/dependency.

==================================================
AUTOMAZIONE FILE
==================================================

NON far inserire manualmente grandi file in nano se evitabile.

Preferire:

cat > path/to/file <<'PY'
...
PY

poi:

python3 -m py_compile ...

poi test.

Per file molto grandi:
- heredoc;
- script Python;
- generazione automatica;
- divisione solo se tecnicamente necessaria.

==================================================
UNTRACKED NOTI
==================================================

Alla verifica precedente risultavano non tracciati:

"AI_BRIDGE V2 — PROMPT DI CONTINUITÀ"
"AI_BRIDGE V2 — Prompt di Continuità.pdf"
AI_BRIDGE_V2_CONTINUITY_PROMPT.md

NON aggiungerli automaticamente.

Sono documenti esterni/di continuità e non devono essere inclusi nei commit senza decisione esplicita.

==================================================
PROSSIMO PASSO
==================================================

M16.5 deve essere completata consolidando automazione continuità.

Priorità:

1. Verificare che tools/dev.py verify sia realmente disponibile.
2. Verificare snapshot generation.
3. Integrare rigenerazione Developer Snapshot nella procedura finish.
4. Evitare che fine milestone richieda comando manuale separato.
5. Aggiornare documentazione milestone.
6. Eseguire verify.
7. Commit significativo.
8. Aggiornare NEXT_SESSION.md e DEVELOPER_SNAPSHOT.md.

Obiettivo finale:

Un solo comando di fine milestone deve:
- verificare progetto;
- rigenerare DEVELOPER_SNAPSHOT.md;
- aggiornare stato;
- preparare commit.

==================================================
VINCOLI
==================================================

NON:
- ricominciare M17;
- rifare System Diagnostics;
- rifare Monitoring Evolution;
- rifare verifiche già riuscite;
- chiedere file già presenti nello snapshot;
- fare refactoring non richiesto;
- inventare nuove API;
- aggiungere uncommitted continuity files automaticamente.

SÌ:
- continuare M16.5;
- automatizzare;
- ridurre comandi;
- ridurre copia manuale;
- mantenere repository coerente;
- produrre milestone/commit concreti.

==================================================
PRIMA AZIONE NUOVA CHAT
==================================================

Leggere questo documento + DEVELOPER_SNAPSHOT.md.

Poi eseguire direttamente prossimo passo M16.5.

Non chiedere all'utente di ricostruire il contesto.

==================================================
FINE HANDOFF
==================================================
