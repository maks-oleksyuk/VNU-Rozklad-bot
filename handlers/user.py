from config import bot, dp, faculty, searchGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from request import getFaculties
from keyboard import setKeyboard
from message import answer, reply

class FSMStudent(StatesGroup):
    faculty = State()
    group   = State()
    search  = State()


async def start(message: types.Message):
    await answer(message, "start")


async def text(message: types.Message):
    match message.text:
        case "Студент 🎓":
            await getFaculties()
            await FSMStudent.faculty.set()
            await answer(message, "faculty")
        case "Викладач 💼":
            print("Заглушка для викладача")


async def cancelFSMStudent(message: types.Message, state: FSMContext):
    await state.finish()
    await answer(message, "choice")


async def setStudentFaculty(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await cancelFSMStudent(message, state)
    elif message.text in faculty:
        await FSMStudent.next()
        await answer(message, "group")
    else:
        await setGroupSearch(message, state)


async def setStudentGroup(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.finish()
        await FSMStudent.faculty.set()
        await answer(message, "faculty")
    else:
        await setGroupSearch(message, state)

async def setGroupSearch(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.finish()
        await FSMStudent.faculty.set()
        await answer(message, "faculty")
    else:
        l = len(await searchGroup(message.text))
        if l == 1:
            await state.finish()
            await message.answer(
                "👋 Функціонал у розробці",
                reply_markup = await setKeyboard(message, "timetable")
            )
        elif l > 1:
            await reply(message, "goodsearch")
        else:
            await reply(message, "failsearch")

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cancelFSMStudent, commands="cancel", state="*", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(text, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentFaculty, state=FSMStudent.faculty, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentGroup, state=FSMStudent.group, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setGroupSearch, state=FSMStudent.search, chat_type=types.ChatType.PRIVATE)

