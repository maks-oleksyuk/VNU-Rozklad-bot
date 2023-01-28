import json
from datetime import date
from os import getenv

from api.timetable_api import get_groups, get_teachers
from database.db import get_departments_by_mode

chair, faculty = [], []
week = ['Понеділок', 'Вівторок', 'Середа', 'Четвер',
        "П'ятниця", 'Субота', 'Неділя'] * 2

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
             + 'не соромся, пиши [сюди](tg://user?id=' + str(
        getenv('ADMIN_ID')) + '), він допоможе 😎\n\n'
             + '*🎨 Велике дякую* [Tim Boniuk](https://t.me/timboniuk) за чудовий аватар\n\n'
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
}


async def get_message_by_key(key: str) -> str:
    return message.get(key, '⏳')


async def departments_init():
    # global faculty, chair
    if date.today().day == 1:
        await get_groups()
        await get_teachers()
    faculty[:] = await get_departments_by_mode('groups')
    chair[:] = await get_departments_by_mode('teachers')


async def search(query: str, d_type: str):
    """ Data search by json files

    Args:
        query (str): Text to search
        d_type (str): Search results of a specific type (chair or faculty)

    Returns:
        Array with search results
    """
    search_result = []
    with open(f'./../json/{d_type}.min.json') as f:
        text = json.loads(f.read())
        for d in text['psrozklad_export']['departments']:
            for i in d['objects']:
                if d_type == 'faculty':
                    if i['name'].lower() == query.lower():
                        return [i['name']]
                    if i['name'].lower().find(query.lower()) != -1:
                        search_result.append(i['name'])
                if d_type == 'chair':
                    fullname = '{} {} {}'.format(i['P'], i['I'], i['B'])
                    if fullname.lower().find(query.lower()) != -1:
                        search_result.append(fullname)
        if len(search_result):
            search_result.sort()
    return search_result


async def get_data_id_and_name(query: str, d_type: str):
    with open(f'./../json/{d_type}.min.json') as f:
        text = json.loads(f.read())
        for d in text['psrozklad_export']['departments']:
            for i in d['objects']:
                fullname = '{} {} {}'.format(i['P'], i['I'], i[
                    'B']) if d_type == 'chair' else ''
                if i[
                    'name'].lower() == query.lower() or fullname.lower() == query.lower():
                    return {'id': int(i['ID']), 'name': i['name']}
