# Registro Test Risorse Esterne (Scouting)

Questo file documenta i test effettuati sui progetti trovati dagli scout (GitHub, HF, arXiv). Serve per non ripetere gli stessi test e per capire cosa adottare se cambiamo hardware.

## 2026-10-31: TradingAgents (TauricResearch)
- **Test**: Eseguito in sandbox con Python 3.11.
- **Esito**: 1396 test passati, 1 skipped. Installazione riuscita.
- **Verdetto**: **SCARTATO** come dipendenza. Richiede API a pagamento (OpenAI/Anthropic) e RAM elevata. **IDEE DA PRENDERE**: Separazione dei ruoli (Risk Manager vs Portfolio Manager) e meccanismo di "Reflection" post-trade.

## 2026-10-31: OpenBacktesting (lucidcog)
- **Test**: Clonato in sandbox.
- **Esito**: Richiede Python 3.12–3.14. Il nostro sistema ha Python 3.10/3.11.
- **Verdetto**: **SCARTATO** (per ora). Se in futuro aggiorniamo Python, è un candidato per il backtesting. **IDEE DA PRENDERE**: Esportazione dati per plotting e ottimizzazione parametri.

## 2026-10-31: EA31337-classes
- **Test**: Clonato in sandbox.
- **Esito**: È un framework MQL4/MQL5 (C++), non Python. Non testabile con pytest.
- **Verdetto**: **SCARTATO**. Il nostro EA (AI_BRIDGE_EA) è già funzionante e specifico per il nostro scopo.

## 2026-10-31: DeltaForge (QuantSingularity)
- **Test**: In corso (installazione dipendenze).
- **Esito**: Da definire.
