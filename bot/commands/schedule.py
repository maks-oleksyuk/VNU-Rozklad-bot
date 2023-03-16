from datetime import date, timedelta

from aiogram import types

from loader import dp, db
from ..utils.messages import answer
from ..utils.timetable import now_subject, timetable_for_date, \
    timetable_for_week


@dp.message_handler(commands=['now'])
async def now(message: types.Message):
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await now_subject(message, date.today())
    else:
        await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['today'])
async def today(message: types.Message):
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await db.update_user_data_date(message.from_user.id, date.today())
        await timetable_for_date(message, date.today())
    else:
        await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['tomorrow'])
async def tomorrow(message: types.Message):
    tmw = date.today() + timedelta(days=1)
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await db.update_user_data_date(message.from_user.id, tmw)
        await timetable_for_date(message, tmw)
    else:
        await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['week'])
async def week(message: types.Message, weeks: int = 0):
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await timetable_for_week(message, date.today() + timedelta(weeks=weeks))
    else:
        await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['nextweek'])
async def nextweek(message: types.Message):
    await week(message, 1)


@dp.message_handler(commands=['set_date'])
async def set_date(message: types.Message):
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        from ..states.set_date import FSMSetDate
        await answer(message, 'set-date')
        await FSMSetDate.first()
    else:
        await answer(message, 'no-ud-exist', 'choice')
