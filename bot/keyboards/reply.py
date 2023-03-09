from aiogram import types
from aiogram.types import KeyboardButton as Kb
from aiogram.types import ReplyKeyboardMarkup

from loader import db


# from database.db import get_objects_by_department, get_users_data_by_id, search


# from .storage import chair, faculty


async def get_reply_keyboard_by_key(message: types.Message, key) -> ReplyKeyboardMarkup:
    """Return the keyboard for the required variant

    Args:
        message (types.Message): Message with additional data
        key (str): Keyboard identifier to build

    Returns:
        ReplyKeyboardMarkup: Keyboard of the right option
    """
    markup = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)
    match key:
        case 'choice':
            markup.input_field_placeholder = 'Оберіть варіант з меню'
            markup.row(Kb(text='Викладач 💼'), Kb(text='Студент 🎓'))
        case 'faculty':
            faculty = await db.get_departments_by_mode('groups')
            markup.input_field_placeholder = 'Пошук (наприклад `КНІТ-43`)'
            markup = await one_column_reply_keyboard(markup, faculty, True)
        # case 'chair':
        #     markup = await one_column_reply_keyboard(markup, chair, True)
        # case 'group':
        #     data = await get_objects_by_department('groups', message.text)
        #     markup = await two_column_reply_keyboard(markup, data, True)
        # case 'surname':
        #     data = await get_objects_by_department('teachers', message.text)
        #     markup = await one_column_reply_keyboard(markup, data, True)
        # case 'search-group':
        #     data = await search('groups', message.text)
        #     markup = await two_column_reply_keyboard(markup, data, True)
        # case 'search-teacher':
        #     data = await search('teachers', message.text)
        #     markup = await one_column_reply_keyboard(markup, data, True)
        # case 'timetable':
        #     days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд']
        #     res = await get_users_data_by_id(message.from_user.id)
        #     days[res['d_date'].weekday()] = '🟢'
        #     markup.row(*days)
        #     markup.row('⬅️ тиждень', 'сьогодні', 'тиждень ➡️')
        #     markup.row('Змінити запит', 'на тиждень', 'Ввести дату')
    return markup


async def one_column_reply_keyboard(markup: ReplyKeyboardMarkup, data,
                                    use_back: bool = False) -> ReplyKeyboardMarkup:
    if use_back:
        markup.add(Kb(text='⬅️ Назад'))
    for i in data:
        markup.add(Kb(text=i))
    return markup

#
# async def two_column_reply_keyboard(markup: ReplyKeyboardMarkup, data,
#                                     use_back: bool = False) -> ReplyKeyboardMarkup:
#     if use_back:
#         markup.add(Kb(text='⬅️ Назад'))
#     for i in range(0, len(data), 2):
#         if i == len(data) - 1:
#             markup.add(Kb(text=data[i]))
#         else:
#             markup.row(Kb(text=data[i]), Kb(text=data[i + 1]))
#     return markup
