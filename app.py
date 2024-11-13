from flask import Flask, redirect, jsonify
import os

app = Flask(__name__)

# Environment variables
CHANNEL_ID = os.getenv("CHANNEL_ID").replace("-100", "")  # Channel ID without "-100" for the link
BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.route('/redirect/<message_id>', methods=['GET'])
def redirect_to_channel(message_id):
    """Redirect to the message in the Telegram channel."""
    telegram_link = f"https://t.me/c/{CHANNEL_ID}/{message_id}"
    return redirect(telegram_link, code=302)

@app.route("/", methods=["GET"])
def home():
    """Root endpoint for testing."""
    return "Telegram Bot Redirect Service is Active."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=443)
