from aiogram import types
from keyboard import setKeyboard

async def answer(message: types.Message, option):
    match option:
        case "start":
            await message.answer(
                "👋 *Привіт!*\n\n"
                + "*Я* – 🤖 помічник, у якого,\n"
                + "ти завжди можеш дізнатись,\n"
                + "які в тебе пари протягом тижня.\n\n"
                + "🦾 Обери для кого будемо формувати\n"
                + "розклад використовуючи меню знизу:\n\n"
                + "❕Якщо меню недоступне натисни на *⌘*",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard(None, "choice"),
            )
        case "choice":
            await message.answer(
                "🦾 Обери для кого будемо формувати\n"
                + "розклад використовуючи меню знизу:",
                reply_markup = await setKeyboard(None, "choice"),
            )
        case "faculty":
            await message.answer(
                "*☰* Обери *факультет* зі списку або\n"
                + "введи назву групи для пошуку 🔎",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard(None, "faculty"),
            )
        case "group":
            await message.answer(
            "*☶* Обери *групу* зі списку:\n",
            parse_mode = "Markdown",
            reply_markup = await setKeyboard(message, "group"),
        )

async def reply(message: types.Message, option):
    match option:
        case "goodsearch":
            await message.reply(
                "🗂 Ось що я знайшов:",
                reply_markup = await setKeyboard(message, "search"),
            )
        case "failsearch":
            await message.reply(
                "За цим запитом нічого не знайдено🧐\n\n"
                + "⁉️ Вкажіть більш точні дані або\n"
                + " ☰  використовуйте меню знизу:",
                reply_markup = await setKeyboard(message, "faculty"),
            )

    