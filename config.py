import json
import psycopg2 as ps
from aiogram import Bot
from decouple import config
from request import getChair, getFaculties
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

base = ps.connect(config("DATABASE_URL"), sslmode="require")
cur = base.cursor()

bot = Bot(token=config("TOKEN", default=""))
dp = Dispatcher(bot, storage=storage)

chair = []
faculty = []

week = [
    "Понеділок",
    "Вівторок",
    "Середа",
    "Четвер",
    "П'ятниця",
    "Субота",
    "Неділя",
    "Понеділок",
    "Вівторок",
    "Середа",
    "Четвер",
    "П'ятниця",
    "Субота",
    "Неділя",
]


async def on_startup(dp):
    print("Bot Started")
    await getChair()
    await getFaculties()
    with open("json/chair.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            chair.append(d["name"])
    with open("json/faculties.min.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            faculty.append(d["name"])


async def on_shutduwn(dp):
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
