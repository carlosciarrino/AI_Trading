import json, time, os, requests

# Legge il file generato da ai_researcher
RESEARCH_FILE = os.path.expanduser("~/AI_Trading/ai_research.txt")
TEST_RESULTS = os.path.expanduser("~/AI_Trading/ai_test_results.json")

def load_candidates():
    if not os.path.exists(RESEARCH_FILE):
        return []
    with open(RESEARCH_FILE, "r") as f:
        lines = f.readlines()
    models = [line.strip().split(" ")[1] for line in lines if line.startswith("- ")]
    return models

def test_model(model_name):
    """
    Test reale: manda una richiesta a Ollama con un prompt di trading.
    Se il modello non esiste o non risponde, viene scartato.
    """
    url = "http://localhost:11434/api/generate"
    prompt = "Rispondi solo con BUY, SELL o HOLD per EURUSD sul timeframe 15min."
    try:
        response = requests.post(url, json={"model": model_name, "prompt": prompt, "stream": False}, timeout=300)
        response.raise_for_status()
        answer = response.json()["response"].strip().upper()
        if answer in ["BUY", "SELL", "HOLD"]:
            return True
        else:
            return False
    except:
        return False

def run_tests():
    models = load_candidates()
    results = []
    for m in models:
        ok = test_model(m)
        results.append({"model": m, "test_passed": ok})
        print(f"Testato {m}: {'OK' if ok else 'SCARTATO'}")
    with open(TEST_RESULTS, "w") as f:
        json.dump(results, f, indent=2)

while True:
    run_tests()
    time.sleep(86400)  # una volta al giorno
