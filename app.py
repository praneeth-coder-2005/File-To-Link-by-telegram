from flask import Flask, redirect
import os

app = Flask(__name__)

# Get the channel ID from environment variables and remove the "-100" prefix for Telegram link format
CHANNEL_ID = os.getenv("CHANNEL_ID", "").replace("-100", "")

@app.route('/redirect/<message_id>', methods=['GET'])
def redirect_to_channel(message_id):
    """Redirect to a specific message in the Telegram channel."""
    telegram_link = f"https://t.me/c/{CHANNEL_ID}/{message_id}"
    return redirect(telegram_link, code=302)

@app.route("/", methods=["GET"])
def home():
    """Root endpoint for testing the server."""
    return "Telegram Bot Redirect Service is Active."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=443)
