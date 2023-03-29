from aiogram import types

from data.storage import messages
from ..keyboards.reply import get_reply_keyboard_by_key


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
