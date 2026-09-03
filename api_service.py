from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class UtilityAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/diagnostic-tool':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            payload = {
                "status": "ready",
                "utility": "Automated Technical Diagnostics API",
                "payment_link": "https://www.paypal.me/CornellEugene"
            }
            self.wfile.write(json.dumps(payload).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), UtilityAPIHandler)
    server.serve_forever()
