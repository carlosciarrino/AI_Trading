#!/bin/bash
# ===================================================================
# AI_BRIDGE V3 - Installer Universale (Stile Linux)
# ===================================================================

set -e  # Ferma lo script in caso di errore

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 AI_BRIDGE V3 - Installer Universale${NC}"
echo -e "${YELLOW}Questo programma installerà AI_BRIDGE V3 sul tuo sistema.${NC}"
echo ""

# --- FASE 1: DOMANDE SEMPLICI ---
echo -e "${GREEN}📋 Rispondi a poche domande per iniziare...${NC}"

# 1. Cartella di installazione
read -p "📁 Cartella di installazione (default: ~/AI_Trading): " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-~/AI_Trading}

# 2. Lingua (per Ollama e log)
read -p "🌐 Lingua (it/en, default: it): " LANG
LANG=${LANG:-it}

# 3. API Key Twelve Data (opzionale, ma richiesta)
read -p "🔑 Inserisci la tua Twelve Data API key (https://twelvedata.com): " TWELVE_KEY
if [ -z "$TWELVE_KEY" ]; then
    echo "⚠️  Attenzione: senza API key, il sistema non potrà scaricare dati live."
fi

# 4. Conferma
echo ""
echo -e "${YELLOW}Riepilogo:${NC}"
echo "  Cartella: $INSTALL_DIR"
echo "  Lingua: $LANG"
echo "  API Key: ${TWELVE_KEY:0:8}... (se inserita)"
read -p "✅ Procedere con l'installazione? (s/n): " CONFIRM
if [[ "$CONFIRM" != "s" && "$CONFIRM" != "S" ]]; then
    echo "Installazione annullata."
    exit 0
fi

# --- FASE 2: INSTALLAZIONE ---
echo -e "${GREEN}🔧 Inizio installazione...${NC}"

# 2.1 Crea la cartella e clona il repository
echo "📦 Clonazione del repository..."
if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  La cartella esiste già. Verranno sovrascritti i file."
    rm -rf "$INSTALL_DIR"
fi
git clone https://github.com/carlosciarrino/AI_Trading.git "$INSTALL_DIR"

cd "$INSTALL_DIR"

# 2.2 Rilevamento sistema operativo
echo "🖥️  Rilevamento sistema operativo..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "   Sistema operativo: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "   Sistema operativo: macOS"
else
    echo "❌ Sistema operativo non supportato. Solo Linux e macOS."
    exit 1
fi

# 2.3 Installazione dipendenze di sistema (solo Linux)
if [[ "$OS" == "linux" ]]; then
    echo "📦 Installazione dipendenze di sistema..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv git curl wget tmux
fi

# 2.4 Creazione ambiente virtuale Python
echo "🐍 Creazione ambiente virtuale Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2.5 Installazione Ollama e download del modello
echo "🧠 Installazione Ollama e download del modello AI..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi
ollama pull tinyllama  # Modello leggero

# 2.6 Configurazione file .env (chiavi API)
echo "🔑 Configurazione chiavi API..."
cat > .env << EOF
TWELVE_KEY=$TWELVE_KEY
LANG=$LANG
EOF

# 2.7 Creazione della struttura dati
mkdir -p data/historical mt4_shared logs

# 2.8 Avvio dei servizi in tmux
echo "🚀 Avvio dei servizi..."
tmux kill-session -t ai_workforce 2>/dev/null
tmux kill-session -t dashboard 2>/dev/null

tmux new-session -d -s ai_workforce "cd $INSTALL_DIR && source venv/bin/activate && while true; do python3 orchestrator.py; sleep 3600; done"
tmux new-session -d -s dashboard "cd $INSTALL_DIR && source venv/bin/activate && python3 web_app.py"

echo -e "${GREEN}✅ Installazione completata!${NC}"
echo ""
echo -e "${GREEN}📊 Dashboard: http://localhost:5000${NC}"
echo -e "${GREEN}📌 Per controllare: tmux attach -t ai_workforce${NC}"
echo -e "${GREEN}📌 Per fermare: tmux kill-session -t ai_workforce${NC}"

