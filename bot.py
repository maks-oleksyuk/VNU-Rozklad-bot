from aiogram.utils import executor

from config import dp, on_shutduwn, on_startup
from handlers import schedule_commands, user

schedule_commands.register_handlers_schedule_commands(dp)
user.register_handlers_user(dp)


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutduwn
    )
