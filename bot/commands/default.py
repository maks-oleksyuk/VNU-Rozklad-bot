from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from loader import dp, db
from ..states.set_date import cmd_cancel_date
from ..utils.messages import answer


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message) -> types.Message:
    """Handler function for the `/start` command.

    Args:
        message: The message sent by the user.
    """
    await db.insert_update_user(message)
    return await answer(message, 'start', 'choice')


@dp.message_handler(CommandHelp())
async def cmd_help(message: types.Message) -> types.Message:
    """Handler function for the `/help` command.

    Args:
        message: The message sent by the user.
    """
    await db.insert_update_user(message)
    return await answer(message, 'help')


@dp.message_handler(commands=['about'])
async def cmd_about(message: types.Message) -> types.Message:
    """Handler function for the `/about` command.

    Args:
        message: The message sent by the user.
    """
    await db.insert_update_user(message)
    return await answer(message, 'about')


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext = None) -> types.Message:
    """Handler function for the `/cancel` command, allow cancel any action.

    Args:
        message: The message sent by the user.
        state: An optional argument for the finite state machine context.
    """
    if state:
        await state.finish()
    await db.insert_update_user(message)
    return await answer(message, 'choice', 'choice')
