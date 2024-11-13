from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    """Receive updates from Telegram via webhook."""
    update = request.get_json()

    # Log incoming updates for debugging
    print("Received update:", update)

    # Handle updates (this is where your bot's logic would go)
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        message_text = "Hello! I received your message."
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": message_text
        })

    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def index():
    """Root endpoint to confirm the app is running."""
    return "Welcome to the Telegram Bot Webhook Service."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
