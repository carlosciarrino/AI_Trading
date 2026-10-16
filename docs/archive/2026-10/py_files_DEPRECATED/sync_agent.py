import subprocess, os, time, shutil

# Percorso USB (da cambiare quando inserisci la chiavetta)
USB_PATH = "/media/carlo/USB/AI_BRIDGE"
REPO_PATH = "/home/carlo/AI_Trading"

def sync_to_usb():
    if os.path.exists(USB_PATH):
        shutil.copytree(REPO_PATH, USB_PATH, dirs_exist_ok=True)
        print("Sincronizzato su USB.")
    else:
        print("USB non trovata.")

def sync_to_github():
    try:
        subprocess.run(["git", "-C", REPO_PATH, "add", "."], check=True)
        subprocess.run(["git", "-C", REPO_PATH, "commit", "-m", "Aggiornamento automatico"], check=True)
        subprocess.run(["git", "-C", REPO_PATH, "push"], check=True)
        print("Sincronizzato su GitHub.")
    except Exception as e:
        print(f"Errore GitHub: {e}")

while True:
    sync_to_usb()
    sync_to_github()
    time.sleep(3600)  # Ogni ora
