# STATUTO DELL'AZIENDA DIGITALE AI_BRIDGE

## Principi Fondamentali
1. L'azienda opera in modo autonomo tramite agenti intelligenti.
2. Ogni decisione di trading è presa dall'AI, non da regole fisse.
3. La sicurezza del capitale è prioritaria: massimo 1 operazione aperta alla volta.
4. Le operazioni avvengono solo durante le sessioni di mercato selezionate.

## Regole Operative
- **Modifiche al codice**: sempre tramite sostituzione completa del file (svuota e incolla).
- **Backup**: prima di ogni modifica, eseguire `cp file.py _backups/file_backup.py`.
- **Documentazione**: il file `MANUALE_PROGETTO.md` deve essere aggiornato ad ogni modifica.
- **Nuovi agenti**: se un agente viene approvato, deve essere creato, avviato e documentato immediatamente.

## Gestione degli Orari
- L'azienda può operare nelle sessioni di Londra, New York, Tokyo o in tutte.
- La selezione avviene dalla dashboard, nella sezione Configura.
- L'orchestratore rispetta la scelta e non apre ordini fuori dagli orari selezionati.

## Gestione degli Errori
- Se un agente smette di lavorare (falso positivo), la Sentinella ferma tutto il sistema.
- Le strategie testate vengono salvate e quelle non redditizie vengono archiviate per non ripeterle.
