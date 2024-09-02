from telegram import Update
from telegram.ext import CallbackContext

user_started = {}


def check_start(func):
    """
    Decorator to ensure that the user has initiated the bot with the /start command before executing a function.

    This decorator checks if the current user has started the bot by using the /start command.
    If the user hasn't started the bot, it sends a message prompting them to use the /start command
    and prevents the execution of the wrapped function. If the user has started the bot,
    the wrapped function is executed as normal.

    Args:
        func (Callable): The function to be wrapped, which is expected to take an `update` and `context`
                         as arguments and perform some bot functionality.

    Returns:
        Callable: The wrapper function which checks the user's state and conditionally runs the original function.

    Example:
        @check_start
        async def my_command(update: Update, context: CallbackContext):
            # Command logic goes here
    """

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
