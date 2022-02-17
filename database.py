from config import base, cur
from aiogram import types

async def user_data(message: types.Message, option):
    uid = message.from_user.id
    name = message.from_user.full_name
    match option:
        case "choice":
            cur.execute("SELECT uid FROM users WHERE uid = %s", [uid])
            res = cur.fetchone()
            if not res:
                cur.execute("INSERT INTO users (uid, name, status, state) VALUES (%s, %s, true, 'choice')", [uid, name])
            else:
                cur.execute("UPDATE users SET name = %s, status = true, state = 'choice' WHERE uid = %s", [name, uid])
        case "faculty":
            cur.execute("UPDATE users SET name = %s, status = true, state = 'faculty' WHERE uid = %s", [name, uid])
        case "chair":
            cur.execute("UPDATE users SET name = %s, status = true, state = 'chair' WHERE uid = %s", [name, uid])
        case "group":
            cur.execute("UPDATE users SET name = %s, status = true, state = 'group' WHERE uid = %s", [name, uid])
        case "surname":
            cur.execute("UPDATE users SET name = %s, status = true, state = 'surname' WHERE uid = %s", [name, uid])
        case "data":
            data = message.text
            cur.execute("UPDATE users SET name = %s, status = true, state = 'timetable', data = %s WHERE uid = %s", [name, data, uid])

    base.commit()


async def schedule_data(message: types.Message, option, data):
    name = message.text
    match option:
        case "have_timetable":
            cur.execute("SELECT mon, tue, wed, thu, fri, sat, sun  FROM timetable WHERE name = %s", [name])
            res = cur.fetchone()
            return res
            # if res: return True
            # else: return