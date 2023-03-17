from datetime import date, timedelta

from aiogram import types

from loader import dp, db
from ..utils.messages import answer
from ..utils.timetable import now_subject, timetable_for_date, \
    timetable_for_week


@dp.message_handler(commands=['now'])
async def now(message: types.Message) -> types.Message:
    """Handler function for the `/now` command.

    Args:
        message: The message sent by the user.
    """
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        return await now_subject(message, date.today())
    else:
        return await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['today'])
async def today(message: types.Message) -> types.Message:
    """Handler function for the `/today` command.

    Args:
        message: The message sent by the user.
    """
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await db.update_user_data_date(message.from_user.id, date.today())
        return await timetable_for_date(message, date.today())
    else:
        return await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['tomorrow'])
async def tomorrow(message: types.Message) -> types.Message:
    """Handler function for the `/tomorrow` command.

    Args:
        message: The message sent by the user.
    """
    tmw = date.today() + timedelta(days=1)
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        await db.update_user_data_date(message.from_user.id, tmw)
        return await timetable_for_date(message, tmw)
    else:
        return await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['week'])
async def week(message: types.Message, weeks: int = 0) -> types.Message:
    """Handler function for the `/week` command.

    Args:
        message: The message sent by the user.
        weeks: Weeks delta for display from the current, 0 by default
    """
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        return await timetable_for_week(message, date.today() + timedelta(weeks=weeks))
    else:
        return await answer(message, 'no-ud-exist', 'choice')


@dp.message_handler(commands=['nextweek'])
async def nextweek(message: types.Message) -> types.Message:
    """Handler function for the `/nextweek` command.

    Args:
        message: The message sent by the user.
    """
    return await week(message, 1)


@dp.message_handler(commands=['set_date'])
async def set_date(message: types.Message) -> types.Message | None:
    """Handler function for the `/set_date` command.

    Args:
        message: The message sent by the user.
    """
    await db.insert_update_user(message)
    if await db.get_users_data_by_id(message.from_user.id):
        from ..states.set_date import FSMSetDate
        await answer(message, 'set-date')
        await FSMSetDate.first()
    else:
        return await answer(message, 'no-ud-exist', 'choice')
