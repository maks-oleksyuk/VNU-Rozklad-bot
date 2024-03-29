from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.storage import room_types
from loader import api, db, dp
from ..utils import add_room_floor, is_date
from ..utils.messages import answer
from ..utils.timetable import formation_free_rooms


class FSMRooms(StatesGroup):
    date = State()
    lesson = State()
    block = State()
    over = State()
    type = State()


@dp.message_handler(state=FSMRooms.date)
async def process_date(message: types.Message, state: FSMContext) -> types.Message:
    user_date = ''
    if message.text == '⬅️ Назад':
        from ..commands.default import cmd_cancel
        return await cmd_cancel(message, state)
    elif message.text == 'сьогодні':
        user_date = date.today()
    elif message.text == 'завтра':
        user_date = date.today() + timedelta(days=1)
    else:
        user_date = await is_date(message.text)
    if user_date:
        await state.update_data(date=user_date)
        await FSMRooms.next()
        return await answer(message, 'set-lesson-for-rooms', 'lessons')
    else:
        return await answer(message, 'date-error', 'rooms-date')


@dp.message_handler(state=FSMRooms.lesson)
async def process_lesson(message: types.Message, state: FSMContext) -> types.Message:
    if message.text == '⬅️ Назад':
        await FSMRooms.previous()
        return await answer(message, 'set-date-for-rooms', 'rooms-date')
    elif message.text in ['1', '2', '3', '4', '5', '6', '7', '8']:
        await state.update_data(lesson=int(message.text))
        await FSMRooms.next()
        return await answer(message, 'set-block-for-rooms', 'blocks')
    else:
        return await answer(message, 'set-data-for-rooms-error')


@dp.message_handler(state=FSMRooms.block)
async def process_block(message: types.Message, state: FSMContext) -> types.Message:
    if message.text == '⬅️ Назад':
        await FSMRooms.previous()
        return await answer(message, 'set-lesson-for-rooms', 'lessons')
    elif message.text in await db.get_audience_blocks():
        await state.update_data(block=message.text)
        if await db.get_block_floors(message.text):
            await FSMRooms.next()
            return await answer(message, 'set-floor-for-rooms', 'over')
        else:
            await state.update_data(floor=None)
            await FSMRooms.last()
            return await answer(message, 'set-type-for-rooms', 'room-type')
    else:
        return await answer(message, 'set-data-for-rooms-error')


@dp.message_handler(state=FSMRooms.over)
async def process_floor(message: types.Message, state: FSMContext) -> types.Message:
    data = await state.get_data()
    if message.text == '⬅️ Назад':
        await FSMRooms.previous()
        return await answer(message, 'set-block-for-rooms', 'blocks')
    elif message.text in list(map(str, await db.get_block_floors(data['block']))):
        await state.update_data(floor=int(message.text))
        await FSMRooms.next()
        return await answer(message, 'set-type-for-rooms', 'room-type')
    else:
        return await answer(message, 'set-data-for-rooms-error')


@dp.message_handler(state=FSMRooms.type)
async def process_type(message: types.Message, state: FSMContext) -> types.Message:
    if message.text == '⬅️ Назад':
        data = await state.get_data()
        if data['floor'] is not None:
            message.text = data['block']
            await FSMRooms.previous()
            return await answer(message, 'set-floor-for-rooms', 'over')
        else:
            await FSMRooms.block.set()
            return await answer(message, 'set-block-for-rooms', 'blocks')
    elif message.text in room_types.values():
        await state.update_data(type=[k for k, v in room_types.items() if v == message.text][0])
        data = await state.get_data()
        await state.finish()
        rooms = await api.get_free_rooms(data['date'], data['lesson'], data['block'], data['type'])
        if rooms:
            rooms = await add_room_floor(rooms)
            rooms = list(filter(lambda x: x.get('floor') == data['floor'], rooms))
        await formation_free_rooms(message, data, rooms)
    else:
        return await answer(message, 'set-data-for-rooms-error')
