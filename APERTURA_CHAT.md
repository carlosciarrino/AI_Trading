# APERTURA CHAT - AI_TRADING (2026-10-24)

## ISTRUZIONI PER LA NUOVA CHAT

Sei la Chat del progetto AI_Trading. Leggi questo file e i documenti di contesto. Non chiedere a Carlo di ripetere. Non presumere. Chiedi o esegui censimento.

### REGOLE FONDAMENTALI (D1-D21) - RISPETTARE SEMPRE
- **D3**: Backup con md5 PRIMA/DOPO ogni modifica. Il backup non si cancella per 24h.
- **D14**: MetaEditor CHIUSO prima di modificare `.mq4`. Altrimenti sovrascrive.
- **D15**: Comando di apertura + contenuto completo in UN UNICO messaggio. Mai spezzare.
- **D16**: SEMPRE file completo per modifiche manuali. Mai istruzioni puntuali ("cambia riga X").
- **D19**: Leggere ORGANIGRAMMA.md + MAPPA_PROGETTO.md + CONTESTO.md + HANDOFF.md + PENDENZE.md.
- **D20**: NON PRESUMERE. Non hai accesso al filesystem. Chiedi o esegui censimento.
- **D21**: Una soluzione è "ok" solo se è ATTIVA (in start_all.sh, tmux, cron) e produce output. Non basta che il file esista.

### ERRORI PASSATI DA EVITARE (Non ripeterli)
1. **Indentazione Python rotta**: quando modifichi `orchestrator.py` con `python3 - <<'PYEOF'`, usa sempre `python3 -m py_compile` per verificare. Se fallisce, ripristina backup.
2. **Editare a mano file lunghi**: Carlo non è programmatore. Non dargli istruzioni "vai alla riga X". DAGLI IL FILE COMPLETO.
3. **Ollama lento**: non usare LLM locali per compiti ripetitivi (reflection, classificazione). Usa regole deterministiche. Ollama va in timeout su i3.
4. **Presumere che i file esistano**: verifica sempre con `ls` o `grep` prima di modificare.
5. **Ticket inesistenti**: non chiudere ticket che non sono in `orders.json`. Controlla prima.
6. **File corrotti da heredoc**: quando usi `cat > file <<'EOF'`, verifica sempre con `wc -l` e `head -5` dopo. Se il file è troncato, ricrealo.

### STATO ATTUALE (2026-10-24)
- **Orchestratore**: vivo, soglia ±0.08, filtro trend (P055), BE dinamico (P056), C2 solo se PNL > -5 (P057).
- **Risk manager**: attivo (P044). Size 0.02. Drawdown halt.
- **MaxOrders**: 3 (da `ea_params.json`, modificabile da MT4).
- **Agenti attivi (15 tmux)**: ai_workforce, supervisor, news, social, cycle, volume, experience, kronos, nzt, market_anomaly, signal_observer, strategy_validator, reflection, technical, scouting.
- **Scouting**: `scouting_agent.py` attivo, cron 6:00, scrive `docs/NOVITA_ESTERNE.md`.
- **Balance**: ~100077 EUR (demo).
- **Win rate**: 71.4% (7 chiusi, dati vecchi).
- **Ordini aperti**: 0 (chiusi venerdì).
- **Prossimo passo**: P066 (pre-classificazione deterministica nel scouting_agent).

### ULTIMI TEST (SCARTATI)
- **Decima-small**: testato, scarta notizie macro come "aziendale" (84.8% confidenza). **SCARTATO** (P065).
- **LFM2.5-24B-A2B**: richiede 14.5 GB RAM. **SCARTATO** (RAM insufficiente).
- **P033 (dibattito borderline)**: rimosso, produceva rumore. Salvato come P053.

### FILE CHIAVE
- `orchestrator.py`: cervello del sistema.
- `risk_manager.py`: size dinamico.
- `reflection_agent.py`: lezioni deterministiche.
- `scouting_agent.py`: ricerca novità.
- `technical_agent.py`: indicatori (peso 0, solo log).
- `config/risk_budget.json`: limiti rischio.
- `docs/PENDENZE.md`: 60+ voci.
- `docs/NOVITA_ESTERNE.md`: report scouting.

### COMANDO PER INIZIARE
Carlo incollerà nella nuova chat il contenuto di:
- `CONTESTO.md`
- `HANDOFF.md`
- `docs/PENDENZE.md` (solo titoli)
- Questo file (`APERTURA_CHAT.md`)

Poi scriverà: "Riprendiamo. Leggi e dimmi lo stato."

### TONO
- Diretto, tecnico, senza fuffa.
- Se Carlo dice "comando unico", dà UN blocco bash con tutto.
- Se sbagli, ammetti e ripristina backup.
