import os
import json
from datetime import datetime

LOG_FILE = "system_activity.json"

def analyze_and_evolve():
    if not os.path.exists(LOG_FILE):
        print("No log file found to analyze.")
        return

    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    total_runs = len(logs)
    dual_successes = sum(1 for entry in logs if entry.get("status") == "DUAL_ENGINE_SUCCESS")

    print(f"--- Autonomous System Evaluation ---")
    print(f"Total Logged Pipeline Executions: {total_runs}")
    print(f"Successful Dual-Engine Cycles: {dual_successes}")

    # Evolution adjustment: dynamically scale output targets based on success volume
    evolution_factor = dual_successes * 2
    print(f"Evolution Parameter Updated: Target asset batch size scaled to {evolution_factor} units.")

    # Log the optimization event
    optimization_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_runs": total_runs,
        "evolution_factor": evolution_factor,
        "status": "SYSTEM_EVOLVED"
    }

    logs.append(optimization_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    print("Optimization cycle complete and logged.")

if __name__ == "__main__":
    analyze_and_evolve()
