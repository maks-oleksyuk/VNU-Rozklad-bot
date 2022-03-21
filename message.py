from time import strftime
from aiogram import types
from decouple import config

from keyboard import setKeyboard


async def answer(message: types.Message, option, data=None):
    """Sending a message using the answer aiogram method

    Args:
        message (types.Message): Message with additional data
        option (str): Message identifier to send
        data (str, optional): Data to send. Defaults to None.
    """
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
                reply_markup = await setKeyboard("choice"),
            )
        case "choice":
            await message.answer(
                "🦾 Обери для кого будемо формувати\n"
                + "розклад використовуючи меню знизу:",
                reply_markup = await setKeyboard("choice"),
            )
        case "chair":
            await message.answer(
                "📁 Обери *кафедру* зі списку або\n"
                + "введи прізвище для пошуку 🔎",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard("chair"),
            )
        case "faculty":
            await message.answer(
                "📁 Обери *факультет* зі списку або\n"
                + "введи назву групи для пошуку 🔎",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard("faculty"),
            )
        case "surname":
            await message.answer(
                "📂 Обери *викладача* зі списку:\n",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard("surname", message),
            )
        case "group":
            await message.answer(
                "📂 Обери *групу* зі списку:\n",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard("group", message),
            )
        case "data":
            await message.answer(
                data, parse_mode="MarkdownV2",
                reply_markup = await setKeyboard("timetable", message))
        case "no-data":
            await message.answer(
                "🌀 Потрібнe оновлення даних",
                reply_markup = await setKeyboard("choice"))
        case "set-date":
            await message.answer(
                "📆 *Введіть дату:*\n"
                + "☝️ Найкращий варіант – `dd.mm`\n"
                + "але доступно також багато інших\n\n"
                + "/cancel – для відміни",
                parse_mode="MarkdownV2")
        case "error-date":
            await message.answer(
                "❗️ *Невірний формат дати* ❗️\n"
                + "🌀 Повторіть спробу ще раз\n\n"
                + "☝️ Найкращий варіант – `dd.mm`\n\n"
                + "/cancel – для відміни",
                parse_mode="MarkdownV2")
        case "cancel-date":
            await message.answer("❕ Введеня дати скасовано")
        case "about":
            await message.answer(
                "Бот, для швидкого перегляду розкладу VNU\n\n"
                + "Бот в знаходиться в розробці, тому,\n"
                + "якщо виникнуть якісь проблеми або питання\n"
                + "не соромся і пиши [сюди](tg://user?id=" + str(config("ADMIN_ID"))+ "), він допоможе 😎\n\n"
                + "*Велике дякую* [Tim Boniuk](https://t.me/timboniuk) за чудовий аватар\n\n"
                + "[💸 Підтримати проект](https://send.monobank.ua/8mZyo57Cpu)",
                disable_web_page_preview=True,
                parse_mode="MarkdownV2")
        case "help":
            await message.answer(
                "✳️ __*Для отримання розкладу потрібно\:*__\n\n"
                + "*1\.* Обрати категорію для кого формувати розклад\n"
                + "*2\.* Обрати потрібні дані, або скористатись пошуком\n\n"
                + "⚠️ Якщо помилився або передумав, існує команда /cancel\n\n"
                + "❕Якщо меню недоступне натисни на *⌘*",
                parse_mode="MarkdownV2")


async def reply(message: types.Message, option):
    """Sending a message using the reply aiogram method

    Args:
        message (types.Message): Message with additional data
        option (str): Message identifier to send
    """
    match option:
        case "good-search-group":
            await message.reply(
                "🗂 Ось що я знайшов:",
                reply_markup = await setKeyboard("search-group", message),
            )
        case "fail-search-group":
            await message.reply(
                "За цим запитом нічого не знайдено🧐\n\n"
                + "⁉️ Вкажіть більш точні дані або\n"
                + "📁 використовуйте меню знизу:",
                reply_markup = await setKeyboard("faculty", message),
            )
        case "good-search-teacher":
            await message.reply(
                "🗂 Ось що я знайшов:",
                reply_markup = await setKeyboard("search-teacher", message),
            )
        case "fail-search-teacher":
            await message.reply(
                "За цим запитом нічого не знайдено🧐\n\n"
                + "⁉️ Вкажіть більш точні дані або\n"
                + "📁 використовуйте меню знизу:",
                reply_markup = await setKeyboard("chair", message),
            )
    