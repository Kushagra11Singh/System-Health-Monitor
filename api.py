from flask import Flask, jsonify
from datetime import datetime, timezone, timedelta
import json

app = Flask(__name__)
LOG_FILE = "metrics.log"

def read_logs():
    try:
        with open(LOG_FILE) as f:
            return [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError:
        return []

@app.route("/metrics/live")
def live():
    from monitor import collect
    return jsonify(collect())

@app.route("/metrics/summary")
def summary():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    logs = [l for l in read_logs()
            if datetime.fromisoformat(l["timestamp"]) > cutoff]
    if not logs:
        return jsonify({"error": "no data"})
    return jsonify({
        "samples": len(logs),
        "avg_cpu": sum(l["cpu_percent"] for l in logs) / len(logs),
        "avg_ram": sum(l["ram_percent"] for l in logs) / len(logs),
    })

if __name__ == "__main__":
    app.run(port=5000)