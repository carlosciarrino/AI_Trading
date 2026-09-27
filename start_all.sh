#!/bin/bash
sleep 20
cd /home/carlo/AI_Trading
PY=/home/carlo/AI_Trading_Agents_py311/bin/python3

tmux new-session -d -s ai_workforce "cd /home/carlo/AI_Trading && $PY orchestrator.py > /home/carlo/ai_workforce.log 2>&1"
tmux new-session -d -s web_app "cd /home/carlo/AI_Trading && $PY web_app.py > /home/carlo/web_app.log 2>&1"
tmux new-session -d -s supervisor "cd /home/carlo/AI_Trading && $PY supervisor_agent.py > /home/carlo/supervisor.log 2>&1"
tmux new-session -d -s news_agent "cd /home/carlo/AI_Trading && $PY news_agent.py > /home/carlo/news_agent.log 2>&1"
tmux new-session -d -s social_agent "cd /home/carlo/AI_Trading && $PY social_agent.py > /home/carlo/social_agent.log 2>&1"
tmux new-session -d -s cycle_agent "cd /home/carlo/AI_Trading && $PY cycle_agent.py > /home/carlo/cycle_agent.log 2>&1"
tmux new-session -d -s volume_agent "cd /home/carlo/AI_Trading && $PY volume_agent.py > /home/carlo/volume_agent.log 2>&1"
tmux new-session -d -s experience_agent "cd /home/carlo/AI_Trading && $PY experience_agent.py > /home/carlo/experience_agent.log 2>&1"
tmux new-session -d -s kronos_agent "cd /home/carlo/AI_Trading && $PY kronos_agent.py > /home/carlo/kronos_agent.log 2>&1"
tmux new-session -d -s nzt_agent "cd /home/carlo/AI_Trading && $PY nzt_agent.py > /home/carlo/nzt_agent.log 2>&1"
tmux new-session -d -s monday_agent "cd /home/carlo/AI_Trading && $PY monday_pattern_agent.py > /home/carlo/monday_agent.log 2>&1"
tmux new-session -d -s market_anomaly "cd /home/carlo/AI_Trading && $PY market_anomaly_agent.py > /home/carlo/market_anomaly.log 2>&1"
tmux new-session -d -s signal_observer "cd /home/carlo/AI_Trading && $PY signal_observer_agent.py > /home/carlo/signal_observer.log 2>&1"
tmux new-session -d -s strategy_validator "cd /home/carlo/AI_Trading && $PY strategy_validator.py > /home/carlo/strategy_validator.log 2>&1"
