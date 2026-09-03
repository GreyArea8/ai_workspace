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
