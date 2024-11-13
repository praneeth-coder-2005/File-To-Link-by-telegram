import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import atexit

# Path for lock file to prevent multiple instances
LOCK_FILE_PATH = "/tmp/bot_lock_file"

def check_and_create_lock():
    """Checks for an existing lock file and creates one if it does not exist."""
    if os.path.exists(LOCK_FILE_PATH):
        print("Another instance is running. Exiting to prevent conflict.")
        sys.exit(0)  # Exit if another instance is running
    else:
        with open(LOCK_FILE_PATH, 'w') as lock_file:
            lock_file.write(str(os.getpid()))  # Write current process ID to lock file

def remove_lock_file():
    """Removes the lock file on exit."""
    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)

# Register the cleanup function to run on exit
atexit.register(remove_lock_file)

# Check and create lock at the start of the script
check_and_create_lock()

# Retrieve bot token from environment variables for security
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Base URL for the Render app, where files can be downloaded
RENDER_APP_URL = "https://file-to-link-by-telegram.onrender.com"  # Your Render app URL

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
    # Use filters.ALL to handle any document, photo, or video
    application.add_handler(MessageHandler(filters.ALL, file_handler))

    # Start polling to listen for messages
    application.run_polling()

if __name__ == '__main__':
    main()
