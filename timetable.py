from datetime import date, datetime, time, timedelta

from aiogram import types

from config import get_teacher_full_name, multy_replase, week
from database import schedule_data
from request import get_schedule


async def schedule(message: types.Message, mode, id):
    """Forming the schedule and saving it

    Args:
        message (types.Message): message with additional data
        mode (str): type of schedule
        id (obj): data about the object for which the schedule is formed
    """
    # Variables for working with dates
    ND = date.today()
    NW = date.today().weekday()
    SD = ND - timedelta(days=NW)
    ED = ND - timedelta(days=NW - 13)
    # The header with the title
    if mode == "group":
        ttype = "🎓 *Розклад групи `" + id[1]
    if mode == "teacher":
        ttype = "💼 *Розклад викладача `" + id[1]
    # Forming an array and getting query
    schedule_arr = [id[0], id[1], mode, SD, ED]
    res = await get_schedule(id[0], mode)
    # Generation of the schedule on successful request
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
                    item = await add_lesson(item, i, lsn)
                    week_message = await add_week_lesson(week_message, i, lsn, mode)
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
    # Checking for data updates
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


async def schedule_for_the_date(message: types.Message, mode, tid, date):
    """Forming a message with a schedule for a specific date

    Args:
        message (types.Message): message with additional data
        mode (str): type of schedule
        tid (obj): data about the object for which the schedule is formed
        date (datetime): date on which to generate the schedule

    Returns:
        str: Messages schedule for the date
    """
    res = await get_schedule(tid[0], mode, date)
    if mode == "group":
        ttype = "🎓 *Розклад групи `" + tid[1]
    if mode == "teacher":
        ttype = "💼 *Розклад викладача `" + tid[1]
    mes = (
        ttype
        + "`\n🔹 на "
        + date.strftime("%d.%m.%Y")
        + " ("
        + week[date.weekday()]
        + ")*"
    )
    if (
        res["psrozklad_export"]["code"] == "0"
        and len(res["psrozklad_export"]["roz_items"]) != 0
    ):
        lsn = 0
        for i in res["psrozklad_export"]["roz_items"]:
            if i["date"] == date.strftime("%d.%m.%Y") and i["lesson_number"] != "0":
                mes = await add_lesson(mes, i, lsn)
                lsn = i["lesson_number"]
    else:
        mes += "\n\n🔺 Даних не знайдено!"
    mes = await multy_replase(mes)
    return mes


async def now_subject(message: types.Message, mode, tid):
    """Forming a message about the current lesson

    Args:
        message (types.Message): message with additional data
        mode (str): type of schedule
        tid (int): schedule identifier

    Returns:
        str: Message about the current lesson
    """
    res = await get_schedule(tid, mode, date.today())
    mes = ""
    has = 0
    if (
        res["psrozklad_export"]["code"] == "0"
        and len(res["psrozklad_export"]["roz_items"]) != 0
    ):
        name = res["psrozklad_export"]["roz_items"][0]["object"]
        if mode == "group":
            mes += "🎓 *Група* `" + name + "`\n"
        if mode == "teacher":
            mes += "💼 *Викладач* `" + name + "`\n"
        for i in res["psrozklad_export"]["roz_items"]:
            s = time.fromisoformat(i["lesson_time"][:5])
            n = datetime.now().time()
            e = time.fromisoformat(i["lesson_time"][6:])
            if s <= n and n <= e:
                has = 1
                if i["reservation"]:
                    mes += "\n📌 *" + i["reservation"] + "*"
                if i["replacement"]:
                    mes += "\n❗️ *" + i["replacement"] + "*"
                if i["title"]:
                    mes += "\n📕 *" + i["title"] + "*"
                if i["type"]:
                    mes += " _(" + i["type"] + ")_"
                if mode == "group":
                    if i["teacher"]:
                        teacher = await get_teacher_full_name(i["teacher"])
                        mes += "\n💼 " + teacher
                    if i["room"] and i["group"] and await has_need_group(i["group"]):
                        mes += "\n👥 " + i["room"] + "  |  " + i["group"]
                    elif i["room"]:
                        mes += "\n🔑 " + i["room"]
                    elif i["group"] and await has_need_group(i["group"]):
                        mes += "\n👥 " + i["group"]
                elif mode == "teacher":
                    if i["room"] and i["group"]:
                        mes += "\n👥 " + i["room"] + "  |  " + i["group"]
                    elif i["room"]:
                        mes += "\n🔑 " + i["room"]
                    elif i["group"]:
                        mes += "\n👥 " + i["group"]
                st = timedelta(hours=e.hour, minutes=e.minute)
                ed = timedelta(hours=n.hour, minutes=n.minute)
                left = st - ed
                mes += "\n*Залишилось* – `" + str(left)[:4] + "`_хв_"
    if not has:
        mes = "❕Зараз пари немає"
    mes = await multy_replase(mes)
    return mes


async def add_lesson(mes, ls, lsn):
    """Adding a schedule item to the week message

    Args:
        mes (str): the message of the weekly schedule
        ls (obj): data array about the timetable element
        lsn (str): item schedule number

    Returns:
        str: Message schedule with added element
    """
    if lsn == ls["lesson_number"]:
        mes += "\n"
    else:
        mes += (
            "\n\n🔅 _"
            + ls["lesson_number"]
            + " Пара ("
            + ls["lesson_time"].replace("-", " - ")
            + ")_\n"
        )
    if ls["reservation"]:
        mes += "📌 __*" + ls["reservation"] + "*__"
    if ls["replacement"]:
        mes += "❗️ *" + ls["replacement"] + "*\n"
    if ls["title"]:
        mes += "📕 __*" + ls["title"] + "*__"
    if ls["type"]:
        mes += "  _(" + ls["type"] + ")_"
    if ls["teacher"]:
        mes += "\n💼 _" + ls["teacher"] + "_"
    if ls["room"] and ls["group"]:
        mes += "\n👥 " + ls["room"] + "  |  " + ls["group"]
    elif ls["room"]:
        mes += "\n🔑 " + ls["room"]
    elif ls["group"]:
        mes += "\n👥 " + ls["group"]
    return mes


async def add_week_lesson(wmes, ls, lsn, mode):
    """Adding a schedule item to the week message

    Args:
        wmes (str): the message of the weekly schedule
        ls (obj): data array about the timetable element
        lsn (str): item schedule number
        mode (str): type of schedule

    Returns:
        str: Message schedule for the week with added element
    """
    if lsn == ls["lesson_number"]:
        wmes += "\n *⊙* "
    else:
        wmes += "\n *" + ls["lesson_number"] + ". *"
    if ls["reservation"]:
        wmes += ls["reservation"]
    if ls["title"]:
        wmes += ls["title"]
    if mode == "group" and await has_need_group(ls["group"]):
        wmes += " | ___" + ls["group"] + "_\r__"
    if mode == "teacher":
        wmes += " | ___" + ls["group"] + "_\r__"
    return wmes


async def has_need_group(txt):
    """Checking for specified elements in the text

    Args:
        txt str: Text to check

    Returns:
        bool: True if found and False if not
    """
    if (
        txt.find("підгр.") != -1
        or txt.find("част. групи") != -1
        or txt.find("Збірна група") != -1
    ):
        return True
    else:
        return False
