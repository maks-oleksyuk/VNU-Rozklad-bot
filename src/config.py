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
