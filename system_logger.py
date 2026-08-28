import platform
import json
import os
from datetime import datetime

LOG_FILE = "system_activity.json"
MAX_LOG_ENTRIES = 5

def log_system_state():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_data = {
            "timestamp": timestamp,
            "system": platform.system(),
            "release": platform.release(),
            "node": platform.node(),
            "status": "SUCCESS"
        }
        
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
                    
        logs.append(log_data)
        if len(logs) > MAX_LOG_ENTRIES:
            logs = logs[-MAX_LOG_ENTRIES:]
            
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
            
        print("Structured system state successfully logged to JSON.")
        
    except Exception as e:
        print(f"Failed to log system state: {e}")

if __name__ == "__main__":
    log_system_state()
