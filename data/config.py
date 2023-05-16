from os import getenv

# Telegram bot API token from @BotFather.
BOT_TOKEN = getenv('BOT_TOKEN', default='')

# Admin user ID.
ADMIN_ID = int(getenv('ADMIN_ID', default=''))

# Database settings.
DB_USER = getenv('DB_USER', default='')
DB_PASS = getenv('DB_PASS', default='')
DB_NAME = getenv('DB_NAME', default='')
DB_HOST = getenv('DB_HOST', default='')

# API IP address.
API_IP = getenv('API_IP', default='')
