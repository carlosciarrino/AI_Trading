# AI_BRIDGE_V2_ARCHITECTURAL_DESIGN.md

# AI_BRIDGE V2 — Visione e Progettazione Architetturale

Documento di riferimento principale per la progettazione strategica di AI_BRIDGE V2. Nessun codice, nessuna modifica ai file esistenti, nessuna implementazione proposta: questa è una guida di alto livello per le decisioni di sviluppo presenti e future.

**Relazione con `core_v2/ARCHITECTURE.md`**: quel documento è il riferimento tecnico dettagliato — interfacce pubbliche, ordine esatto delle chiamate, tabelle di dipendenza per singolo engine, gerarchie di eccezioni. Questo documento sta un livello sopra: risponde a "perché il sistema è progettato così" e "dove sta andando", non a "quale metodo chiama quale". Dove i due documenti toccano lo stesso argomento, `core_v2/ARCHITECTURE.md` è l'autorità sui dettagli tecnici; questo documento è l'autorità sull'intento e sulla direzione. Se un giorno i due entrassero in contraddizione su un dettaglio tecnico, vince `core_v2/ARCHITECTURE.md`; se entrassero in contraddizione su un principio o una priorità, vince questo documento, e `core_v2/ARCHITECTURE.md` va aggiornato di conseguenza.

---

## 1. Visione generale del sistema

AI_BRIDGE V2 è la ricostruzione di AI_Trading come Trading Operating System, non come script di trading. La differenza non è di scala ma di natura: uno script esegue una strategia; un sistema operativo di trading fornisce un'infrastruttura stabile — percezione, decisione, rischio, esecuzione, osservabilità, apprendimento — dentro cui strategie diverse possono nascere, essere valutate ed essere sostituite senza mai rimettere in discussione le fondamenta.

La spinta a costruire V2 non nasce da un'ambizione astratta, ma da un fallimento misurato e documentato: V1 (`AI_ARCHITECTURE_AUDIT.md`) è arrivato a contenere quattro architetture incompatibili e ventinove implementazioni per sei responsabilità, senza che nessuna delle quattro filiere fosse mai eseguibile end-to-end. La visione di V2 è la risposta diretta a quella diagnosi: **un sistema in cui l'esistenza di una seconda implementazione della stessa responsabilità è per definizione un errore di progettazione**, non una variante tollerabile.

AI_BRIDGE V2 deve poter, nel tempo:

- operare su più broker e più piattaforme (MT4/MT5, e potenzialmente altre) senza che il nucleo decisionale cambi;
- evolvere la propria logica di decisione — da euristica oggi a eventualmente basata su modelli appresi — senza toccare esecuzione o rischio;
- sopravvivere ai propri errori (recovery, kill switch, degrado controllato) invece di limitarsi a fallire;
- restare comprensibile da un solo sviluppatore (o da una singola IA collaboratrice) leggendo un numero finito di moduli con confini netti, non un albero di dipendenze da ricostruire per via empirica come è stato necessario fare con V1.

---

## 2. Principi architetturali

### 2.1 Modularità

Ogni responsabilità del sistema vive in esattamente un modulo. La modularità non è un valore estetico: è la condizione che rende possibile sostituire un componente (per esempio il Decision Engine euristico con uno basato su apprendimento automatico) senza una riscrittura a cascata. V1 aveva già una segmentazione concettuale ragionevole (rischio, eventi, esecuzione, stato come idee distinte) — il suo fallimento non è stato concettuale, è stato la mancata convergenza fisica: le stesse idee riscritte più volte invece di condivise. V2 impone che la convergenza fisica sia parte della definizione di "fatto", non un passo successivo facoltativo.

### 2.2 Indipendenza dei componenti

Ogni engine deve poter essere istanziato, testato ed eseguito con dipendenze finte, senza l'intero sistema in esecuzione. Questo non è solo un vantaggio di test: è ciò che rende possibile sviluppare AI_BRIDGE V2 in modo incrementale, un engine alla volta, dal basso verso l'alto della gerarchia di dipendenza, con ogni componente verificabile prima che il successivo venga scritto — l'esatto contrario del percorso che ha prodotto V1, dove interi moduli sono stati scritti senza mai verificare se si collegassero a qualcosa.

### 2.3 Separazione delle responsabilità

Percepire il mercato, decidere, valutare il rischio, eseguire: sono quattro atti distinti, con quattro proprietari distinti. Un Decision Engine che sa già se il Risk Engine approverebbe una decisione, o un Execution Engine che ricalcola il rischio prima di eseguire, non stanno "ottimizzando" — stanno reintroducendo l'accoppiamento implicito che in V1 ha reso impossibile capire, da un audit esterno, quale file facesse davvero cosa.

### 2.4 Scalabilità futura

Il sistema deve poter crescere in tre direzioni senza richiedere una riprogettazione:

- **Orizzontale**: più istanze (per simbolo, per broker) dello stesso Orchestrator, rese possibili dal fatto che nessun engine tranne Runtime Controller mantiene stato globale implicito.
- **Di trasporto**: nuovi modi di raggiungere un broker (file, socket, API REST) senza toccare la logica di decisione o di rischio, grazie al confine `BrokerAdapter` già stabilito in `execution_engine.py`.
- **Di intelligenza**: un Decision Engine più sofisticato, o un Learning Engine con tecniche di ottimizzazione più avanzate, senza che il resto del sistema debba saperlo.

---

## 3. Ruolo dei componenti (vista strategica)

Per il dettaglio di responsabilità, interfacce e dipendenze di ciascun modulo, `core_v2/ARCHITECTURE.md` resta l'autorità. A livello strategico, i diciassette moduli si raggruppano in tre strati di intento:

- **Strato infrastrutturale** (`bootstrap.py`, `runtime_controller.py`, `config.py`, `telemetry.py`, `constants.py`, `exceptions.py`, `utils.py`): non sa nulla di trading. Il suo unico compito è garantire che il sistema abbia un ambiente coerente in cui girare — se un giorno AI_BRIDGE V2 diventasse un sistema per un dominio diverso dal trading, questo strato resterebbe quasi invariato.
- **Strato di dominio operativo** (`market_engine.py`, `decision_engine.py`, `risk_engine.py`, `execution_engine.py`): il ciclo che trasforma percezione in azione. È lo strato che deve restare più stabile nel tempo: ogni cambiamento qui ha effetto diretto sul comportamento di trading.
- **Strato di governo del sistema** (`monitoring_engine.py`, `recovery_engine.py`, `memory_engine.py`, `learning_engine.py`, `event_engine.py`): osserva, ricorda, impara e protegge lo strato operativo, senza mai agire direttamente su di esso se non attraverso Runtime Controller.

`orchestrator.py` non appartiene a nessuno dei tre strati: li attraversa tutti, per costruzione, essendo l'unico modulo autorizzato a farlo.

---

## 4. Progettazione dell'Orchestrator

### 4.1 Cosa deve gestire

L'Orchestrator gestisce la **composizione** del sistema (quali engine esistono e come sono collegati) e il **tempo** del sistema (in che ordine e con quale cadenza le cose accadono). Nient'altro.

### 4.2 Cosa non deve gestire

L'Orchestrator non decide, non valuta rischio, non esegue, non ricorda, non impara. Se una futura modifica aggiungesse anche solo una condizione `if` con significato di dominio dentro l'Orchestrator (per esempio "non tradare se il simbolo è X"), quella logica appartiene a un altro engine ed è stata messa nel posto sbagliato — indipendentemente da quanto sia piccola.

### 4.3 Come coordina gli engine

Attraverso composizione esplicita all'avvio (ogni engine riceve le proprie dipendenze come parametri, mai le cerca da solo) e attraverso un ciclo a fasi ordinate a runtime, dettagliato in `core_v2/ARCHITECTURE.md` §4–5. La responsabilità strategica dell'Orchestrator è garantire che l'ordine delle fasi rispecchi sempre la sequenza logica del dominio (non si può valutare il rischio di una decisione che non esiste ancora), non l'implementazione tecnica di un singolo ciclo.

### 4.4 Come comunica con gli altri componenti

In due modi distinti, mai intercambiabili:

- **Chiamata diretta** per il percorso critico sincrono (percezione → decisione → rischio → esecuzione), dove l'ordine e la latenza contano.
- **Evento asincrono**, tramite Event Engine, per tutto ciò che è notifica di un accaduto (esito registrato, salute osservata, recovery attivato) e non richiede una risposta immediata nello stesso ciclo.

Questa distinzione è una decisione strategica, non un dettaglio implementativo: mescolare i due canali (per esempio, far dipendere l'esecuzione da un evento asincrono) introdurrebbe latenza e incertezza esattamente nel punto del sistema dove servono meno.

---

## 5. Flusso operativo (vista narrativa)

Il dettaglio fase-per-fase è in `core_v2/ARCHITECTURE.md` §4. A livello narrativo:

1. **Avvio**: `bootstrap.py` prepara l'ambiente (Python, directory, log, configurazione) senza sapere nulla del dominio di trading.
2. **Inizializzazione**: l'Orchestrator compone il sistema, iniettando in ogni engine solo le dipendenze che gli servono davvero.
3. **Ciclo operativo**: il sistema respira — percepisce, decide, valuta, eventualmente agisce — a intervalli regolari, sempre nello stesso ordine.
4. **Gestione delle decisioni**: ogni decisione candidata è sempre sottoposta ad approvazione di rischio prima di poter diventare un'azione; non esiste un percorso che la aggiri.
5. **Esecuzione**: solo decisioni approvate raggiungono il confine con il mondo esterno (broker), e sempre attraverso un adapter sostituibile, mai attraverso una chiamata diretta e specifica di un broker.
6. **Monitoraggio**: ogni esito, positivo o negativo, alimenta una vista di salute aggregata — il sistema deve sapere come sta, non solo eseguire.
7. **Recovery**: quando la salute osservata peggiora oltre soglia, il sistema si protegge da solo, ma non si "riabilita" da solo: l'uscita da una protezione grave richiede intervento esplicito, per progettazione, non per limite tecnico.
8. **Memorizzazione**: ogni decisione e il suo esito diventano un pattern storicizzato, passivo, disponibile per essere interrogato ma mai interpretato dal modulo che lo conserva.
9. **Apprendimento**: periodicamente, non a ogni ciclo, il sistema rivede i propri parametri di decisione alla luce di ciò che ha imparato — mai in modo da poter toccare l'esecuzione direttamente.

---

## 6. Diagrammi ASCII

### 6.1 I tre strati, vista strategica

```
┌───────────────────────────────────────────────────────────┐
│                  STRATO DI GOVERNO DEL SISTEMA              │
│   Monitoring · Recovery · Memory · Learning · Event Engine   │
└───────────────────────────────────────────────────────────┘
                              ▲  osserva / protegge
                              │
┌───────────────────────────────────────────────────────────┐
│                 STRATO DI DOMINIO OPERATIVO                  │
│     Market → Decision → Risk → Execution Engine               │
└───────────────────────────────────────────────────────────┘
                              ▲  opera dentro un ambiente preparato da
                              │
┌───────────────────────────────────────────────────────────┐
│                  STRATO INFRASTRUTTURALE                     │
│  Bootstrap · Runtime Controller · Config · Telemetry ·         │
│  Constants · Exceptions · Utils                                │
└───────────────────────────────────────────────────────────┘

                    (Orchestrator attraversa tutti e tre)
```

### 6.2 Roadmap evolutiva, vista a fasi

```
Fase 0 (oggi)        Fase 1                Fase 2                 Fase 3
─────────────       ─────────────         ─────────────          ─────────────
Bootstrap solido     Engine di dominio      Broker reale           Decisione
+ infrastruttura  →  operativo completo  →  (MT4/MT5 concreto)  →  adattiva
                     su dati simulati        + persistenza          (apprendimento
                                              esterna                 automatico)
```

---

## 7. Regole sulle dipendenze (principi, non tabella)

Il dettaglio completo (chi può dipendere da chi) è in `core_v2/ARCHITECTURE.md` §7–8. I principi che generano quella tabella, e che devono guidare ogni futura eccezione o estensione:

- **Le dipendenze scorrono in una sola direzione**, dallo strato infrastrutturale verso l'Orchestrator, mai al contrario.
- **Nessun modulo diverso dall'Orchestrator conosce più di tre o quattro collaboratori diretti.** Un numero più alto è il sintomo, non la causa, di un modulo che ha accumulato troppe responsabilità.
- **Le dipendenze evitabili vanno evitate anche quando sarebbero comode.** Il caso più concreto: Execution Engine potrebbe, in teoria, chiamare direttamente Decision Engine per "sapere di più" sul contesto di una richiesta — non lo fa, perché la comodità a breve termine costerebbe l'indipendenza che rende il sistema testabile e sostituibile a lungo termine.
- **L'accoppiamento implicito (via file condivisi, variabili globali, convenzioni non dichiarate) è vietato quanto quello esplicito.** V1 ne è la prova: `self_healing_engine.py` e `failure_analysis_engine.py` non si importavano a vicenda, ma erano comunque accoppiati tramite un file JSON condiviso — un accoppiamento invisibile a qualunque analisi del solo grafo di import.

---

## 8. Gestione degli eventi

Event Engine esiste per una ragione strategica precisa: disaccoppiare **cosa succede** da **chi deve saperlo**. Senza un canale di eventi, ogni nuovo consumatore di un'informazione (un futuro modulo di alerting, una dashboard, un secondo Learning Engine sperimentale) richiederebbe di modificare il modulo produttore per aggiungere una nuova chiamata diretta. Con un canale di eventi, il produttore pubblica una sola volta e non deve mai sapere quanti o quali consumatori esistono oggi o esisteranno domani.

La resilienza del canale (retry, dead-letter) non è un dettaglio tecnico: è la garanzia strategica che un consumatore temporaneamente non disponibile non faccia perdere un'informazione di sistema, in un dominio — il trading — dove "non sapevo che l'ordine fosse fallito" è un rischio operativo, non solo un bug.

---

## 9. Gestione degli errori e strategie di recovery

La filosofia di V2 su questo punto è esplicita: **un sistema di trading che fallisce silenziosamente è peggiore di uno che si ferma**. Ogni errore deve avere un destino chiaro: o viene tradotto in un risultato esplicito che il chiamante gestisce (validazione), o innesca una protezione strutturale (recovery, safe mode), o interrompe l'avvio (bootstrap). Non esiste una quarta categoria — "l'errore che viene ignorato" — per progettazione.

La strategia di recovery è deliberatamente asimmetrica: entrare in protezione è automatico, uscirne da una protezione grave non lo è. Questa asimmetria è una decisione architetturale, non una limitazione: un sistema che si è protetto da un pattern di errori non ha, da solo, l'informazione per sapere se quel pattern è davvero cessato o si è solo interrotto temporaneamente.

---

## 10. Telemetria e osservabilità

Un Trading Operating System che non può rispondere, in ogni momento, alla domanda "come sto andando?" non è pronto per gestire capitale reale, indipendentemente da quanto sia corretta la sua logica di trading. Monitoring Engine e Telemetry (logging) coprono due bisogni diversi e complementari: il primo risponde a "qual è lo stato aggregato del sistema ora", il secondo risponde a "cosa è successo esattamente, in ordine, quando è successo". Nessuno dei due sostituisce l'altro; V2 li mantiene entrambi per design, non per ridondanza.

---

## 11. Evoluzione futura

- **Integrazione broker/MT4**: il confine `BrokerAdapter` è già pronto a ricevere un'implementazione concreta (file-based, come in V1, o socket-based). La decisione strategica qui non è tecnica ma di sequenza: l'adapter reale va introdotto solo dopo che l'intero ciclo operativo è stato validato su dati simulati, mai prima.
- **Persistenza dati**: Memory Engine oggi può restare in-process; la migrazione verso una persistenza esterna (file strutturati, database) è un cambiamento isolato a quel solo modulo, per costruzione — nessun altro engine deve accorgersene.
- **Sistemi adattivi**: Learning Engine è il punto di innesto naturale per tecniche più sofisticate di ottimizzazione dei parametri, ma la decisione strategica è mantenere sempre una distinzione netta tra "i parametri cambiano" (Learning) e "la struttura della decisione cambia" (una revisione di Decision Engine stesso, evento raro e deliberato, non un effetto collaterale dell'apprendimento continuo).
- **Miglioramento dell'intelligenza decisionale**: quando Decision Engine evolvesse verso un modello appreso, il contratto pubblico (`decide(snapshot) -> DecisionCandidate | None`) non deve cambiare — è la condizione che rende questa evoluzione un'estensione, non una riscrittura.

---

## 12. Rischi architetturali da evitare

- **La tentazione della scorciatoia "per ora".** Ogni violazione del grafo di dipendenza inizia come un'eccezione temporanea giustificata da una scadenza. V1 non è diventato quattro architetture incompatibili in un giorno: ci è arrivato una scorciatoia alla volta.
- **La proliferazione silenziosa di varianti.** Se un domani qualcuno propone "un secondo Risk Engine più semplice per i test", la risposta corretta è un `RiskEngine` configurabile o un test double, mai un secondo file con una responsabilità che si sovrappone al primo.
- **Documentazione che si allontana dal codice.** Questo stesso documento rischia di invecchiare male se non viene aggiornato quando le decisioni strategiche cambiano — va trattato come parte del sistema, non come nota a margine.
- **Ottimizzazione prematura della comunicazione tra engine.** Sostituire chiamate dirette con eventi asincroni ovunque, "per uniformità", romperebbe la garanzia di sincronicità del percorso critico (§4.4) senza un beneficio reale.
- **Broker/trasporto reale introdotto prima che il ciclo logico sia validato.** È il rischio operativo più grave in assoluto: collegare un sistema non ancora validato a un conto reale, anche demo, prima che l'intero ciclo mercato→decisione→rischio→esecuzione sia stato esercitato a fondo su dati simulati.

---

## 13. Raccomandazioni finali per lo sviluppo

1. Costruire dal basso verso l'alto della gerarchia di dipendenza (Memory ed Event Engine per primi, Orchestrator per ultimo), mai il contrario: ogni modulo superiore deve poter essere validato contro dipendenze reali già esistenti, non contro finzioni che rimarranno tali.
2. Trattare `core_v2/ARCHITECTURE.md` e questo documento come una coppia inseparabile nella revisione di ogni nuova funzionalità: una modifica che cambia un principio qui deve riflettersi là, e viceversa.
3. Non introdurre l'integrazione con un broker reale, nemmeno in modalità demo, prima che l'intero ciclo operativo sia stato eseguito e osservato a lungo su dati simulati.
4. Misurare l'aderenza architetturale con lo stesso rigore riservato in precedenza all'audit di V1: uno strumento come `tools/audit/import_graph.py`, già esistente per V1, dovrebbe avere un equivalente per `core_v2/` non appena il numero di engine implementati lo giustifica.
5. Ogni volta che un nuovo requisito sembra richiedere di violare una regola di dipendenza di questo documento, la priorità è rivedere il requisito o il documento esplicitamente — mai violare la regola in silenzio "solo per questa volta".
