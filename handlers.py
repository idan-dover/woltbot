from telegram import Location, Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
from constants import RESTAURANT
from decorators import check_start, user_started
from logger import logger
from wolt_exception import WoltException
from wolt_services import is_restaurant_open

restaurant_index: int | None = None
restaurant_is_open: bool | str = False
lat: float | None = None
lon: float | None = None

restaurant_list = "\n".join(
    [f"{i+1}. {name}" for i, name in enumerate(RESTAURANT.keys())]
)


async def handle_start(update: Update, context: CallbackContext) -> None:
    """
    Handle the bot's /start command. This function should be used with the command handler.

    Args:
        update (telegram.Update): Contains information about the incoming update.
        context (telegram.ext.CallbackContext): Provides context for the command, including the bot instance
    Returns:
        None: This function does not return a value.
    """
    user = update.message.from_user
    user_started[user.id] = True
    message = f"Hi {user.first_name}, Which restaurant should we check for you?\n{restaurant_list}"
    await context.bot.send_message(update.effective_chat.id, message)


@check_start
async def handle_location(update: Update, context: CallbackContext) -> None:
    """
    Handle the users location messages. This function should be used with the message handler.

    Args:
        update (telegram.Update): Contains information about the incoming update.
        context (telegram.ext.CallbackContext): Provides context for the command, including the bot instance
    Returns:
        None: This function does not return a value
    """
    global restaurant_is_open, lat, lon
    location: Location | None = (
        update.message.location
        if update.message
        else update.edited_message.location
        if update.edited_message
        else None
    )

    if location is None:
        return

    lat = location.latitude
    lon = location.longitude

    if restaurant_index is None:
        await context.bot.send_message(
            update.effective_chat.id,
            f"Received your location: {lat}, {lon}, now choose your restaurant\n{restaurant_list}",
        )
        return

    restaurant_name = list(RESTAURANT.keys())[restaurant_index]
    restaurant_id = RESTAURANT[restaurant_name]
    if restaurant_is_open:
        restaurant_is_open = is_restaurant_open(restaurant_id, lat, lon)
        return

    try:
        restaurant_is_open = is_restaurant_open(restaurant_id, lat, lon)
    except WoltException as e:
        logger.info(f"Was not able to retrieve data from wolt api: {e}")
        await context.bot.send_message(
            update.effective_chat.id,
            "oops, seems like we had some issues getting the data, try to send your location again",
        )

    await context.bot.send_message(
        update.effective_chat.id,
        f"{restaurant_name} is {"open" if restaurant_is_open else "close"}",
    )


@check_start
async def handle_restaurant_selection(update: Update, context: CallbackContext) -> None:
    """
    Handle the users text messages. This function should be used with the message handler. It will only trigger when after the user used /start and it will pick the restaurant from the given list

    Args:
        update (telegram.Update): Contains information about the incoming update.
        context (telegram.ext.CallbackContext): Provides context for the command, including the bot instance
    Returns:
        None: This function does not return a value
    """
    global restaurant_is_open, restaurant_index, lat, lon

    if update.message.text is None or not update.message.text.isdigit():
        await context.bot.send_message(
            update.effective_chat.id,
            "Please send a number corresponding to the list above",
        )
        return

    restaurant_index = int(update.message.text) - 1
    if restaurant_index < 0 or restaurant_index >= len(RESTAURANT):
        restaurant_index = None
        await context.bot.send_message(
            update.effective_chat.id,
            f"Please choose a number between 1 to {len(RESTAURANT)}",
        )
        return

    if lat is None or lon is None:
        await context.bot.send_message(
            update.effective_chat.id,
            "Great, now send me your location",
        )
        return

    restaurant_name = list(RESTAURANT.keys())[restaurant_index]
    restaurant_id = RESTAURANT[restaurant_name]
    try:
        restaurant_is_open = is_restaurant_open(restaurant_id, lat, lon)
    except WoltException as e:
        logger.info(f"Was not able to retrieve data from wolt api: {e}")
        await context.bot.send_message(
            update.effective_chat.id,
            "oops, seems like we had some issues getting the data, try to send your location again",
        )

    await context.bot.send_message(
        update.effective_chat.id,
        f"{restaurant_name} is {"open" if restaurant_is_open else "close"}",
    )


handlers = [
    CommandHandler("start", handle_start),
    MessageHandler(filters.LOCATION, handle_location),
    MessageHandler(filters.TEXT, handle_restaurant_selection),
]
