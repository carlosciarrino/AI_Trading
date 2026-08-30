#!/usr/bin/env python3
import os
import json
import subprocess
import requests
import time
from datetime import datetime
from packaging import version

BASE = os.path.expanduser("~/AI_Trading")
REPORT_FILE = os.path.join(BASE, "tool_updater_report.txt")
LOG_FILE = os.path.join(BASE, "tool_updater_log.json")

# Lista di strumenti da monitorare (nome, sorgente, link, versione attuale)
TOOLS = [
    {
        "name": "panoscribe",
        "source": "pypi",
        "link": "https://pypi.org/pypi/panoscribe/json",
        "current_version": "0.1.0"
    },
    {
        "name": "yt-dlp",
        "source": "github",
        "link": "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest",
        "current_version": "2026.08.28"
    },
    {
        "name": "whisper",
        "source": "github",
        "link": "https://api.github.com/repos/openai/whisper/releases/latest",
        "current_version": "20250625"
    },
    {
        "name": "faster-whisper",
        "source": "github",
        "link": "https://api.github.com/repos/SYSTRAN/faster-whisper/releases/latest",
        "current_version": "1.0.3"
    }
]

def check_pypi(package_name):
    try:
        r = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            latest = data.get("info", {}).get("version", "unknown")
            return latest
    except:
        pass
    return None

def check_github_repo(repo_url):
    try:
        r = requests.get(repo_url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            latest = data.get("tag_name", "unknown")
            return latest
    except:
        pass
    return None

def check_github_stars(repo_name):
    try:
        r = requests.get(f"https://api.github.com/repos/{repo_name}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("stargazers_count", 0)
    except:
        pass
    return 0

def check_github_activity(repo_name):
    try:
        r = requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                return data[0].get("commit", {}).get("committer", {}).get("date", "unknown")
    except:
        pass
    return "unknown"

def search_new_tools():
    """Cerca nuovi strumenti su GitHub usando parole chiave."""
    keywords = ["video transcription", "video analyzer", "whisper", "yt-dlp", "instagram transcript"]
    found = []
    for kw in keywords:
        try:
            r = requests.get(
                f"https://api.github.com/search/repositories?q={kw}+sort=updated&per_page=3",
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                for item in data.get("items", []):
                    found.append({
                        "name": item.get("name"),
                        "full_name": item.get("full_name"),
                        "description": item.get("description"),
                        "stars": item.get("stargazers_count"),
                        "url": item.get("html_url"),
                        "updated_at": item.get("updated_at")
                    })
        except:
            pass
    return found

def run_audit():
    result = {
        "timestamp": datetime.now().isoformat(),
        "tools": {},
        "new_tools": [],
        "updates_available": []
    }

    # Controlla gli strumenti esistenti
    for tool in TOOLS:
        latest = None
        if tool["source"] == "pypi":
            latest = check_pypi(tool["name"])
        elif tool["source"] == "github":
            latest = check_github_repo(tool["link"])
        
        if latest and latest != tool["current_version"]:
            result["updates_available"].append({
                "name": tool["name"],
                "current": tool["current_version"],
                "latest": latest
            })

    # Cerca nuovi strumenti
    new_tools = search_new_tools()
    for nt in new_tools:
        # Evita duplicati con gli strumenti già monitorati
        if nt["name"] not in [t["name"] for t in TOOLS]:
            # Controlla se ha almeno 10 stelle (filtro base)
            if nt["stars"] >= 10:
                result["new_tools"].append(nt)

    # Salva report JSON per la dashboard
    with open(os.path.join(BASE, "tool_updater_status.json"), "w") as f:
        json.dump(result, f, indent=2)

    # Genera report leggibile
    lines = []
    lines.append(f"=== TOOL UPDATER REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    if result["updates_available"]:
        lines.append("\n[AGGIORNAMENTI DISPONIBILI]")
        for u in result["updates_available"]:
            lines.append(f"  {u['name']}: {u['current']} → {u['latest']}")
    else:
        lines.append("\n[AGGIORNAMENTI] Nessuno disponibile.")
    
    if result["new_tools"]:
        lines.append("\n[NOVITÀ TROVATE]")
        for nt in result["new_tools"][:5]:  # massimo 5
            lines.append(f"  {nt['name']} (★{nt['stars']})")
            lines.append(f"    {nt['description'][:80]}...")
            lines.append(f"    {nt['url']}")
    else:
        lines.append("\n[NOVITÀ] Nessun nuovo strumento interessante trovato.")

    report = "\n".join(lines)
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    # Log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "updates": len(result["updates_available"]),
        "new_tools": len(result["new_tools"])
    }
    try:
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    except:
        log = []
    log.append(log_entry)
    if len(log) > 100:
        log = log[-100:]
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    print(report)
    return result

if __name__ == "__main__":
    run_audit()
