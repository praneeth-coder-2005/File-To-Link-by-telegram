import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Path for lock file to prevent multiple instances
LOCK_FILE_PATH = "/tmp/bot_lock_file"

# Check for lock file
if os.path.exists(LOCK_FILE_PATH):
    print("Another instance is running. Exiting...")
    sys.exit(0)  # Exit if another instance is running
else:
    open(LOCK_FILE_PATH, 'w').close()  # Create lock file

# Remove lock file on exit
import atexit
def remove_lock_file():
    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)
atexit.register(remove_lock_file)

# Retrieve bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Base URL for the Render app
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! Send me a file, and I'll generate a download link for you.")

async def file_handler(update: Update, context: CallbackContext) -> None:
    file = update.message.document or update.message.video or update.message.photo[-1]
    if not file:
        await update.message.reply_text("Please send a file.")
        return
    file_id = file.file_id
    download_link = f"{RENDER_APP_URL}/download/{file_id}"
    await update.message.reply_text(f"Here is your download link:\n{download_link}")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, file_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
