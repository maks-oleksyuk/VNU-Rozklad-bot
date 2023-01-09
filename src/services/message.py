from aiogram import types

from .keyboard import get_reply_keyboard_by_key
from .storage import get_message_by_key


async def answer(message: types.Message, text_key: str, markup_key=None, **kwargs):
    await message.answer(
        parse_mode='MarkdownV2',
        text=await get_message_by_key(text_key),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
        disable_web_page_preview=kwargs.get('disable_web_page_preview', None)
    )


async def reply(message: types.Message, text_key: str, markup_key=None, **kwargs):
    await message.reply(
        parse_mode='MarkdownV2',
        text=await get_message_by_key(text_key),
        reply_markup=await get_reply_keyboard_by_key(message, markup_key),
        disable_web_page_preview=kwargs.get('disable_web_page_preview', None)
    )
