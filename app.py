from datetime import date

from aiogram import executor, Dispatcher

from loader import dp, db, api, logger


async def on_startup(dp: Dispatcher) -> None:
    """A function that sends a message to the admin when the bot is started.

    Args:
        dp: A dispatcher instance used by the bot.
    """
    # Update the tables on the 1st day of each month, or if they are missing data.
    if await db._table_is_empty('groups') or date.today().day == 1:
        await api.get_groups()
    if await db._table_is_empty('teachers') or date.today().day == 1:
        await api.get_teachers()
    logger.info('Bot Started Successfully')


if __name__ == '__main__':
    from bot import commands

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        # on_shutdown=on_shutdown
    )
