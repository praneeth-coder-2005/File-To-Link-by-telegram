from flask import Flask, redirect, jsonify
import requests
import os

app = Flask(__name__)

# Retrieve the bot token from environment variables for security
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Log the bot token to verify it's being set (optional for debugging; remove in production)
if not BOT_TOKEN:
    print("Error: BOT_TOKEN environment variable is not set.")
    exit(1)  # Exit if bot token is not set
else:
    print("Bot token found:", BOT_TOKEN[:5] + "..." + BOT_TOKEN[-5:])  # Log partial token for security

def get_telegram_file_link(file_id):
    """Fetch the Telegram file download link using file_id."""
    # Step 1: Use Telegram's getFile API to get the file path
    file_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(file_info_url)
    
    # Print the response for debugging
    print("Telegram API response:", response.json())
    
    if response.status_code == 200:
        # Extract file path from response
        file_path = response.json().get('result', {}).get('file_path')
        
        if file_path:
            # Step 2: Construct the download URL
            download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            return download_url
        else:
            print("Error: File path not found in Telegram API response.")
            return None
    else:
        # Log error response for troubleshooting
        print("Failed to retrieve file:", response.json())
        return None

@app.route('/', methods=['GET'])
def index():
    """Root endpoint to confirm the app is running."""
    return jsonify({"message": "Welcome to the Telegram File Redirect Service. Use /download/<file_id> to access files."}), 200

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
