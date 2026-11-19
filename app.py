import os
import threading
from flask import Flask
from bot import main

app = Flask(__name__)

@app.route("/")
def home():
    return "TTS Coin Bot is running!"

threading.Thread(
    target=main,
    daemon=True
).start()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
