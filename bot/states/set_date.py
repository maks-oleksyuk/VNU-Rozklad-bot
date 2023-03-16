from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, db
from ..utils import is_date
from ..utils.messages import answer
from ..utils.timetable import timetable_for_date


class FSMSetDate(StatesGroup):
    set_date = State()


@dp.message_handler(state=FSMSetDate.set_date)
async def set_date(message: types.Message, state: FSMContext):
    new_date = await is_date(message.text)
    if new_date:
        await state.finish()
        await db.update_user_data_date(message.from_user.id, new_date)
        await timetable_for_date(message, new_date)
    else:
        await answer(message, 'date-error')
