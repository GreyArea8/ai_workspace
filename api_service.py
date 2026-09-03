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

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    reply = f"Processed prompt: {prompt}"
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
