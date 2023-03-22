from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import db, dp
from ..utils import is_date
from ..utils.messages import answer


class FSMRooms(StatesGroup):
    date = State()
    lesson = State()
    block = State()
    over = State()
    type = State()


@dp.message_handler(state=FSMRooms.date)
async def process_date(message: types.Message, state: FSMContext) -> types.Message:
    date = await is_date(message.text)
    if date:
        async with state.proxy() as data:
            data['date'] = date
        await FSMRooms.next()
        return await answer(message, 'process_lesson')
    else:
        return await answer(message, 'date-error')


@dp.message_handler(state=FSMRooms.lesson)
async def process_lesson(message: types.Message, state: FSMContext) -> types.Message:
    if message.text in ['1', '2', '3', '4', '5', '6', '7', '8']:
        async with state.proxy() as data:
            data['lesson'] = int(message.text)
        await FSMRooms.next()
        return await answer(message, 'process_lesson_success', 'blocks')
    else:
        return await answer(message, 'process_lesson_error')


@dp.message_handler(state=FSMRooms.block)
async def process_block(message: types.Message, state: FSMContext) -> types.Message:
    if message.text in await db.get_audience_blocks():
        if await db.get_block_overs(message.text):
            await FSMRooms.next()
            return await answer(message, 'process_block_success', 'group')
        else:
            await FSMRooms.last()
            return await answer(message, 'process_block_success_type', 'room-type')
    else:
        return await answer(message, 'process_block_error')


@dp.message_handler(state=FSMRooms.over)
async def process_over(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(state=FSMRooms.type)
async def process_type(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад':
        await FSMRooms.previous()
    await state.finish()
