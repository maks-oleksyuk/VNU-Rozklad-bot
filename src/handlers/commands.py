from aiogram import Dispatcher, types
from services.message import answer


async def cmd_start(message: types.Message):
    await answer(message, 'start')
    # await user_data(message, "save", None)


async def cmd_help(message: types.Message):
    await answer(message, 'help')


async def cmd_about(message: types.Message):
    await answer(message, 'about')


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_about, commands='about', chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_help, commands='help', chat_type=types.ChatType.PRIVATE)
