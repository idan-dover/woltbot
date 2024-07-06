import os
import dotenv
from telegram.ext import ApplicationBuilder
from handlers import handlers

dotenv.load_dotenv()
bot_api_key = os.getenv("BOT_API_KEY")


def main():
    application = ApplicationBuilder().token(bot_api_key).build()
    application.add_handlers(handlers)
    application.run_polling()


main()
