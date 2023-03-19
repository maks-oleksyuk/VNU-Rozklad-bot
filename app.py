from datetime import date

from aiogram import Dispatcher, executor

from data.config import ADMIN_ID
from loader import api, bot, db, dp, logger, add_over_room


async def on_startup(dp: Dispatcher) -> None:
    """A function that sends a message to the admin when the bot is started.

    Args:
        dp: A dispatcher instance used by the bot.
    """
    today = date.today()
    # Update the tables on the 1st day of each month, or if they are missing data.
    if await db._table_is_empty('groups') or today.day == 1:
        await api.get_groups()
    if await db._table_is_empty('teachers') or today.day == 1:
        await api.get_teachers()

    if await db._table_is_empty('audiences') or today.day == 1:
        rooms = await api.get_audiences()
        if rooms:
            await db.save_audiences(rooms)

        additions_rooms_data = await api.get_free_rooms()
        if additions_rooms_data:
            additions_rooms_data = await add_over_room(additions_rooms_data)
            await db.update_additions_to_audiences(additions_rooms_data)

    await bot.send_message(chat_id=ADMIN_ID, text='Bot started', disable_notification=True)
    logger.info('Bot Started Successfully')


async def on_shutdown(dp: Dispatcher) -> None:
    await db._close()
    # await bot.send_message(chat_id=ADMIN_ID, text='Bot stopped', disable_notification=True)
    logger.info('Bot Stopped')


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
