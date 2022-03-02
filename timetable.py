from config import week
from config import get_group_id
from config import get_teacher_id
from aiogram import types
from request import get_schedule
from database import schedule_data
from datetime import datetime, timedelta


async def schedule(message: types.Message, mode, name):
    ND = datetime.now()
    NW = datetime.now().weekday()
    if mode == "group":
        id = await get_group_id(name)
        ttype = "🎓 *Розклад групи `" + id[1]
    if mode == "teacher":
        id = await get_teacher_id(name)
        ttype = "💼 *Розклад викладача `" + id[1]
    ttable = []
    res = await get_schedule(id[0], mode)
    if res["psrozklad_export"]["code"] == "0":
        for d in range(14):
            cd = (ND - timedelta(days=NW - d)).strftime("%d.%m.%Y")
            if d == 0 or d == 7:
                start_date = (ND - timedelta(days=NW - d)).strftime("%d.%m.%y")
                end_date = (ND - timedelta(days=NW - d - 6)).strftime("%d.%m.%y")
                week_message = ttype + "`\n🔹 з " + start_date + " по " + end_date + "*"
            item = []
            item = ttype + "`\n🔹 на " + cd + " (" + week[d] + ")*"
            lsn = 0
            has_item = 0
            for i in res["psrozklad_export"]["roz_items"]:
                if i["date"] == cd and i["lesson_number"] != "0":
                    if has_item != i["date"]:
                        has_item = i["date"]
                        week_message += (
                            "\n\n🔅 _*" + i["date"][:5] + " " + week[d] + "*_"
                        )
                    if lsn == i["lesson_number"]:
                        item += "\n"
                        week_message += "\n *✧* "
                    else:
                        item += (
                            "\n\n🔅 _"
                            + i["lesson_number"]
                            + " Пара ("
                            + i["lesson_time"][:5]
                            + " - "
                            + i["lesson_time"][6:]
                            + ")_\n"
                        )
                        week_message += "\n *" + i["lesson_number"] + ". *"
                    if i["reservation"]:
                        item += "📌 __*" + i["reservation"] + "*__"
                        week_message += i["reservation"]
                    if i["replacement"]:
                        item += "❗️ __*" + i["replacement"] + "*__ ❗️\n"
                    if i["title"]:
                        item += "📕 __*" + i["title"] + "*__"
                        week_message += i["title"]
                    if i["teacher"] and i["type"]:
                        item += "  _(" + i["teacher"] + "  |  " + i["type"] + ")_"
                    elif i["teacher"]:
                        item += "  _(" + i["teacher"] + ")_"
                    elif i["type"]:
                        item += "  _(" + i["type"] + ")_"
                    if i["room"] and i["group"]:
                        item += "\n👥 " + i["room"] + "  |  " + i["group"]
                    elif i["room"]:
                        item += "\n👥 " + i["room"]
                    elif i["group"]:
                        item += "\n👥 " + i["group"]
                    if mode == "group" and await has_need_group(i["group"]):
                        week_message += " | ___" + i["group"] + "_\r__"
                    if mode == "teacher":
                        week_message += " | ___" + i["group"] + "_\r__"
                    lsn = i["lesson_number"]
            if has_item == 0:
                item += "\n\n🎉 *Вітаю!* В тебе вихідний 😎"
            item = await multy_replase(item)
            await message.answer(item, parse_mode="MarkdownV2")
    else:
        week_message = "Данних не знайдено"
    week_message = await multy_replase(week_message)
    await message.answer(week_message, parse_mode="MarkdownV2")


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
        "|": "\|",
        "!": "\!",
    }
    transTable = txt.maketrans(characters)
    txt = txt.translate(transTable)
    return txt