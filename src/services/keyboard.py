from aiogram import types
from aiogram.types import KeyboardButton as Kb
from aiogram.types import ReplyKeyboardMarkup

from .storage import faculty, get_groups_by_faculty, search


async def get_reply_keyboard_by_key(message: types.Message, key) -> ReplyKeyboardMarkup:
    """Return the keyboard for the required variant

    Args:
        message (types.Message): Message with additional data
        key (str): Keyboard identifier to build

    Returns:
        ReplyKeyboardMarkup: Keyboard of the right option
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = Kb(text='⬅️ Назад')

    match key:
        case 'choice':
            markup.row(Kb(text='Викладач 💼'), Kb(text='Студент 🎓'))
        case 'faculty':
            markup.add(back)
            for d in faculty:
                markup.add(Kb(text=d))
        # case "chair":
        #     markup.add(b_back)
        #     for b in chair:
        #         markup.add(kb(text=b))
        case 'group':
            markup.add(back)
            groups = await get_groups_by_faculty(message.text)
            markup = await two_column_reply_keyboard(markup, groups)
        # case "surname":
        #     markup.add(b_back)
        #     teachers = await get_teachers_by_chair(message.text)
        #     for i in teachers:
        #         markup.add(kb(text=i))
        case 'search-group':
            markup.add(back)
            res = await search(message.text, 'faculty')
            markup = await two_column_reply_keyboard(markup, res)
        # case "search-teacher":
        #     markup.add(b_back)
        #     res = await search_teacher(message.text)
        #     for i in res:
        #         markup.add(kb(text=i))
        # case "timetable":
        #     days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        #     res = await user_data(message, "get_data_id", None)
        #     days[res[3].weekday()] = "🔘"
        #     markup.row(days[0], days[1], days[2], days[3], days[4], days[5], days[6])
        #     markup.row("⬅️ тиждень", "сьогодні", "тиждень ➡️")
        #     markup.row("Змінити запит", "На тиждень", "📆 Ввести дату")
    return markup


async def two_column_reply_keyboard(markup: ReplyKeyboardMarkup, data) -> ReplyKeyboardMarkup:
    for i in range(0, len(data), 2):
        if i == len(data) - 1:
            markup.add(Kb(text=data[i]))
        else:
            markup.row(Kb(text=data[i]), Kb(text=data[i + 1]))
    return markup
