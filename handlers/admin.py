from aiogram import Dispatcher, types
from database import admin_data
from decouple import config
from message import answer


async def admin(message: types.Message):
    await answer(message, "admin")


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


# -----------------------------------------------------------
# Registration of all handlers
# -----------------------------------------------------------


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands="admin", user_id=config("ADMIN_ID"))
    dp.register_message_handler(
        all_stats, commands="all_stats", user_id=config("ADMIN_ID")
    )
