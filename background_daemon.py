import time
import subprocess
import os
from datetime import datetime

LOG_FILE = "daemon_activity.log"
INTERVAL_SECONDS = 15  # Run every 60 seconds for testing/demonstration

def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_FILE, "a") as f:
        f.write(formatted + "\n")

def run_loop():
    log_message("Background daemon started.")
    while True:
        try:
            log_message("Executing automated cycle...")
            subprocess.run(["python3", "-B", "run_full_cycle.py"], check=True)
            log_message("Cycle completed successfully.")
        except Exception as e:
            log_message(f"Error during execution: {e}")
        
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run_loop()


import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Daemon is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
