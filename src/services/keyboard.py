from aiogram import types
from aiogram.types import KeyboardButton as Kb
from aiogram.types import ReplyKeyboardMarkup

from .storage import chair, faculty, search, get_teachers_by_chair, get_groups_by_faculty


async def get_reply_keyboard_by_key(message: types.Message, key) -> ReplyKeyboardMarkup:
    """Return the keyboard for the required variant

    Args:
        message (types.Message): Message with additional data
        key (str): Keyboard identifier to build

    Returns:
        ReplyKeyboardMarkup: Keyboard of the right option
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    match key:
        case 'choice':
            markup.row(Kb(text='Викладач 💼'), Kb(text='Студент 🎓'))
        case 'faculty':
            markup = await one_column_reply_keyboard(markup, faculty, True)
        case 'chair':
            markup = await one_column_reply_keyboard(markup, chair, True)
        case 'group':
            groups = await get_groups_by_faculty(message.text)
            markup = await two_column_reply_keyboard(markup, groups, True)
        case 'surname':
            teachers = await get_teachers_by_chair(message.text)
            markup = await one_column_reply_keyboard(markup, teachers, True)
        case 'search-group':
            res = await search(message.text, 'faculty')
            markup = await two_column_reply_keyboard(markup, res, True)
        case 'search-teacher':
            res = await search(message.text, 'chair')
            markup = await one_column_reply_keyboard(markup, res, True)
        # case "timetable":
        #     days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        #     res = await user_data(message, "get_data_id", None)
        #     days[res[3].weekday()] = "🔘"
        #     markup.row(days[0], days[1], days[2], days[3], days[4], days[5], days[6])
        #     markup.row("⬅️ тиждень", "сьогодні", "тиждень ➡️")
        #     markup.row("Змінити запит", "На тиждень", "📆 Ввести дату")
    return markup


async def one_column_reply_keyboard(markup: ReplyKeyboardMarkup, data, use_back: bool = False) -> ReplyKeyboardMarkup:
    if use_back:
        markup.add(Kb(text='⬅️ Назад'))
    for i in data:
        markup.add(Kb(text=i))
    return markup


async def two_column_reply_keyboard(markup: ReplyKeyboardMarkup, data, use_back: bool = False) -> ReplyKeyboardMarkup:
    if use_back:
        markup.add(Kb(text='⬅️ Назад'))
    for i in range(0, len(data), 2):
        if i == len(data) - 1:
            markup.add(Kb(text=data[i]))
        else:
            markup.row(Kb(text=data[i]), Kb(text=data[i + 1]))
    return markup

# async def inline(option, message: types.Message = None):
#     markup = InlineKeyboardMarkup()
#     match option:
#         case "who":
#             all = ikb("Всім", callback_data='all')
#             group = ikb("Групі", callback_data='group')
#             user = ikb("За UID", callback_data='user')
#             markup.row(all, group, user)
#         case "back":
#             back = ikb("⬅️ Назад", callback_data='back')
#             markup.add(back)
#         case "confirm":
#             cancel = ikb("Скасувати ❌", callback_data='cancel')
#             confirm = ikb("Підтвердити ✅", callback_data='confirm')
#             markup.add(cancel, confirm)
#     return markup
