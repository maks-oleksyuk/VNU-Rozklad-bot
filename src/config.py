import json
from datetime import date
from os import getenv

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dateutil.parser import parse

from database.db_init import db_init, db_close
from services.storage import departments_init

storage = MemoryStorage()

bot = Bot(token=getenv('TOKEN', default=''))
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    await db_init()
    await departments_init()
    print('Bot Started Successfully')


async def on_shutdown(dp: Dispatcher):
    await db_close()
    print('Bot Stopped')


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
    if weekday is not None:
        col = colums[weekday]
    if week:
        col = colums[-1]
    if next:
        col = "n_" + col
    return col


async def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        if len(string) == 5 and int(string[3:]) <= 12 and int(
                string[:2]) <= 31:
            d = date(date.today().year, int(string[3:]), int(string[:2]))
            return d
        elif len(string) == 5 and int(string[3:]) <= 31 and int(
                string[:2]) <= 12:
            d = date(date.today().year, int(string[:2]), int(string[3:]))
            return d
        elif len(string) == 5 and int(string[3:]) > 12 and int(
                string[:2]) > 12:
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
