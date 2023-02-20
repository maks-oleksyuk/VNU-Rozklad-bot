from datetime import date, timedelta

import database.db as db
from aiogram import Dispatcher, types
from services.message import answer
from services.timetable import timetable_for_date, timetable_for_week, \
    now_subject


async def now(message: types.Message):
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await now_subject(message, date.today())
    else:
        await answer(message, 'no-ud-exist', 'choice')


async def today(message: types.Message):
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await db.update_user_data_date(message.from_user.id, date.today())
        await timetable_for_date(message, date.today())
    else:
        await answer(message, 'no-ud-exist', 'choice')


async def tomorrow(message: types.Message):
    tmp = date.today() + timedelta(days=1)
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await db.update_user_data_date(message.from_user.id, tmp)
        await timetable_for_date(message, tmp)
    else:
        await answer(message, 'no-ud-exist', 'choice')


async def week(message: types.Message, **kwargs):
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await timetable_for_week(message, date.today() +
                                 timedelta(kwargs.get('next_week', 0)))
    else:
        await answer(message, 'no-ud-exist', 'choice')


async def nextweek(message: types.Message):
    await week(message, next_week=1)


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(now, commands='now',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(today, commands='today',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(tomorrow, commands='tomorrow',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(week, commands='week',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(nextweek, commands='nextweek',
                                chat_type=types.ChatType.PRIVATE)
