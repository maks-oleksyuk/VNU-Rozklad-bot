import json
from aiogram import Bot
from decouple import config
from request import getChair, getFaculties
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=config("TOKEN", default=""))
dp = Dispatcher(bot, storage=storage)

chair = []
faculty = []


async def onStart(_):
    print("Bot Started")
    await getChair()
    await getFaculties()
    with open("json/chair.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            chair.append(d["name"])
    with open("json/faculties.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            faculty.append(d["name"])


async def getGroupsByFaculty(faculty):
    groups = []
    with open("json/faculties.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            if d["name"] == faculty:
                for g in d["objects"]:
                    groups.append(g["name"])
                return groups


async def getTeachersByChair(chair):
    surnames = []
    with open("json/chair.json") as f:
        text = json.loads(f.read())
        for d in text["psrozklad_export"]["departments"]:
            if d["name"] == chair:
                for t in d["objects"]:
                    surname = t["P"] + " " + t["I"] + " " + t["B"]
                    surnames.append(surname)
                return surnames


async def searchGroup(query):
    search = []
    if len(query) < 11:
        with open("json/faculties.json") as f:
            text = json.loads(f.read())
            for d in text["psrozklad_export"]["departments"]:
                for g in d["objects"]:
                    if g["name"].lower().find(query.lower()) != -1:
                        search.append(g["name"])
            if len(search):
                search.sort()
                return search
            else:
                return []
    else:
        return []


# TODO REBILD to teacher
async def searchTeacher(query):
    search = []
    if len(query) < 11:
        with open("json/faculties.json") as f:
            text = json.loads(f.read())
            for d in text["psrozklad_export"]["departments"]:
                for g in d["objects"]:
                    if g["name"].lower().find(query.lower()) != -1:
                        search.append(g["name"])
            if len(search):
                search.sort()
                return search
            else:
                return []
    else:
        return []
