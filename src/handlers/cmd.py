from aiogram import Dispatcher, types
from services.message import answer


# -----------------------------------------------------------
# Implementation of basic command handlers
# -----------------------------------------------------------

async def start(message: types.Message):
    await answer(message, 'start')
    # await user_data(message, "save", None)


async def help(message: types.Message):
    await answer(message, "help")


async def about(message: types.Message):
    await answer(message, "about")


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(help, commands="help", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(about, commands="about", chat_type=types.ChatType.PRIVATE)
