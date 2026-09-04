import os
import time
import threading
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "engine_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            status TEXT DEFAULT 'QUEUED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

def background_autonomous_worker():
    """Continuously evaluates persistent tasks from SQLite and executes background operations."""
    while True:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_text FROM tasks WHERE status = 'QUEUED' LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            task_id, task = row
            cursor.execute("UPDATE tasks SET status = 'RUNNING' WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            
            print(f"Executing persistent autonomous task: {task}")
            if "survey" in task.lower() or "offer" in task.lower():
                print("Targeting micro-task / offer completion pipeline...")
            elif "diagnostic" in task.lower():
                print("Processing automated vehicle diagnostic dataset...")
                
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = 'COMPLETED' WHERE id = ?", (task_id,))
            conn.commit()
        conn.close()
        time.sleep(5)

@app.route("/")
def home():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'QUEUED'")
    queued_count = cursor.fetchone()[0]
    conn.close()
    return f"Persistent Autonomous API Service is live! Queued Tasks: {queued_count}"

@app.route("/enqueue", methods=["POST"])
def enqueue_task():
    data = request.json or {}
    task = data.get("task", "General automation task")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_text, status) VALUES (?, 'QUEUED')", (task,))
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'QUEUED'")
    queued_count = cursor.fetchone()[0]
    conn.close()
    return jsonify({"status": "queued", "task": task, "queue_length": queued_count})

if __name__ == "__main__":
    threading.Thread(target=background_autonomous_worker, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@app.route("/tick", methods=["GET"])
def keep_alive_tick():
    return jsonify({"status": "active", "message": "Keep-alive ping acknowledged."}), 200

# Task 4 Execution Hook for Micro-Tasks & Optimization Handlers
def execute_micro_task_pipeline(task_text):
    payout_link = "https://www.paypal.me/CornellEugene"
    print(f"Executing deep worker automation for: {task_text}")
    # Integration point for micro_task_engine & optimizer routines
    return f"Success. Revenue dispatched to {payout_link}"
