import urllib.request
import json
import time

def check_status():
    try:
        req = urllib.request.Request("http://127.0.0.1:5000/status")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Agent Status: {data}")
            return data
    except Exception as e:
        print(f"Status check error: {e}")
        return None

def enqueue_task(task_name):
    try:
        payload = json.dumps({"task": task_name}).encode("utf-8")
        req = urllib.request.Request("http://127.0.0.1:5000/enqueue", data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Task successfully queued: {data}")
            return data
    except Exception as e:
        print(f"Enqueue error: {e}")
        return None

if __name__ == "__main__":
    print("Starting autonomous command loop...")
    check_status()
    enqueue_task("Run automated survey micro-task pipeline targeting payout")
    time.sleep(2)
    check_status()
