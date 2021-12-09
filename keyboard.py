import variables
from telebot import types


def set_markup(id, n):
    item_group = types.KeyboardButton(text="Група")
    item_teacher = types.KeyboardButton(text="Викладач")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Початкова клавіатура для вибору викладача або групи
    if n == 1:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(item_teacher, item_group)
        # markup.add(item_teacher, item_group)

    # Клавіатура вибору збереженого викладача
    elif n == 2.1:
        if id in variables.user_teacher:
            item_last_teacher = types.KeyboardButton(text=variables.user_teacher[id])
            markup.add(item_last_teacher)
        else:
            markup = types.ReplyKeyboardRemove()

    # Клавіатура вибору збереженої групи
    elif n == 2.2:
        if id in variables.user_group:
            item_last_group = types.KeyboardButton(text=variables.user_group[id])
            markup.add(item_last_group)
        else:
            markup = types.ReplyKeyboardRemove()

    # Клавіатура для навігації
    elif n == 3:
        markup.row("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")
        markup.row("⬅️ тиждень", "сьогодні", "тиждень ➡️")
        markup.row("Змінити запит", "Ввести дату")

    return markup
