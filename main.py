import os
import dotenv
from telegram.ext import ApplicationBuilder
from telegram.error import InvalidToken
from handlers import handlers
from logger import logger

dotenv.load_dotenv()
bot_api_key = os.getenv("BOT_API_KEY")


def main():
    if bot_api_key is None:
        raise ValueError("BOT_API_KEY environment variable not set")

    try:
        application = ApplicationBuilder().token(bot_api_key).build()
        application.add_handlers(handlers)
        logger.info("Starting wolt bot")
        application.run_polling()
    except InvalidToken as e:
        logger.warning(f"Invalid Telegram API Key: {e}")
        return
    except ValueError as e:
        logger.error(f"An unknown error occurred: {e}")
        return


if __name__ == "__main__":
    main()
