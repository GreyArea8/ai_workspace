import subprocess
import requests
import json
import os

RENDER_WEBHOOK_URL = "https://ai-workspace-mpif.onrender.com"

def git_commit_and_push(commit_message="Autonomous update"):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "master"], check=True)
        print("Successfully pushed updates to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")

def enqueue_task(task_description):
    url = f"{RENDER_WEBHOOK_URL}/task"
    payload = {"task": task_description}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"Task successfully queued: {task_description}")
            print(response.json())
        else:
            print(f"Failed to queue task: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

def check_agent_status():
    try:
        response = requests.get(f"{RENDER_WEBHOOK_URL}/status", timeout=10)
        print("Agent Status:", response.json())
    except Exception as e:
        print(f"Failed to fetch status: {e}")

if __name__ == "__main__":
    check_agent_status()
