from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from ..config import dp


class FSMStudent(StatesGroup):
    faculty = State()
    group = State()
    search = State()


@dp.message_handler(state=FSMStudent.faculty)
async def process_faculty(message: types.Message, state: FSMContext):
    pass
    # if message.text == '⬅️ Назад':
    #     await state.finish()
    #     await cmd_cancel(message, state)
    # elif message.text in faculty:
    #     await FSMStudent.next()
    #     await answer(message, 'group', 'group')
    # else:
    #     await set_group_search(message, state)
