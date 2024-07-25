from telegram import Update
from telegram.ext import CallbackContext

user_started = {}


def check_start(func):
    async def wrapper(update: Update, context: CallbackContext):
        if (
            update.message is None
            or update.message.from_user is None
            or update.effective_chat is None
        ):
            return

        user_id = update.message.from_user.id if update.message else None
        if user_id and not user_started.get(user_id):
            await context.bot.send_message(
                update.effective_chat.id,
                "Please use the /start command first.",
            )
            return
        return await func(update, context)

    return wrapper
