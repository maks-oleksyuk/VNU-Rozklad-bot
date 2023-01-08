from aiogram import Dispatcher, types
from database.db import insert_update_user
from services.message import answer


async def cmd_start(message: types.Message):
    await answer(message, 'start', 'choice')
    await insert_update_user(message)


async def cmd_help(message: types.Message):
    await answer(message, 'help')
    await insert_update_user(message)


async def cmd_about(message: types.Message):
    await answer(message, 'about', disable_web_page_preview=True)
    await insert_update_user(message)


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_about, commands='about', chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_help, commands='help', chat_type=types.ChatType.PRIVATE)
