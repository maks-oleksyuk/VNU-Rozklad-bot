import locale

from aiogram import types

from .message import answer

locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')


async def formation_schedule_for_day(message: types.Message,
                                     data: list, user_data: dict, ):
    # If we get any results, we create a message to send.
    if data:
        if user_data['d_mode'] == 'group':
            title = f'🎓 *Розклад групи* `{user_data["d_name"]}`'
        if user_data['d_mode'] == 'teacher':
            title = f'💼 *Розклад викладача* `{user_data["d_name"]}`'
        date = user_data['d_date'].strftime('🔹 на %d.%m.%Y (%A)\n\n')
        pass
    # If there is no data, but the request is for a day off,
    # we will send a corresponding message about it.
    elif user_data['d_date'].weekday() > 5:
        await answer(message, 'holiday', 'timetable')
    # We send a message about missing data.
    else:
        await answer(message, 'no-data', 'timetable')
