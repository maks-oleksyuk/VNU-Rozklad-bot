from aiogram import types
from request import get_schedule
from database import schedule_data
from datetime import datetime, timedelta


async def schedule(message: types.Message, mode):
    # t = await schedule_data(message, "have_timetable")
    # if t:
    # print("yes")
    # else:
    ttable = []
    res = await get_schedule(message.text, mode)
    if res["psrozklad_export"]["code"] == "0":
        cd = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime(
            "%d.%m.%Y"
        )
        for d in range(1):
            for i in res["psrozklad_export"]["roz_items"]:
                if i["date"] == cd and i["lesson_number"] != "0":
                    print(i["title"])
