from aiogram import types
from .storage import getMessageByKey


async def answer(message: types.Message, text_key: str, markup=None):
    await message.answer(
        text=await getMessageByKey(text_key),
        parse_mode="MarkdownV2",
        reply_markup=markup,
    )
