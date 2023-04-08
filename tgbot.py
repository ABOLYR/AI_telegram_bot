import config
import logging
import telegram_bot.handlers as handlers
from telegram.ext import ApplicationBuilder

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

if __name__ == '__main__':
    # You need to create config.py file in root directory and provide api key there
    token = config.TOKEN

    application = ApplicationBuilder().token(token).build()

    application.add_handler(handlers.conversation_handler)
    
    application.run_polling()
