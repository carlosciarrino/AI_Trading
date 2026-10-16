# CONFRONTO CON PROGETTI ESTERNI

Ultimo aggiornamento: 2026-10-16 23:55
Autore: Carlo + Chat

Confronto tra il nostro sistema e due progetti open source studiati:
TradingAgents (Tauric Research) e Quant-Agent-Trader (guge199205-byte).

Repository clonati in /home/carlo/Progetti/Research/.

---

## 1. TRADINGAGENTS (Tauric Research)

- **URL**: https://github.com/TauricResearch/TradingAgents
- **Paper**: arXiv 2412.20138
- **Stelle GitHub**: ~71.000 (uno dei repo piu' popolari del settore)
- **Licenza**: Apache 2.0
- **Versione attuale**: v0.7.0 (ottobre 2026)
- **Linguaggio**: Python + LangGraph
- **LLM supportati**: GPT, Gemini, Claude, Grok, Ollama, DeepSeek, Qwen, GLM
- **Mercati**: multi-asset (azioni, crypto, forex)

### Architettura

7+ agenti specializzati:
- `agents/analysts/` — analisti fondamentali, sentiment, tecnici
- `agents/researchers/` — bull_researcher.py e bear_researcher.py (dibattito)
- `agents/risk_mgmt/` — 3 risk analyst: aggressive, conservative, neutral
- `agents/trader/` — trader che propone
- `agents/managers/` — portfolio manager, research manager (sintetizzano)

### Cosa fanno di meglio

1. **Dibattito bull/bear**: 2 agenti che argomentano pro/contro. Ogni uno
   riceve le risposte dell'altro e contro-argomenta. Dopo N round, un manager
   sintetizza.
2. **Risk management separato**: 3 risk analyst che dibattono sulla proposta
   del trader. Nessuno puo' bypassare il risk manager.
3. **Memoria con riflessione** (`memory/`):
   - `log.py`: TradingMemoryLog markdown append-only. Idempotenza + rotazione.
   - `settlement.py`: misura alpha vs benchmark (SPY) dopo N giorni,
     point-in-time corretto.
   - `reflection.py`: LLM genera 2-4 frasi di lezione specifica, reiniettate
     nei prompt futuri dello stesso ticker.
4. **Multi-provider LLM**: un modello per ruolo (mini per analisi, large per
   decisione).
5. **Multi-vendor dati**: Yahoo, FRED, Alpha Vantage, Polymarket, Reddit,
   SEC EDGAR.

---

## 2. QUANT-AGENT-TRADER (guge199205-byte)

- **URL**: https://github.com/guge199205-byte/quant-Trader
- **Licenza**: MIT
- **Linguaggio**: Python + DeepSeek Agent + MCP + React (Arena)
- **Mercati**: A股 (Cina), US, HK
- **Broker reali**: Futu, IBKR, Tiger, TDX bridge

### Architettura

- 3 agenti con ruoli diversi (快枪手/研究员/消息面)
- 5 MCP server per mercato (math/search/trade/price/memory)
- 17 skill pronte (`dsh/skills/`)
- Docker compose con 5+ container

### Cosa fanno di meglio

1. **Self-evolution** (`docs/AGENT_ROADMAP.md`):
   - **盘后复盘 agent** (post-market review): ogni giorno a chiusura, analizza
     il PNL di ogni decisione, estrae lezioni, scrive `logs/review/{agent}/{date}.md`,
     aggiorna memory.
   - **明日预案** (piano del giorno dopo): prodotto dal review agent.
2. **Hypothesis library** (`configs/hypotheses/*.json`):
   - Ogni ipotesi qualitativa ("缩量洗盘" = washout with low volume) ha:
     - trigger condition, direction, validation window
     - win rate, sample size, data ultima validazione
     - status: proposed / verified / deprecated
   - **Validatore notturno** con event study su 2 anni di dati.
   - Se fallisce 2 volte, va in `deprecated`.
3. **Dynamic risk budget** (`risk.py`):
   - Meta-agent calcola `LEVERAGE_MAX`, size per ticker, numero massimo di
     nuove azioni al giorno, in base a volatilita', drawdown, sentiment.
   - "模型不可绕过" (i modelli non possono aggirarlo).
4. **Skill ecosystem** (17 skill): stock analysis, news sentiment, market
   sentiment, futures, ecc.
5. **MCP services**: comunicazione strutturata tra agenti.

---

## 3. CONFRONTO CON IL NOSTRO SISTEMA

| Aspetto | Nostro | TradingAgents | Quant-Agent |
|---|---|---|---|
| Orchestrazione | 1 orchestratore lineare | LangGraph multi-agente | DeepSeek + MCP |
| Agenti decisionali | 5 segnali | 7+ agenti con dibattito | 3 agenti con ruoli |
| Dibattito | No | Si' (bull/bear + 3 risk) | Si' (solo se disaccordo) |
| Risk manager separato | No | Si' (3 prospettive) | Si' (non bypassabile) |
| Memoria | experiences.json (84 record) | log.md + settlement + reflection | memory + hypothesis library |
| Lezioni specifiche | No (frase generica) | Si' (2-4 frasi per decisione) | Si' (review giornaliero) |
| Rotazione memoria | No (P002) | Si' (max_entries) | Si' |
| Settlement point-in-time | No | Si' (alpha vs benchmark) | Si' |
| Size dinamica | No | Si' (risk analyst) | Si' (risk budget) |
| Multi-vendor dati | No (3 fonti base) | Si' (6+ vendor) | Si' (specializzati) |
| Multi-provider LLM | No (solo Ollama 0.5b) | Si' (5+ provider) | Si' (DeepSeek) |
| MCP | No | No | Si' (5 server/mercato) |
| Skill ecosystem | 5 agenti | N/A | 17 skill |
| Broker reale | MT4 (demo) | No (paper) | Futu/IBKR/Tiger/TDX |
| Mercati | EURUSD | multi-asset | A股/US/HK |
| Deploy | tmux + systemd | CLI + Docker | Docker compose |
| Dashboard | Flask custom | CLI | React (Arena) |

### Cosa abbiamo noi che loro NON hanno

1. **EA MQL4 collegato a MT4 reale (demo)** — loro fanno paper trading o
   broker API. Il nostro esegue ordini veri su MT4.
2. **Semplicita' e leggerezza** — 13 file, ~160 MB, gira su i3 con 12 GB RAM.
3. **Controllo totale** — ogni pezzo e' nostro, ogni modifica tracciata.

### Verdetto onesto

Siamo **indietro di 12-18 mesi** rispetto a TradingAgents e Quant-Agent-Trader
sul piano architetturale. Il loro codice e' scritto da team con test e CI. Il
nostro e' scritto in chat.

**Ma**: il nostro ha un conto reale collegato. Questo e' il nostro vantaggio.

---

## 4. COSA ADATTARE (priorita')

### ALTA (fare subito)
- **P031**: memoria con riflessione (da TradingAgents reflection.py).
- **P032**: rotazione experiences.json (chiude P002).
- **P033**: dibattito bull/bear borderline (solo in zona grigia).
- **P034**: risk manager separato con size dinamica.

### MEDIA
- **P035**: hypothesis library (da Quant-Agent).
- **P036**: multi-vendor dati (FRED, Alpha Vantage, Reddit).
- **P037**: settlement point-in-time.

### BASSA
- **P038**: multi-provider LLM.
- **P039**: MCP services.
- **P040**: Arena web / React.

---

## 5. PIANO OPERATIVO

1. **Subito**: P031 (memoria con riflessione) — il piu' alto valore, complessita' media.
2. **Poi**: P032 (rotazione) — 20 righe, chiude P002.
3. **Poi**: P034 (risk manager separato) — complessita' alta ma critico.
4. **Poi**: P033 (dibattito borderline) — richiede prompt ben scritti.
5. **Poi**: P035, P036, P037 (media priorita').

Target: entro 7 giorni, il sistema ha memoria con riflessione, rotazione,
risk manager separato, e dibattito borderline. Pari o superiore a
TradingAgents su quei punti, mantenendo il vantaggio del conto reale.
