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
                    if i["room"] and i["group"] and await has_need_group(
                            i["group"]):
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
