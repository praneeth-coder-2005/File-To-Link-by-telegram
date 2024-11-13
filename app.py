from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Webhook endpoint
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    """Receive updates from Telegram via webhook."""
    update = request.get_json()

    # Log incoming update for debugging
    print("Received update:", update)

    # Process the message if it exists
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        user_message = update["message"].get("text", "")
        
        # Check if it's a start command or file request
        if user_message.startswith("/start"):
            message_text = "Hello! Send me a file, and I'll provide a download link."
        elif user_message.startswith("/get_file_"):
            # Handle file request by extracting the file_id
            file_id = user_message.split("_")[-1]
            send_file(chat_id, file_id)
            return jsonify({"status": "file sent"}), 200
        else:
            message_text = "Message received! Type /start to begin."

        # Respond to the user
        send_message(chat_id, message_text)
    
    return jsonify({"status": "ok"}), 200

def send_message(chat_id, text):
    """Send a message to the Telegram chat."""
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def send_file(chat_id, file_id):
    """Send the file with the given file_id to the user."""
    requests.post(f"{TELEGRAM_API_URL}/sendDocument", json={
        "chat_id": chat_id,
        "document": file_id
    })

@app.route('/', methods=["GET"])
def index():
    """Root endpoint for testing."""
    return "Telegram bot webhook is active."

if __name__ == '__main__':
    # Start Flask server on Render (port 443 for HTTPS)
    app.run(host="0.0.0.0", port=443)
