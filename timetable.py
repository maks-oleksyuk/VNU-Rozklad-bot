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
        ttype = "🎓 *Розклад групи `"
    if mode == "teacher":
        ttype = "🎓 *Розклад викладача __"
    ttable = []
    res = await get_schedule(message.text, mode)
    if res["psrozklad_export"]["code"] == "0":
        try:
            name = (
                res["psrozklad_export"]["roz_items"][0]["object"]
                .replace("-", "\-")
                .replace("(", "\(")
                .replace(")", "\)")
            )
        except IndexError:
            name = message.text.replace("-", "\-").replace("(", "\(").replace(")", "\)")
        for d in range(7):
            cd = (
                datetime.now() - timedelta(days=datetime.now().weekday() - d)
            ).strftime("%d.%m.%Y")
            item = []
            item = (
                ttype
                + name
                + "`\n🔹 на "
                + cd.replace(".", "\.")
                + " \("
                + week[d]
                + "\)*"
            )
            for i in res["psrozklad_export"]["roz_items"]:
                if i["date"] == cd and i["lesson_number"] != "0":
                    item += (
                        "\n\n🔅 _"
                        + i["lesson_number"]
                        + " Пара \("
                        + i["lesson_time"].replace("-", " \- ")
                        + "\)_\n"
                    )
                    if i["reservation"]:
                        item += "📌 __*" + i["reservation"] + "*__"
                    if i["replacement"]:
                        item += (
                            "‼️ __*"
                            + i["replacement"]
                            .replace("!", "\!")
                            .replace(".", "\.")
                            .replace(":", "\:")
                            + "*__ ‼️\n"
                        )
                    if i["title"]:
                        item += (
                            "📌 __*"
                            + i["title"]
                            .replace("(", "\(")
                            .replace(")", "\)")
                            .replace("-", "\-")
                            .replace(".", "\.")
                            + "*__"
                        )
                    if i["teacher"] and i["type"]:
                        item += (
                            "  _\("
                            + i["teacher"]
                            .replace(".", "\.")
                            .replace("-", "\-")
                            .replace("(", "\(")
                            .replace(")", "\)")
                            + "  \|  "
                            + i["type"]
                            + "\)_"
                        )
                    elif i["teacher"]:
                        item += (
                            "  _\("
                            + i["teacher"]
                            .replace(".", "\.")
                            .replace("-", "\-")
                            .replace("(", "\(")
                            .replace(")", "\)")
                            + "\)_"
                        )
                    elif i["type"]:
                        item += "  _\(" + i["type"] + "\)_"
                    if i["room"] and i["group"]:
                        item += (
                            "\n👥 "
                            + i["room"].replace("-", "\-").replace(".", "\.")
                            + "  \|  "
                            + i["group"]
                            .replace(".", "\.")
                            .replace("-", "\-")
                            .replace("(", "\(")
                            .replace(")", "\)")
                            .replace("+", "\+")
                        )
                    elif i["room"]:
                        item += "\n👥 " + i["room"].replace("-", "\-").replace(".", "\.")
                    elif i["group"]:
                        item += "\n👥 " + i["group"].replace(".", "\.").replace(
                            "-", "\-"
                        ).replace("(", "\(").replace(")", "\)").replace("+", "\+")
            await message.answer(item, parse_mode="MarkdownV2")
