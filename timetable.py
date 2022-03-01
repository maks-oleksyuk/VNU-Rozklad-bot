from config import week
from aiogram import types
from request import get_schedule
from database import schedule_data
from datetime import datetime, timedelta

# Now date
ND = datetime.now()
# Now weekday number
NW = datetime.now().weekday()


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
            cd = (ND - timedelta(days=NW - d)).strftime("%d.%m.%Y")
            if d == 0 or d == 7:
                start_date = (
                    (ND - timedelta(days=NW - d))
                    .strftime("%d.%m.%y")
                    .replace(".", "\.")
                )
                end_date = (
                    (ND - timedelta(days=NW - d - 6))
                    .strftime("%d.%m.%y")
                    .replace(".", "\.")
                )
                week_message = (
                    ttype + name + "`\n🔹 з " + start_date + " по " + end_date + "*"
                )
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
                    if has_item != i["date"]:
                        has_item = i["date"]
                        week_message += (
                            "\n\n🔅 _*"
                            + i["date"][:5].replace(".", "\.")
                            + " "
                            + week[d]
                            + "*_"
                        )
                    week_message = await add_subject_week(week_message, i, mode)
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
                            "❗️ __*"
                            + await multy_replase(i["replacement"])
                            + "*__ ❗️\n"
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
    else:
        week_message = "Данних не знайдено"
    await message.answer(week_message, parse_mode="MarkdownV2")


async def add_subject_week(week_message, row, mode):
    week_message += "\n *" + row["lesson_number"] + "\.* "
    if row["title"]:
        week_message += await multy_replase(row["title"])
    if row["reservation"]:
        week_message += await multy_replase(row["reservation"])
    if mode == "group" and await has_need_group(row["group"]):
        week_message += " \| ___" + await multy_replase(row["group"]) + "_\r__"
    if mode == "teacher":
        week_message += " \| ___" + await multy_replase(row["group"]) + "_\r__"
    return week_message


async def has_need_group(txt):
    if (
        txt.find("част. групи") != -1
        or txt.find("підгр.") != -1
        or txt.find("4.1") != -1
        or txt.find("4.2") != -1
        or txt.find("4.3") != -1
        or txt.find("4.4") != -1
    ):
        return True
    else:
        return False


async def multy_replase(txt):
    txt = txt.replace(" (за професійним спрямуванням)", "")
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
