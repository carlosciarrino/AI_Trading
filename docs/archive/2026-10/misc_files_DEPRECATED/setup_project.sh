#!/bin/bash
# Setup automatico per AI_BRIDGE V3
echo "🔧 Installazione AI_BRIDGE V3..."

# 1. Clona repository (se non esiste)
if [ ! -d "~/AI_Trading" ]; then
    git clone https://github.com/carlosciarrino/AI_Trading.git ~/AI_Trading
fi
cd ~/AI_Trading

# 2. Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Installa Ollama e scarica modello
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama

# 4. Configura chiavi API (chiede input)
read -p "Inserisci Twelve Data API key: " TWELVE_KEY
echo "TWELVE_KEY=$TWELVE_KEY" > .env

# 5. Avvia servizi in tmux
tmux kill-session -t ai_workforce 2>/dev/null
tmux kill-session -t dashboard 2>/dev/null
tmux new-session -d -s ai_workforce "cd ~/AI_Trading && source venv/bin/activate && while true; do python3 orchestrator.py; sleep 3600; done"
tmux new-session -d -s dashboard "cd ~/AI_Trading && source venv/bin/activate && python3 web_app.py"

echo "✅ AI_BRIDGE V3 installato e avviato."
echo "📊 Dashboard: http://localhost:5000"
echo "📌 Per controllare: tmux attach -t ai_workforce"
