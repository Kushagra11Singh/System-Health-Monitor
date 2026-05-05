import json
from datetime import datetime, timezone, timedelta

from flask import Flask, jsonify

app = Flask(__name__)
LOG_FILE = "metrics.log"


def read_logs():
    try:
        with open(LOG_FILE) as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []


@app.route("/metrics/live")
def live():
    from monitor import collect
    return jsonify(collect())


@app.route("/metrics/summary")
def summary():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    logs = [
        line for line in read_logs()
        if datetime.fromisoformat(line["timestamp"]) > cutoff
    ]
    if not logs:
        return jsonify({"error": "no data"})
    return jsonify({
        "samples": len(logs),
        "avg_cpu": sum(line["cpu_percent"] for line in logs) / len(logs),
        "avg_ram": sum(line["ram_percent"] for line in logs) / len(logs),
    })


if __name__ == "__main__":
    app.run(port=5000)
    