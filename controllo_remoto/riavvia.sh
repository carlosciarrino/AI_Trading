#!/bin/bash
tmux kill-session -t web_app 2>/dev/null
tmux new-session -d -s web_app "python3 /home/carlo/AI_Trading/web_app.py"
echo "Dashboard riavviata"
