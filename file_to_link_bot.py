from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Retrieve bot token from environment variables for security
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Base URL for the Render app, where files can be downloaded
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Your Render app URL

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

    # Retrieve the file ID for generating the Render-based download link
    file_id = file.file_id

    # Construct the Render-based download link
    download_link = f"https://file-to-link-by-telegram.onrender.com/download/{file_id}"

    # Send the Render-based download link to the user
    update.message.reply_text(f"Here is your download link:\n{download_link}")

def main():
    # Initialize the bot and the updater
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Register command and file handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.photo, file_handler))

    # Start polling to listen for messages
    updater.start_polling()
    print("Bot is running with polling...")

    # Idle to keep the bot running
    updater.idle()

if __name__ == '__main__':
    main()
