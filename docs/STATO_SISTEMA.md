# STATO SISTEMA AI_TRADING

## 1. Stato rilevato (auto)
Timestamp: 2026-10-16 22:52:34
TMUX: ai_workforce: 1 windows (created Wed Oct 14 22:31:56 2026)
cycle_agent: 1 windows (created Wed Oct 14 22:53:12 2026)
experience_agent: 1 windows (created Wed Oct 14 21:58:49 2026)
kronos_agent: 1 windows (created Wed Oct 14 21:58:49 2026)
market_anomaly: 1 windows (created Wed Oct 14 21:58:49 2026)
news_agent: 1 windows (created Thu Oct 15 20:43:52 2026)
nzt_agent: 1 windows (created Wed Oct 14 21:58:49 2026)
signal_observer: 1 windows (created Wed Oct 14 21:58:49 2026)
social_agent: 1 windows (created Wed Oct 14 22:43:50 2026)
strategy_validator: 1 windows (created Wed Oct 14 21:58:49 2026)
supervisor: 1 windows (created Wed Oct 14 21:58:49 2026)
volume_agent: 1 windows (created Wed Oct 14 21:58:49 2026)
Servizi systemd user: web-app: active; controllo-remoto: active; ai-trading-agenti: active
Processi Windows: terminal.exe: nessun processo terminal.exe; metaeditor.exe: nessun processo metaeditor.exe
File condivisi MT4: orders.json: presente (294 bytes); open_time.json: presente (2002 bytes); sl_commands.json: presente (109 bytes)
IP Tailscale: 100.77.33.7
Git: commit 5325f18: pendenze: P016-P020 (tools fossile, mt4_shared, engram, tests, position_manager)

## 2. Diario azioni

- 29 October 2026 - dc82452: auto-sync gio 29 ott 2026, 22:00:02, -03
- 29 October 2026 - 592f39a: auto-sync gio 29 ott 2026, 23:00:01, -03
- 30 October 2026 - 1bc7eb0: auto-sync ven 30 ott 2026, 00:00:02, -03
- 30 October 2026 - a4550ea: auto-sync ven 30 ott 2026, 01:00:01, -03
- 30 October 2026 - 7f10827: auto-sync ven 30 ott 2026, 02:00:01, -03
- 30 October 2026 - 21358bb: auto-sync ven 30 ott 2026, 03:00:01, -03
- 30 October 2026 - eb0850b: auto-sync ven 30 ott 2026, 04:00:01, -03
- 30 October 2026 - c4176b8: auto-sync ven 30 ott 2026, 05:00:02, -03
- 30 October 2026 - 632ce2d: auto-sync ven 30 ott 2026, 06:00:01, -03
- 30 October 2026 - b65b64f: auto-sync ven 30 ott 2026, 07:00:01, -03
- 30 October 2026 - 039b2fc: auto-sync ven 30 ott 2026, 08:00:01, -03
- 30 October 2026 - d289f82: auto-sync ven 30 ott 2026, 09:00:02, -03
- 30 October 2026 - d3f67ec: auto-sync ven 30 ott 2026, 10:00:01, -03
- 30 October 2026 - 0e5c4cb: auto-sync ven 30 ott 2026, 11:00:01, -03
- 30 October 2026 - d0992e8: auto-sync ven 30 ott 2026, 12:00:01, -03
- 30 October 2026 - 74cde87: auto-sync ven 30 ott 2026, 13:00:01, -03
- 30 October 2026 - cadeb55: Fix: trend parser (bear=true) e ribilanciamento pesi (news 0.1, volume/exp 0.3)
- 30 October 2026 - 268f9c0: auto-sync ven 30 ott 2026, 14:00:01, -03
- 30 October 2026 - a5bf541: auto-sync ven 30 ott 2026, 14:00:01, -03
- 30 October 2026 - 2b02dc6: Security: ignora token huggingface
- 30 October 2026 - 421aa55: Feature: EMA veloci (9/21), agente report settimanale. Fix strategia.
- 30 October 2026 - 2ce9bfb: Fix: EMA veloci (9/21), report settimanale, fallback token GitHub
- 30 October 2026 - 8ed1c31: Risk Manager: aggiunti halt per margine libero (<20%) e perdita giornaliera (>=5%)
- 30 October 2026 - b9e32e7: Feature: query GitHub (topic), experience pattern (3 BUY loss)
- 30 October 2026 - d4500ef: Scout GitHub: 21 repo con token valido
- 30 October 2026 - e3889c7: auto-sync ven 30 ott 2026, 15:00:02, -03
- 30 October 2026 - 1a95dcb: Supervisor v4: Financial Guard (blocco su drawdown >8%, perdita giornaliera >3%). ALERT.md.
- 30 October 2026 - 1158086: Dashboard: integrazione Financial Guard (stato supervisore e banner ALERT)
- 30 October 2026 - 741556e: Supervisor: blocco automatico dopo 3 perdite consecutive
- 30 October 2026 - d3ab26a: Fix Dashboard: aggiunte variabili Financial Guard mancanti
- 30 October 2026 - a91a12e: Feature: Supervisore Diagnostico (analisi cause) e Filtro Scout (scarta repo scadenti)
- 30 October 2026 - c0803e2: auto-sync ven 30 ott 2026, 16:00:01, -03
- 30 October 2026 - c9501ca: auto-sync ven 30 ott 2026, 17:00:01, -03
- 30 October 2026 - 2881890: auto-sync ven 30 ott 2026, 18:00:01, -03
- 30 October 2026 - ecf1677: auto-sync ven 30 ott 2026, 19:00:01, -03
- 30 October 2026 - 5c42c08: auto-sync ven 30 ott 2026, 20:00:01, -03
- 30 October 2026 - b19f312: auto-sync ven 30 ott 2026, 21:00:02, -03
- 30 October 2026 - 103dea3: auto-sync ven 30 ott 2026, 22:00:01, -03
- 30 October 2026 - 2285286: auto-sync ven 30 ott 2026, 23:00:01, -03
- 31 October 2026 - ebd47fd: auto-sync sab 31 ott 2026, 00:00:01, -03
- 31 October 2026 - 377840f: auto-sync sab 31 ott 2026, 01:00:01, -03
- 31 October 2026 - e333f9b: auto-sync sab 31 ott 2026, 02:00:01, -03
- 31 October 2026 - e3d61fe: auto-sync sab 31 ott 2026, 03:00:01, -03
- 31 October 2026 - 1ede934: auto-sync sab 31 ott 2026, 04:00:01, -03
- 31 October 2026 - 3ff3308: auto-sync sab 31 ott 2026, 05:00:01, -03
- 31 October 2026 - 4236682: auto-sync sab 31 ott 2026, 06:00:01, -03
- 31 October 2026 - 5e2cafd: auto-sync sab 31 ott 2026, 07:00:01, -03
- 31 October 2026 - 4011983: auto-sync sab 31 ott 2026, 08:00:01, -03
- 31 October 2026 - 2e2e35c: auto-sync sab 31 ott 2026, 09:00:01, -03
- 31 October 2026 - 5cf8093: auto-sync sab 31 ott 2026, 10:00:01, -03
- 31 October 2026 - 6835b45: auto-sync sab 31 ott 2026, 12:00:01, -03
- 31 October 2026 - 85f9b0f: Milestone: test autonomo di TradingAgents riuscito. Aggiornato AGENTS.md.
- 31 October 2026 - 55d9aa2: Docs: creato registro esiti test risorse esterne
- 31 October 2026 - 7d7be2b: Docs: aggiunta sezione risorse future in AGENTS.md
- 31 October 2026 - 0c5f3a9: Docs: DeltaForge testato con successo (424 test). Candidato.
- 31 October 2026 - 07c787a: Feature: Trailing Stop Dinamico (basato su ATR) ispirato a DeltaForge
- 31 October 2026 - cd07ac1: Feature: Limite ordini per lato e calcolo Supporti/Resistenze (da DeltaForge)
- 31 October 2026 - f680ded: auto-sync sab 31 ott 2026, 13:00:01, -03
- 31 October 2026 - b5def04: Feature: Limite ordini per lato (max 2 buy / max 2 sell) da DeltaForge
- 31 October 2026 - 4b0c7d1: auto-sync sab 31 ott 2026, 14:00:02, -03
- 31 October 2026 - 6a8f998: auto-sync sab 31 ott 2026, 15:00:02, -03
- 31 October 2026 - 0e9f284: auto-sync sab 31 ott 2026, 16:00:01, -03
- 31 October 2026 - bd284dd: auto-sync sab 31 ott 2026, 17:00:01, -03
- 31 October 2026 - a969e10: auto-sync sab 31 ott 2026, 18:00:01, -03
- 31 October 2026 - 49827c2: auto-sync sab 31 ott 2026, 19:00:01, -03
- 31 October 2026 - 16adace: auto-sync sab 31 ott 2026, 20:00:01, -03
- 31 October 2026 - 5c6d3f2: auto-sync sab 31 ott 2026, 21:00:01, -03
- 31 October 2026 - b37e9f8: auto-sync sab 31 ott 2026, 22:00:01, -03
- 31 October 2026 - 549f134: auto-sync sab 31 ott 2026, 23:00:01, -03
- 01 November 2026 - 07441d5: auto-sync dom 1 nov 2026, 00:00:01, -03
- 01 November 2026 - b7fde7c: auto-sync dom 1 nov 2026, 01:00:01, -03
- 01 November 2026 - d6a8e22: auto-sync dom 1 nov 2026, 02:00:01, -03
- 01 November 2026 - 15fe497: auto-sync dom 1 nov 2026, 03:00:01, -03
- 01 November 2026 - 705364c: auto-sync dom 1 nov 2026, 04:00:01, -03
- 01 November 2026 - 170b925: auto-sync dom 1 nov 2026, 05:00:01, -03
- 01 November 2026 - f3b59b4: auto-sync dom 1 nov 2026, 06:00:01, -03
- 01 November 2026 - f266cec: auto-sync dom 1 nov 2026, 07:00:01, -03
- 01 November 2026 - a1321b9: auto-sync dom 1 nov 2026, 08:00:01, -03
- 01 November 2026 - 2f85a46: auto-sync dom 1 nov 2026, 09:00:01, -03
- 01 November 2026 - 3c6edaa: auto-sync dom 1 nov 2026, 10:00:02, -03
- 01 November 2026 - 19ff763: Fix critico: drawdown iniziale, azione risk manager, allineamento supervisore
- 01 November 2026 - 975f69c: Fix: forza il salvataggio di config/risk_budget.json (necessario per il drawdown)
- 01 November 2026 - 2a5700f: Feature: calcolo Supporti/Resistenze in technical_agent (da DeltaForge)
- 01 November 2026 - e44f306: Docs: esito test freqtrade (scartato)
- 01 November 2026 - 89e4729: auto-sync dom 1 nov 2026, 11:00:01, -03
- 01 November 2026 - f5cc036: Feature: Trigger Engine (Volume, Regime, News) + blocco se <2/3 attivi
- 01 November 2026 - 090896f: Fix: check_triggers integrato in orchestrator (blocco se <2/3 trigger)
- 01 November 2026 - 7a65898: Feature: FinBERT + keyword inglesi (ibrido). News in inglese.
- 01 November 2026 - a168511: Feature: TimesFM forecast integrato nel trigger engine (4° trigger)
- 01 November 2026 - a1ff194: Fix: trigger engine legge forecast.json (4° trigger)
- 01 November 2026 - a9e4da7: Feature: Bull vs Bear (maggioranza chiara invece di somma pesata) da TradingAgents
- 01 November 2026 - ac95abe: Fix: trigger engine controlla market_open (no ordini a mercato chiuso)
- 01 November 2026 - e363e61: auto-sync dom 1 nov 2026, 12:00:01, -03
- 01 November 2026 - 091422a: auto-sync dom 1 nov 2026, 13:00:02, -03
- 01 November 2026 - a6bac9b: auto-sync dom 1 nov 2026, 14:00:01, -03
- 01 November 2026 - b671e7e: auto-sync dom 1 nov 2026, 15:00:01, -03
- 01 November 2026 - fd293a1: auto-sync dom 1 nov 2026, 16:00:01, -03
- 01 November 2026 - 4d4814a: auto-sync dom 1 nov 2026, 17:00:01, -03
- 01 November 2026 - b64001b: auto-sync dom 1 nov 2026, 18:00:01, -03
- 01 November 2026 - 0423ff4: auto-sync dom 1 nov 2026, 19:00:01, -03
- 01 November 2026 - 8b32592: auto-sync dom 1 nov 2026, 20:00:01, -03
- 01 November 2026 - 2eb58a3: auto-sync dom 1 nov 2026, 21:00:01, -03
- 01 November 2026 - 56df0a3: auto-sync dom 1 nov 2026, 22:00:01, -03
- 01 November 2026 - 0e3e778: auto-sync dom 1 nov 2026, 23:00:01, -03
- 02 November 2026 - a915fcb: auto-sync lun 2 nov 2026, 00:00:02, -03
- 02 November 2026 - 4bdcc72: auto-sync lun 2 nov 2026, 01:00:01, -03
- 02 November 2026 - 69431e4: auto-sync lun 2 nov 2026, 02:00:01, -03
- 02 November 2026 - 38d5a74: auto-sync lun 2 nov 2026, 03:00:01, -03
- 02 November 2026 - 152737f: auto-sync lun 2 nov 2026, 04:00:01, -03
- 02 November 2026 - fd435b9: auto-sync lun 2 nov 2026, 05:00:01, -03
- 02 November 2026 - 469ae60: auto-sync lun 2 nov 2026, 06:00:01, -03
- 02 November 2026 - cd805a6: auto-sync lun 2 nov 2026, 07:00:01, -03
- 02 November 2026 - e362068: auto-sync lun 2 nov 2026, 08:00:02, -03
- 02 November 2026 - db37863: auto-sync lun 2 nov 2026, 09:00:01, -03
- 02 November 2026 - dcfa034: auto-sync lun 2 nov 2026, 10:00:01, -03
- 02 November 2026 - a3ca474: auto-sync lun 2 nov 2026, 11:00:01, -03
- 02 November 2026 - e6e8a7b: auto-sync lun 2 nov 2026, 12:00:01, -03
- 02 November 2026 - 08e3139: auto-sync lun 2 nov 2026, 13:00:02, -03
- 02 November 2026 - 75a7e20: auto-sync lun 2 nov 2026, 14:00:01, -03
- 02 November 2026 - 11f3ded: auto-sync lun 2 nov 2026, 15:00:01, -03
- 02 November 2026 - 22188a2: auto-sync lun 2 nov 2026, 16:00:01, -03
- 02 November 2026 - 83ac146: auto-sync lun 2 nov 2026, 17:00:01, -03
- 02 November 2026 - 81ba12b: auto-sync lun 2 nov 2026, 18:00:02, -03
- 02 November 2026 - 2f5218b: auto-sync lun 2 nov 2026, 19:00:01, -03
- 02 November 2026 - 4feabaa: auto-sync lun 2 nov 2026, 20:00:01, -03
- 02 November 2026 - d5e74ac: auto-sync lun 2 nov 2026, 21:00:01, -03
- 02 November 2026 - c1ef4f7: auto-sync lun 2 nov 2026, 22:00:01, -03
- 02 November 2026 - ccc9a87: auto-sync lun 2 nov 2026, 23:00:01, -03
- 03 November 2026 - ae5b98c: auto-sync mar 3 nov 2026, 00:00:01, -03
- 03 November 2026 - 5f4742e: auto-sync mar 3 nov 2026, 01:00:01, -03
- 03 November 2026 - b2c6ae2: auto-sync mar 3 nov 2026, 02:00:01, -03
- 03 November 2026 - 0781e95: auto-sync mar 3 nov 2026, 03:00:01, -03
- 03 November 2026 - 8f57222: auto-sync mar 3 nov 2026, 04:00:01, -03
- 03 November 2026 - bae00e4: auto-sync mar 3 nov 2026, 05:00:01, -03
- 03 November 2026 - 415aec6: auto-sync mar 3 nov 2026, 06:00:01, -03
- 03 November 2026 - 1eab1d9: auto-sync mar 3 nov 2026, 07:00:01, -03
- 03 November 2026 - 6a75b05: auto-sync mar 3 nov 2026, 08:00:01, -03
- 03 November 2026 - 6cd56c9: auto-sync mar 3 nov 2026, 09:00:01, -03
- 03 November 2026 - ab0bca3: auto-sync mar 3 nov 2026, 10:00:01, -03
- 03 November 2026 - bcc8dbf: auto-sync mar 3 nov 2026, 11:00:01, -03
- 03 November 2026 - 5f3419a: auto-sync mar 3 nov 2026, 12:00:01, -03
- 03 November 2026 - 7eb2955: auto-sync mar 3 nov 2026, 13:00:01, -03
- 03 November 2026 - 71bb78d: auto-sync mar 3 nov 2026, 14:00:01, -03
- 03 November 2026 - 346da06: auto-sync mar 3 nov 2026, 15:00:01, -03
- 03 November 2026 - 1605232: auto-sync mar 3 nov 2026, 16:01:42, -03
- 03 November 2026 - bfb9be2: auto-sync mar 3 nov 2026, 17:00:01, -03
- 03 November 2026 - d4e483f: auto-sync mar 3 nov 2026, 18:00:01, -03
- 03 November 2026 - 0e9a1a8: auto-sync mar 3 nov 2026, 19:00:01, -03
- 03 November 2026 - d57be57: auto-sync mar 3 nov 2026, 20:00:01, -03
- 03 November 2026 - 7022207: auto-sync mar 3 nov 2026, 21:00:01, -03
- 03 November 2026 - f9e49a3: auto-sync mar 3 nov 2026, 22:00:01, -03
- 03 November 2026 - ce370d8: auto-sync mar 3 nov 2026, 23:00:01, -03
- 04 November 2026 - c3be3b5: auto-sync mer 4 nov 2026, 00:00:01, -03
- 04 November 2026 - 7233ff7: auto-sync mer 4 nov 2026, 10:00:02, -03
- 04 November 2026 - 6933322: auto-sync mer 4 nov 2026, 11:00:01, -03
- 04 November 2026 - ebc21f4: auto-sync mer 4 nov 2026, 12:00:01, -03
- 04 November 2026 - ad71bf7: auto-sync mer 4 nov 2026, 13:00:01, -03
- 04 November 2026 - 80f0dbf: auto-sync mer 4 nov 2026, 14:00:01, -03
- 04 November 2026 - 2ec0853: auto-sync mer 4 nov 2026, 15:00:01, -03
- 04 November 2026 - e289da8: auto-sync mer 4 nov 2026, 16:00:01, -03
- 04 November 2026 - c4a8366: auto-sync mer 4 nov 2026, 17:00:02, -03
- 04 November 2026 - dee5851: auto-sync mer 4 nov 2026, 18:00:01, -03
- 04 November 2026 - 3d6fdb8: auto-sync mer 4 nov 2026, 19:00:01, -03
- 04 November 2026 - fd19d63: auto-sync mer 4 nov 2026, 20:00:02, -03
- 04 November 2026 - 152ba35: auto-sync mer 4 nov 2026, 21:00:01, -03
- 04 November 2026 - 16fbc56: auto-sync mer 4 nov 2026, 22:00:01, -03
- 04 November 2026 - 3b79885: auto-sync mer 4 nov 2026, 23:00:01, -03
- 05 November 2026 - c379ae2: auto-sync gio 5 nov 2026, 00:00:01, -03
- 05 November 2026 - 9d2f85f: auto-sync gio 5 nov 2026, 01:00:01, -03
- 05 November 2026 - d22d008: auto-sync gio 5 nov 2026, 02:00:01, -03
- 05 November 2026 - 735f0fd: auto-sync gio 5 nov 2026, 03:00:01, -03
- 05 November 2026 - dcc6119: auto-sync gio 5 nov 2026, 04:00:01, -03
- 05 November 2026 - 1055e39: auto-sync gio 5 nov 2026, 05:00:01, -03
- 05 November 2026 - f243f33: auto-sync gio 5 nov 2026, 06:00:01, -03
- 05 November 2026 - 13185e8: auto-sync gio 5 nov 2026, 07:00:01, -03
- 05 November 2026 - b57e4a1: auto-sync gio 5 nov 2026, 08:00:01, -03
- 05 November 2026 - 2cef7f4: auto-sync gio 5 nov 2026, 09:00:01, -03
- 05 November 2026 - 6b78632: auto-sync gio 5 nov 2026, 10:00:01, -03
- 05 November 2026 - 8713884: auto-sync gio 5 nov 2026, 11:00:01, -03
- 05 November 2026 - 7505c52: auto-sync gio 5 nov 2026, 12:00:01, -03
- 05 November 2026 - a142dec: auto-sync gio 5 nov 2026, 13:00:01, -03
- 05 November 2026 - 6112ba9: auto-sync gio 5 nov 2026, 14:00:01, -03
- 06 November 2026 - 7c8b832: auto-sync ven 6 nov 2026, 13:00:01, -03
- 06 November 2026 - 0af7232: auto-sync ven 6 nov 2026, 14:00:01, -03
- 06 November 2026 - dcae560: auto-sync ven 6 nov 2026, 15:00:01, -03
- 06 November 2026 - d6bb626: auto-sync ven 6 nov 2026, 16:00:02, -03
- 06 November 2026 - 56c109c: auto-sync ven 6 nov 2026, 17:00:01, -03
- 06 November 2026 - 4ae51ad: auto-sync ven 6 nov 2026, 18:00:01, -03
- 06 November 2026 - d3a3b79: auto-sync ven 6 nov 2026, 19:00:01, -03
- 06 November 2026 - 1af2d58: auto-sync ven 6 nov 2026, 20:00:01, -03
- 06 November 2026 - a3fa384: auto-sync ven 6 nov 2026, 21:00:01, -03
- 06 November 2026 - ff5ead2: auto-sync ven 6 nov 2026, 22:00:01, -03
- 06 November 2026 - 257b290: auto-sync ven 6 nov 2026, 23:00:01, -03
- 07 November 2026 - da7c456: auto-sync sab 7 nov 2026, 00:00:01, -03
- 07 November 2026 - 53b08ae: auto-sync sab 7 nov 2026, 01:00:01, -03
- 07 November 2026 - e505af3: auto-sync sab 7 nov 2026, 02:00:01, -03
- 07 November 2026 - ab81b62: auto-sync sab 7 nov 2026, 03:00:01, -03
- 07 November 2026 - 993d561: auto-sync sab 7 nov 2026, 04:00:01, -03
- 07 November 2026 - 1b762e8: auto-sync sab 7 nov 2026, 05:00:01, -03
- 07 November 2026 - e173cd6: auto-sync sab 7 nov 2026, 06:00:01, -03

## 3. Problemi noti

- EA UpdateOrdersFile accumula ordini nel file senza cancellazione
- supervisor venv rotto (percorso venv non corretto o mancante)
- web_app ridotto (funzionalità limitate rispetto alla versione completa)
- saldo non letto da MT4 (EA non invia o script non legge correttamente)
- loop sell non diagnosticato (possibile bug nella logica di chiusura)

## 4. Prossimo passo

- recuperare dashboard da web_app_backup.py per ripristinare funzionalità complete
- correggere supervisor verificando percorso venv e riavviando servizi
- aggiungere account.json scritto dall'EA per sincronizzare conto di trading
