import os
import time
import threading
import requests
from flask import Flask

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "VeloraReelsBot aktif ✅"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    }, timeout=20)

def bot_loop():
    offset = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {"timeout": 30}

            if offset:
                params["offset"] = offset

            response = requests.get(url, params=params, timeout=40)
            data = response.json()

            for update in data.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text == "/start":
                    send_message(
                        chat_id,
                        "🎬 Selamat datang di VeloraReels!\n\n"
                        "✨ Konten eksklusif dan fitur VIP segera hadir.\n\n"
                        "Bot kamu sudah aktif ✅"
                    )

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("BOT_TOKEN belum diatur!")
    else:
        threading.Thread(target=bot_loop, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
