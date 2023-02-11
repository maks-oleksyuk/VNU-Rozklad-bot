import locale
from datetime import date
from datetime import timedelta

import database.db as db
from aiogram import types
from aiogram.utils.markdown import markdown_decoration as md

from .message import answer, answer_text
from .storage import week

locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')


async def timetable_for_date(message: types.Message, date: date):
    ud = await db.get_users_data_by_id(message.from_user.id)
    data = await db.get_timetable(ud['d_id'], ud['d_mode'], date, date)
    await formation_schedule_for_day(message, data, ud)


async def formation_schedule_for_day(message: types.Message,
                                     data: list, user_data: dict):
    # If we get any results, we create a message to send.
    if data:
        mode, lessons = '', ''
        if user_data['d_mode'] == 'group':
            mode = md.bold('🎓 Розклад групи')
        if user_data['d_mode'] == 'teacher':
            mode = md.bold('💼 Розклад викладача')
        name = md.code(md.quote(user_data['d_name']))
        date = user_data['d_date'].strftime('🔹 на %d.%m.%Y (%A)\n')
        date = md.bold(md.quote(date))
        for i in data:
            time = f"\n🔅 {i['lesson_number']} Пара ({i['lesson_time'].replace('-', ' - ')})\n"
            lessons += md.italic(md.quote(time))
            if i['reservation']:
                lessons += md.bold(md.quote(f"📌 {i['reservation']}\n"))
            if i['replacement']:
                lessons += md.bold(md.quote(f"❗️ {i['replacement']}\n"))
            if i['title']:
                lessons += '📚 ' \
                           + md.underline(md.bold(md.quote(f"{i['title']}")))
            lessons += md.italic(md.quote(f" ({i['type']})\n"))
            if i['teacher']:
                lessons += md.italic(md.quote(f"💼 {i['teacher']}\n"))
            if i['room'] and i['group']:
                lessons += md.quote(f"🏷 {i['room']}")
                lessons += md.quote(f"  |  {i['group']}\n")
            else:
                if i['room']:
                    lessons += md.quote(f"🔑 {i['room']}\n")
                if i['group']:
                    lessons += md.quote(f"👥 {i['group']}\n")
        mes = f'{mode} {name}\n{date}{lessons}'
        await answer_text(message, mes, 'timetable')
    # If there is no data, but the request is for a day off,
    # we will send a corresponding message about it.
    elif user_data['d_date'].isoweekday() > 5:
        await answer(message, 'holiday', 'timetable')
    # We send a message about missing data.
    else:
        await answer(message, 'no-data', 'timetable')


async def change_week_day(message: types.Message):
    ud = await db.get_users_data_by_id(message.from_user.id)
    if message.text == '🟢':
        await timetable_for_date(message, ud['d_date'])
    else:
        x = week.index(message.text)
        y = ud['d_date'].weekday()
        date = ud['d_date'] + timedelta(days=x - y)
        await db.update_user_data_date(message.from_user.id, date)
        await timetable_for_date(message, date)


async def change_week(message: types.Message, side: str):
    ud = await db.get_users_data_by_id(message.from_user.id)
    date = ud['d_date'] + timedelta(weeks=1 if side == 'next' else -1)
    await db.update_user_data_date(message.from_user.id, date)
    await timetable_for_date(message, date)
