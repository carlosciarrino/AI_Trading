# Skill: Test Repository in Sandbox

## Quando usarla
Quando l'utente o uno scout trova un repository GitHub e vuole testare se è utile per il progetto.

## Cosa fa
Clona il repository in una cartella temporanea e tenta di installarlo. Non tocca mai il sistema di produzione.

## Passi (esegui in ordine, un comando alla volta)
1. Chiedi all'utente l'URL del repository.
2. Crea una cartella di test isolata:
   `mkdir -p /tmp/ai_trading_test && cd /tmp/ai_trading_test`
3. Clona il repo:
   `git clone <URL> repo_test`
4. Entra nella cartella:
   `cd repo_test`
5. Leggi il README per capire come si installa (es. `cat README.md | head -50`).
6. Se c'è un file `requirements.txt`, installa le dipendenze in un venv temporaneo:
   `python3 -m venv venv_test && source venv_test/bin/activate && pip install -r requirements.txt`
7. Esegui un test base (es. `python3 -m pytest` se ci sono test, o `python3 <file_principale>.py`).
8. Riporta l'esito all'utente.

## Cosa NON fare
- Non installare nulla nel venv di produzione (`/home/carlo/AI_Trading_Agents/venv`).
- Non clonare nella root di `AI_Trading`.
- Non eseguire comandi di installazione globale (`sudo apt install`).

## Pulizia (obbligatoria)
Alla fine del test, cancella la cartella temporanea:
`rm -rf /tmp/ai_trading_test`
