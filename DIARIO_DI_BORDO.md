# DIARIO DI BORDO — AI_Trading

## Stato: 19 nov 2026
Forward test: MT4 SweepEA attivo. XAUUSD.r M15. Lotto 0.01. Filtro news ON (5 date: NFP 6/11, 4/12; CPI 10/11, 10/12; FOMC 18/11). Pattern: sweep 0.30×ATR + EMA50 H1 + conferma 3 barre. TP 2R. SL 0.1×ATR oltre wick.

## Deciso
- Strategia: solo SELL/BUY su EMA50 H1. News window 30/30 (NFP/FOMC 30/60). No trailing (TP fisso 2R).
- Backtest: PF 1.17 (2022-25 OOS), PF 1.25 (2026 OOS). 410+120 trade. Edge reale.
- Lotto: 0.01 fisso (Quarter Kelly su conto 500€). 0.10 troppo rischioso (12 perdite consecutive possibili).
- Kilo: non usare per simulazioni. Solo task atomici. Fallito per model not found / server error.

## Cancellato
- Eikos-4B (3.6GB, Research, non integrato). Riscaricabile da HuggingFace se serve.
- Docker prune (769MB). Immagini non in uso (ai_bridge, postgres, redis, openhands).

## Aperto
- Forward test: 8-12 settimane o 30+ trade. Se PF>1.1 → live 500€, lotto 0.01.
- Se forward fallisce (expectancy<0 o DD>0.41%): tornare a design con dati reali.
- Inventario disco: /home/carlo/Progetti/AI_Trading/INVENTARIO_DISCO.md

## Memoria
- Io (assistente) non ho memoria tra chat. Questo file è la memoria.
- All'inizio di ogni nuova chat: incollare questo file. Io riparto da qui.
- Aggiornare a fine sessione (io scrivo, tu salvi).

## Sessione 2026-11-27

**Obiettivo**: Ripristinare il funzionamento del sistema di trading e testare l'integrazione orchestratore + EA MT4.

**Cosa è stato fatto (ordine cronologico)**:
1. **Diagnosi XAUUSD (SweepEA)**: scoperto che l'EA era "fermo" da giorni per un problema di init di MT4 (uninit reason 5). Ripartito manualmente alle 14:01.
2. **Fix EURUSD**: corretto mismatch unità SL/TP (orchestratore inviava prezzi assoluti, EA leggeva pips); disattivato bypass del trigger engine (ora usa solo punteggio composito); allineato `ea_params.json` (StopLoss=10, TakeProfit=20).
3. **Costruzione Simulatore MT4**: creati `sim_loader.py`, `sim_bridge.py`, `sim_runner.py` in `backtest_sim/` per testare l'orchestratore su dati storici M1/M15.
4. **Documentazione**: creato `docs/ECOSISTEMA_E_METODO.md`, aggiornati `APERTURA_CHAT.md` e `ISTRUZIONI_AGENTI.md` con riferimenti al report strategico e alla direttiva lingua.

**Stato attuale**:
- EURUSD: fix applicati, in attesa di test lunedì a mercato aperto.
- XAUUSD (SweepEA): ripartito, in attesa di segnali. Monitorare.
- Simulatore: funzionante (smoke test passato), ma genera 0 operazioni perché i context file sono neutri (Punteggio 0.0). Da migliorare per generare segnali.

**Prossimi passi**:
1. Risolvere il problema dei context file neutri nel simulatore (dare dati veri o disattivare filtri).
2. Testare il simulatore su EURUSD (2024-2025) e XAUUSD (2024-2025).
3. Aggiornare `RICERCA_ESITI.md` con l'esito dei test e degli strumenti valutati (mcp-mt5, EA31337, etc.).
