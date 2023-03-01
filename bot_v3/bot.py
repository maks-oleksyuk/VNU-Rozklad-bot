from aiogram import executor

from src.commands.default import *
from src.config import logger


async def on_startup(dp):
    """A function that sends a message to the admin when the bot is started.

    Args:
        dp: A dispatcher instance used by the bot.
    """
    logger.info('Bot Started Successfully')


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        # on_shutdown=on_shutdown
    )
