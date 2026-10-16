# Tentativi falliti / Test non funzionanti

## 2026-08-29 – OmniRoute
- **Obiettivo:** Sostituire Ollama con router AI per token gratuiti.
- **Tentativo:** Installazione via pip (`pip install omniroute`).
- **Risultato:** Pacchetto non trovato su PyPI.
- **Tentativo alternativo:** LiteLLM (`pip install 'litellm[proxy]'`).
- **Risultato:** Errore `ImportError: cannot import name 'NotRequired' from 'typing'`.
- **Causa:** LiteLLM richiede Python 3.11+. Sistema ha Python 3.10.
- **Conclusione:** Impossibile su questo hardware/SO. Rimane su Ollama.

---

## Regole per futuri test
1. Ogni tentativo va documentato qui con data, obiettivo, comandi usati, errore e causa.
2. Se un'idea richiede upgrade hardware/SO, segnarlo come "bloccato".
3. Non ripetere test già documentati.
