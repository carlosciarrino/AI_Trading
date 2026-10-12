from flask import Flask
import subprocess, os

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))

@app.route('/ferma')
def ferma():
    r = subprocess.run([f'{BASE}/ferma.sh'], capture_output=True, text=True)
    return f"<h1>Ferma</h1><pre>{r.stdout}{r.stderr}</pre>"

@app.route('/riavvia')
def riavvia():
    r = subprocess.run([f'{BASE}/riavvia.sh'], capture_output=True, text=True)
    return f"<h1>Riavvia</h1><pre>{r.stdout}{r.stderr}</pre>"

@app.route('/stato')
def stato():
    r = subprocess.run([f'{BASE}/stato.sh'], capture_output=True, text=True)
    return f"<h1>Stato</h1><pre>{r.stdout}{r.stderr}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
