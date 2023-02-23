from datetime import datetime
from os import getenv

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

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


async def is_date(date_string):
    formats = ['%d.%m', '%d/%m', '%d-%m', '%d.%m.%y', '%d/%m/%y', '%d-%m-%y',
               '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y']
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            if date_obj.year == 1900:
                date_obj = date_obj.replace(year=datetime.now().year)
            print(f'{date_string} is a valid date with format {fmt}')
            return date_obj
        except ValueError:
            pass
    else:
        print(f'{date_string} is not a valid date')
        return False
