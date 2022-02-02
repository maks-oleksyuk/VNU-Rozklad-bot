from aiogram import types
from config import searchGroup
from config import bot, faculty, chair, getGroupsByFaculty, getTeachersByChair
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
            groups = await getGroupsByFaculty(message.text)
            for i in range(0, len(groups), 2):
                if i == len(groups)-1:
                    markup.add(KeyboardButton(text=groups[i]))
                else:
                    markup.row(KeyboardButton(text=groups[i]), KeyboardButton(text=groups[i+1]))
        case "surname":
            markup.add(b_back)
            teachers = await getTeachersByChair(message.text)
            for i in teachers:
                markup.add(KeyboardButton(text=i))
        case "search":
            markup.add(b_back)
            res = await searchGroup(message.text)
            for i  in range(0, len(res), 2):
                if i == len(res)-1:
                    markup.add(KeyboardButton(text=res[i]))
                else:
                    markup.row(KeyboardButton(text=res[i]), KeyboardButton(text=res[i+1]))
        case "timetable":
            markup.row("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")
            markup.row("⬅️ тиждень", "сьогодні", "тиждень ➡️")
            markup.row("Нагадування ⏰", "На тиждень", "📆 Ввести дату")
    return markup
