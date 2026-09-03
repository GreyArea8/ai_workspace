import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

RENDER_API_URL = "https://ai-workspace-mpif.onrender.com"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        response = requests.post(RENDER_API_URL, json={"prompt": user_text}, timeout=10)
        data = response.json()
        reply = data.get("reply", "Command received, but no reply formatted.")
    except Exception as e:
        reply = f"Error communicating with Render backend: {e}"
        
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Telegram control bot polling for cross-device commands...")
    app.run_polling()
