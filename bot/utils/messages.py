from aiogram import types

from data.config import ADMIN_ID
from ..keyboards.reply import get_reply_keyboard_by_key

messages = {
    'start': '👋 *Привіт\\!* Я – твій помічник\n'
             + 'для відображення розкладу занять\\.\n\n'
             + 'Тут ти можеш дізнатись про свої пари протягом тижня\\.\n\n'
             + 'Обери, для кого хочеш отримати інформацію,\n'
             + 'скориставшись меню нижче 👇',

    'help': '✳️ __*Для отримання розкладу потрібно\\:*__\n\n'
            + '*1\\.* Обрати категорію для кого формувати розклад\n'
            + '*2\\.* Обрати потрібні дані, або скористатись пошуком\n\n'
            + '⚠️ Якщо помилився або передумав, існує команда /cancel\n\n'
            + '❕Якщо меню недоступне натисни на *⌘*',

    'about': '🤖 Бот, для швидкого перегляду розкладу VNU\n\n'
             + '👨🏼‍💻 Бот знаходиться в розробці, тому,\n'
             + 'якщо виникнуть якісь проблеми або питання\n'
             + 'не соромся, пиши '
             + '[сюди](tg://user?id=' + str(ADMIN_ID)
             + '), він допоможе 😎\n\n*🎨 Велике дякую* '
             + '[Tim Boniuk](https://t.me/timboniuk) за чудовий аватар\n\n'
             + '[🇺🇦 Підтримати ЗСУ](https://savelife.in.ua/donate/)',

    'choice': '🦾 Оберіть для кого будемо формувати\n'
              + 'розклад використовуючи меню знизу:',

    'faculty': '📁 Оберіть *факультет* зі списку або\n'
               + 'введіть назву групи для пошуку 🔎',

    'group': '📂 Оберіть *групу* зі списку:',

    'chair': '📁 Обери *кафедру* зі списку або\n'
             + 'введіть прізвище для пошуку 🔎',

    'surname': '📂 Обери *викладача* зі списку:',

    'good-search': '🗂 Ось що я відшукав:',

    'fail-search': 'За цим запитом нічого не знайдено 🧐\n\n'
                   + '⁉️ Вкажіть більш точні дані або\n'
                   + '📁 використовуйте меню знизу:',

    'holiday': '😎 *Вітаю\\!* В тебе вихідний',

    'no-data': '💢 Opps\\.\\.\\. Даних не знайдено\\!\n'
               + "♻️ Можливо, вони з'являться згодом\\.\\.\\.",

    'no-ud-exist': '🌀 Потрібно оновити дані\\.\\.\\.',

    'no-pair': '❕Зараз пари немає',

    'set-date': '📆 *Введіть дату:*\n'
                + '☝️ Найкращий варіант – `dd.mm`\n'
                + 'але доступно також багато інших\n\n'
                + '/cancel – для відміни',

    'date-error': '❗️ *Невірний формат дати* ❗️\n'
                  + '🌀 Повторіть спробу ще раз\n\n'
                  + '☝️ Найкращий варіант – `dd.mm`\n\n'
                  + '/cancel – для відміни',

    'cancel-date': '❕ Введення дати скасовано',
}


async def answer(message: types.Message, text_key: str, markup_key: str = None) -> types.Message:
    """Send a message to the user using the answer aiogram method.

    Args:
        message: The message to reply to.
        text_key: The key for the desired message text.
        markup_key: The key for the desired reply keyboard.
    """
    return await message.answer(
        text=messages.get(text_key, '⏳'),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )


async def answer_text(message: types.Message, text: str, markup_key: str = None) -> types.Message:
    return await message.answer(
        text=text,
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )


async def reply(message: types.Message, text_key: str, markup_key: str = None) -> types.Message:
    """Send a message to the user using the reply aiogram method.

    Args:
        message: The message to reply to.
        text_key: The key for the desired message text.
        markup_key: The key for the desired reply keyboard.
    """
    return await message.reply(
        text=messages.get(text_key, '⏳'),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )
