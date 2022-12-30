from datetime import date

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.config import (chair, faculty, get_group_id, get_teacher_id, is_date,
                        search_group, search_teacher)
from bot.database import user_data
from bot.message import answer, reply

from bot.handlers import sched_cmd


# -----------------------------------------------------------
# Implementation of basic handlers
# -----------------------------------------------------------

# Implementation of the handler for command /start
async def start(message: types.Message):
    await answer(message, "start")
    await user_data(message, "save", None)


# Implementation of a handler for text messages
async def text(message: types.Message):
    match message.text:
        case "Студент 🎓":
            await FSMStudent.faculty.set()
            await answer(message, "faculty")
        case "Викладач 💼":
            await FSMTeaсher.chair.set()
            await answer(message, "chair")
        case "сьогодні":
            await sched_cmd.today(message)
        case "На тиждень":
            await sched_cmd.week(message)
        case "Пн" | "Вт" | "Ср" | "Чт" | "Пт" | "Сб" | "Нд" | "🔘":
            await sched_cmd.get_day_timetable(message, None)
        case "⬅️ тиждень":
            await sched_cmd.changeweek(message, "prev")
        case "тиждень ➡️":
            await sched_cmd.changeweek(message, "next")
        case "Змінити запит":
            await cancel(message, None)
        case "📆 Ввести дату":
            await answer(message, "set-date")
            await FSMSetDate.set_date.set()


# Implementation of the handler for command /cancel
async def cancel(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    await user_data(message, "save", None)
    await answer(message, "choice", None)


# -----------------------------------------------------------
# Implementation of the branch of development for the student
# -----------------------------------------------------------

class FSMStudent(StatesGroup):
    faculty = State()
    group = State()
    search = State()


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
        gr = await search_group(message.text)
        if len(gr) == 1:
            await state.finish()
            arr_data = await get_group_id(gr[0]) + ["group", date.today()]
            await user_data(message, "save", None)
            await user_data(message, "data", arr_data)
            await sched_cmd.today(message)
        elif len(gr) > 1:
            await reply(message, "good-search-group")
        else:
            await FSMStudent.faculty.set()
            await reply(message, "fail-search-group")


# -----------------------------------------------------------
# Implementation of the branch of development for the teacher
# -----------------------------------------------------------

class FSMTeacher(StatesGroup):
    chair = State()
    surname = State()
    search = State()


async def setTeacherChair(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.finish()
        await cancel(message, state)
    elif message.text in chair:
        await FSMTeacher.next()
        await answer(message, "surname")
    else:
        await setTeacherSearch(message, state)


async def setTeacherSurname(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await FSMTeacher.chair.set()
        await answer(message, "chair")
    else:
        await setTeacherSearch(message, state)


async def setTeacherSearch(message: types.Message, state: FSMContext):
    await FSMTeacher.search.set()
    if message.text == "⬅️ Назад":
        await FSMTeacher.chair.set()
        await answer(message, "chair")
    else:
        tr = await search_teacher(message.text)
        if len(tr) == 1:
            await state.finish()
            arr_data = await get_teacher_id(tr[0]) + ["teacher", date.today()]
            await user_data(message, "save", None)
            await user_data(message, "data", arr_data)
            await sched_cmd.today(message)
        elif len(tr) > 1:
            await reply(message, "good-search-teacher")
        else:
            await FSMTeacher.chair.set()
            await reply(message, "fail-search-teacher")


# -----------------------------------------------------------
# Handler implementation of date input from user
# -----------------------------------------------------------

class FSMSetDate(StatesGroup):
    set_date = State()


async def cancel_date(message: types.Message, state: FSMSetDate):
    await state.finish()
    await answer(message, "cancel-date")


async def set_date(message: types.Message, state: FSMContext):
    new_date = await is_date(message.text)
    if new_date:
        await state.finish()
        await sched_cmd.get_day_timetable(message, new_date)
    else:
        await answer(message, "error-date")


async def setdate(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] != None:
            await answer(message, "set-date")
            await FSMSetDate.set_date.set()
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data")


# -----------------------------------------------------------
# Registration of all handlers
# -----------------------------------------------------------

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, chat_type=types.ChatType.PRIVATE, commands="start")
    dp.register_message_handler(cancel_date, state=FSMSetDate.set_date, chat_type=types.ChatType.PRIVATE,
                                commands="cancel")
    dp.register_message_handler(cancel, state="*", chat_type=types.ChatType.PRIVATE, commands="cancel", )
    dp.register_message_handler(setdate, chat_type=types.ChatType.PRIVATE, commands="setdate")
    dp.register_message_handler(text, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentFaculty, state=FSMStudent.faculty, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setTeacherChair, state=FSMTeacher.chair, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setStudentGroup, state=FSMStudent.group, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setTeacherSurname, state=FSMTeacher.surname, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setGroupSearch, state=FSMStudent.search, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(setTeacherSearch, state=FSMTeacher.search, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_date, state=FSMSetDate.set_date, chat_type=types.ChatType.PRIVATE)
