#!/usr/bin/env python3
import subprocess
import sys
import os
import datetime

def run_cmd(cmd, default='N/A', cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5, cwd=cwd)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return default
    except Exception:
        return default

def get_tmux_sessions():
    output = run_cmd('tmux list-sessions 2>/dev/null', 'tmux non disponibile o nessuna sessione')
    if output == 'tmux non disponibile o nessuna sessione':
        if run_cmd('which tmux', '') == '':
            return 'tmux non installato'
    return output

def get_systemd_services():
    services = ['web-app', 'controllo-remoto', 'ai-trading-agenti']
    statuses = []
    for s in services:
        out = run_cmd(f'systemctl --user is-active {s} 2>/dev/null', 'inattivo')
        statuses.append(f'{s}: {out}')
    return '; '.join(statuses)

def get_windows_processes():
    term = run_cmd("ps aux | grep -i '[t]erminal.exe'", 'nessun processo terminal.exe')
    meta = run_cmd("ps aux | grep -i '[m]etaeditor.exe'", 'nessun processo metaeditor.exe')
    return f"terminal.exe: {term}; metaeditor.exe: {meta}"

def get_shared_files():
    base = '/home/carlo/mt4_shared/'
    files = ['orders.json', 'open_time.json', 'sl_commands.json']
    statuses = []
    for f in files:
        path = os.path.join(base, f)
        if os.path.isfile(path):
            size = os.path.getsize(path)
            statuses.append(f'{f}: presente ({size} bytes)')
        else:
            statuses.append(f'{f}: mancante')
    return '; '.join(statuses)

def get_tailscale_ip():
    ip = run_cmd('tailscale ip -4 2>/dev/null', 'Tailscale non connesso o non installato')
    if ip == '':
        ip = run_cmd('tailscale ip 2>/dev/null', 'Tailscale non connesso o non installato')
    return ip

def get_git_info():
    repo = '/home/carlo/AI_Trading'
    if not os.path.isdir(os.path.join(repo, '.git')):
        return 'Non è un repository Git'
    short = run_cmd('git rev-parse --short HEAD', 'N/A', cwd=repo)
    subject = run_cmd('git log -1 --pretty=%s', 'N/A', cwd=repo)
    return f'commit {short}: {subject}'

def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    md_path = '/home/carlo/AI_Trading/docs/STATO_SISTEMA.md'
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    
    # Read the file if it exists
    lines = []
    if os.path.isfile(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    # Find the headers for section 1 and 2
    idx1 = -1
    idx2 = -1
    for i, line in enumerate(lines):
        if line.strip() == '## 1. Stato rilevato (auto)':
            idx1 = i
            break
    if idx1 != -1:
        for i in range(idx1 + 1, len(lines)):
            if lines[i].strip() == '## 2. Diario azioni':
                idx2 = i
                break
    
    # If we found both headers, replace the content between them
    if idx1 != -1 and idx2 != -1:
        # Build new lines: keep everything up to and including idx1
        new_lines = lines[:idx1+1]
        # Add state detection lines
        state_lines = [
            f'Timestamp: {get_current_time()}',
            f'TMUX: {get_tmux_sessions()}',
            f'Servizi systemd user: {get_systemd_services()}',
            f'Processi Windows: {get_windows_processes()}',
            f'File condivisi MT4: {get_shared_files()}',
            f'IP Tailscale: {get_tailscale_ip()}',
            f'Git: {get_git_info()}'
        ]
        for sl in state_lines:
            new_lines.append(sl + '\n')
        # Add a blank line before the next header
        new_lines.append('\n')
        # Keep everything from idx2 onwards
        new_lines.extend(lines[idx2:])
    else:
        # Fallback: create a new file with the given structure
        new_lines = []
        new_lines.append('# STATO SISTEMA AI_TRADING\n\n')
        new_lines.append('## 1. Stato rilevato (auto)\n\n')
        state_lines = [
            f'Timestamp: {get_current_time()}',
            f'TMUX: {get_tmux_sessions()}',
            f'Servizi systemd user: {get_systemd_services()}',
            f'Processi Windows: {get_windows_processes()}',
            f'File condivisi MT4: {get_shared_files()}',
            f'IP Tailscale: {get_tailscale_ip()}',
            f'Git: {get_git_info()}'
        ]
        for sl in state_lines:
            new_lines.append(sl + '\n')
        new_lines.append('\n')
        new_lines.append('## 2. Diario azioni\n\n')
        new_lines.append('## 3. Problemi noti\n\n')
        new_lines.append('- EA UpdateOrdersFile accumula ordini nel file senza cancellazione\n')
        new_lines.append('- supervisor venv rotto (percorso venv non corretto o mancante)\n')
        new_lines.append('- web_app ridotto (funzionalità limitate rispetto alla versione completa)\n')
        new_lines.append('- saldo non letto da MT4 (EA non invia o script non legge correttamente)\n')
        new_lines.append('- loop sell non diagnosticato (possibile bug nella logica di chiusura)\n\n')
        new_lines.append('## 4. Prossimo passo\n\n')
        new_lines.append('- recuperare dashboard da web_app_backup.py per ripristinare funzionalità complete\n')
        new_lines.append('- correggere supervisor verificando percorso venv e riavviando servizi\n')
        new_lines.append("- aggiungere account.json scritto dall'EA per sincronizzare conto di trading\n")
    
    # Write back
    with open(md_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    main()
