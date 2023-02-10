from datetime import date
from os import getenv

from api.timetable_api import get_groups, get_teachers
from database.db import get_departments_by_mode

chair, faculty = [], []
week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд']

message = {
    'start': '👋 *Привіт\\!*\n\n'
             + '*Я* – 🤖 помічник, у якого,\n'
             + 'ти завжди можеш дізнатись,\n'
             + 'які в тебе пари протягом тижня\\.\n\n'
             + '🦾 Обери для кого будемо формувати\n'
             + 'розклад використовуючи меню знизу:\n\n'
             + '❕Якщо меню недоступне, натисни на *⌘*',

    'help': '✳️ __*Для отримання розкладу потрібно\\:*__\n\n'
            + '*1\\.* Обрати категорію для кого формувати розклад\n'
            + '*2\\.* Обрати потрібні дані, або скористатись пошуком\n\n'
            + '⚠️ Якщо помилився або передумав, існує команда /cancel\n\n'
            + '❕Якщо меню недоступне натисни на *⌘*',

    'about': '🤖 Бот, для швидкого перегляду розкладу VNU\n\n'
             + '👨🏼‍💻 Бот знаходиться в розробці, тому,\n'
             + 'якщо виникнуть якісь проблеми або питання\n'
             + 'не соромся, пиши'
             + '[сюди](tg://user?id=' + str(getenv('ADMIN_ID'))
             + '), він допоможе 😎\n\n*🎨 Велике дякую* '
             + '[Tim Boniuk](https://t.me/timboniuk) за чудовий аватар\n\n'
             + '[🇺🇦 Підтримати ЗСУ](https://savelife.in.ua/donate/)',

    'choice': '🦾 Оберіть для кого будемо формувати\n'
              + 'розклад використовуючи меню знизу:',

    'faculty': '📁 Оберіть *факультет* зі списку або\n'
               + 'введіть назву групи для пошуку 🔎',

    'group': '📂 Оберіть *групу* зі списку:\n',

    'chair': '📁 Обери *кафедру* зі списку або\n'
             + 'введіть прізвище для пошуку 🔎',

    'surname': '📂 Обери *викладача* зі списку:\n',

    'good-search': '🗂 Ось що я відшукав:',

    'fail-search': 'За цим запитом нічого не знайдено 🧐\n\n'
                   + '⁉️ Вкажіть більш точні дані або\n'
                   + '📁 використовуйте меню знизу:',

    'holiday': '🎉 *Вітаю\\!* В тебе вихідний 😎',

    'no-data': '💢 Даних не знайдено\\!\n'
               + "♻️ Можливо, вони з'являться згодом\\.\\.\\.",
}


async def get_message_by_key(key: str) -> str:
    return message.get(key, '⏳')


async def departments_init():
    # We update data about groups and teachers on the first day of the month.
    if date.today().day == 1:
        await get_groups()
        await get_teachers()
    faculty[:] = await get_departments_by_mode('groups')
    chair[:] = await get_departments_by_mode('teachers')
