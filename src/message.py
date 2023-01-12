from aiogram import types

from keyboard import setKeyboard


async def answer(message: types.Message, option, data=None):
    match option:
        case "data":
            await message.answer(
                data, parse_mode="MarkdownV2",
                reply_markup=await setKeyboard("timetable", message))
        case "no-data":
            await message.answer(
                "🌀 Потрібнe оновлення даних",
                reply_markup=await setKeyboard("choice"))
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
