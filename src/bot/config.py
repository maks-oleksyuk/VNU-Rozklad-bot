import json
from datetime import date

from os import getenv
import psycopg2 as ps
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dateutil.parser import parse

from request import get_chair, get_faculties

storage = MemoryStorage()

base = ps.connect(
    host="postgres",
    user=getenv("DB_USER", default=""),
    password=getenv("DB_PASS", default=""),
    database=getenv("DB_NAME", default=""),
)
cur = base.cursor()

bot = Bot(token=getenv("TOKEN", default=""))
dp = Dispatcher(bot, storage=storage)

chair = []
faculty = []

week = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"] * 2


async def on_startup(dp):
    print("Bot Started")
    await get_chair()
    await get_faculties()
    with open("json/chair.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            chair.append(d["name"])
    with open("json/faculties.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            faculty.append(d["name"])


async def on_shutduwn(dp):
    print('close')
    cur.close()
    base.close()


async def get_groups_by_faculty(faculty):
    groups = []
    with open("json/faculties.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            if d["name"] == faculty:
                for g in d["objects"]:
                    groups.append(g["name"])
                return groups


async def get_teachers_by_chair(chair):
    teachers = []
    with open("json/chair.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            if d["name"] == chair:
                for t in d["objects"]:
                    surname = t["P"] + " " + t["I"] + " " + t["B"]
                    teachers.append(surname)
                return teachers


async def search_group(query):
    search_result = []
    if len(query) < 11:
        with open("json/faculties.min.json") as f:
            text = json.loads(f.read())
            for d in text["psrozklad_export"]["departments"]:
                for g in d["objects"]:
                    if g["name"].lower() == query.lower():
                        return [g["name"]]
                    if g["name"].lower().find(query.lower()) != -1:
                        search_result.append(g["name"])
            if len(search_result):
                search_result.sort()
                return search_result
    return []


async def search_teacher(query):
    search_result = []
    if len(query) < 40:
        with open("json/chair.min.json") as f:
            text = json.loads(f.read())
            for d in text["psrozklad_export"]["departments"]:
                for t in d["objects"]:
                    i = t["P"] + " " + t["I"] + " " + t["B"]
                    if i.lower().find(query.lower()) != -1:
                        search_result.append(i)
            if len(search_result):
                search_result.sort()
                return search_result
    return []


async def get_group_id(query):
    with open("json/faculties.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            for g in d["objects"]:
                if g["name"].lower() == query.lower():
                    return [g["ID"], g["name"]]


async def get_teacher_id(query):
    with open("json/chair.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            for t in d["objects"]:
                i = t["P"] + " " + t["I"] + " " + t["B"]
                if i.lower() == query.lower():
                    return [t["ID"], t["name"]]


async def get_teacher_full_name(query):
    with open("json/chair.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            for t in d["objects"]:
                if query.lower().find(t["name"].lower()) != -1:
                    i = t["P"] + " " + t["I"] + " " + t["B"]
                    return i


async def get_column(weekday, week, next):
    col = ""
    colums = [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun",
        "week",
    ]
    if weekday != None:
        col = colums[weekday]
    if week:
        col = colums[-1]
    if next:
        col = "n_" + col
    return col


async def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        if len(string) == 5 and int(string[3:]) <= 12 and int(string[:2]) <= 31:
            d = date(date.today().year, int(string[3:]), int(string[:2]))
            return d
        elif len(string) == 5 and int(string[3:]) <= 31 and int(string[:2]) <= 12:
            d = date(date.today().year, int(string[:2]), int(string[3:]))
            return d
        elif len(string) == 5 and int(string[3:]) > 12 and int(string[:2]) > 12:
            return False
        else:
            return parse(string).date()

    except ValueError:
        return False


async def multy_replase(text, all=None):
    """Formatting special characters for MarkdownV2.

    Args:
        text (str): Text to be formatted.
        all (bool, optional): If need replase all characters. Defaults to None.

    Returns:
        _type_: Formatted text in MarkdownV2.
    """
    text = text.replace(" (за професійним спрямуванням)", "")
    chars = "[]()>#+-={|}.!"
    if all:
        chars += "_*~`"
    for c in chars:
        text = text.replace(c, "\\" + c)
    return text
