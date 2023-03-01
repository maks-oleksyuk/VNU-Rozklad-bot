import logging
from os import getenv

from aiogram import Bot, Dispatcher
from logging.handlers import RotatingFileHandler

# Telegram bot API token from @BotFather
BOT_TOKEN = getenv('BOT_TOKEN', default='')

# Admin user ID
ADMIN_ID = int(getenv('ADMIN_ID', default=''))

# Logging settings
LOG_LEVEL = getenv('LOG_LEVEL', default='INFO')
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# handler = RotatingFileHandler('bot.log', maxBytes=100000, backupCount=3)
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, validate_token=True,
          parse_mode='MarkdownV2', disable_web_page_preview=True)
dp = Dispatcher(bot)
