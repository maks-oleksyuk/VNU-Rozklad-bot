from aiogram import types
from request import searchGroup
from config import bot, faculty, getGroupsByFaculty
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def setKeyboard(message: types.Message, step):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    b_back = KeyboardButton(text="⬅️ Назад")
    b_group = KeyboardButton(text="Студент 🎓")
    b_teacher = KeyboardButton(text="Викладач 💼")

    match step:
        case 1:
            markup.row(b_teacher, b_group)            
        case 2.1:
            markup.add(b_back)
            for b in faculty:
               markup.add(KeyboardButton(text=b))
        case 2.12:
            markup.add(b_back)
            groups = await getGroupsByFaculty(message.text)
            for i in range(0, len(groups), 2):
                if i == len(groups)-1:
                    markup.add(KeyboardButton(text=groups[i]))
                else:
                    markup.row(KeyboardButton(text=groups[i]), KeyboardButton(text=groups[i+1]))
        case 2.15:
            if await searchGroup(message.text):
                res = await searchGroup(message.text)
                markup.add(b_back)
                for i  in range(0, len(res), 2):
                    if i == len(res)-1:
                        markup.add(KeyboardButton(text=res[i]))
                    else:
                        markup.row(KeyboardButton(text=res[i]), KeyboardButton(text=res[i+1]))
            else:
                return            
    return markup
