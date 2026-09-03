import os
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
# Import your actual pipeline execution module/function here (e.g., from your main script)
# import main_pipeline_module

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return

def run_task_loop():
    while True:
        try:
            # Trigger your master cycle here
            # main_pipeline_module.run_master_cycle()
            pass
        except Exception as e:
            print(f"Error in task loop: {e}")
        time.sleep(60)

if __name__ == "__main__":
    task_thread = threading.Thread(target=run_task_loop, daemon=True)
    task_thread.start()

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health check server live on port {port}")
    server.serve_forever()
