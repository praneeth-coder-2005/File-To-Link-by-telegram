from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os
import logging

# Retrieve bot token and channel/chat ID from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Use your channel ID for permanent storage

# Set up Render webhook URL
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Replace with your actual Render URL
WEBHOOK_URL = f"{RENDER_APP_URL}/webhook/{BOT_TOKEN}"  # Webhook URL for Telegram to send updates

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! Send me a file, and I'll store it permanently in our channel.")

async def file_handler(update: Update, context: CallbackContext) -> None:
    """Handle received files and provide the Render link for retrieval."""
    file = update.message.document or update.message.video or update.message.photo[-1]
    if not file:
        await update.message.reply_text("Please send a file.")
        return

    # Store the file_id and give a Render-based URL for retrieval
    file_id = file.file_id
    render_link = f"{RENDER_APP_URL}/redirect/{file_id}"
    await update.message.reply_text(f"Access your file [here]({render_link})", parse_mode="Markdown")

async def retrieve_file(update: Update, context: CallbackContext) -> None:
    """Retrieve and send the file based on the command."""
    # Extract file_id from the command
    command = update.message.text
    file_id = command.split('_')[-1]

    # Send the file back to the user
    await context.bot.send_document(chat_id=update.message.chat_id, document=file_id)

def main():
    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command and file handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, file_handler))
    application.add_handler(MessageHandler(filters.Regex(r"^/get_file_"), retrieve_file))  # Listen for file retrieval

    # Set the webhook for the application
    application.run_webhook(
        listen="0.0.0.0",
        port=443,
        url_path=f"webhook/{BOT_TOKEN}",
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()
