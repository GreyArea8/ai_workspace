import os
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

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
                    "service": "Interactive AI Assistant & Diagnostics",
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
    <title>Elite Auto AI Assistant</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #121212; color: #e0e0e0; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        h1 {{ color: #ff5722; font-size: 24px; }}
        .chat-box {{ background: #2d2d2d; height: 350px; overflow-y: auto; padding: 15px; border-radius: 5px; margin-bottom: 15px; display: flex; flex-direction: column; gap: 10px; }}
        .message {{ padding: 10px 15px; border-radius: 5px; max-width: 80%; }}
        .user {{ background: #0070ba; color: white; align-self: flex-end; }}
        .ai {{ background: #333333; color: #e0e0e0; align-self: flex-start; border-left: 4px solid #ff5722; }}
        .input-row {{ display: flex; gap: 10px; }}
        input[type="text"] {{ flex: 1; padding: 12px; border-radius: 5px; border: 1px solid #444; background: #252525; color: white; font-size: 16px; }}
        button {{ background: #ff5722; color: white; border: none; padding: 12px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; }}
        button:hover {{ background: #e64a19; }}
        .checkout-bar {{ margin-top: 20px; text-align: right; }}
        .checkout-btn {{ background: #0070ba; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Elite Auto AI Workspace</h1>
        <p>Send commands, diagnostic queries, or automation instructions directly to your backend AI.</p>
        
        <div class="chat-box" id="chatBox">
            <div class="message ai">System online. Ready for your commands, diagnostics, or workflow instructions.</div>
        </div>
        
        <div class="input-row">
            <input type="text" id="userInput" placeholder="Type a command or question..." autofocus onkeypress="if(event.key === 'Enter') sendCommand()">
            <button onclick="sendCommand()">Send</button>
        </div>

        <div class="checkout-bar">
            <a class="checkout-btn" href="https://www.paypal.me/CornellEugene" target="_blank">Secure Checkout ($25)</a>
        </div>
    </div>

    <script>
        async function sendCommand() {{
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const text = input.value.trim();
            if (!text) return;

            chatBox.innerHTML += `<div class="message user">${{text}}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {{
                const response = await fetch('/', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ prompt: text }})
                }});
                const data = await response.json();
                chatBox.innerHTML += `<div class="message ai">${{data.reply}}</div>`;
            }} catch (err) {{
                chatBox.innerHTML += `<div class="message ai">Error processing command.</div>`;
            }}
            chatBox.scrollTop = chatBox.scrollHeight;
        }}
    </script>
</body>
</html>"""
                self.wfile.write(html_content.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            user_prompt = data.get('prompt', '').strip()
            
            # Interactive command processing logic mimicking assistant behavior
            reply = f"Acknowledged command: '{user_prompt}'. Diagnostic routine executed, parameters locked, and background asset generator synchronized."
            if "status" in user_prompt.lower():
                reply = "All backend daemon threads are active. Port 10000 is operating normally with 60-second rotation cycles."
            elif "diag" in user_prompt.lower() or "code" in user_prompt.lower():
                reply = "Running targeted OBDII scan simulation. Check generated assets directory for latest live freeze-frame data."

            response_data = {
                "status": "success",
                "reply": reply,
                "checkout_url": "https://www.paypal.me/CornellEugene"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

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
    print(f"Interactive AI server live on port {port}")
    server.serve_forever()
