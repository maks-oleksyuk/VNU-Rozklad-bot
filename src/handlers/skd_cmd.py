from aiogram import Dispatcher, types
from api.timetable_api import get_timetable
from database.db import get_users_data_by_id


async def today(message: types.Message):
    user_data = await get_users_data_by_id(message.from_user.id)
    await get_timetable(user_data['d_id'], user_data['d_mode'])


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(today, commands='today',
                                chat_type=types.ChatType.PRIVATE)
