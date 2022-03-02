from config import dp
from config import on_startup, on_shutduwn
from aiogram.utils import executor

from handlers import user

user.register_handlers_user(dp)


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutduwn
    )
