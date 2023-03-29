from aiogram import types
from aiogram.types import KeyboardButton as Kb
from aiogram.types import ReplyKeyboardMarkup

from loader import db
from data.storage import room_types


async def get_reply_keyboard_by_key(message: types.Message, key) -> ReplyKeyboardMarkup:
    """Return the keyboard for the required variant.

    Args:
        message: The message sent by the user.
        key: Keyboard identifier to build.

    Returns:
        ReplyKeyboardMarkup: Keyboard of the right option.
    """
    markup = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)
    match key:
        case 'choice':
            markup.input_field_placeholder = 'Оберіть варіант з меню'
            markup.row(Kb(text='Викладач 💼'), Kb(text='Студент 🎓'))
        case 'faculty':
            faculty = await db.get_departments_by_mode('groups')
            markup.input_field_placeholder = 'Пошук (наприклад `КНІТ-43`)'
            markup = await one_column_reply_keyboard(markup, faculty, True)
        case 'group':
            data = await db.get_objects_by_department('groups', message.text)
            markup.input_field_placeholder = 'Пошук'
            markup = await two_column_reply_keyboard(markup, data, True)
        case 'search-group':
            data = await db.search('groups', message.text)
            markup.input_field_placeholder = 'Пошук'
            markup = await two_column_reply_keyboard(markup, data[:99], True)
        case 'chair':
            chair = await db.get_departments_by_mode('teachers')
            markup.input_field_placeholder = 'Пошук (наприклад `Катерина`)'
            markup = await one_column_reply_keyboard(markup, chair, True)
        case 'surname':
            data = await db.get_objects_by_department('teachers', message.text)
            markup.input_field_placeholder = 'Пошук'
            markup = await one_column_reply_keyboard(markup, data, True)
        case 'search-teacher':
            data = await db.search('teachers', message.text)
            markup.input_field_placeholder = 'Пошук'
            markup = await one_column_reply_keyboard(markup, data[:99], True)
        case 'timetable':
            days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд']
            res = await db.get_users_data_by_id(message.from_user.id)
            days[res['d_date'].weekday()] = '🟢'
            markup.row(*days)
            markup.row('⬅️ тиждень', 'сьогодні', 'тиждень ➡️')
            markup.row('Змінити запит', 'на тиждень', 'Ввести дату')
        case 'rooms-date':
            data = ['сьогодні', 'завтра']
            markup = await two_column_reply_keyboard(markup, data, True)
        case 'lessons':
            data = ['1', '2', '3', '4', '5', '6', '7', '8']
            markup.add(Kb(text='⬅️ Назад'))
            markup.row(*data)
        case 'blocks':
            data = await db.get_audience_blocks()
            markup = await one_column_reply_keyboard(markup, data, True)
        case 'over':
            data = await db.get_block_floors(message.text)
            markup.add(Kb(text='⬅️ Назад'))
            markup.row(*list(map(str, data)))
        case 'room-type':
            markup = await two_column_reply_keyboard(markup, list(room_types.values()), True)
    return markup


async def one_column_reply_keyboard(markup: ReplyKeyboardMarkup, data: list,
                                    use_back: bool = False) -> ReplyKeyboardMarkup:
    """Adds a one-column keyboard layout to the given ReplyKeyboardMarkup object.

    Args:
        markup: The markup to which the buttons will be added.
        data: The list of strings to be displayed as buttons.
        use_back: Whether to add a 'back' button. Defaults to False.

    Returns:
        ReplyKeyboardMarkup: The markup object with the buttons added.
    """
    if use_back:
        markup.add(Kb(text='⬅️ Назад'))
    [markup.add(Kb(text=i)) for i in data]
    return markup


async def two_column_reply_keyboard(markup: ReplyKeyboardMarkup, data: list,
                                    use_back: bool = False) -> ReplyKeyboardMarkup:
    """Creates a reply keyboard markup with two columns.

    Args:
        markup: The markup to which the buttons will be added.
        data: The list of strings to be displayed as buttons.
        use_back: Whether to add a 'back' button. Defaults to False.

    Returns:
        ReplyKeyboardMarkup: The markup object with the buttons added.
    """
    if use_back:
        markup.add(Kb(text='⬅️ Назад'))
    [markup.add(Kb(text=data[i])) if i == len(data) - 1
     else markup.row(Kb(text=data[i]), Kb(text=data[i + 1]))
     for i in range(0, len(data), 2)]
    return markup
