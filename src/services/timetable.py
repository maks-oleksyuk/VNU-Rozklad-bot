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


async def timetable_for_week(message: types.Message, date: date):
    ud = await db.get_users_data_by_id(message.from_user.id)
    sdate = date - timedelta(days=date.weekday())
    edate = sdate + timedelta(days=6)
    data = await db.get_timetable(ud['d_id'], ud['d_mode'], sdate, edate)
    await formation_schedule_for_week(message, data, ud, sdate, edate)


async def formation_schedule_for_day(message: types.Message,
                                     data: list, ud: dict):
    # If we get any results, we create a message to send.
    if data:
        mode, lessons = '', ''
        if ud['d_mode'] == 'group':
            mode = md.bold('🎓 Розклад групи')
        if ud['d_mode'] == 'teacher':
            mode = md.bold('💼 Розклад викладача')
        name = md.code(md.quote(ud['d_name']))
        date = md.bold(md.quote(ud['d_date'].strftime('🔹 на %d.%m.%Y (%A)\n')))
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
                lessons += md.italic(md.quote(f"👨‍🏫 {i['teacher']}\n"))
            if i['room'] and i['group']:
                lessons += md.quote(f"🏷 {i['room']}")
                lessons += md.quote(f"  |  {i['group']}\n")
            else:
                if i['room']:
                    lessons += md.quote(f"🚪 {i['room']}\n")
                if i['group']:
                    lessons += md.quote(f"👥 {i['group']}\n")
        mes = f'{mode} {name}\n{date}{lessons}'
        await answer_text(message, mes, 'timetable')
    # If there is no data, but the request is for a day off,
    # we will send a corresponding message about it.
    elif ud['d_date'].isoweekday() > 5:
        await answer(message, 'holiday', 'timetable')
    # We send a message about missing data.
    else:
        await answer(message, 'no-data', 'timetable')


async def formation_schedule_for_week(message: types.Message, data: list,
                                      ud: dict, sdate: date, edate: date):
    # If we get any results, we create a message to send.
    if data:
        mode, lessons, day, lsn = '', '', '', 0
        if ud['d_mode'] == 'group':
            mode = md.bold('🎓 Розклад групи')
        if ud['d_mode'] == 'teacher':
            mode = md.bold('💼 Розклад викладача')
        name = md.code(md.quote(ud['d_name']))
        date = md.bold(md.quote(
            sdate.strftime('🔹 з %d.%m.%Y') + edate.strftime(' по %d.%m.%Y')))
        for i in data:
            if day != i['date']:
                day = i['date']
                lsn = 0
                lessons += md.italic(md.quote(
                    i['date'].strftime('\n\n🔅 %d.%m %A')))
            if lsn == i['lesson_number']:
                lessons += md.bold('\n ╰  ')
            else:
                lsn = i['lesson_number']
                lessons += md.bold(f"\n {i['lesson_number']}\\. ")
            if i['reservation']:
                lessons += md.quote(f"{i['reservation']}")
            if i['title']:
                lessons += md.quote(f"{i['title']}")
            if ud['d_mode'] == 'group' and await has_need_group(i['group']):
                lessons += ' \\| '
                lessons += md.bold(md.italic(md.quote(f"{i['group']}")))
            if ud['d_mode'] == 'teacher':
                lessons += ' \\| ' + md.italic(md.quote(f"{i['group']}"))
        mes = f'{mode} {name}\n{date}{lessons}'
        await answer_text(message, mes, 'timetable')
    else:
        await answer(message, 'no-data', 'timetable')


async def change_week_day(message: types.Message):
    ud = await db.get_users_data_by_id(message.from_user.id)
    if ud:
        if message.text == '🟢':
            await timetable_for_date(message, ud['d_date'])
        else:
            x = week.index(message.text)
            y = ud['d_date'].weekday()
            date = ud['d_date'] + timedelta(days=x - y)
            await db.update_user_data_date(message.from_user.id, date)
            await timetable_for_date(message, date)
    else:
        await answer(message, 'no-ud-exist', 'choice')


async def change_week(message: types.Message, side: str):
    ud = await db.get_users_data_by_id(message.from_user.id)
    if ud:
        date = ud['d_date'] + timedelta(weeks=1 if side == 'next' else -1)
        await db.update_user_data_date(message.from_user.id, date)
        await timetable_for_date(message, date)
    else:
        await answer(message, 'no-ud-exist', 'choice')


async def has_need_group(txt):
    """Checking for specified elements in the text

    Args:
        txt str: Text to check

    Returns:
        bool: True if found and False if not
    """
    return True if (
            txt.find('підгр.') != -1
            or txt.find('част. групи') != -1
            or txt.find('Збірна група') != -1
    ) else False
