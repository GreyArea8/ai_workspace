import os
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import dual_engine_generator
import publisher

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            diagnostic_snippet = "OBDII DTC scan routine active. Live freeze-frame analysis and sensor mapping locked."
            output_dir = "generated_assets"
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                if files:
                    latest_file = max([os.path.join(output_dir, f) for f in files], key=os.path.getctime)
                    try:
                        with open(latest_file, "r") as f:
                            diagnostic_snippet = f.read()[:500]
                    except Exception:
                        pass

            response_data = {
                "status": "online",
                "service": "Automated Technical Diagnostics & Utilities",
                "latest_diagnostic_preview": diagnostic_snippet,
                "message": "To unlock complete diagnostic data packages, wiring diagrams, and automated repair scripts, complete payment via secure checkout.",
                "checkout_url": "https://www.paypal.me/CornellEugene"
            }
            self.wfile.write(json.dumps(response_data, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {
                "error": "Endpoint not found",
            }
            self.wfile.write(json.dumps(error_data).encode())

    def log_message(self, format, *args):
        return

def run_task_loop():
    while True:
        try:
            print("--- Starting Automated Revenue Cycle ---")
            os.makedirs("generated_assets", exist_ok=True)
            dual_engine_generator.generate_dynamic_assets()
            publisher.publish_releases()
            print("--- Revenue Cycle Complete ---")
        except Exception as e:
            print(f"Error in revenue cycle: {e}")
        time.sleep(60)

if __name__ == "__main__":
    t = threading.Thread(target=run_task_loop, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"Monetized API server live on port {port}")
    server.serve_forever()
