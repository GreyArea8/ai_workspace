import os
import requests
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, ContextTypes

app = Flask(__name__)

RENDER_API_URL = "https://ai-workspace-mpif.onrender.com"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Initialize Telegram Application without starting a local updater/polling loop
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

def process_user_request(prompt):
    text = prompt.lower()
    
    if "evap" in text or "leak" in text:
        return "Diagnostic Rule: Check purge valve, vent solenoid, and gas cap seal for EVAP system integrity."
    elif "code" in text or "dtc" in text:
        return "Diagnostic Lookup: Please provide the specific OBDII trouble code (e.g., P0442) for targeted troubleshooting steps."
    elif "escalade" in text:
        if "suspension" in text or "air ride" in text:
            return "Escalade Air Suspension: Inspect compressor relay, airline connections, and height sensors."
        elif "transmission" in text or "shift" in text:
            return "Escalade Transmission: Check fluid level, 1-2 accumulator piston, and shift solenoids."
        elif "knock" in text or "engine" in text:
            return "Escalade Engine: Verify oil pressure, check lifters, and inspect for active knock sensor codes."
        else:
            return "Vehicle Context: Cadillac Escalade system selected. Specify symptom (e.g., suspension, transmission, engine knock) to proceed."
    else:
        return f"Processed request: {prompt} (System ready for advanced command routing.)"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json() or {}
    
    # Check if the incoming POST is from Telegram
    if "message" in data or "callback_query" in data:
        # Handle Telegram update asynchronously/synchronously via the application
        import asyncio
        async def process_telegram():
            update = Update.de_json(data, telegram_app.bot)
            await telegram_app.initialize()
            
            user_text = update.message.text if update.message else ""
            try:
                response = requests.post(RENDER_API_URL, json={"prompt": user_text}, timeout=10)
                reply = response.json().get("reply", "Command received, but no reply formatted.")
            except Exception as e:
                reply = f"Error communicating with backend: {e}"
                
            await update.message.reply_text(reply)

        asyncio.run(process_telegram())
        return jsonify({"status": "success"})
        
    # Handle internal API prompts
    prompt = data.get("prompt", "")
    reply = process_user_request(prompt)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
