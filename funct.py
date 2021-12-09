import datetime
import variables
from keyboard import *
from parsing import parsing
from data_request import get
from dateutil.parser import parse

# Обробка натиску на кнопку сьогодні
def today(message):
    variables.select_date = datetime.date.today()
    if message.from_user.id in variables.last_selec:
        if variables.last_selec[message.from_user.id] == 1:
            req = get(group=variables.user_group[message.from_user.id])
        elif variables.last_selec[message.from_user.id] == 2:
            req = get(teacher=variables.user_teacher[message.from_user.id])
        parsing(req, message, date=None)

    else:
        variables.bot.send_message(
            message.chat.id,
            "🌀 Оновіть данні",
            reply_markup=set_markup(message.from_user.id, 1),
        )


def next_week(message):
    variables.select_date = variables.select_date + datetime.timedelta(weeks=1)

    if message.from_user.id in variables.last_selec:
        if variables.last_selec[message.from_user.id] == 1:
            req = get(
                group=variables.user_group[message.from_user.id],
                spec_date=variables.select_date,
            )
        elif variables.last_selec[message.from_user.id] == 2:
            req = get(
                teacher=variables.user_teacher[message.from_user.id],
                spec_date=variables.select_date,
            )
        if check_message(req):
            parsing(req, message, variables.select_date)
        else:
            variables.bot.send_message(
                message.chat.id,
                "❗️Данних не знайдено❗️",
                reply_markup=set_markup(message.from_user.id, 3),
            )
    else:
        variables.bot.send_message(
            message.chat.id,
            "🌀 Оновіть данні",
            reply_markup=set_markup(message.from_user.id, 1),
        )


def prev_week(message):
    variables.select_date = variables.select_date - datetime.timedelta(weeks=1)

    if message.from_user.id in variables.last_selec:
        if variables.last_selec[message.from_user.id] == 1:
            req = get(
                group=variables.user_group[message.from_user.id],
                spec_date=variables.select_date,
            )
        elif variables.last_selec[message.from_user.id] == 2:
            req = get(
                teacher=variables.user_teacher[message.from_user.id],
                spec_date=variables.select_date,
            )
        if check_message(req):
            parsing(req, message, variables.select_date)
        else:
            variables.bot.send_message(
                message.chat.id,
                "❗️Данних не знайдено❗️",
                reply_markup=set_markup(message.from_user.id, 3),
            )

    else:
        variables.bot.send_message(
            message.chat.id,
            "🌀 Оновіть данні",
            reply_markup=set_markup(message.from_user.id, 1),
        )


def set_day(message):
    if message.text == "Пн":
        variables.select_date = variables.select_date - datetime.timedelta(
            days=variables.select_date.weekday()
        )
    elif message.text == "Вт":
        variables.select_date = variables.select_date - datetime.timedelta(
            days=variables.select_date.weekday() - 1
        )
    elif message.text == "Ср":
        variables.select_date = variables.select_date - datetime.timedelta(
            days=variables.select_date.weekday() - 2
        )
    elif message.text == "Чт":
        variables.select_date = variables.select_date - datetime.timedelta(
            days=variables.select_date.weekday() - 3
        )
    elif message.text == "Пт":
        variables.select_date = variables.select_date - datetime.timedelta(
            days=variables.select_date.weekday() - 4
        )
    elif message.text == "Сб":
        variables.select_date = variables.select_date - datetime.timedelta(
            days=variables.select_date.weekday() - 5
        )
    elif message.text == "Нд":
        variables.select_date = variables.select_date - datetime.timedelta(
            days=variables.select_date.weekday() - 6
        )

    if message.from_user.id in variables.last_selec:
        if variables.last_selec[message.from_user.id] == 1:
            req = get(
                group=variables.user_group[message.from_user.id],
                spec_date=variables.select_date,
            )
        elif variables.last_selec[message.from_user.id] == 2:
            req = get(
                teacher=variables.user_teacher[message.from_user.id],
                spec_date=variables.select_date,
            )
        if check_message(req):
            parsing(req, message, variables.select_date)
        else:
            variables.bot.send_message(
                message.chat.id,
                "❗️Данних не знайдено❗️",
                reply_markup=set_markup(message.from_user.id, 3),
            )
    else:
        variables.bot.send_message(
            message.chat.id,
            "🌀 Оновіть данні",
            reply_markup=set_markup(message.from_user.id, 1),
        )


def change(message):
    variables.bot.send_message(
        message.chat.id,
        "🌀 Зміни запит за потреби",
        reply_markup=set_markup(message.from_user.id, 1),
    )


def check_message(request):
    if (
        "записів не знайдено" in request.text
        or "виникла помилка" in request.text
        or "Уточніть" in request.text
        or "Змініть" in request.text
    ):
        return False
    else:
        return True


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check felif date
    :param fuzzy: bool, ignelife unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False
