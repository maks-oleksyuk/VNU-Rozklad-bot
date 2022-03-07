from config import week
from aiogram import types
from request import get_schedule
from database import schedule_data
from datetime import timedelta, date


async def schedule(message: types.Message, mode, id):

    ND = date.today()
    NW = date.today().weekday()
    SD = ND - timedelta(days=NW)
    ED = ND - timedelta(days=NW - 13)

    if mode == "group":
        ttype = "🎓 *Розклад групи `" + id[1]
    if mode == "teacher":
        ttype = "💼 *Розклад викладача `" + id[1]

    schedule_arr = [id[0], id[1], mode, SD, ED]
    res = await get_schedule(id[0], mode, None, None)

    if (
        res["psrozklad_export"]["code"] == "0"
        and len(res["psrozklad_export"]["roz_items"]) != 0
    ):
        schedule_arr.append(True)
        for d in range(14):
            cd = (ND - timedelta(days=NW - d)).strftime("%d.%m.%Y")
            if d == 0 or d == 7:
                end_date = (ND - timedelta(days=NW - d - 6)).strftime("%d.%m.%y")
                week_message = ttype + "`\n🔹 з " + cd + " по " + end_date + "*"
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
                            + i["lesson_time"].replace("-", " - ")
                            + ")_\n"
                        )
                        week_message += "\n *" + i["lesson_number"] + ". *"
                    if i["reservation"]:
                        item += "📌 __*" + i["reservation"] + "*__"
                        week_message += i["reservation"]
                    if i["replacement"]:
                        item += "❗️ __*" + i["replacement"] + "*__❗️\n"
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
            schedule_arr.append(item)
            if d == 6 or d == 13:
                week_message = await multy_replase(week_message)
                schedule_arr.append(week_message)
    else:
        schedule_arr.append(False)

    res = await schedule_data(message, "check", schedule_arr)
    if not res:
        await schedule_data(message, "save", schedule_arr)
    elif (
        schedule_arr[5]
        or (not schedule_arr[5] and res[6] and SD > res[5])
        or (not schedule_arr[5] and res[6] and SD == res[4])
    ):
        await schedule_data(message, "update", schedule_arr)
    elif not schedule_arr[5] and res[6] and SD < res[5] and SD > res[4]:
        await schedule_data(message, "week_update", schedule_arr)


async def has_need_group(txt):
    if (
        txt.find("підгр.") != -1
        or txt.find("част. групи") != -1
        or txt.find("Збірна група") != -1
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
