# AI_BRIDGE — AUTONOMOUS AGENT MISSION

## Obiettivo
Trasformare AI_BRIDGE in sistema sviluppabile da agenti, riducendo intervento umano a:
- approvazione decisioni ad alto rischio;
- supervisione;
- definizione obiettivi.

## Regola fondamentale
Repository = source of truth.
Non chiedere all'operatore di copiare file manualmente.
Non chiedere file già presenti nel repository.
Non ripetere verifiche già documentate.

## Ciclo autonomo
1. Leggere docs/DEVELOPER_SNAPSHOT.md.
2. Leggere docs/PROJECT_PROGRESS.md.
3. Identificare milestone corrente.
4. Analizzare solo file necessari.
5. Formulare piano minimo.
6. Modificare repository direttamente.
7. Eseguire compile/test/diagnostics.
8. Correggere errori.
9. Rigenerare docs/DEVELOPER_SNAPSHOT.md.
10. Aggiornare documentazione milestone.
11. Creare commit Git significativo.
12. Generare report operativo.
13. Proporre automaticamente prossimo task.

## Sicurezza
Mai eseguire automaticamente:
- sudo;
- installazioni sistema;
- credenziali/segreti;
- operazioni distruttive;
- deploy produzione;
- operazioni finanziarie reali.

Security findings = classificare prima di agire.

## Priorità
1. Automazione.
2. Riproducibilità.
3. Test.
4. Osservabilità.
5. Modularità.
6. Riduzione intervento umano.

## Risultato atteso
Ogni sessione agente deve produrre almeno:
- una modifica concreta;
- verifica;
- commit;
- stato aggiornato;
- prossimo task macchina-eseguibile.

## Anti-copy/paste
Terminale deve diventare interfaccia di bootstrap, non interfaccia operativa.
Agenti devono lavorare su repository direttamente.
Operatore deve ricevere solo:
- stato;
- decisioni richieste;
- errori bloccanti;
- risultati;
- prossimo obiettivo.

## Evoluzione
Costruire progressivamente:
AGENT → TASK QUEUE → EXECUTOR → TESTER → REVIEWER → COMMITTER → REPORTER → SUPERVISOR.

Fine missione solo quando ciclo autonomo è verificabile.
