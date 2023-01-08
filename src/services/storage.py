import json
from os import getenv

from api.timetable_api import get_chair, get_faculties

chair, faculty = [], []
week = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота', 'Неділя'] * 2

message = {
    'start': "👋 *Привіт\\!*\n\n"
             + "*Я* – 🤖 помічник, у якого,\n"
             + "ти завжди можеш дізнатись,\n"
             + "які в тебе пари протягом тижня\\.\n\n"
             + "🦾 Обери для кого будемо формувати\n"
             + "розклад використовуючи меню знизу:\n\n"
             + "❕Якщо меню недоступне, натисни на *⌘*",

    'help': "✳️ __*Для отримання розкладу потрібно\\:*__\n\n"
            + "*1\\.* Обрати категорію для кого формувати розклад\n"
            + "*2\\.* Обрати потрібні дані, або скористатись пошуком\n\n"
            + "⚠️ Якщо помилився або передумав, існує команда /cancel\n\n"
            + "❕Якщо меню недоступне натисни на *⌘*",

    'about': "🤖 Бот, для швидкого перегляду розкладу VNU\n\n"
             + "👨🏼‍💻 Бот знаходиться в розробці, тому,\n"
             + "якщо виникнуть якісь проблеми або питання\n"
             + "не соромся, пиши [сюди](tg://user?id=" + str(getenv("ADMIN_ID")) + "), він допоможе 😎\n\n"
             + "*🎨 Велике дякую* [Tim Boniuk](https://t.me/timboniuk) за чудовий аватар\n\n"
             + "[🇺🇦 Підтримати ЗСУ](https://savelife.in.ua/donate/)"
}


async def get_message_by_key(key: str) -> str:
    return message.get(key, '⏳')


async def departments_init():
    await get_chair()
    with open('./../json/chair.min.json') as f:
        text = json.loads(f.read())
    for d in text['psrozklad_export']['departments']:
        chair.append(d['name'])

    await get_faculties()
    with open('./../json/faculties.min.json') as f:
        text = json.loads(f.read())
        for d in text['psrozklad_export']['departments']:
            faculty.append(d['name'])
