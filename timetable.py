from config import week
from aiogram import types
from request import get_schedule
from database import schedule_data
from datetime import datetime, timedelta


async def schedule(message: types.Message, mode):
    # t = await schedule_data(message, "have_timetable")
    # if t:
    # print("yes")
    # else:
    if mode == "group":
        ttype = "🎓 *Розклад групи __"
    if mode == "teacher":
        ttype = "🎓 *Розклад викладача __"
    ttable = []
    res = await get_schedule(message.text, mode)
    if res["psrozklad_export"]["code"] == "0":
        if res["psrozklad_export"]["roz_items"][0]["object"]:
            name = (
                res["psrozklad_export"]["roz_items"][0]["object"]
                .replace("-", "\-")
                .replace("(", "\(")
                .replace(")", "\)")
            )
        else:
            name = message.text.replace("-", "\-").replace("(", "\(").replace(")", "\)")
        for d in range(6):
            cd = (
                datetime.now() - timedelta(days=datetime.now().weekday() - d)
            ).strftime("%d.%m.%Y")
            title = []
            title = (
                ttype
                + name
                + "__\n🔹 на "
                + cd.replace(".", "\.")
                + " \("
                + week[d]
                + "\)*\n"
            )
            for i in res["psrozklad_export"]["roz_items"]:
                if i["date"] == cd and i["lesson_number"] != "0":
                    title += (
                        "\n🔅 _"
                        + i["lesson_number"]
                        + " Пара \("
                        + i["lesson_time"].replace("-", " \- ")
                        + "\)_\n__*"
                    )
                    if i["reservation"]:
                        title += i["reservation"] + "\n"
                    if i["replacement"]:
                        title += (
                            "‼️ "
                            + i["replacement"]
                            .replace("!", "\!")
                            .replace(".", "\.")
                            .replace(":", "\:")
                            + "‼️\n"
                        )
                    if i["title"]:
                        title += (
                            i["title"]
                            .replace("(", "\(")
                            .replace(")", "\)")
                            .replace("-", "\-")
                            + " "
                        )
                    title += "\(" + i["type"] + "\)*__"
            await message.answer(title, parse_mode="MarkdownV2")
