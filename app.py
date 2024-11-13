from flask import Flask, redirect, jsonify
import requests
import os

app = Flask(__name__)

# Retrieve the bot token from environment variables for security
BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_telegram_file_link(file_id):
    """Function to get the Telegram file download link using file_id."""
    # Step 1: Get file path using Telegram's getFile API
    file_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(file_info_url)
    
    if response.status_code == 200:
        # Extract file path from response
        file_path = response.json()['result']['file_path']
        
        # Step 2: Construct the download URL
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        return download_url
    else:
        # Return None if there's an error
        return None

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Endpoint to generate and redirect to a Telegram file download link."""
    download_link = get_telegram_file_link(file_id)
    if download_link:
        # Redirect the user to the Telegram download link
        return redirect(download_link, code=302)
    else:
        # If unable to retrieve, return an error response
        return jsonify({"error": "File not found or unable to retrieve"}), 404

if __name__ == '__main__':
    # Run the Flask app (Render will handle running it in production)
    app.run(host='0.0.0.0', port=443)
