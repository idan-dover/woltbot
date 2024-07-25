import os
import dotenv
from telegram.ext import ApplicationBuilder
from handlers import handlers

dotenv.load_dotenv()
bot_api_key = os.getenv("BOT_API_KEY")


def main():
    if bot_api_key is None:
        raise ValueError("BOT_API_KEY environment variable not set")

    application = ApplicationBuilder().token(bot_api_key).build()
    application.add_handlers(handlers)
    print("Starting wolt bot")
    application.run_polling()


if __name__ == "__main__":
    main()
