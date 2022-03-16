from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import (bot, chair, faculty, get_groups_by_faculty,
                    get_teachers_by_chair, search_group, search_teacher)
from database import user_data


async def setKeyboard(message: types.Message, step):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    b_back = KeyboardButton(text="⬅️ Назад")
    b_group = KeyboardButton(text="Студент 🎓")
    b_teacher = KeyboardButton(text="Викладач 💼")

    match step:
        case "choice":
            markup.row(b_teacher, b_group)
        case "faculty":
            markup.add(b_back)
            for b in faculty:
               markup.add(KeyboardButton(text=b))
        case "chair":
            markup.add(b_back)
            for b in chair:
               markup.add(KeyboardButton(text=b))           
        case "group":
            markup.add(b_back)
            groups = await get_groups_by_faculty(message.text)
            for i in range(0, len(groups), 2):
                if i == len(groups)-1:
                    markup.add(KeyboardButton(text=groups[i]))
                else:
                    markup.row(KeyboardButton(text=groups[i]), KeyboardButton(text=groups[i+1]))
        case "surname":
            markup.add(b_back)
            teachers = await get_teachers_by_chair(message.text)
            for i in teachers:
                markup.add(KeyboardButton(text=i))
        case "searchGroup":
            markup.add(b_back)
            res = await search_group(message.text)
            for i  in range(0, len(res), 2):
                if i == len(res)-1:
                    markup.add(KeyboardButton(text=res[i]))
                else:
                    markup.row(KeyboardButton(text=res[i]), KeyboardButton(text=res[i+1]))
        case "searchTeacher":
            markup.add(b_back)
            res = await search_teacher(message.text)
            for i in res:
                markup.add(KeyboardButton(text=i))
        case "timetable":
            days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
            res = await user_data(message, "get_data_id", None)
            days[res[3].weekday()] = "🔘"
            markup.row(days[0], days[1], days[2], days[3], days[4], days[5], days[6])
            markup.row("⬅️ тиждень", "сьогодні", "тиждень ➡️")
            markup.row("Нагадування ⏰", "На тиждень", "📆 Ввести дату")
    return markup
