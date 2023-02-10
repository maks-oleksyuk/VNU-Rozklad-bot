from aiogram import types

from .keyboard import get_reply_keyboard_by_key
from .storage import get_message_by_key


async def answer(message: types.Message, text_key: str, markup_key=None,
                 **kwargs):
    """Sending a message using the answer aiogram method

    Args:
        message (types.Message): Message with additional data
        text_key (str): Text message search key
        markup_key (str): The key to create the corresponding keyboard
    """
    await message.answer(
        parse_mode='MarkdownV2',
        text=await get_message_by_key(text_key),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
        disable_web_page_preview=kwargs.get('disable_web_page_preview', None)
    )


async def answer_text(message: types.Message, text: str, markup_key=None):
    await message.answer(
        parse_mode='MarkdownV2',
        text=text,
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )


async def reply(message: types.Message, text_key: str, markup_key=None,
                **kwargs):
    await message.reply(
        parse_mode='MarkdownV2',
        text=await get_message_by_key(text_key),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
    )
