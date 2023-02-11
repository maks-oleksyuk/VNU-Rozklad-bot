from datetime import date

import database.db as db
from aiogram import Dispatcher, types
from services.timetable import timetable_for_date


async def today(message: types.Message):
    await db.update_user_data_date(message.from_user.id, date.today())
    await timetable_for_date(message, date.today())


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(today, commands='today',
                                chat_type=types.ChatType.PRIVATE)
