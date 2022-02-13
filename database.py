from config import base, cur
from aiogram import types

async def user_data(message: types.Message, option):
    match option:
        case "start":
            uid = message.from_user.id
            name = message.from_user.full_name
            cur.execute("SELECT uid FROM users WHERE uid = %s", [uid])
            res = cur.fetchone()
            if not res:
                cur.execute("INSERT INTO users (uid, name, status, state) VALUES (%s, %s, true, 'start')", [uid, name])
            else:
                cur.execute("UPDATE users SET name = %s, status = true, state = 'start' WHERE uid = %s", [name, uid])
    base.commit()