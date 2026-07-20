# AI_BRIDGE V2 — Project Rules

## Scopo

Questo documento definisce le regole decisionali del progetto.

Le decisioni contenute in questo file hanno priorità rispetto a qualsiasi suggerimento architetturale o tecnico.

---

# Filosofia

AI_BRIDGE V2 viene sviluppato in modo progressivo.

L'obiettivo NON è costruire immediatamente un Trading Operating System professionale completo.

L'obiettivo è costruire un sistema semplice, stabile e realmente utilizzabile.

Prima costruiamo una casa.

La utilizziamo.

Facciamo esperienza.

Solo dopo costruiremo il castello.

---

# Esistono due progetti

## 1. Progetto Primario

Il progetto principale deve essere:

- semplice;
- stabile;
- testabile;
- realmente utilizzabile;
- facilmente comprensibile.

Ogni modifica deve avere un'utilità immediata.

---

## 2. Progetto Clone

Il Clone è il laboratorio.

Qui verranno sperimentati:

- nuove architetture;
- AI avanzata;
- strategie innovative;
- refactoring importanti;
- sistemi adattivi;
- nuove tecnologie.

Solo ciò che dimostra un reale miglioramento verrà portato nel progetto principale.

---

# Regole operative

## Regola 1

La casa prima del castello.

---

## Regola 2

Ogni commit deve avere un solo obiettivo.

---

## Regola 3

Ogni commit deve poter essere spiegato con una sola frase.

---

## Regola 4

Ogni commit deve essere testato prima di essere salvato.

---

## Regola 5

Mai fare refactoring preventivi.

---

## Regola 6

Riutilizzare sempre il codice esistente prima di crearne di nuovo.

---

## Regola 7

Ogni Engine deve avere una sola responsabilità.

---

## Regola 8

Il sistema deve essere sempre funzionante.

Dopo ogni commit deve essere possibile eseguire:

python3 main_v2.py

senza errori.

---

## Regola 9

Ogni modifica deve risolvere un problema reale.

---

## Regola 10

Git racconta la storia del progetto.

Ogni commit rappresenta un piccolo passo avanti.

---

## Regola 11

Prima capire.

Poi programmare.

Mai il contrario.

---

## Regola 12

Prima di implementare una modifica chiedersi:

"Se oggi usassi AI_BRIDGE con denaro reale,
questa modifica mi aiuterebbe davvero?"

Se la risposta è NO,
la modifica appartiene probabilmente al progetto Clone.

---

# Metodo di sviluppo

Per ogni nuova funzionalità seguire sempre questa sequenza.

1. Analisi.
2. Obiettivo.
3. Soluzione più semplice.
4. Implementazione.
5. Test.
6. Commit.

Mai saltare un passaggio.

---

# Regola finale

Quando esistono due soluzioni corrette,
scegliere sempre quella:

- più semplice;
- più leggibile;
- più facile da mantenere;
- più facile da testare.

La complessità deve essere introdotta solo quando diventa realmente necessaria.

------------------------------------------------------------
EVOLUZIONI DIFFERITE (PROGETTO CLONE)
------------------------------------------------------------

Le seguenti funzionalità sono considerate valide ma NON devono
essere implementate nel Progetto Primario finché non esiste una
necessità reale.

Saranno sviluppate nel Progetto Clone.

DashboardEngine

Responsabilità futura:

- stato completo del sistema
- statistiche della pipeline
- memoria
- apprendimento
- monitoraggio
- dashboard web
- API REST
- monitoraggio remoto

Nel Progetto Primario è sufficiente un semplice report testuale.

Principio:

Quando una funzionalità può essere realizzata con una soluzione
semplice, la soluzione semplice ha sempre la priorità.

------------------------------------------------------------
PARCHEGGIO DELLE IDEE
------------------------------------------------------------

Le idee elencate qui NON devono essere implementate nel
Progetto Primario solo perché sono interessanti.

Rimangono disponibili come evoluzioni del Progetto Clone.

[ ] DashboardEngine

[ ] Web Dashboard

[ ] API REST

[ ] MT5 Adapter

[ ] Multi Broker Adapter

[ ] AI avanzata

[ ] Machine Learning avanzato

[ ] Auto Optimization

[ ] Distributed Runtime

[ ] Cloud Runtime

Ogni nuova idea futura va aggiunta qui prima di essere
presa in considerazione.
