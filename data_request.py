# Запит на сервер

import datetime
import requests


def get(teacher=None, group=None, spec_date=None, id=None):

    # Кодування за присутності
    if teacher:
        teacher = teacher.encode("Windows 1251")
    elif group:
        group = group.encode("Windows 1251")

    # Розрахунок дати
    if spec_date == None:
        sdate = (
            datetime.date.today()
            - datetime.timedelta(days=datetime.date.today().weekday())
        ).strftime("%d.%m.%Y")
        edate = (
            datetime.date.today()
            + datetime.timedelta(days=6 - datetime.date.today().weekday())
        ).strftime("%d.%m.%Y")

    else:
        if type(spec_date) == datetime.date:
            sd = spec_date
        else:
            print(type(spec_date))
            sd = datetime.datetime.strptime(spec_date, "%d.%m.%y").date()

        sdate = (sd - datetime.timedelta(days=sd.weekday())).strftime("%d.%m.%Y")
        edate = (sd + datetime.timedelta(days=6 - sd.weekday())).strftime("%d.%m.%Y")

    # Надсилання запиту
    r = requests.post(
        "http://194.44.187.20/cgi-bin/timetable.cgi?n=700",
        data={
            "faculty": 0,
            "teacher": teacher,
            "group": group,
            "sdate": sdate,
            "edate": edate,
            "n": 700,
        },
    )
    r.encoding = "Windows 1251"
    return r
