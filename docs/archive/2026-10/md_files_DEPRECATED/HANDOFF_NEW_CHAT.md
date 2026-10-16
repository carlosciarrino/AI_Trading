# HANDOFF — Nuova Chat 2026-10-07

## Cos'è questo documento

Contesto per iniziare nuova chat con DeepSeek. Contiene stato attuale, decisioni, prossimi step.

## Chi siamo

- **Utente (Carlo):** CEO. Decide strategie, non esegue comandi tecnici.
- **AI (DeepSeek):** socio tecnico. Scrive codice, propone soluzioni, coordina agenti.
- **Super agente:** da scegliere (Kilo Code candidato).

## Visione

Azienda digitale multi-progetto. Ogni progetto indipendente. Come acqua: si adatta, non dipende da AI specifiche. Moduli sostituibili.

## Cosa abbiamo fatto finora

### Forex (in produzione demo)
- Orchestratore multi-agente (news, social, volume, cycle, experience).
- Position Manager (break-even + trailing stop).
- EA MT4 AI_Bridge con `ApplySLModifications`.
- Verifier test automatici.
- Watchdog controllo sistema.
- Dashboard web.
- Bot Telegram.
- Conto demo FP Markets 450000065, server FPTrading-demo.

### Infrastruttura
- Repository GitHub: `https://github.com/carlosciarrino/AI_Trading.git`
- Dashboard: `http://100.77.33.7:5000` (Tailscale)
- Bot Telegram: `@AI_Bridge_Forex_Bot`
- Memoria: `.engram/index.md` + Neuragram

## Fix recenti (2026-10-07)

- Orchestratore: bug ordini infiniti risolto (`MAX_OPEN_ORDERS=3`).
- Isolamento MT4 real vs demo.
- Regole MT4 in `.engram`.

## Problemi aperti

1. **Mustang (real):** 4 operazioni buy, drawdown ~113€. Aspetta TP.
2. **Microfono Linux:** voce bassa, trascrizione imprecisa.
3. **Super agente:** Aider abbandonato. Da testare Kilo Code.
4. **Media Company:** da avviare.
5. **E-commerce:** da progettare.

## Prossimo step immediato

**Testare Kilo Code + Nemotron 3 Super:**
1. Installa Kilo Code in VS Code (Extensions).
2. Configura OpenRouter + `nvidia/nemotron-3-super-120b-a12b:free`.
3. Attiva Orchestrator mode.
4. Task: "Crea docs/COMPANY_BLUEPRINT.md con struttura aziendale".

## Come lavoriamo

- **Chat = sala riunioni.** Decisioni strategiche.
- **Super agente = capo cantiere.** Esegue modifiche in autonomia.
- **Verifier = controllo qualità.** Test automatici.
- **Watchdog = sicurezza.** Blocca se errore.
- **Utente = CEO.** Interviene solo su problemi gravi.

## Regole operative

1. **Zero costi.** Solo tool gratuiti.
2. **Hardware i3, 12GB RAM.** Progetti leggeri.
3. **File completo con `nano`.** Mai `sed`/`cat` lunghi.
4. **Un solo agente decide su denaro.**
5. **File vecchi cancellati, solo storico. Backup non attivo.**
6. **Mai toccare MT4 real (Teletrade). Solo demo (XM MT4).**
7. **Ogni modifica → Verifier testa.**
8. **Ogni decisione → salva in `.engram/index.md`.**

## Progetti futuri

1. **Media Company** — video automatici TikTok/YouTube, affiliazione.
2. **E-commerce** — Amazon, TikTok Shop, Shopee, Temu.
3. **Piattaforma scommesse** — multilingua, Brasile (normative locali).

## Come iniziare nuova chat

1. Incolla `.engram/index.md` (contesto completo).
2. Incolla questo `HANDOFF_NEW_CHAT.md`.
3. Di': "Riprendiamo da Kilo Code. Prima opzione A, B o C."
4. Procedi con test Kilo Code.
