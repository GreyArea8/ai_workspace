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
            
            diagnostic_snippet = "OBDII DTC scan routine active. Live freeze-frame analysis and sensor mapping locked."
            output_dir = "generated_assets"
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                if files:
                    latest_file = max([os.path.join(output_dir, f) for f in files], key=os.path.getctime)
                    try:
                        with open(latest_file, "r") as f:
                            diagnostic_snippet = f.read()
                    except Exception:
                        pass

            if self.path == '/health':
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = {
                    "status": "online",
                    "service": "Automated Technical Diagnostics & Utilities",
                    "latest_diagnostic_preview": diagnostic_snippet,
                    "checkout_url": "https://www.paypal.me/CornellEugene"
                }
                self.wfile.write(json.dumps(response_data, indent=2).encode())
            else:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Elite Auto Diagnostics & Technical Portal</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #121212; color: #e0e0e0; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        h1 {{ color: #ff5722; font-size: 24px; }}
        pre {{ background: #2d2d2d; padding: 15px; border-radius: 5px; overflow-x: auto; color: #a9b7c6; font-size: 14px; }}
        .btn {{ display: inline-block; background: #0070ba; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; }}
        .btn:hover {{ background: #005ea6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Elite Auto Diagnostics - Live Technical Feed</h1>
        <p>Access automated OBDII fault code analysis, pinout charts, and step-by-step repair workflows.</p>
        <h3>Latest Generated Diagnostic Asset:</h3>
        <pre>{diagnostic_snippet}</pre>
        <h3>Unlock Full Wiring Diagrams & ECU Flash Packages</h3>
        <p>Complete secure checkout to receive instant access to full technical manuals and repair scripts.</p>
        <a class="btn" href="https://www.paypal.me/CornellEugene" target="_blank">Proceed to Secure Checkout ($25)</a>
    </div>
</body>
</html>"""
                self.wfile.write(html_content.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

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
