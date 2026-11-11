from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def index():
    return f"<h1>Bienvenue sur legeni-webapp</h1><p>Version {os.environ.get('APP_VERSION', 'dev')}</p>"

@app.route("/health")
def health():
    return {"status": "ok"}
