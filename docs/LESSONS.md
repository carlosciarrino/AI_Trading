# Lezioni Apprese (Post-Mortem)

Questo file raccoglie gli errori che ci sono costati tempo, denaro o opportunità. Ogni lezione è scritta in modo da non essere ripetuta.

## 2026-11-10: L'onda perduta (100 pip)
- **Cosa è successo**: Il mercato ha fatto un movimento di 100 pip in poche ore. Il sistema non ha aperto nessuna operazione.
- **Causa**: `trigger_engine.py` usava una history di 20 valori (20 minuti) e campionava ogni 60 secondi. La media del volume era "sporcata" da valori vecchi. Quando il volume è esploso, la media era ancora alta, e il sistema non ha visto lo spike.
- **Lezione**: La memoria del volume deve essere breve (5 minuti). Il campionamento deve essere frequente (15 secondi). Il surfista guarda l'onda che arriva, non quella di ieri.
- **Fix applicato**: `history[-5:]` e `time.sleep(15)` in `trigger_engine.py`. Commit `8a70678`.
- **Come evitarlo in futuro**: Testare sempre i parametri con dati live, non solo con backtest. La simulazione non cattura il ritardo del tempo reale.
