from config import bot, dp, faculty
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from request import getFaculties
from keyboard import setKeyboard

class FSMStudent(StatesGroup):
    faculty = State()
    group = State()


async def start(message: types.Message):
    await message.answer(
        "👋 *Привіт!*\n\n"
        + "*Я* – 🤖 помічник, у якого,\n"
        + "ти завжди можеш дізнатись,\n"
        + "які в тебе пари протягом тижня.\n\n"
        + "🦾 Обери для кого будемо формувати\n"
        + "розклад використовуючи меню знизу:\n\n"
        + "❕Якщо меню недоступне натисни на *⌘*",
        parse_mode = "Markdown",
        reply_markup = await setKeyboard(None, 1),
    )


async def text(message: types.Message):
    match message.text:
        case "Студент 🎓":
            getFaculties()
            await FSMStudent.faculty.set()
            await message.answer(
                "📑 Обери *факультет* зі списку або\n"
                + "введи назву групи для пошуку 🔎",
                parse_mode = "Markdown",
                reply_markup = await setKeyboard(None, 2.1),
            )
            
        case "Викладач 💼":
            print("Заглушка для викладача")


async def cancelFSMStudent(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "🦾 Обери для кого будемо формувати\n"
        + "розклад використовуючи меню знизу:",
        reply_markup = await setKeyboard(None, 1),
    )


async def setStudentFaculty(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await cancelFSMStudent(message, state)
    elif message.text in faculty:
        await FSMStudent.next()
        await message.answer(
            "📑 Обери *групу* зі списку або\n"
            + "введи назву групи для пошуку 🔎",
            parse_mode = "Markdown",
            reply_markup = await setKeyboard(message, 2.12),
        )
    else:
        print("Заглушка для пошуку")
    print("Кінець 1 стану очікування")


async def setStudentGroup(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        # await setStudentFaculty(message, state)
        await message.answer(
            "📑 Обери *факультет* зі списку або\n"
            + "введи назву групи для пошуку 🔎",
            parse_mode = "Markdown",
            reply_markup = await setKeyboard(None, 2.1),
        )
    print("Кінець 2 стану очікування")
    await state.finish()

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cancelFSMStudent, commands="cancel", state="*", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(text, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentFaculty, state=FSMStudent.faculty, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentGroup, state=FSMStudent.group, chat_type=types.ChatType.PRIVATE)
