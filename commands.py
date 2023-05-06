from variables import bot
from keyboard import set_markup


def start(message):
    bot.send_message(
        message.chat.id,
        "👋 *Привіт!*\n\n"
        + "Я — твій корисний помічник під час навчального року,\n"
        + "адже в мене ти завжди можеш дізнатись, які в тебе пари протягом тижня.\n\n"
        + "Потрібна допомога з командами?\n"
        + "Просто відправ мені /help\n\n"
        + "Хочеш більше дізнатися про бота?\n"
        + "Знаєш як його покращити?\n"
        + "Щось пішло не так?\n"
        + "Всю потрібну інформацію ти знайдеш натиснувши /about\n\n"
        + "Для початку, скажи мені\nдля кого будемо формувати розклад🤓:\n\n"
        + "❕ Якщо немає квавіш натисти на квадратик справа ↘️",
        parse_mode="Markdown",
        reply_markup=set_markup(message.from_user.id, 1),
    )


def change(message):
    bot.send_message(
        message.chat.id,
        "Вибери для кого шукати розклад цього разу:",
        reply_markup=set_markup(message.from_user.id, 1),
    )


def about(message):
    bot.send_message(
        message.chat.id,
        "Бот, який створений, щоб спростити життя студентам і не тільки 😉\n\n"
        + "⛔️Щось не працює?\n"
        + "😎Знаєш як покращити мене?\n"
        + "Не соромся, пиши йому - [admin](https://t.me/maks_oleksyuk)\n"
        + "Він точно знає що з цим робити👾\n\n"
        + "[💸 шекель](https://send.monobank.ua/8mZyo57Cpu) для трудяги",
        disable_web_page_preview=True,
        parse_mode="Markdown",
    )


def help(message):
    bot.send_message(
        message.chat.id,
        "✳️ <b><u>Для отримання розкладу потрібно:</u></b>\n\n"
        + "<b>1.</b> Обрати категорію для кого формувати розклад\n\n"
        + "<b>2.</b> Ввести дані для пошуку:\n"
        + "  <b>2.1</b> Для викладача достатньо ввести прізвище\n"
        + "  <b>2.2</b> Для групи ввести її код у форматі <code>[Назва-##]</code>\n\n"
        + "⚠️ Якщо помилився або передумав, існує команда /cancel\n\n"
        + "❕Для того щоб з'явилась квавіатура взамодії\n"
        + "❕клацай на квадратик знизу справа ↘️",
        reply_markup=set_markup(message.from_user.id, 1),
        parse_mode="html",
    )


def cancel(message):
    bot.send_message(
        message.chat.id,
        "❕ Скасовано",
        reply_markup=set_markup(message.from_user.id, 1),
    )
