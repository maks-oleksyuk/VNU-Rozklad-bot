from config import week
from aiogram import types
from request import get_schedule
from database import schedule_data
from datetime import datetime, timedelta


async def schedule(message: types.Message, mode):
    if mode == "group":
        ttype = "🎓 *Розклад групи `"
    if mode == "teacher":
        ttype = "🎓 *Розклад викладача `"
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
        for d in range(14):
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
            has_item = 0
            for i in res["psrozklad_export"]["roz_items"]:
                if i["date"] == cd and i["lesson_number"] != "0":
                    has_item = 1
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
                            + await multy_replase(i["replacement"])
                            + "*__ ‼️\n"
                        )
                    if i["title"]:
                        item += "📕 __*" + await multy_replase(i["title"]) + "*__"
                    if i["teacher"] and i["type"]:
                        item += (
                            "  _\("
                            + await multy_replase(i["teacher"])
                            + "  \|  "
                            + i["type"]
                            + "\)_"
                        )
                    elif i["teacher"]:
                        item += "  _\(" + await multy_replase(i["teacher"]) + "\)_"
                    elif i["type"]:
                        item += "  _\(" + i["type"] + "\)_"
                    if i["room"] and i["group"]:
                        item += (
                            "\n👥 "
                            + await multy_replase(i["room"])
                            + "  \|  "
                            + await multy_replase(i["group"])
                        )
                    elif i["room"]:
                        item += "\n👥 " + await multy_replase(i["room"])
                    elif i["group"]:
                        item += "\n👥 " + await multy_replase(i["group"])
            if has_item == 0:
                item += "\n\n🎉 *Вітаю\!* В тебе вихідний 😎"

            await message.answer(item, parse_mode="MarkdownV2")


async def multy_replase(txt):
    characters = {
        ".": "\.",
        ":": "\:",
        "-": "\-",
        "+": "\+",
        "(": "\(",
        ")": "\)",
        "!": "\!",
    }
    transTable = txt.maketrans(characters)
    txt = txt.translate(transTable)
    return txt
