#!/bin/bash
echo "Installazione AI_BRIDGE in corso..."
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip git tmux -y
pip install flask yfinance requests feedparser beautifulsoup4 pandas
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:0.5b
echo "Installazione completata! Avvia il sistema con il comando: bash start.sh"
