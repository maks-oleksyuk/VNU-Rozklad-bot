from aiogram import types

messages = {
    'start': '👋 *Привіт\\!* Я – твій помічник\n'
             + 'для відображення розкладу занять\\.\n\n'
             + 'Тут ти можеш дізнатись про свої пари протягом тижня\\.\n\n'
             + 'Обери, для кого хочеш отримати інформацію,\n'
             + 'скориставшись меню знизу 👇'
}


async def get_message_by_key(key: str) -> str:
    """Returns a string message by the provided key from the messages' dictionary.

    Args:
        key (str): The key to search the messages' dictionary.

    Returns:
        str: The message string if key is found, otherwise returns the default message '⏳'.
    """
    return messages.get(key, '⏳')


async def answer(message: types.Message, text_key: str, markup_key=None):
    """Send a message to the user using the answer aiogram method.

    Args:
        message (types.Message): The message to reply to.
        text_key (str): The key for the desired message text.
        markup_key (str, optional): The key for the desired reply keyboard.
    """
    await message.answer(
        text=await get_message_by_key(text_key),
        # reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )
