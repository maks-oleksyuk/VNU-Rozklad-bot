import logging.config
from os import getenv

import yaml
from aiogram import Bot, Dispatcher

# Admin user ID.
ADMIN_ID = int(getenv('ADMIN_ID', default=''))

# Loading the logger configuration from a file.
with open('logs/log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
logging.config.dictConfig(log_config)
logger = logging.getLogger('bot')

# Initialize bot and dispatcher.
bot = Bot(token=getenv('BOT_TOKEN', default=''), validate_token=True,
          parse_mode='MarkdownV2', disable_web_page_preview=True)
dp = Dispatcher(bot)
