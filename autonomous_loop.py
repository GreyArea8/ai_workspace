import requests
import time

url = "http://127.0.0.1:5000/enqueue"
headers = {"Content-Type": "application/json"}

print("[Autonomous Loop] Initialized. Running continuous micro-task evolution...")
counter = 4
while True:
    payload = {"task": f"Autonomous evolution and optimization cycle #{counter}"}
    try:
        response = requests.post(url, json=payload, timeout=2)
        print(f"[Cycle {counter}] Enqueued successfully: {response.json()}")
    except Exception as e:
        print(f"[Cycle {counter}] Error connecting to engine: {e}")
    counter += 1
    time.sleep(2)
