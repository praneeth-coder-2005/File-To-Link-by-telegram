from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters
import os
import logging

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Use the full channel ID with "-100..."
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Replace with your Render URL

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    """Welcome message for /start command."""
    await update.message.reply_text("Hello! Send me a file, and I'll store it in our channel with a link for access.")

async def file_handler(update: Update, context: CallbackContext) -> None:
    """Handle files and forward them to the channel."""
    file = update.message.document or update.message.video or update.message.photo[-1]
    if not file:
        await update.message.reply_text("Please send a valid file.")
        return

    # Forward the file to the designated channel
    forwarded_message = await context.bot.forward_message(
        chat_id=CHANNEL_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    # Generate Render-based link for access
    access_link = f"{RENDER_APP_URL}/redirect/{forwarded_message.message_id}"
    await update.message.reply_text(f"Your file has been stored permanently. Access it [here]({access_link})", parse_mode="Markdown")

def main():
    # Initialize the bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command and file handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, file_handler))

    # Run the bot with polling (webhook can be added if preferred)
    application.run_polling()

if __name__ == '__main__':
    main()
