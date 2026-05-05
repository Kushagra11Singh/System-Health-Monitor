import psutil, json, time
from datetime import datetime, timezone

LOG_FILE = "metrics.log"

def collect():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "top_processes": sorted(
            [{"pid": p.info["pid"], "name": p.info["name"], "cpu": p.info["cpu_percent"]}
             for p in psutil.process_iter(["pid","name","cpu_percent"])],
            key=lambda x: x["cpu"], reverse=True
        )[:5]
    }

def run():
    cpu_alert_count = 0
    while True:
        data = collect()
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")
        print(f"[{data['timestamp']}] CPU:{data['cpu_percent']}% RAM:{data['ram_percent']}%")
        # Alert logic: 3 consecutive samples > 85%
        if data["cpu_percent"] > 85:
            cpu_alert_count += 1
            if cpu_alert_count >= 3:
                print("🚨 ALERT: CPU sustained high!")
        else:
            cpu_alert_count = 0
        time.sleep(30)

if __name__ == "__main__":
    run()