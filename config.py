import json
from aiogram import Bot
from decouple import config
from request import getFaculties
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=config("TOKEN", default=""))
dp = Dispatcher(bot, storage=storage)

faculty = []


async def onStart(_):
    print("Bot Started")
    await getFaculties()
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
