from config import bot, dp
from config import faculty, chair
from config import searchGroup, searchTeacher
from message import answer, reply
from keyboard import setKeyboard
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# -----------------------------------------------------------
# Implementation of basic handlers
# -----------------------------------------------------------

# Implementation of the handler for command /start
async def start(message: types.Message):
    await answer(message, "start")


# Implementation of a handler for text messages
async def text(message: types.Message):
    match message.text:
        case "Студент 🎓":
            await FSMStudent.faculty.set()
            await answer(message, "faculty")
        case "Викладач 💼":
            await FSMTeaсher.chair.set()
            await answer(message, "chair")


# Implementation of the handler for command /cancel
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await answer(message, "choice")

# -----------------------------------------------------------
# Implementation of the branch of development for the student
# -----------------------------------------------------------

class FSMStudent(StatesGroup):
    faculty = State()
    group   = State()
    search  = State()


async def setStudentFaculty(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.finish()
        await cancel(message, state)
    elif message.text in faculty:
        await FSMStudent.next()
        await answer(message, "group")
    else:
        await setGroupSearch(message, state)

async def setStudentGroup(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await FSMStudent.faculty.set()
        await answer(message, "faculty")
    else:
        await setGroupSearch(message, state)

async def setGroupSearch(message: types.Message, state: FSMContext):
    await FSMStudent.search.set()
    if message.text == "⬅️ Назад":
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
            await reply(message, "goodsearchGroup")
        else:
            await reply(message, "failsearchGroup")

# -----------------------------------------------------------
# Implementation of the branch of development for the teacher
# -----------------------------------------------------------

class FSMTeaсher(StatesGroup):
    chair   = State()
    surname = State()
    search  = State()

async def setTeaсherChair(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.finish()
        await cancel(message, state)
    elif message.text in chair:
        await answer(message, "surname")
    else:
        await setTeacherSearch(message, state)


async def setTeacherSurname(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await FSMTeaсher.chair.set()
        await answer(message, "chair")
    else:
        await setTeacherSearch(message, state)


async def setTeacherSearch(message: types.Message, state: FSMContext):
    await FSMTeaсher.search.set()
    if message.text == "⬅️ Назад":
        await FSMTeaсher.chair.set()
        await answer(message, "chair")
    else:
        l = len(await searchTeacher(message.text))
        if l == 1:
            await state.finish()
            await message.answer(
                "👋 Функціонал у розробці",
                reply_markup = await setKeyboard(message, "timetable")
            )
        elif l > 1:
            await reply(message, "goodsearchTeacher")
        else:
            await reply(message, "failsearchTeacher")


# -----------------------------------------------------------
# Registration of all handlers
# -----------------------------------------------------------

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start,  commands = "start", chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(cancel, commands = "cancel", state = "*", chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(text, chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentFaculty, state = FSMStudent.faculty, chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(setTeaсherChair,   state = FSMTeaсher.chair,   chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentGroup,   state = FSMStudent.group,   chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(setTeacherSurname, state = FSMTeaсher.surname, chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(setGroupSearch,    state = FSMStudent.search,  chat_type = types.ChatType.PRIVATE)
    dp.register_message_handler(setTeacherSearch,  state = FSMTeaсher.search,  chat_type = types.ChatType.PRIVATE)


