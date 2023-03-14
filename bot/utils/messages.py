from aiogram import types

from ..keyboards.reply import get_reply_keyboard_by_key

messages = {
    'start': '👋 *Привіт\\!* Я – твій помічник\n'
             + 'для відображення розкладу занять\\.\n\n'
             + 'Тут ти можеш дізнатись про свої пари протягом тижня\\.\n\n'
             + 'Обери, для кого хочеш отримати інформацію,\n'
             + 'скориставшись меню нижче 👇',

    'choice': '🦾 Оберіть для кого будемо формувати\n'
              + 'розклад використовуючи меню знизу:',

    'faculty': '📁 Оберіть *факультет* зі списку або\n'
               + 'введіть назву групи для пошуку 🔎',

    'group': '📂 Оберіть *групу* зі списку:',

    'good-search': '🗂 Ось що я відшукав:',

    'fail-search': 'За цим запитом нічого не знайдено 🧐\n\n'
                   + '⁉️ Вкажіть більш точні дані або\n'
                   + '📁 використовуйте меню знизу:',
}


async def answer(message: types.Message, text_key: str, markup_key=None):
    """Send a message to the user using the answer aiogram method.

    Args:
        message: The message to reply to.
        text_key: The key for the desired message text.
        markup_key: The key for the desired reply keyboard.
    """
    await message.answer(
        text=messages.get(text_key, '⏳'),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )


async def reply(message: types.Message, text_key: str, markup_key: str = None):
    """Send a message to the user using the reply aiogram method.

    Args:
        message: The message to reply to.
        text_key: The key for the desired message text.
        markup_key: The key for the desired reply keyboard.
    """
    await message.reply(
        text=messages.get(text_key, '⏳'),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )
