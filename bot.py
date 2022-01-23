from config import dp, onStart
from aiogram.utils import executor

from handlers import user

user.register_handlers_user(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=onStart)
