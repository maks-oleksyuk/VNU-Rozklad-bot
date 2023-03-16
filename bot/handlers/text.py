from aiogram import types

from loader import dp
from ..commands import schedule
from ..commands.default import cmd_cancel
from ..utils.messages import answer
from ..utils.timetable import change_week, change_week_day


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text(message: types.Message) -> None:
    """Handler function for processing text messages.

    Args:
        message: The message sent by the user.
    """
    match message.text:
        case 'Студент 🎓':
            # Importing a class here and not at the beginning,
            # for the correct order of handlers in the Dispatcher.
            from ..states.student import FSMStudent
            await FSMStudent.first()
            await answer(message, 'faculty', 'faculty')
        case 'Викладач 💼':
            # Importing a class here and not at the beginning,
            # for the correct order of handlers in the Dispatcher.
            from ..states.teacher import FSMTeacher
            await FSMTeacher.first()
            await answer(message, 'chair', 'chair')
        case 'сьогодні':
            await schedule.today(message)
        case 'на тиждень':
            await schedule.week(message)
        case 'пн' | 'вт' | 'ср' | 'чт' | 'пт' | 'сб' | 'нд' | '🟢':
            await change_week_day(message)
        case '⬅️ тиждень':
            await change_week(message, 'prev')
        case 'тиждень ➡️':
            await change_week(message, 'next')
        case 'Змінити запит':
            await cmd_cancel(message)
        case 'Ввести дату':
            await schedule.set_date(message)
