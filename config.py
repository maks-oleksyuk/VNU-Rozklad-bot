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
    getFaculties()
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
