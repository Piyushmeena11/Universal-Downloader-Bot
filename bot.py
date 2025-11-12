#!/usr/bin/env python3
import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import Config
from handlers.start import start, help_command, stats_command
from handlers.download import handle_download
from handlers.admin import admin_stats, broadcast

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("admin", admin_stats))
    application.add_handler(CommandHandler("broadcast", broadcast))
    
    # Handle text messages (URLs)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_download))

    # Start the Bot
    if Config.APP_URL:  # Webhook for Heroku
        PORT = int(os.environ.get('PORT', Config.PORT))
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=Config.BOT_TOKEN,
            webhook_url=f"{Config.APP_URL}/{Config.BOT_TOKEN}"
        )
    else:  # Polling for local development
        application.run_polling()

if __name__ == '__main__':
    # Create downloads directory
    os.makedirs('downloads', exist_ok=True)
    main()