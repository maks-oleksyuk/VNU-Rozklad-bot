from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from ..config import dp
from ..utils.messages import answer


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    """Handler function for the `/start` command.

    Args:
        message (types.Message): object representing the message sent by the user.
    """
    await answer(message, 'start')
