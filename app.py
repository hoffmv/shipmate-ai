# app.py

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "status": "Shipmate AI is online",
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True)
