from aiogram import types
from database import timetable_data
from request import get_timetable


async def timetable(message: types.Message, mode):
    t = await timetable_data(message, "have_timetable")
    if t:
        print("yes")
    else:
        await get_timetable(message.text, mode)
        print("no")
