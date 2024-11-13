from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os
import logging

# Retrieve bot token and channel ID from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Set your channel ID here

# Set up Render webhook URL
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Replace with your actual Render URL
WEBHOOK_URL = f"{RENDER_APP_URL}/webhook/{BOT_TOKEN}"  # Webhook URL for Telegram to send updates

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! Send me a file, and I'll store it permanently in our channel.")

async def file_handler(update: Update, context: CallbackContext) -> None:
    """Handle received files and forward them to a storage channel."""
    # Get the file object (this could be a document, photo, or video)
    file = update.message.document or update.message.video or update.message.photo[-1]

    if not file:
        await update.message.reply_text("Please send a file.")
        return

    # Forward the file to the channel for permanent storage
    forwarded_message = await context.bot.forward_message(
        chat_id=CHANNEL_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    # Provide the user with the link to access the stored file in the channel
    channel_link = f"https://t.me/c/{CHANNEL_ID.replace('-100', '')}/{forwarded_message.message_id}"
    await update.message.reply_text(f"Your file has been stored permanently. Access it [here]({channel_link}).", parse_mode="Markdown")

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
