import os
import time
import threading
from flask import Flask, jsonify, request

app = Flask(__name__)

task_queue = ["Survey optimization pipeline", "Automated vehicle diagnostic processing"]
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
    return f"Autonomous API Service is live! Status: {agent_status}, Queue Size: {len(task_queue)}"

@app.route("/enqueue", methods=["POST"])
def enqueue_task():
    data = request.json or {}
    task = data.get("task", "General automation task")
    task_queue.append(task)
    return jsonify({"status": "queued", "task": task, "queue_length": len(task_queue)})

if __name__ == "__main__":
    # Start background thread for continuous autonomous loop execution
    threading.Thread(target=background_autonomous_worker, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
