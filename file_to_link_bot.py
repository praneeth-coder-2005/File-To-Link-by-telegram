from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os
import logging
import requests

# Set up bot token and Render app URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Replace with your Render URL
WEBHOOK_URL = f"{RENDER_APP_URL}/webhook/{BOT_TOKEN}"

# Configure logging
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
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
    await update.message.reply_text(f"Your file has been stored. Access it [here]({retrieval_link})", parse_mode="Markdown")

def clear_webhook():
    """Clear any existing webhook to prevent conflicts."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Existing webhook cleared successfully.")
    else:
        logging.error(f"Failed to clear existing webhook: {response.text}")

def set_webhook():
    """Set the webhook for the bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})

    if response.status_code == 200:
        logging.info("Webhook set successfully.")
    else:
        logging.error(f"Failed to set webhook: {response.text}")

def main():
    # Clear any existing webhook to ensure only one instance is active
    clear_webhook()
    # Set the new webhook
    set_webhook()

    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command and file handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, file_handler))

    # Run only webhook, no polling fallback
    application.run_webhook(
        listen="0.0.0.0",
        port=443,
        url_path=f"webhook/{BOT_TOKEN}",
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()
