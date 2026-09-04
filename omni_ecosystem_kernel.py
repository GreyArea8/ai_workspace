import os
import time
import threading
from flask import Flask, render_template_string, request, jsonify

# Configuration
STORAGE_DIR = "/tmp/ecosystem_storage"
PROMPTS_DIR = os.path.join(STORAGE_DIR, "prompts")
OUTPUT_LOG = os.path.join(STORAGE_DIR, "omni_output.log")

os.makedirs(PROMPTS_DIR, exist_ok=True)

# Initialize Flask App
app = Flask(__name__)

CHAT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Omni AI Native Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #121212; color: #e0e0e0; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background: #1f1f1f; padding: 15px; text-align: center; font-size: 1.1em; font-weight: bold; border-bottom: 1px solid #333; }
        #chat-box { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 80%; padding: 12px 16px; border-radius: 12px; line-height: 1.4; word-break: break-word; }
        .user { align-self: flex-end; background: #0056b3; color: #fff; }
        .ai { align-self: flex-start; background: #2a2a2a; color: #e0e0e0; border: 1px solid #444; }
        .input-area { display: flex; padding: 15px; background: #1f1f1f; border-top: 1px solid #333; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #444; background: #2a2a2a; color: #fff; font-size: 1em; }
        button { padding: 0 20px; border-radius: 8px; border: none; background: #0056b3; color: #fff; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <header>Omni AI Mobile Interface</header>
    <div id="chat-box">
        <div class="message ai">Kernel and web server online. Ready for mobile connection.</div>
    </div>
    <div class="input-area">
        <input type="text" id="message-input" placeholder="Type a message..." autofocus>
        <button onclick="sendMessage()">Send</button>
    </div>
    <script>
        const chatBox = document.getElementById('chat-box');
        const messageInput = document.getElementById('message-input');
        messageInput.addEventListener('keypress', function (e) { if (e.key === 'Enter') sendMessage(); });

        function appendMessage(text, sender) {
            const div = document.createElement('div');
            div.className = 'message ' + sender;
            div.textContent = text;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendMessage() {
            const text = messageInput.value.trim();
            if (!text) return;
            appendMessage(text, 'user');
            messageInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                appendMessage(data.reply, 'ai');
            } catch (err) {
                appendMessage('Error communicating with kernel.', 'ai');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(CHAT_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    prompt_filename = f"web_prompt_{int(time.time() * 1000)}.prompt"
    prompt_path = os.path.join(PROMPTS_DIR, prompt_filename)
    with open(prompt_path, 'w') as f:
        f.write(user_message)
        
    time.sleep(2.0)
    
    reply = "Prompt processed by local kernel."
    if os.path.exists(OUTPUT_LOG):
        with open(OUTPUT_LOG, 'r') as f:
            lines = f.readlines()
            if lines:
                reply = lines[-1].strip()

    return jsonify({'reply': reply})

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def kernel_polling_loop():
    print("[KERNEL] Background polling daemon started.")
    while True:
        if os.path.exists(PROMPTS_DIR):
            files = os.listdir(PROMPTS_DIR)
            for file in files:
                if file.endswith('.prompt'):
                    p_path = os.path.join(PROMPTS_DIR, file)
                    with open(p_path, 'r') as pf:
                        content = pf.read()
                    os.remove(p_path)
                    
                    log_entry = f"[AI_RESPONSE] Received and processed: {content}"
                    with open(OUTPUT_LOG, 'a') as og:
                        og.write(log_entry + "\n")
        time.sleep(1)

if __name__ == '__main__':
    t = threading.Thread(target=kernel_polling_loop, daemon=True)
    t.start()
    run_flask()
