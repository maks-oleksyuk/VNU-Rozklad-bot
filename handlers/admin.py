from sre_constants import ANY
from aiogram import Dispatcher, types
import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import admin_data
from decouple import config
from message import answer
from timetable import multy_replase
from config import bot


async def admin(message: types.Message):
    await message.answer(
        "*Список команд адміна:*\n\n"
        + "/all\_stats – Загальна статистика\n"
        + "/last\_activity – Активність користувачів\n"
        + "/last\_users – UID останіх користувачів\n"
        + "/all\_active – Список всіх активних користувачів\n"
        + "/send\_msg\_user – Надіслати повідомлення за UID\n",
        parse_mode="MarkdownV2",
    )


async def all_stats(message: types.Message):
    res = await admin_data("all-stats")
    await message.answer(
        "👤 *Всього користувачів – *"
        + str(res[0])
        + "\n✅    Активних – "
        + str(res[1])
        + "\n⛔️    Заблокували бота – "
        + str(res[2])
        + "\n\n🎓 *Всього cтудентів – *"
        + str(res[3])
        + "\n✅    Активних – "
        + str(res[4])
        + "\n⛔️    Заблокували бота – "
        + str(res[5])
        + "\n\n💼 *Всього викладачів – *"
        + str(res[6])
        + "\n✅    Активних – "
        + str(res[7])
        + "\n⛔️    Заблокували бота – "
        + str(res[8])
        + "\n\n⚠️ *Невизначились – *"
        + str(res[9])
        + "\n\n📚 *Всього розкладів у базі – *"
        + str(res[10])
        + "\n🎓    Для груп – "
        + str(res[11])
        + "\n💼    Для викладачів – "
        + str(res[12]),
        parse_mode="MarkdownV2",
    )


async def last_activity(message: types.Message):
    res = await admin_data("last-activity")
    await message.answer(
        "👤 *Активність користувачів:*\n"
        + "\n  Сьогодні – "
        + str(res[0])
        + "\n  Цього тижня – "
        + str(res[1])
        + "\n  Цього місяця – "
        + str(res[2])
        + "\n  Всього користувачів – "
        + str(res[3]),
        parse_mode="MarkdownV2",
    )


async def last_users(message: types.Message):
    res = await admin_data("last-users")
    mes = (
        "*Користувалися ботом сьогодні – "
        + str(len(res))
        + "\n\nTIME   |  UID               |  NAME*\n"
        + "————————————————————————\n"
    )
    for r in res:
        mes += r[0].strftime("%H:%M") + "  |  " + str(r[1]) + "  |  " + r[2] + "\n"
    mes = await multy_replase(mes)
    await message.answer(mes, parse_mode="MarkdownV2")


async def all_active(message: types.Message):
    res = await admin_data("all-active")
    mes = (
        "*Активних користувачів – "
        + str(len(res))
        + "\n\nDATE       |  UID               |  NAME and DATA*\n"
        + "————————————————————————\n"
    )
    for r in res:
        date = r[0].strftime("%m.%d.%y")
        mes += date + "  |  " + str(r[1]) + "  |  " + r[2] + " – " + str(r[3]) + "\n"
    mes = await multy_replase(mes)
    await message.answer(mes, parse_mode="MarkdownV2")


# -----------------------------------------------------------
# Send users message
# -----------------------------------------------------------


class FSMSendMsg(StatesGroup):
    uid = State()
    tid = State()
    msg = State()


async def cancel_send(message: types.Message, state: FSMSendMsg):
    await state.finish()
    await message.answer("❕ Скасовано", parse_mode="MarkdownV2")


async def get_uid(message: types.Message, state: FSMContext):
    try:
        uid = int(message.text)
        res = 0
        if uid < 9223372036854775807 and uid > -9223372036854775807:
            res = await admin_data("user-uid", message.text)
        mes = ""
        if res:
            name = await multy_replase(res[0])
            mes = (
                "🗂 Знайшов у себе за UID – ["
                + name
                + "](tg://user?id="
                + message.text
                + ")\n\n"
            )
        else:
            mes = (
                "⚠️ Можливо це правильний [UID](tg://user?id="
                + message.text
                + ") ⚠️\n\n"
            )
        mes += (
            "Чекаю повідомлення для відправлення\.\.\.\n"
            + " Я можу надіслати наступне:\n"
            + "  • відео\n"
            + "  • стікер\n"
            + "  • голосове\n"
            + "  • зображення\n"
            + "  • аудіо \(mp3\)\n"
            + "  • відео \(кружок\)\n"
            + "  • анімацію \(gif\)\n"
        )
        await message.answer(mes, parse_mode="MarkdownV2")
        await state.update_data(uid=message.text)
        await FSMSendMsg.last()
    except ValueError:
        await message.answer("❌ Невірний UID")


async def get_tid(message: types.Message, state: FSMContext):
    pass


async def get_msg(message: types.ContentType.ANY, state: FSMContext):
    user_data = await state.get_data()
    uid = user_data["uid"]
    try:
        if message.animation:
            await bot.send_animation(
                uid,
                message.animation.file_id,
                caption=message.html_text,
                parse_mode="HTML",
            )
        if message.audio:
            await bot.send_audio(
                uid, message.audio.file_id, caption=message.html_text, parse_mode="HTML"
            )
        if message.document and not message.animation:
            await bot.send_document(
                uid,
                message.document.file_id,
                caption=message.html_text,
                parse_mode="HTML",
            )
        if message.photo:
            await bot.send_photo(
                uid,
                message.photo[0].file_id,
                caption=message.html_text,
                parse_mode="HTML",
            )
        if message.sticker:
            await bot.send_sticker(uid, message.sticker.file_id)
        if message.text:
            await bot.send_message(uid, message.html_text, parse_mode="HTML")
        if message.video:
            await bot.send_video(
                uid, message.video.file_id, caption=message.html_text, parse_mode="HTML"
            )
        if message.video_note:
            await bot.send_video_note(uid, message.video_note.file_id)
        if message.voice:
            await bot.send_voice(
                uid, message.voice.file_id, caption=message.html_text, parse_mode="HTML"
            )
        # TODO Доробити надсилання media_group
        # if message.media_group_id:
        #     await bot.send_media_group(uid, gr)
        await message.answer("✅ Повідомлення успішно надіслано")
    except aiogram.utils.exceptions.ChatNotFound:
        await message.answer(
            "❗️ Повідомлення не надіслано\n" + "❌ Не знайдено чат для відправлення"
        )
    except aiogram.utils.exceptions.BotBlocked:
        await message.answer(
            "❗️ Повідомлення не надіслано\n" + "⛔️ Користувач заблокував бота"
        )
    except Exception as e:
        await message.answer(
            "❗️ Повідомлення не надіслано\n"
            + "❌ Сталася неочікувана помилка:\n\n"
            + str(e)
        )
    await state.finish()


async def send_msg_user(message: types.Message):
    await message.answer("🆔 Введіть UID користувача Telegram")
    await FSMSendMsg.uid.set()


# -----------------------------------------------------------
# Registration of all handlers
# -----------------------------------------------------------


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands="admin", user_id=config("ADMIN_ID"))
    dp.register_message_handler(
        all_stats, commands="all_stats", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        last_activity, commands="last_activity", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        last_users, commands="last_users", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        all_active, commands="all_active", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        send_msg_user, commands="send_msg_user", user_id=config("ADMIN_ID")
    )
    dp.register_message_handler(
        cancel_send,
        commands="cancel",
        state=FSMSendMsg.all_states,
        chat_type=types.ChatType.PRIVATE,
    )
    dp.register_message_handler(
        get_uid, state=FSMSendMsg.uid, chat_type=types.ChatType.PRIVATE
    )
    dp.register_message_handler(
        get_tid, state=FSMSendMsg.tid, chat_type=types.ChatType.PRIVATE
    )
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
