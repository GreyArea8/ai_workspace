import os
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import your monetization modules
import dual_engine_generator
import publisher

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
            print("--- Starting Automated Revenue Cycle ---")
            dual_engine_generator.generate_dynamic_assets()
            publisher.publish_releases()
            print("--- Revenue Cycle Complete ---")
        except Exception as e:
            print(f"Error in revenue cycle: {e}")
        time.sleep(60)

if __name__ == "__main__":
    task_thread = threading.Thread(target=run_task_loop, daemon=True)
    task_thread.start()

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health check server live on port {port}")
    server.serve_forever()
