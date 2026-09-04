#!/bin/bash
# Esegue agenti di ricerca e test durante la notte (fuori orario di trading)
cd /home/carlo/AI_Trading

# Avvia gli agenti di ricerca (se non sono già attivi)
for agent in github_researcher skill_researcher strategy_tester_agent news_critical ai_researcher_agent; do
    if ! tmux has-session -t $agent 2>/dev/null; then
        tmux new-session -d -s $agent "cd /home/carlo/AI_Trading && /home/carlo/AI_Trading_Agents_py311/bin/python3 ${agent}.py > /home/carlo/${agent}_night.log 2>&1"
        echo "$agent avviato in notturna"
    fi
done

# Avvia anche l'audit notturno (più approfondito)
tmux new-session -d -s night_audit "cd /home/carlo/AI_Trading && /home/carlo/AI_Trading_Agents_py311/bin/python3 audit_agent.py --full > /home/carlo/audit_night.log 2>&1"
