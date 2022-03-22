from aiogram import types
from aiogram.types import InlineKeyboardButton as ikb
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton as kb
from aiogram.types import ReplyKeyboardMarkup

from config import (chair, faculty, get_groups_by_faculty,
                    get_teachers_by_chair, search_group, search_teacher)
from database import user_data


async def setKeyboard(option, message: types.Message = None):
    """Return the keyboard for the required variant 

    Args:
        message (types.Message): Message with additional data
        option (str): Keyboard identifier to build

    Returns:
        ReplyKeyboardMarkup: Keyboard of the right option
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    b_back = kb(text="⬅️ Назад")

    match option:
        case "choice":
            markup.row(kb(text="Викладач 💼"), kb(text="Студент 🎓"))
        case "faculty":
            markup.add(b_back)
            for b in faculty:
               markup.add(kb(text=b))
        case "chair":
            markup.add(b_back)
            for b in chair:
               markup.add(kb(text=b))
        case "group":
            markup.add(b_back)
            groups = await get_groups_by_faculty(message.text)
            for i in range(0, len(groups), 2):
                if i == len(groups)-1:
                    markup.add(kb(text=groups[i]))
                else:
                    markup.row(kb(text=groups[i]), kb(text=groups[i+1]))
        case "surname":
            markup.add(b_back)
            teachers = await get_teachers_by_chair(message.text)
            for i in teachers:
                markup.add(kb(text=i))
        case "search-group":
            markup.add(b_back)
            res = await search_group(message.text)
            for i  in range(0, len(res), 2):
                if i == len(res)-1:
                    markup.add(kb(text=res[i]))
                else:
                    markup.row(kb(text=res[i]), kb(text=res[i+1]))
        case "search-teacher":
            markup.add(b_back)
            res = await search_teacher(message.text)
            for i in res:
                markup.add(kb(text=i))
        case "timetable":
            days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
            res = await user_data(message, "get_data_id", None)
            days[res[3].weekday()] = "🔘"
            markup.row(days[0], days[1], days[2], days[3], days[4], days[5], days[6])
            markup.row("⬅️ тиждень", "сьогодні", "тиждень ➡️")
            markup.row("Змінити запит", "На тиждень", "📆 Ввести дату")
    return markup

async def inline(option, message: types.Message = None):
    markup = InlineKeyboardMarkup()
    match option:
        case "who":
            all = ikb("Всім", callback_data='all')
            group = ikb("Групі", callback_data='group')
            user = ikb("За UID", callback_data='user')
            markup.row(all, group, user)
        case "back":
            back = ikb("⬅️ Назад", callback_data='back')
            markup.add(back)
        case "confirm":
            cancel = ikb("Скасувати ❌", callback_data='cancel')
            confirm = ikb("Підтвердити ✅", callback_data='confirm')
            markup.add(cancel, confirm)
    return markup
