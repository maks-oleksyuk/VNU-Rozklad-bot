from aiogram import types
from keyboard import setKeyboard

async def answer(message: types.Message, option, data):
    match option:
        case "start":
            await message.answer(
                "👋 *Привіт\!*\n\n"
                + "*Я* – 🤖 помічник, у якого,\n"
                + "ти завжди можеш дізнатись,\n"
                + "які в тебе пари протягом тижня\.\n\n"
                + "🦾 Обери для кого будемо формувати\n"
                + "розклад використовуючи меню знизу:\n\n"
                + "❕Якщо меню недоступне натисни на *⌘*",
                parse_mode = "MarkdownV2",
                reply_markup = await setKeyboard(None, "choice"),
            )
        case "choice":
            await message.answer(
                "🦾 Обери для кого будемо формувати\n"
                + "розклад використовуючи меню знизу:",
                reply_markup = await setKeyboard(None, "choice"),
            )
        case "chair":
            await message.answer(
                "📁 Обери *кафедру* зі списку або\n"
                + "введи прізвище для пошуку 🔎",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard(None, "chair"),
            )
        case "faculty":
            await message.answer(
                "📁 Обери *факультет* зі списку або\n"
                + "введи назву групи для пошуку 🔎",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard(None, "faculty"),
            )
        case "surname":
            await message.answer(
                "📂 Обери *викладача* зі списку:\n",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard(message, "surname"),
            )
        case "group":
            await message.answer(
                "📂 Обери *групу* зі списку:\n",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard(message, "group"),
            )
        case "data":
            await message.answer(
                data, parse_mode="MarkdownV2",
                reply_markup = await setKeyboard(None, "timetable"))

        case "not_data":
            await message.answer(
                "🌀 Обери для кого будемо формувати розклад",
                reply_markup = await setKeyboard(None, "choice"))

async def reply(message: types.Message, option):
    match option:
        case "goodsearchGroup":
            await message.reply(
                "🗂 Ось що я знайшов:",
                reply_markup = await setKeyboard(message, "searchGroup"),
            )
        case "failsearchGroup":
            await message.reply(
                "За цим запитом нічого не знайдено🧐\n\n"
                + "⁉️ Вкажіть більш точні дані або\n"
                + "📁 використовуйте меню знизу:",
                reply_markup = await setKeyboard(message, "faculty"),
            )
        case "goodsearchTeacher":
            await message.reply(
                "🗂 Ось що я знайшов:",
                reply_markup = await setKeyboard(message, "searchTeacher"),
            )
        case "failsearchTeacher":
            await message.reply(
                "За цим запитом нічого не знайдено🧐\n\n"
                + "⁉️ Вкажіть більш точні дані або\n"
                + "📁 використовуйте меню знизу:",
                reply_markup = await setKeyboard(message, "chair"),
            )
    