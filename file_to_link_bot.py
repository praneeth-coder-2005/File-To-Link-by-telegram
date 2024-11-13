import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Retrieve bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Webhook configuration
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Your Render app URL
PORT = 443  # Explicitly set to port 443, which Telegram requires for secure webhooks

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text("Hello! Send me a file, and I'll generate a download link for you.")

def file_handler(update: Update, context: CallbackContext) -> None:
    """Handle received files and generate a download link."""
    # Get the file object (this could be a document, photo, or video)
    file = update.message.document or update.message.video or update.message.photo[-1]

    if not file:
        update.message.reply_text("Please send a file.")
        return

    # Retrieve the file ID and file name (if available)
    file_id = file.file_id
    file_name = file.file_name if hasattr(file, 'file_name') else "Your file"

    # Construct the download link directly
    download_link = construct_file_url(BOT_TOKEN, file_id)

    # Send the download link to the user
    if download_link:
        update.message.reply_text(f"Here is your download link for {file_name}:\n{download_link}")
    else:
        update.message.reply_text("Failed to generate a download link.")

def construct_file_url(bot_token, file_id):
    """Construct a download URL directly for a given file ID."""
    download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_id}"
    return download_url

def main():
    # Initialize the bot and the updater
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Register command and file handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.photo, file_handler))

    # Set webhook URL using the Render app URL on port 443
    webhook_url = f"https://file-to-link-by-telegram.onrender.com/7550771021:AAEugqwyyW_yl0k5aBLl7PwUcLmySwZuFtM"
    updater.start_webhook(
        port=PORT,         # Use port 443
        url_path=BOT_TOKEN
    )
    updater.bot.set_webhook(webhook_url)
    print(f"Webhook URL set to {webhook_url}")
    updater.idle()

if __name__ == '__main__':
    main()
