from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp, db
from ..states.student import FSMStudent
from ..utils.messages import answer


@dp.message_handler(CommandStart())
async def start(message: types.Message) -> None:
    """Handler function for the `/start` command.

    Args:
        message (types.Message): object representing the message sent by the user.
    """
    await answer(message, 'start', 'choice')
    await db.insert_update_user(message)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text(message: types.Message) -> None:
    """
    Handler function for processing text messages.

    Args:
        message (types.Message): object representing the received message.
    """
    match message.text:
        case 'Студент 🎓':
            await FSMStudent.faculty.set()
            await answer(message, 'faculty', 'faculty')
