from flask import Flask, redirect, jsonify
import os
import requests

app = Flask(__name__)

# Retrieve bot token and channel/chat ID (use your bot's chat ID for testing)
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")  # The chat ID where the bot will send messages

BOT_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/redirect/<file_id>', methods=['GET'])
def redirect_to_bot(file_id):
    """Send a request to the bot to retrieve the file for the user."""
    # Send a message to the bot's chat with the file ID
    data = {
        "chat_id": BOT_CHAT_ID,
        "text": f"/get_file_{file_id}"
    }
    
    # Send the command to the bot to initiate file retrieval
    response = requests.post(BOT_API_URL, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        return jsonify({"message": "Request sent to the bot. Check the bot messages for your file."})
    else:
        return jsonify({"error": "Failed to send request to the bot."}), 500

@app.route('/', methods=['GET'])
def home():
    """Home route for testing."""
    return "Welcome to the Telegram Bot File Redirect Service."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
