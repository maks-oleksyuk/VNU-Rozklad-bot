import logging.config

import yaml
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from api.schedule_api import ScheduleAPI
from bot.database.db import Database
from data.config import BOT_TOKEN, DB_NAME, DB_USER, DB_PASS, API_IP

# Loading the logger configuration from a file.
with open('logs/log_conf.yml', 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))
logger = logging.getLogger('bot')

bot = Bot(token=BOT_TOKEN,
          validate_token=True,
          parse_mode=types.ParseMode.MARKDOWN_V2,
          disable_web_page_preview=True)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

db = Database(DB_NAME, DB_USER, DB_PASS)

api = ScheduleAPI(API_IP)
