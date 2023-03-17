from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db
from ..utils import is_date
from ..utils.messages import answer
from ..utils.timetable import timetable_for_date


class FSMSetDate(StatesGroup):
    """The FSMSetDate class defines a state group with one state set_date."""
    set_date = State()


@dp.message_handler(commands=['cancel'], state=FSMSetDate.set_date)
async def cmd_cancel_date(message: types.Message, state: FSMSetDate) -> types.Message:
    """Handler function for the `/cancel` command when in the 'set_date' state.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.

    Returns:
        types.Message: The message object sent as a response to the user.
    """
    await state.finish()
    return await answer(message, 'cancel-date')


@dp.message_handler(state=FSMSetDate.set_date)
async def set_date(message: types.Message, state: FSMContext) -> types.Message:
    """Handler function for setting a new date in the user's data.

    Args:
        message: The message sent by the user.
        state: Current state of the conversation for the user.

    Returns:
        types.Message: A message with the schedule for the new date,
            or an error message if the user entered an invalid date.
    """
    new_date = await is_date(message.text)
    if new_date:
        await state.finish()
        await db.update_user_data_date(message.from_user.id, new_date)
        return await timetable_for_date(message, new_date)
    else:
        return await answer(message, 'date-error')
