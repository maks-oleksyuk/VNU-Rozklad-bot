from config import get_column
from message import answer
from database import schedule_data, user_data
from timetable import schedule
from datetime import date
from aiogram import Dispatcher, types


async def today(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    if not id[0]:
        await answer(message, "not_data")
    else:
        await schedule(message, id[2], id)
        await user_data(message, "data", [id[0], id[1], id[2], date.today()])
        col = await get_column(date.today().weekday(), 0, 0)
        mes = await schedule_data(message, "get_col", [col, id[0]])
        await answer(message, "data", mes[0])


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(
        today, commands="today", chat_type=types.ChatType.PRIVATE
    )
