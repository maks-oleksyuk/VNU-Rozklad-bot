from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp, db
from ..utils.messages import answer


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message) -> None:
    """Handler function for the `/start` command.

    Args:
        message: object representing the message sent by the user.
    """
    await answer(message, 'start', 'choice')
    await db.insert_update_user(message)


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext = None) -> None:
    """Handler function for the `/cancel` command, allow cancel any action.

    Args:
        message: object representing the message sent by the user.
        state: An optional argument for the finite state machine context.
    """
    if state:
        await state.finish()
    await db.insert_update_user(message)
    await answer(message, 'choice', 'choice')


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text(message: types.Message) -> None:
    """Handler function for processing text messages.

    Args:
        message: object representing the received message.
    """
    match message.text:
        case 'Студент 🎓':
            # Importing a class here and not at the beginning,
            # for the correct order of handlers in the Dispatcher.
            from ..states.student import FSMStudent
            await FSMStudent.faculty.set()
            await answer(message, 'faculty', 'faculty')
