# APERTURA CHAT - Istruzioni per iniziare una nuova sessione

## Regola

Quando apri una nuova chat, fai questo:

1. Incolla il contenuto di CONTESTO.md
2. Incolla il contenuto di HANDOFF.md
3. Chiedi alla chat nuova di rispondere a 3 domande di verifica
4. Solo se risponde bene, inizia a lavorare

Per generare al volo il pacchetto completo (CONTESTO.md + HANDOFF.md),
esegui da terminale Linux:

    cat CONTESTO.md HANDOFF.md

E incolla l'output come primo messaggio della nuova chat, preceduto da:

    "Riprendiamo il progetto AI_Trading. Leggi tutto e rispondi alle 3
    domande di verifica. Poi aspetta istruzioni."

## 3 domande di verifica (la chat nuova deve rispondere a tutte)

1. Cosa e' O7c e perche' e' il prossimo passo?
2. Elenca i 5 segnali dell'orchestratore e i loro pesi.
3. Stato attuale di: orchestratore, MT4, dashboard?

Se la chat nuova risponde correttamente a tutte e 3, e' in pari.
Se sbaglia una o piu' domande, manca contesto: incolla di nuovo i file.

## Cosa NON incollare

- Non incollare STATO_SISTEMA.md (log automatico, rumore).
- Non incollare interi log (ai_workforce.log, supervisor.log): sono grandi.
- Non incollare git log: si puo' fare dopo, se serve.
- Non incollare i backup (.pre_*): non servono all'inizio.

## Cosa fare se la chat nuova NON risponde bene

1. Reincolla CONTESTO.md.
2. Poi HANDOFF.md.
3. Poi le 3 domande.
4. Ripeti finche' risponde bene.

Se dopo 2 tentativi non risponde bene, la chat nuova ha un problema:
chiudila e aprine un'altra. Non continuare con una chat che non ha
letto il contesto.

## Comando di check-stato (opzionale, dopo le 3 domande)

Da terminale Linux, per verificare che il sistema e' come lo abbiamo
lasciato:

    tmux ls | grep -E "ai_workforce|supervisor"
    systemctl --user is-active web-app
    tail -3 /home/carlo/AI_Trading/decision_log.jsonl
    cat /home/carlo/Scrivania/XM MT4/MQL4/Files/account.json

Atteso:
- ai_workforce e supervisor attive
- web-app active
- decision_log.jsonl cresce di 1 riga ogni ora (HOLD o BUY/SELL)
- account.json aggiornato

## Regola per la vecchia chat

Prima di chiudere la vecchia chat, assicurati che:
- CONTESTO.md sia aggiornato (data, sezione 4, sezione 7).
- HANDOFF.md sia aggiornato (diario della sessione).
- I file .pre_* siano stati creati (backup del turno precedente).

Se questi 3 punti sono veri, la nuova chat partira' senza perdere nulla.
