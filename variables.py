import funct
import telebot
import datetime
import dateutil.parser
import commands
from parsing import parsing
from data_request import get
from keyboard import set_markup

# from variables import user_group, user_teacher

TOKEN = "token"
bot = telebot.TeleBot(TOKEN)

last_selec = {}
user_group = {}
user_teacher = {}
now_date = datetime.date.today()
select_date = datetime.date.today()
week = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]


def set_group(message):
    req = get(group=message.text)
    if funct.check_message(req):
        user_group[message.from_user.id] = message.text
        last_selec[message.from_user.id] = 1
        parsing(req, message, date=None)
    elif message.text == "/cancel":
        commands.cancel(message)
    else:
        msg = bot.send_message(
            message.chat.id,
            "❗️Змініть або вкажіть більш точні дані\n❗️для формування розкладу\n\n"
            + "/cancel - для відміни",
        )
        bot.register_next_step_handler(msg, set_group)


def set_teacher(message):
    req = get(teacher=message.text)
    if funct.check_message(req):
        user_teacher[message.from_user.id] = message.text
        last_selec[message.from_user.id] = 2
        parsing(req, message, date=None)
    elif message.text == "/cancel":
        commands.cancel(message)
    else:
        msg = bot.send_message(
            message.chat.id,
            "❗️Змініть або вкажіть більш точні дані\n❗️для формування розкладу\n\n"
            + "/cancel - для відміни",
        )
        bot.register_next_step_handler(msg, set_teacher)


def change_date(message):
    if funct.is_date(message.text):

        select_date = dateutil.parser.parse(message.text).date()

        if message.from_user.id in last_selec:

            if last_selec[message.from_user.id] == 1:
                req = get(spec_date=select_date, group=user_group[message.from_user.id])

            elif last_selec[message.from_user.id] == 2:
                req = get(
                    spec_date=select_date, teacher=user_teacher[message.from_user.id]
                )

            if funct.check_message(req):
                parsing(req, message, select_date)

            else:
                bot.send_message(
                    message.chat.id,
                    "❗️Данних не знайдено❗️",
                    reply_markup=set_markup(message.from_user.id, 3),
                )
        else:
            bot.send_message(
                message.chat.id,
                "🌀 Оновіть данні",
                reply_markup=set_markup(message.from_user.id, 1),
            )

    elif message.text == "/cancel":
        commands.cancel(message)

    else:
        msg = bot.send_message(
            message.chat.id,
            "❗️Змініть або вкажіть більш точні дані \n❗️для формування розкладу\n\n"
            + "/cancel - для відміни",
        )
        bot.register_next_step_handler(msg, change_date)
