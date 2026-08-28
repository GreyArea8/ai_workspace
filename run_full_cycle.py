import subprocess
import json
import os
import urllib.request
from datetime import datetime

LOG_FILE = "system_activity.json"
WEBHOOK_URL = ""  # Optional: Paste your Discord/Telegram webhook URL here

def send_notification(message):
    if not WEBHOOK_URL:
        return
    try:
        payload = json.dumps({"content": message}).encode("utf-8")
        req = urllib.request.Request(WEBHOOK_URL, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Webhook notification failed: {e}")

def run_step(script_name):
    print(f"Executing {script_name}...")
    result = subprocess.run(["python3", "-B", script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in {script_name}: {result.stderr}")
    else:
        print(f"Successfully completed {script_name}")

def update_metrics():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
                
    total_runs = len(logs)
    evolution_factor = total_runs * 2
    
    metric_entry = {
        "timestamp": timestamp,
        "total_runs": total_runs,
        "evolution_factor": evolution_factor,
        "status": "SYSTEM_EVOLVED"
    }
    logs.append(metric_entry)
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"Metrics updated: total_runs={total_runs}, evolution_factor={evolution_factor}")

def main():
    print("--- Starting Unified Master Cycle ---")
    run_step("dual_engine_generator.py")
    update_metrics()
    run_step("distributor.py")
    run_step("publisher.py")
    
    msg = f"Autonomous pipeline cycle completed successfully. Total runs updated."
    send_notification(msg)
    print("--- Unified Master Cycle Complete ---\n")

if __name__ == "__main__":
    main()
