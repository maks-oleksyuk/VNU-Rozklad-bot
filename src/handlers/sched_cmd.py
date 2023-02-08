from datetime import date, timedelta

from aiogram import Dispatcher, types
from bot.config import get_column
from bot.message import answer
from bot.database import schedule_data, user_data
from bot.timetable import now_subject, schedule, schedule_for_the_date


async def now(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] != None:
            mes = await now_subject(message, id[2], id[0])
            await answer(message, "data", mes)
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data")


# async def today(message: types.Message):
#     id = await user_data(message, "get_data_id", None)
#     try:
#         if id[0] != None:
#             await schedule(message, id[2], id)
#             await user_data(message, "data", [id[0], id[1], id[2], date.today()])
#             col = await get_column(date.today().weekday(), 0, 0)
#             mes = await schedule_data(message, "get_col", [col, id[0]])
#             await answer(message, "data", mes[0])
#         else:
#             await answer(message, "no-data")
#     except:
#         await answer(message, "no-data")


async def tomorrow(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] != None:
            await schedule(message, id[2], id)
            user_date = date.today() + timedelta(days=1)
            await user_data(message, "data", [id[0], id[1], id[2], id[3]])
            if user_date.weekday() == 0:
                col = await get_column(user_date.weekday(), 0, 1)
            else:
                col = await get_column(user_date.weekday(), 0, 0)
            mes = await schedule_data(message, "get_col", [col, id[0]])
            await answer(message, "data", mes[0])
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data", None)


async def week(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] != None:
            await schedule(message, id[2], id)
            await user_data(message, "data", [id[0], id[1], id[2], id[3]])
            col = await get_column(None, 1, 0)
            mes = await schedule_data(message, "get_col", [col, id[0]])
            await answer(message, "data", mes[0])
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data", None)


async def nextweek(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] != None:
            await schedule(message, id[2], id)
            await user_data(message, "data", [id[0], id[1], id[2], id[3]])
            col = await get_column(None, 1, 1)
            mes = await schedule_data(message, "get_col", [col, id[0]])
            await answer(message, "data", mes[0])
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data", None)


async def changeweek(message: types.Message, type):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] != None:
            if type == "next":
                SD = id[3] + timedelta(weeks=1)
            elif type == "prev":
                SD = id[3] - timedelta(weeks=1)
            message.text = "🔘"
            await user_data(message, "data", [id[0], id[1], id[2], SD])
            await get_day_timetable(message, SD)
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data", None)


async def get_day_timetable(message: types.Message, date):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] != None:
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
            if message.text == "🔘":
                SD = id[3]
                day = days[message.text]
            if date:
                SD = date
                day = date.weekday()
            else:
                day = days[message.text]
                SD = id[3] - timedelta(id[3].weekday()) + timedelta(days=day)
            res = await schedule_data(None, "get_date", id[0])
            if SD >= res[0] and SD <= res[1]:
                await user_data(message, "data", [id[0], id[1], id[2], SD])
                if SD - res[0] < timedelta(days=7):
                    col = await get_column(day, 0, 0)
                else:
                    col = await get_column(day, 0, 1)
                mes = await schedule_data(message, "get_col", [col, id[0]])
                await answer(message, "data", mes[0])
            else:
                mes = await schedule_for_the_date(message, id[2],
                                                  [id[0], id[1]], SD)
                await user_data(message, "data", [id[0], id[1], id[2], SD])
                await answer(message, "data", mes)
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data")


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(now, commands="now",
                                chat_type=types.ChatType.PRIVATE)
    # dp.register_message_handler(
    #     today, commands="today", chat_type=types.ChatType.PRIVATE
    # )
    dp.register_message_handler(
        tomorrow, commands="tomorrow", chat_type=types.ChatType.PRIVATE
    )
    dp.register_message_handler(week, commands="week",
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(
        nextweek, commands="nextweek", chat_type=types.ChatType.PRIVATE
    )
