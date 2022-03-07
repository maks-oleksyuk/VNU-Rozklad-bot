from config import get_column
from message import answer
from database import schedule_data, user_data
from timetable import schedule
from datetime import date, timedelta
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


async def tomorrow(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    if not id[0]:
        await answer(message, "not_data")
    else:
        await schedule(message, id[2], id)
        user_date = date.today() + timedelta(days=1)
        await user_data(message, "data", [id[0], id[1], id[2], id[3]])
        col = await get_column(user_date.weekday(), 0, 0)
        mes = await schedule_data(message, "get_col", [col, id[0]])
        await answer(message, "data", mes[0])


async def week(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    if not id[0]:
        await answer(message, "not_data")
    else:
        await schedule(message, id[2], id)
        await user_data(message, "data", [id[0], id[1], id[2], id[3]])
        col = await get_column(None, 1, 0)
        mes = await schedule_data(message, "get_col", [col, id[0]])
        await answer(message, "data", mes[0])


async def nextweek(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    if not id[0]:
        await answer(message, "not_data")
    else:
        await schedule(message, id[2], id)
        await user_data(message, "data", [id[0], id[1], id[2], id[3]])
        col = await get_column(None, 1, 1)
        mes = await schedule_data(message, "get_col", [col, id[0]])
        await answer(message, "data", mes[0])


async def get_day_timetable(message: types.Message, date):
    id = await user_data(message, "get_data_id", None)
    if not id[0]:
        await answer(message, "not_data")
    else:
        text = message.text
        days = {
            "Пн": 0,
            "Вт": 1,
            "Ср": 2,
            "Чт": 3,
            "Пт": 4,
            "Сб": 5,
            "Нд": 6,
            "🔘": id[3].weekday(),
        }
        if text == "🔘":
            SD = id[3]
        else:
            SD = id[3] - timedelta(id[3].weekday()) + timedelta(days=days[text])
        res = await schedule_data(None, "get_date", id[0])
        if SD >= res[0] and SD <= res[1]:
            await user_data(message, "data", [id[0], id[1], id[2], SD])
            if SD - res[0] > timedelta(days=6):
                col = await get_column(days[text], 0, 0)
            else:
                col = await get_column(days[text], 0, 1)
            mes = await schedule_data(message, "get_col", [col, id[0]])
            await answer(message, "data", mes[0])
        else:
            print("not data")


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(
        today, commands="today", chat_type=types.ChatType.PRIVATE
    )
    dp.register_message_handler(
        tomorrow, commands="tomorrow", chat_type=types.ChatType.PRIVATE
    )
    dp.register_message_handler(week, commands="week", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(
        nextweek, commands="nextweek", chat_type=types.ChatType.PRIVATE
    )
