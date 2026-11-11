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
- **Test**: Installazione backend (Python 3.11) in sandbox.
- **Esito**: 424 test passati. Licenza MIT. Supporta EA per MT4/MT5.
- **Verdetto**: **CANDIDATO**. Da approfondire per la logica di risk management e le strategie ML. Hardware compatibile.

## 2026-11-01: Freqtrade (freqtrade/freqtrade)
- **Test**: Non eseguito (richiede Python 3.12+). Licenza GPL-3.0.
- **Verdetto**: **SCARTATO**. Progetto per crypto exchange, non per MT4/Forex. Inutile per il nostro scopo.

## 2026-11-10: LumiBot (Lumiwealth/lumibot)
- **Test**: Analisi README (no installazione).
- **Esito**: Python 3.10+ (ok), no GPU (ok), ma **non supporta MT4/Wine**. Broker supportati: Alpaca, Interactive Brokers, Tradier, Schwab, CCXT, ecc. Richiede API keys a pagamento per AI agents.
- **Verdetto**: **SCARTATO**. Non compatibile con il nostro stack MT4/Wine. Utile solo se in futuro migriamo a un broker API.

## 2026-11-10: Qlib (microsoft/qlib)
- **Test**: Analisi README (no installazione).
- **Esito**: Python 3.8+ (ok), no GPU per core (ok), no API a pagamento (ok). **Ma non supporta Forex, non supporta MT4, non è un execution engine**. Focus su azioni Cina/USA, alpha mining, backtest.
- **Verdetto**: **SCARTATO** per MT4. **IDEE DA PRENDERE**: Alpha158/360 (feature engineering), LightGBM/XGBoost per classificazione segnali, cross-validation per serie temporali.

## 2026-11-10: Agent-Reach (Panniantong/Agent-Reach)
- **Test**: Analisi README (no installazione). Test in sandbox in corso.
- **Esito**: Python 3.10+ (ok), no GPU (ok), gratis (ok). Estrae da X, Reddit, YouTube, GitHub. Canali social "sperimentali" (anti-scraping aggressivo).
- **Verdetto**: **TESTARE**. Utile per sentiment da social (X/Reddit) su EUR/USD. Se instabile, passare a Scrapling.

## 2026-11-10: Agent-Reach (test superato)
- **Test**: `agent-reach reddit search EURUSD --limit 5` -> 5 risultati, 734ms, no anti-scraping.
- **Esito**: Funziona. Sentiment estratto: neutral-to-slightly-bearish.
- **Verdetto**: **ADOTTATO** per `social_scout.py`. Integrato nel sistema come segnale aggiuntivo.

## 2026-11-10: social_scout.py (Agent-Reach integrato)
- **Test**: Eseguito manualmente. Output: sentiment "positivo" da Reddit.
- **Esito**: Funziona. Cron ogni 30 minuti.
- **Verdetto**: **ADOTTATO**. Integrato come conferma in `get_ema_volume_signal()`.

## 2026-11-10: social_context come conferma (integrazione completata)
- **Test**: Riavvio orchestratore, log con `[SOCIAL]`.
- **Esito**: Funziona. Se il social contraddice il segnale, la size viene dimezzata.
- **Verdetto**: **ADOTTATO**. Filtro di rischio sociale attivo.
