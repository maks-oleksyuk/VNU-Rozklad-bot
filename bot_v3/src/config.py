import logging.config
from os import getenv

import yaml
from aiogram import Bot, Dispatcher

from bot_v3.src.database.db import Database

# Admin user ID.
ADMIN_ID = int(getenv('ADMIN_ID', default=''))

# Loading the logger configuration from a file.
with open('logs/log_conf.yml', 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))
logger = logging.getLogger('bot')

# Initialize bot and dispatcher.
bot = Bot(token=getenv('BOT_TOKEN', default=''), validate_token=True,
          parse_mode='MarkdownV2', disable_web_page_preview=True)
dp = Dispatcher(bot)

# Database settings
DB_USER = getenv('DB_USER', default='')
DB_PASS = getenv('DB_PASS', default='')
DB_NAME = getenv('DB_NAME', default='')
db = Database(DB_NAME, DB_USER, DB_PASS)
