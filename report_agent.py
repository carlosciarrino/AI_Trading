import os
from datetime import datetime

BASE = "/home/carlo/AI_Trading/docs"
OUTPUT = os.path.join(BASE, "RICERCA_SETTIMANALE.md")

def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def main():
    gh = read_file(os.path.join(BASE, "SCOUT_GITHUB.md"))
    hf = read_file(os.path.join(BASE, "SCOUT_HF.md"))
    arxiv = read_file(os.path.join(BASE, "SCOUT_ARXIV.md"))

    with open(OUTPUT, "w") as f:
        f.write(f"# RICERCA SETTIMANALE (aggiornato {datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        f.write("Questo file unisce i risultati dei 3 scout. Da qui puoi estrarre idee per testare nuove strategie, modelli o librerie.\n\n")
        
        f.write("## 1. Repository GitHub interessanti\n")
        f.write(gh.replace("# SCOUT GITHUB", "### GitHub") + "\n\n")
        
        f.write("## 2. Modelli Hugging Face\n")
        f.write(hf.replace("# SCOUT HUGGING FACE", "### Hugging Face") + "\n\n")
        
        f.write("## 3. Paper Accademici (arXiv)\n")
        f.write(arxiv.replace("# SCOUT ARXIV", "### arXiv") + "\n\n")
        
    print(f"Report generato: {OUTPUT}")

if __name__ == "__main__":
    main()
