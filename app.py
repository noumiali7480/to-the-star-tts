import os
import threading
import asyncio
from flask import Flask
from bot import main

app = Flask(__name__)

@app.route("/")
def home():
    return "TTS Coin Bot is running!"

def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()

threading.Thread(
    target=run_bot,
    daemon=True
).start()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
