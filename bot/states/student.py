from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db
from ..utils.messages import answer, reply


class FSMStudent(StatesGroup):
    faculty = State()
    group = State()
    search = State()


@dp.message_handler(state=FSMStudent.faculty)
async def process_faculty(message: types.Message, state: FSMContext) -> None:
    """Processes the faculty information from the user's message and updates the state.

    Args:
        message: The message sent by the user.
        state: The FSMContext object that contains the current state of the conversation.
    """
    if message.text == '⬅️ Назад':
        from ..commands.default import cmd_cancel
        await cmd_cancel(message, state)
    elif message.text in await db.get_departments_by_mode('groups'):
        await FSMStudent.next()
        await answer(message, 'group', 'group')
    else:
        await process_search(message, state)


@dp.message_handler(state=FSMStudent.group)
async def process_group(message: types.Message, state: FSMContext) -> None:
    """Processes the group information from the user's message and updates the state.

    Args:
        message: The message sent by the user.
        state: The FSMContext object that contains the current state of the conversation.
    """
    if message.text == '⬅️ Назад':
        await FSMStudent.faculty.set()
        await answer(message, 'faculty', 'faculty')
    else:
        await process_search(message, state)


@dp.message_handler(state=FSMStudent.search)
async def process_search(message: types.Message, state: FSMContext) -> None:
    """Process the user's search for a group name.

    Args:
        message: The message sent by the user.
        state: The FSMContext object that contains the current state of the conversation.
    """
    # Activate the current State, for the correct back button.
    await FSMStudent.last()
    if message.text == '⬅️ Назад':
        await FSMStudent.first()
        await answer(message, 'faculty', 'faculty')
    else:
        groups = await db.search('groups', message.text)
        if len(groups) == 1:
            await state.finish()
            await db.save_user_data(message, 'group')
            # await skd_cmd.today(message)
        elif len(groups) > 1:
            await reply(message, 'good-search', 'search-group')
        else:
            await FSMStudent.first()
            await reply(message, 'fail-search', 'faculty')
