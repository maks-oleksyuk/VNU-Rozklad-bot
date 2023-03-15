from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db
from ..utils.messages import answer, reply


class FSMStudent(StatesGroup):
    """Class representing finite state machine for groups-related operations."""
    faculty = State()  # State for selecting the faculty.
    group = State()  # State for entering group name.
    search = State()  # State for searching for the group.


@dp.message_handler(state=FSMStudent.faculty)
async def process_faculty(message: types.Message, state: FSMContext) -> None:
    """The process of choosing a faculty for the group.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.
    """
    # If the user enters '⬅️ Назад', the cancellation command is called.
    if message.text == '⬅️ Назад':
        from ..commands.default import cmd_cancel
        await cmd_cancel(message, state)
    # If the text matches the department in the database, go to next state.
    elif message.text in await db.get_departments_by_mode('groups'):
        await FSMStudent.next()
        await answer(message, 'group', 'group')
    # Otherwise, the message is passed to the search state.
    else:
        await process_search(message, state)


@dp.message_handler(state=FSMStudent.group)
async def process_group(message: types.Message, state: FSMContext) -> None:
    """The process of choosing a name for the group.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.
    """
    # If the user sends '⬅️ Назад', goes back to the faculty state.
    if message.text == '⬅️ Назад':
        await FSMStudent.previous()
        await answer(message, 'faculty', 'faculty')
    # Otherwise, the message is passed to the search state.
    else:
        await process_search(message, state)


@dp.message_handler(state=FSMStudent.search)
async def process_search(message: types.Message, state: FSMContext) -> None:
    """Process the user's search for a group name.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.
    """
    # Activate the current State, for the correct back button.
    await FSMStudent.last()
    # If the user sends '⬅️ Назад', goes back to the faculty state.
    if message.text == '⬅️ Назад':
        await FSMStudent.first()
        await answer(message, 'faculty', 'faculty')
    else:
        groups = await db.search('groups', message.text)
        # If the search query returns only one result,
        # saves the teacher's name to the user's data and ends the state.
        if len(groups) == 1:
            await state.finish()
            await db.save_user_data(message, 'group')
            # await skd_cmd.today(message)
        # If multiple results, sends a message with a list of the results.
        elif len(groups) > 1:
            await reply(message, 'good-search', 'search-group')
        # If the search query returns no results, goes back to the 'chair' state
        # and sends a message to the user indicating that the search failed.
        else:
            await FSMStudent.first()
            await reply(message, 'fail-search', 'faculty')
