from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os
import logging

# Retrieve bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Base URL for the Render app, where files can be downloaded
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Your Render app URL
WEBHOOK_URL = f"{RENDER_APP_URL}/webhook/{BOT_TOKEN}"  # Webhook URL for Telegram to send updates

# Set up logging for better debugging and visibility
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! Send me a file, and I'll generate a download link for you.")

async def file_handler(update: Update, context: CallbackContext) -> None:
    """Handle received files and generate a download link."""
    # Get the file object (this could be a document, photo, or video)
    file = update.message.document or update.message.video or update.message.photo[-1]

    if not file:
        await update.message.reply_text("Please send a file.")
        return

    # Retrieve the file ID for generating the Render-based download link
    file_id = file.file_id

    # Construct the Render-based download link
    download_link = f"{RENDER_APP_URL}/download/{file_id}"

    # Send the Render-based download link to the user
    await update.message.reply_text(f"Here is your download link:\n{download_link}")

def main():
    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command and file handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, file_handler))

    # Set the webhook for the application
    application.run_webhook(
        listen="0.0.0.0",
        port=443,
        url_path=f"webhook/{BOT_TOKEN}",
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()
