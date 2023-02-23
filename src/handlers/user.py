import handlers.skd_cmd as skd_cmd
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import is_date
from database.db import save_user_data, search, update_user_data_date
from services.message import answer, reply
from services.storage import chair, faculty
from services.timetable import change_week_day, change_week, timetable_for_date

from .commands import cmd_cancel


# -----------------------------------------------------------
# Implementation of basic handlers
# -----------------------------------------------------------

# Implementation of a handler for text messages
async def text(message: types.Message):
    match message.text:
        case 'Студент 🎓':
            await FSMStudent.faculty.set()
            await answer(message, 'faculty', 'faculty')
        case 'Викладач 💼':
            await FSMTeacher.chair.set()
            await answer(message, 'chair', 'chair')
        case 'сьогодні':
            await skd_cmd.today(message)
        case 'на тиждень':
            await skd_cmd.week(message)
        case 'пн' | 'вт' | 'ср' | 'чт' | 'пт' | 'сб' | 'нд' | '🟢':
            await change_week_day(message)
        case '⬅️ тиждень':
            await change_week(message, 'prev')
        case 'тиждень ➡️':
            await change_week(message, 'next')
        case 'Змінити запит':
            await cmd_cancel(message)
        case 'Ввести дату':
            await answer(message, 'set-date')
            await FSMSetDate.set_date.set()


# -----------------------------------------------------------
# Implementation of the branch of development for the student
# -----------------------------------------------------------

class FSMStudent(StatesGroup):
    faculty = State()
    group = State()
    search = State()


async def set_student_faculty(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад':
        await state.finish()
        await cmd_cancel(message, state)
    elif message.text in faculty:
        await FSMStudent.next()
        await answer(message, 'group', 'group')
    else:
        await set_group_search(message, state)


async def set_student_group(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад':
        await FSMStudent.faculty.set()
        await answer(message, 'faculty', 'faculty')
    else:
        await set_group_search(message, state)


async def set_group_search(message: types.Message, state: FSMContext):
    await FSMStudent.search.set()
    if message.text == '⬅️ Назад':
        await FSMStudent.faculty.set()
        await answer(message, 'faculty', 'faculty')
    else:
        groups = await search('groups', message.text)
        if len(groups) == 1:
            await state.finish()
            await save_user_data(message, 'group')
            await skd_cmd.today(message)
        elif len(groups) > 1:
            await reply(message, 'good-search', 'search-group')
        else:
            await FSMStudent.faculty.set()
            await reply(message, 'fail-search', 'faculty')


# -----------------------------------------------------------
# Implementation of the branch of development for the teacher
# -----------------------------------------------------------

class FSMTeacher(StatesGroup):
    chair = State()
    surname = State()
    search = State()


async def set_teacher_chair(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад':
        await state.finish()
        await cmd_cancel(message, state)
    elif message.text in chair:
        await FSMTeacher.next()
        await answer(message, 'surname', 'surname')
    else:
        await set_teacher_search(message, state)


async def set_teacher_surname(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад':
        await FSMTeacher.chair.set()
        await answer(message, 'chair', 'chair')
    else:
        await set_teacher_search(message, state)


async def set_teacher_search(message: types.Message, state: FSMContext):
    await FSMTeacher.search.set()
    if message.text == '⬅️ Назад':
        await FSMTeacher.chair.set()
        await answer(message, 'chair', 'chair')
    else:
        teachers = await search('teachers', message.text)
        if len(teachers) == 1:
            await state.finish()
            message.text = teachers[0]
            await save_user_data(message, 'teacher')
            await skd_cmd.today(message)
        elif len(teachers) > 1:
            await reply(message, 'good-search', 'search-teacher')
        else:
            await FSMTeacher.chair.set()
            await reply(message, 'fail-search', 'chair')


# -----------------------------------------------------------
# Handler implementation of date input from user
# -----------------------------------------------------------

class FSMSetDate(StatesGroup):
    set_date = State()


async def cmd_cancel_date(message: types.Message, state: FSMSetDate):
    await state.finish()
    await answer(message, 'cancel-date')


async def set_date(message: types.Message, state: FSMContext):
    new_date = await is_date(message.text)
    if new_date:
        await state.finish()
        await update_user_data_date(message.from_user.id, new_date)
        await timetable_for_date(message, new_date)
    else:
        await answer(message, 'date-error')


# -----------------------------------------------------------
# Registration of all handlers
# -----------------------------------------------------------

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel_date, state=FSMSetDate.set_date,
                                chat_type=types.ChatType.PRIVATE,
                                commands='cancel')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*',
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(text, chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_student_faculty, state=FSMStudent.faculty,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_teacher_chair, state=FSMTeacher.chair,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_student_group, state=FSMStudent.group,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_teacher_surname, state=FSMTeacher.surname,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_group_search, state=FSMStudent.search,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_teacher_search, state=FSMTeacher.search,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_date, state=FSMSetDate.set_date,
                                chat_type=types.ChatType.PRIVATE)
