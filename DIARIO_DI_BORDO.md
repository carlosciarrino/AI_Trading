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
