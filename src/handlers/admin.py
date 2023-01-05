import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from bot.config import bot, multy_replase
from bot.database import admin_data
from decouple import config
from bot.keyboard import inline


async def admin(message: types.Message):
    """Getting access to admin commands.

    Args:
        message (types.Message): This object represents a message.
    """
    await message.answer(
        "*Список команд адміна:*\n\n"
        + "/stats – Загальна статистика\n"
        + "/activity – Активність користувачів\n"
        + "/all\_users – Список всіх користувачів\n"
        + "/last\_users – UID останіх користувачів\n"
        + "/send\_msg – Надіслати повідомлення\n",
        parse_mode="MarkdownV2",
    )


async def stats(message: types.Message):
    """Getting statistics on users and schedules.

    Args:
        message (types.Message): This object represents a message.
    """
    res = await admin_data("stats")
    msg = (
            "👤 *Всього користувачів – {}*\n"
            + "✅ ` Активних      – {}`\n"
            + "🚫 ` Заблокованих  – {}`\n"
            + "🎓 ` Студентів     – {}`\n"
            + "💼 ` Викладачів    – {}`\n"
            + "⚠️ ` Невизначились – {}`\n\n"
            + "📚 *Всього розкладів у базі  – {}*\n"
            + "🎓 ` Для груп       – {}`\n"
            + "💼 ` Для викладачів – {}`\n"
    ).format(*res)
    await message.answer(msg, parse_mode="MarkdownV2")


async def activity(message: types.Message):
    """Sending bot usage statistics.

    Args:
        message (types.Message): This object represents a message.
    """
    res = await admin_data("activity")
    msg = (
            "👨‍💻 *Активність користувачів:*"
            + "\n  •  Сьогодні – {}"
            + "\n  •  Цього тижня – {}"
            + "\n  •  Цього місяця – {}"
            + "\n  •  Всього користувачів – {}"
    ).format(*res)
    await message.answer(msg, parse_mode="MarkdownV2")


async def last_users(message: types.Message):
    """Getting the last bot users.

    Args:
        message (types.Message): This object represents a message.
    """
    res = await admin_data("last-users")
    msg = (
            "*Останні 50 користувачів*\n\n`"
            + "   TIME  ┃        UID ┃ NAME\n"
            + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`\n"
    )
    for r in res:
        time = r[0].strftime("%H\:%M\:%S")
        empty = (10 - len(str(r[1]))) * " "
        name = await multy_replase(r[2], True)
        msg += "`{} ┃ {}{} ┃ `[{}](tg://user?id={})\n".format(
            time, empty, r[1], name, r[1]
        )
    await message.answer(msg, parse_mode="MarkdownV2")


async def all_users(message: types.Message):
    """Send a file with user data

    Args:
        message (types.Message): This object represents a message.
    """
    res = await admin_data("all-users")
    msg = (
            "DATE     ┃        UID ┃ STATUS ┃ DATA                      ┃ NAME\n"
            + "━" * 100
            + "\n"
    )
    users = open("all-users.txt", "w+")
    users.write(msg)
    for r in res:
        date = r[0].strftime("%m.%d.%y")
        e1 = (10 - len(str(r[1]))) * " "
        e2 = (25 - len(str(r[3]))) * " "
        msg = "{} ┃ {}{} ┃  {}  ┃ {}{} ┃ {}\n".format(
            date, e1, r[1], r[2], r[3], e2, r[4]
        )
        users.write(msg)
    users.close()
    await bot.send_document(config("ADMIN_ID"), open("all-users.txt", "r"))
    os.remove("all-users.txt")


# -----------------------------------------------------------
# Send users message
# -----------------------------------------------------------


async def send_msg(message: types.Message):
    info = (
            " Я можу надіслати наступне:\n"
            + "  • відео\n"
            + "  • стікер\n"
            + "  • голосове\n"
            + "  • зображення\n"
            + "  • аудіо (mp3)\n"
            + "  • відео (кружок)\n"
            + "  • анімацію (gif)\n\n"
            + "Для кого надсилати повідомлення❔"
    )
    await message.answer(info, reply_markup=await inline("who"))


async def callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == "all":
        msg = "Повідомлення буде надіслане всім користувачам\n\nОчікую повідомлення..."
        await call.message.edit_text(msg, reply_markup=await inline("back"))
        await FSMSendMsg.msg.set()
    elif call.data == "group":
        msg = "Повідомлення буде надіслане певній групі\n\nОчікую назву групи або її ID..."
        await call.message.edit_text(msg, reply_markup=await inline("back"))
    elif call.data == "user":
        msg = "Повідомлення буде надіслано лише 1 юзеру\n\nОчікую UID користувача..."
        await call.message.edit_text(msg, reply_markup=await inline("back"))

    elif call.data == "back":
        info = (
                " Я можу надіслати наступне:\n"
                + "  • відео\n"
                + "  • стікер\n"
                + "  • голосове\n"
                + "  • зображення\n"
                + "  • аудіо (mp3)\n"
                + "  • відео (кружок)\n"
                + "  • анімацію (gif)\n\n"
                + "Для кого надсилати повідомлення❔"
        )
        await state.finish()
        await call.message.edit_text(info, reply_markup=await inline("who"))

    elif call.data == "confirm":
        await send_all(None, state)
        await state.finish()
        await call.message.edit_text("Повідомлення надіслано ✅")
    elif call.data == "cancel":
        await call.message.edit_text("Скасовано ❕")
        await state.finish()

    await call.answer()


class FSMSendMsg(StatesGroup):
    uid = State()
    tid = State()
    msg = State()
    send = State()


# async def cancel_send(message: types.Message, state: FSMSendMsg):
#     await state.finish()
#     await message.answer("❕ Скасовано", parse_mode="MarkdownV2")


# async def get_uid(message: types.Message, state: FSMContext):
#     try:
#         uid = int(message.text)
#         res = 0
#         if uid < 9223372036854775807 and uid > -9223372036854775807:
#             res = await admin_data("user-uid", message.text)
#         mes = ""
#         if res:
#             name = await multy_replase(res[0])
#             mes = (
#                 "🗂 Знайшов у себе за UID – ["
#                 + name
#                 + "](tg://user?id="
#                 + message.text
#                 + ")\n\n"
#             )
#         else:
#             mes = (
#                 "⚠️ Можливо це правильний [UID](tg://user?id="
#                 + message.text
#                 + ") ⚠️\n\n"
#             )
#         mes += (
#             "Чекаю повідомлення для відправлення\.\.\.\n"
#             + " Я можу надіслати наступне:\n"
#             + "  • відео\n"
#             + "  • стікер\n"
#             + "  • голосове\n"
#             + "  • зображення\n"
#             + "  • аудіо \(mp3\)\n"
#             + "  • відео \(кружок\)\n"
#             + "  • анімацію \(gif\)\n"
#         )
#         await message.answer(mes, parse_mode="MarkdownV2")
#         await state.update_data(uid=message.text)
#         await FSMSendMsg.last()
#     except ValueError:
#         await message.answer("❌ Невірний UID")


# async def get_tid(message: types.Message, state: FSMContext):
#     pass


async def get_msg(message: types.ContentType.ANY, state: FSMContext):
    await state.update_data(msg=message)
    # fff = await messages.getMessages()
    await send_all(message, None)
    # await bot.delete_message(message.chat.id, message.message_id - 1)
    # await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(
        "Таке повідомлення отримає користувач", reply_markup=await inline("confirm")
    )


async def send_all(
        message: types.Message, state: FSMContext, data=[config("ADMIN_ID")], all=True
):
    chat = config("ADMIN_ID")
    if state:
        user_data = await state.get_data()
        message = user_data["msg"]
        message.message_id = message.message_id + 1
        chat = message.from_user.id
    if all:
        data = [config("ADMIN_ID")]
    for uid in data:
        try:
            try:
                text = message.html_text
            except:
                text = ""
            await bot.copy_message(
                uid, chat, message.media_group_id, text, parse_mode="HTML"
            )
        except exceptions.ChatNotFound:
            # await message.answer(
            #     "❗️ Повідомлення не надіслано\n" + "❌ Не знайдено чат для відправлення"
            # )
            pass
        except exceptions.BotBlocked:
            # await message.answer(
            #     "❗️ Повідомлення не надіслано\n" + "⛔️ Користувач заблокував бота"
            # )
            pass
        except Exception as e:
            pass
            # await message.answer(
            #     "❗️ Повідомлення не надіслано\n"
            #     + "❌ Сталася неочікувана помилка:\n\n"
            #     + str(e)
            # )

    # user_data = await state.get_data()
    # uid = user_data["uid"]


#     await state.finish()


# -----------------------------------------------------------
# Registration of all handlers
# -----------------------------------------------------------


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands="admin", user_id=config("ADMIN_ID"))
    dp.register_message_handler(stats, commands="stats", user_id=config("ADMIN_ID"))
    dp.register_message_handler(
        activity, commands="activity", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        all_users, commands="all_users", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        last_users, commands="last_users", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        send_msg, commands="send_msg", user_id=config("ADMIN_ID")
    )
    # dp.register_message_handler(
    #     cancel_send,
    #     commands="cancel",
    #     state=FSMSendMsg.all_states,
    #     chat_type=types.ChatType.PRIVATE,
    # )
    # dp.register_message_handler(
    #     get_uid, state=FSMSendMsg.uid, chat_type=types.ChatType.PRIVATE
    # )
    # dp.register_message_handler(
    #     get_tid, state=FSMSendMsg.tid, chat_type=types.ChatType.PRIVATE
    # )
    dp.register_message_handler(
        get_msg,
        state=FSMSendMsg.msg,
        chat_type=types.ChatType.PRIVATE,
        content_types=[
            "animation",
            "audio",
            "document",
            "photo",
            "text",
            "video",
            "video_note",
            "voice",
            "sticker",
        ],
    )
    dp.register_callback_query_handler(callback, state="*")
