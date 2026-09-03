import os
import threading
import asyncio
import requests
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

app = Flask(__name__)

RENDER_API_URL = "https://ai-workspace-mpif.onrender.com"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

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
    prompt = data.get("prompt", "")
    reply = process_user_request(prompt)
    return jsonify({"reply": reply})

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = requests.post(RENDER_API_URL, json={"prompt": user_text}, timeout=10)
        data = response.json()
        reply = data.get("reply", "Command received, but no reply formatted.")
    except Exception as e:
        reply = f"Error communicating with Render backend: {e}"
    await update.message.reply_text(reply)

def run_bot():
    if not TELEGRAM_TOKEN:
        print("TELEGRAM_TOKEN not set, skipping bot startup.")
        return
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("Starting Telegram bot polling...")
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.start())
    loop.run_until_complete(application.updater.start_polling(drop_pending_updates=True))
    
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(application.stop())
        loop.run_until_complete(application.shutdown())

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
