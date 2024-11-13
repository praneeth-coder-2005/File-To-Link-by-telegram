from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os
import logging

# Set up bot token and Render app URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Replace with your actual Render URL
WEBHOOK_URL = f"{RENDER_APP_URL}/webhook/{BOT_TOKEN}"

# Configure logging
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message."""
    await update.message.reply_text("Hello! Send me a file, and I'll give you a download link.")

async def file_handler(update: Update, context: CallbackContext) -> None:
    """Handle files sent by users and provide a link for retrieval."""
    file = update.message.document or update.message.video or update.message.photo[-1]
    if not file:
        await update.message.reply_text("Please send a file.")
        return

    # Store the file_id and respond with the Render URL for retrieval
    file_id = file.file_id
    retrieval_link = f"{RENDER_APP_URL}/redirect/{file_id}"
    await update.message.reply_text(f"Access your file [here]({retrieval_link})", parse_mode="Markdown")

def main():
    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers for start and file messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, file_handler))

    # Set the webhook for the application, ensuring persistence
    application.run_webhook(
        listen="0.0.0.0",
        port=443,
        url_path=f"webhook/{BOT_TOKEN}",
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()
