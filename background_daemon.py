import os
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import your monetization modules
import dual_engine_generator
import publisher

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve paid utility endpoints alongside health checks
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {
                "status": "online",
                "service": "Automated Technical Diagnostics & Utilities",
                "message": "To unlock full diagnostic datasets and automated scripts, complete payment via our secure checkout.",
                "checkout_url": "https://www.paypal.me/CornellEugene"
            }
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {
                "error": "Endpoint not found",
                "support_checkout": "https://www.paypal.me/CornellEugene"
            }
            self.wfile.write(json.dumps(error_data).encode())

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
    # Start the background task loop in a separate thread
    t = threading.Thread(target=run_task_loop, daemon=True)
    t.start()

    # Start the HTTP server on port 10000 for Render traffic and health checks
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"Monetized API server live on port {port}")
    server.serve_forever()
