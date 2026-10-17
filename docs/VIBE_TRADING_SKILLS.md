# VIBE-TRADING: CATALOGO SKILL

Ultimo aggiornamento: 2026-10-17 21:00
Fonte: /home/carlo/Progetti/Research/Vibe-Trading/agent/src/skills/

Progetto: HKUDS/Vibe-Trading (Università di Hong Kong, Data Science Lab)
Licenza: MIT
Installazione: pip install vibe-trading-ai
Versione: v0.1.16+ (in sviluppo attivo)
Skill totali: 90

Legenda:
- USARE = utile per il nostro progetto AI_Trading ora
- FUTURO = utile quando l'azienda cresce
- NON PERTINENTE = specifico per A股, crypto, opzioni, ecc.

## 1. SKILL UTILI ORA (6)

| # | Skill | Cosa fa | Azione |
|---|---|---|---|
| 1 | `sentiment-analysis` | Sentiment da news/social (più strutturato del nostro) | Adattare |
| 2 | `technical-basic` | Indicatori (RSI, MACD, SMA, EMA) | Adattare |
| 3 | `volatility` | Volatilità, ATR, Bollinger | Adattare per P034 |
| 4 | `risk-analysis` | Risk management (position sizing, drawdown) | Adattare per P034 |
| 5 | `shadow-account` | Analisi bias del nostro storico (disposition effect) | Adattare |
| 6 | `trade-journal` | Diario di trading strutturato | Adattare |

## 2. SKILL UTILI IN FUTURO (20)

| # | Skill | Cosa fa |
|---|---|---|
| 7 | `alpha-zoo` | Libreria di alpha (fattori) |
| 8 | `asset-allocation` | Allocazione portafoglio |
| 9 | `backtest-diagnose` | Diagnosi backtest |
| 10 | `behavioral-finance` | Finanza comportamentale (bias) |
| 11 | `correlation-analysis` | Correlazioni tra asset |
| 12 | `correlation-regime` | Regimi di correlazione |
| 13 | `cross-market-strategy` | Strategie cross-market |
| 14 | `dividend-analysis` | Analisi dividendi |
| 15 | `earnings-forecast` | Previsione utili |
| 16 | `earnings-revision` | Revisione stime utili |
| 17 | `event-driven` | Strategie event-driven |
| 18 | `execution-model` | Modello di esecuzione |
| 19 | `factor-research` | Ricerca fattori |
| 20 | `fundamental-filter` | Filtro fondamentale |
| 21 | `global-macro` | Macro globale |
| 22 | `hedging-strategy` | Strategie di hedging |
| 23 | `macro-analysis` | Analisi macro (FRED) |
| 24 | `market-microstructure` | Microstruttura di mercato |
| 25 | `ml-strategy` | Strategie ML |
| 26 | `multi-factor` | Multi-fattore |
| 27 | `pair-trading` | Pair trading |
| 28 | `performance-attribution` | Attribuzione performance |
| 29 | `quant-statistics` | Statistica quantitativa |
| 30 | `regulatory-knowledge` | Conoscenza normativa |
| 31 | `research-discipline` | Disciplina di ricerca |
| 32 | `research-goal` | Obiettivi di ricerca |
| 33 | `seasonal` | Stagionalità |
| 34 | `sector-rotation` | Rotazione settoriale |
| 35 | `strategy-dev-manager` | Gestione sviluppo strategie |
| 36 | `strategy-discovery` | Scoperta strategie |
| 37 | `strategy-generate` | Generazione strategie |
| 38 | `thesis-tracker` | Tracking tesi di investimento |
| 39 | `valuation-model` | Modello di valutazione |
| 40 | `volatility` | Volatilità (già in USARE) |
| 41 | `report-generate` | Generazione report |
| 42 | `web-reader` | Lettura web |
| 43 | `doc-reader` | Lettura documenti |

## 3. SKILL SPECIFICHE A-SHARE (CINA) — NON PERTINENTI ORA (18)

| # | Skill | Cosa fa |
|---|---|---|
| 44 | `adr-hshare` | ADR e H-share |
| 45 | `akshare` | Dati A股 via akshare |
| 46 | `ashare-pre-st-filter` | Filtro pre-ST A股 |
| 47 | `chanlun` | Teoria Chan (缠论) |
| 48 | `convertible-bond` | Obbligazioni convertibili |
| 49 | `credit-analysis` | Analisi credito |
| 50 | `eastmoney` | Dati Eastmoney |
| 51 | `hk-connect-flow` | Flussi Stock Connect HK |
| 52 | `mootdx` | Dati Tongdaxin |
| 53 | `qveris` | Piattaforma Qveris |
| 54 | `tushare` | Dati Tushare |
| 55 | `us-etf-flow` | Flussi ETF US |
| 56 | `vnpy-export` | Export VNPy |
| 57 | `edgar-sec-filings` | Filing SEC EDGAR |
| 58 | `sec-edgar` | SEC EDGAR |
| 59 | `financial-statement` | Bilanci |
| 60 | `management-deep-dive` | Deep dive management |
| 61 | `deep-company-series` | Serie aziende deep |

## 4. SKILL CRYPTO — NON PERTINENTI ORA (12)

| # | Skill | Cosa fa |
|---|---|---|
| 62 | `ccxt` | Exchange crypto |
| 63 | `crypto-derivatives` | Derivati crypto |
| 64 | `defi-yield` | Yield DeFi |
| 65 | `liquidation-heatmap` | Heatmap liquidazioni |
| 66 | `okx-market` | Mercato OKX |
| 67 | `onchain-analysis` | Analisi on-chain |
| 68 | `perp-funding-basis` | Funding perpetual |
| 69 | `stablecoin-flow` | Flussi stablecoin |
| 70 | `token-unlock-treasury` | Token unlock |
| 71 | `commodity-analysis` | Materie prime |
| 72 | `geopolitical-risk` | Rischio geopolitico |
| 73 | `options-advanced` | Opzioni avanzate |

## 5. SKILL OPZIONI — NON PERTINENTI ORA (3)

| # | Skill | Cosa fa |
|---|---|---|
| 74 | `options-payoff` | Payoff opzioni |
| 75 | `options-strategy` | Strategie opzioni |
| 76 | `options-advanced` | Opzioni avanzate |

## 6. SKILL ANALISI TECNICA — NON PERTINENTI ORA (8)

| # | Skill | Cosa fa |
|---|---|---|
| 77 | `candlestick` | Pattern candele |
| 78 | `elliott-wave` | Onde di Elliott |
| 79 | `harmonic` | Pattern armonici |
| 80 | `ichimoku` | Ichimoku |
| 81 | `pine-script` | Pine Script |
| 82 | `smc` | Smart Money Concepts |
| 83 | `technical-basic` | Indicatori base (già in USARE) |
| 84 | `minute-analysis` | Analisi minuto |

## 7. ALTRE (6)

| # | Skill | Cosa fa |
|---|---|---|
| 85 | `data-routing` | Routing dati |
| 86 | `investor-lenses` | Lenti investitore (multi-prospettiva) |
| 87 | `private-company-research` | Ricerca aziende private |
| 88 | `fund-analysis` | Analisi fondi |
| 89 | `etf-analysis` | Analisi ETF |
| 90 | `yfinance` | Dati yfinance |

---

## 8. PIANO DI ADATTAMENTO

### Fase 1 (ora, P041-P046)
1. Leggere codice di `sentiment-analysis` → confrontare con `news_agent`/`social_agent`.
2. Leggere codice di `technical-basic` → aggiungere indicatori all'orchestratore.
3. Leggere codice di `volatility` → adattare per position sizing.
4. Leggere codice di `risk-analysis` → adattare per P034.
5. Leggere codice di `shadow-account` → analisi bias.
6. Leggere codice di `trade-journal` → arricchire `trading_memory.md`.

### Fase 2 (futuro)
- `alpha-zoo`, `factor-research`, `multi-factor` per strategie.
- `macro-analysis` per FRED.
- `thesis-tracker` per tracking tesi.

### Fase 3 (quando serve)
- Skill A股, crypto, opzioni: solo se espandiamo.

## 9. COME USARE QUESTO CATALOGO

- **Prima di implementare una nuova feature**: cercare qui se Vibe-Trading ha una skill equivalente. Se sì, leggere il codice e adattarlo invece di scrivere da zero.
- **Quando l'azienda cresce**: rivedere le skill "FUTURO" e capire quali attivare.
- **Non copiare tutto**: ogni skill ha 1-5 file Python. Prendere solo quello che serve.
