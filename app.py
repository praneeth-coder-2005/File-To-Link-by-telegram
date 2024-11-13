from flask import Flask, redirect, request, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # The bot's token
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")  # Chat ID for the bot
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"  # Bot's API URL

@app.route('/redirect/<file_id>', methods=['GET'])
def redirect_to_bot(file_id):
    """Redirect to the bot to retrieve the file."""
    
    # Send a request to the bot to send the file to the user
    message = {
        "chat_id": BOT_CHAT_ID,
        "text": f"File requested: /get_file_{file_id}"  # Special command format
    }
    requests.post(f"{BOT_URL}/sendMessage", json=message)
    
    return jsonify({"message": "Request sent to the bot. Check your bot messages for the file."})

@app.route('/')
def home():
    return "Welcome to the Telegram Bot File Retrieval Service."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
