from aiogram import executor, Dispatcher

from loader import dp, api, logger


async def on_startup(dp: Dispatcher) -> None:
    """A function that sends a message to the admin when the bot is started.

    Args:
        dp: A dispatcher instance used by the bot.
    """
    await api.get_groups()
    logger.info('Bot Started Successfully')


if __name__ == '__main__':
    from bot import commands

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        # on_shutdown=on_shutdown
    )
