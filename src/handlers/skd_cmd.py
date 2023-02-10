import database.db as db
from aiogram import Dispatcher, types
from services.timetable import formation_schedule_for_day


async def today(message: types.Message):
    user_data = await db.get_users_data_by_id(message.from_user.id)
    data = await db.get_timetable(user_data['d_id'], user_data['d_mode'])
    await formation_schedule_for_day(message, data, user_data)


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(today, commands='today',
                                chat_type=types.ChatType.PRIVATE)
