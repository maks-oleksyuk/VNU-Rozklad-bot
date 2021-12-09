import funct
from telebot import types
from keyboard import set_markup
from variables import bot, set_group, set_teacher, change_date, last_selec


# Обробник вхідних повідомлень
def text(message):
    # global user_group
    if message.chat.type == "private":
        if message.text == "Викладач":
            msg = bot.send_message(
                message.chat.id,
                "✅ Okey, Зазвичай достатньо прізвища викладача😉",
                reply_markup=set_markup(message.from_user.id, 2.1),
            )
            bot.register_next_step_handler(msg, set_teacher)

        elif message.text == "Група":
            msg = bot.send_message(
                message.chat.id,
                "✅ Okey, Введи назву групи у форматі `[Назва-##]`",
                parse_mode="Markdown",
                reply_markup=set_markup(message.from_user.id, 2.2),
            )
            bot.register_next_step_handler(msg, set_group)

        elif message.text == "Змінити запит":
            funct.change(message)

        elif message.text == "Ввести дату":
            msg = bot.send_message(
                message.chat.id,
                "📅 Введіть дату",
                reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True),
            )
            bot.register_next_step_handler(msg, change_date)

        elif message.text == "сьогодні":
            funct.today(message)

        elif message.text == "тиждень ➡️":
            funct.next_week(message)

        elif message.text == "⬅️ тиждень":
            funct.prev_week(message)

        elif (
                message.text == "Пн"
                or message.text == "Вт"
                or message.text == "Ср"
                or message.text == "Чт"
                or message.text == "Пт"
                or message.text == "Сб"
                or message.text == "Нд"
        ):
            funct.set_day(message)
        elif message.text == "/admin_stats":
            bot.send_message(
                123123123,
                len(last_selec),
            )
