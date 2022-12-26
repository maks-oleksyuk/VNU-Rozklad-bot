from aiogram import Dispatcher, types
from message import answer


async def help(message: types.Message):
    await answer(message, "help")


async def about(message: types.Message):
    await answer(message, "about")


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(help, commands="help", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(
        about, commands="about", chat_type=types.ChatType.PRIVATE
    )
