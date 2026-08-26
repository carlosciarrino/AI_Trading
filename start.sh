#!/bin/bash
tmux new-session -d -s dashboard "cd ~/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 web_app.py"
tmux new-session -d -s ai_workforce "cd ~/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 orchestrator.py > /home/carlo/orchestrator.log 2>&1"
tmux new-session -d -s sentinel "cd ~/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 sentinel.py"
tmux new-session -d -s news_agent "cd ~/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 news_agent.py"
tmux new-session -d -s social_agent "cd ~/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 social_agent.py"
tmux new-session -d -s cycle_agent "cd ~/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 cycle_agent.py"
echo "AI_BRIDGE avviato!"
