from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db
from ..utils.messages import answer


class FSMStudent(StatesGroup):
    faculty = State()
    group = State()
    search = State()


@dp.message_handler(state=FSMStudent.faculty)
async def process_faculty(message: types.Message, state: FSMContext) -> None:
    if message.text == '⬅️ Назад':
        from ..commands.default import cmd_cancel
        await cmd_cancel(message, state)
    elif message.text in await db.get_departments_by_mode('groups'):
        await FSMStudent.next()
        await answer(message, 'group', 'group')
    else:
        await FSMStudent.last()


@dp.message_handler(state=FSMStudent.group)
async def process_group(message: types.Message, state: FSMContext) -> None:
    if message.text == '⬅️ Назад':
        await FSMStudent.faculty.set()
        await answer(message, 'faculty', 'faculty')
    else:
        await FSMStudent.next()


@dp.message_handler(state=FSMStudent.search)
async def process_search(message: types.Message, state: FSMContext) -> None:
    if message.text == '⬅️ Назад':
        await FSMStudent.previous()
        await answer(message, 'faculty', 'faculty')
    else:
        groups = await db.search('groups', message.text)
        if len(groups) == 1:
            await state.finish()
            # await save_user_data(message, 'group')
            # await skd_cmd.today(message)
        # elif len(groups) > 1:
        #     await reply(message, 'good-search', 'search-group')
        # else:
        #     await FSMStudent.first()
        #     await reply(message, 'fail-search', 'faculty')
