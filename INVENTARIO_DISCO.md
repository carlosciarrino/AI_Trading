# Inventario Disco - Carlo

## Progetti (tutto ciò che è in /home/carlo/Progetti/)
| Cartella | Dimensione | A cosa serve | Firma | Stato |
|---|---|---|---|---|
| AI_Trading | 226 MB | Sistema live (orchestrator, supervisor, web_app) | AI_Trading | Attivo |
| AI_Trading_sandbox | 71 MB | Sandbox Kilo (test sicuri, non tocca il live) | AI_Trading | Sandbox |
| Research | 4,2 GB | Progetto parallelo (quant-Trader, test strategie) | Research | Attivo |
| Weave | 858 MB | E-commerce (video/storie prodotti) | Weave | Attivo |
| stellar-kraken-twirl | 336 MB | App Dyad (Vercel) | stellar-kraken-twirl | Attivo |
| Bussola-Finanziaria | 131 MB | Progetto Bussola Finanziaria | Bussola-Finanziaria | Attivo |
| Bussola-Finanziaria-sandbox | 144 MB | Sandbox Bussola Finanziaria | Bussola-Finanziaria | Sandbox |
| ISTRUZIONI_AGENTI.md | 4 KB | Istruzioni per gli agenti | AI_Trading | Documento |

## Backtest e test (fuori da Progetti, ma legati ad AI_Trading)
| Cartella | Dimensione | A cosa serve | Firma | Stato |
|---|---|---|---|---|
| /home/carlo/backtest_lab | 1,1 GB | Backtest (dati Dukascopy, scraper, venv) | AI_Trading | Attivo |
| /home/carlo/AI_Trading_Agents | 6,1 GB | Venv condiviso (Python + librerie) | AI_Trading | Attivo |
| /home/carlo/AI_Trading_sandbox | 1 GB | Sandbox Kilo (test sicuri) | AI_Trading | Sandbox |

## MT4 e trading (fuori da Progetti)
| Cartella | Dimensione | A cosa serve | Firma | Stato |
|---|---|---|---|---|
| /home/carlo/Scrivania/XM MT4 | ~500 MB | MT4 + EA (SweepEA, AI_BRIDGE) | AI_Trading | Attivo |
| /home/carlo/Scrivania/MT4_Teletrade | ~500 MB | MT4 Teletrade (altro broker) | Trading | Attivo |

## Dati personali (NON legati al progetto)
| Cartella | Dimensione | A cosa serve |
|---|---|---|
| /home/carlo/Musica | 7,2 GB | Musica personale |
| /home/carlo/Documenti | 1,5 GB | Documenti personali |
| /home/carlo/Scaricati | 2,5 GB | Download (da verificare) |

## Note
- Il forward test (MT4 + SweepEA) non usa Docker. Le immagini Docker cancellate non erano in uso.
- Il sistema live usa tmux + Python, non Docker.
- La sandbox (`AI_Trading_sandbox`) è dove Kilo può testare senza toccare il live. Non cancellare.
- `Research` e `Weave` sono progetti attivi, non cancellare.
