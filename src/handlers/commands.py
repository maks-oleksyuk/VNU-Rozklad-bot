from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from database.db import insert_update_user
from services.message import answer


async def cmd_start(message: types.Message):
    """ Conversation's entry point """
    await answer(message, 'start', 'choice')
    await insert_update_user(message)


async def cmd_help(message: types.Message):
    await answer(message, 'help')
    await insert_update_user(message)


async def cmd_about(message: types.Message):
    await answer(message, 'about', disable_web_page_preview=True)
    await insert_update_user(message)


async def cmd_cancel(message: types.Message, state: FSMContext = None):
    """ Allow user to cancel any action """
    if state:
        await state.finish()
    await insert_update_user(message)
    await answer(message, 'choice', 'choice')


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_about, commands='about',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_help, commands='help',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_cancel, commands='cancel',
                                chat_type=types.ChatType.PRIVATE, state='*')
