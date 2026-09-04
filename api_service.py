import os
import time
from flask import Flask

app = Flask(__name__)

task_queue = []
agent_status = "IDLE"

def background_autonomous_worker():
    """Continuously evaluates queued tasks and executes background operations."""
    global agent_status
    while True:
        agent_status = "RUNNING"
        if task_queue:
            task = task_queue.pop(0)
            print(f"Executing autonomous task: {task}")
            
            if "survey" in task.lower() or "offer" in task.lower():
                print("Targeting micro-task / offer completion pipeline...")
            elif "diagnostic" in task.lower():
                print("Processing automated vehicle diagnostic dataset...")
        else:
            agent_status = "IDLE"
        time.sleep(5)

@app.route("/")
def home():
    return "Autonomous API Service is live and active!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
