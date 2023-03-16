from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db
from ..utils.messages import answer, reply
from ..commands.schedule import today


class FSMTeacher(StatesGroup):
    """Class representing finite state machine for teacher-related operations."""
    chair = State()  # State for selecting the chair.
    teacher = State()  # State for entering teacher's name.
    search = State()  # State for searching for the teacher.


@dp.message_handler(state=FSMTeacher.chair)
async def process_chair(message: types.Message, state: FSMContext) -> None:
    """Process teacher's chair selection.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.
    """
    # If the user enters '⬅️ Назад', the cancellation command is called.
    if message.text == '⬅️ Назад':
        from ..commands.default import cmd_cancel
        await cmd_cancel(message, state)
    # If the text matches the department in the database, go to next state.
    elif message.text in await db.get_departments_by_mode('teachers'):
        await FSMTeacher.next()
        await answer(message, 'surname', 'surname')
    # Otherwise, the message is passed to the search state.
    else:
        await process_search(message, state)


@dp.message_handler(state=FSMTeacher.teacher)
async def process_teacher(message: types.Message, state: FSMContext) -> None:
    """Process teacher's name selection.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.
    """
    # If the user sends '⬅️ Назад', goes back to the chair state.
    if message.text == '⬅️ Назад':
        await FSMTeacher.previous()
        await answer(message, 'chair', 'chair')
    # Otherwise, the message is passed to the search state.
    else:
        await process_search(message, state)


@dp.message_handler(state=FSMTeacher.search)
async def process_search(message: types.Message, state: FSMContext) -> None:
    """Processes a user search query for a teacher's name.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.
    """
    # Activate the current state, for the correct back button work.
    await FSMTeacher.last()
    # If the user sends '⬅️ Назад', goes back to the chair state.
    if message.text == '⬅️ Назад':
        await FSMTeacher.first()
        await answer(message, 'chair', 'chair')
    else:
        teachers = await db.search('teachers', message.text)
        # If the search query returns only one result,
        # saves the teacher's name to the user's data and ends the state.
        if len(teachers) == 1:
            await state.finish()
            # Replace the message text with a short form of the teacher's name to save.
            message.text = teachers[0]
            await db.save_user_data(message, 'teacher')
            await today(message)
        # If multiple results, sends a message with a list of the results.
        elif len(teachers) > 1:
            await reply(message, 'good-search', 'search-teacher')
        # If the search query returns no results, goes back to the 'chair' state
        # and sends a message to the user indicating that the search failed.
        else:
            await FSMTeacher.first()
            await reply(message, 'fail-search', 'chair')
