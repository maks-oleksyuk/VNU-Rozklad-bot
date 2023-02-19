from aiogram import Dispatcher, types
from bot.database import user_data
from bot.message import answer
from bot.timetable import now_subject


async def now(message: types.Message):
    id = await user_data(message, "get_data_id", None)
    try:
        if id[0] is not None:
            mes = await now_subject(message, id[2], id[0])
            await answer(message, "data", mes)
        else:
            await answer(message, "no-data")
    except:
        await answer(message, "no-data")


def register_handlers_schedule_commands(dp: Dispatcher):
    dp.register_message_handler(now, commands="now",
                                chat_type=types.ChatType.PRIVATE)
