from base64 import encode
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
            cur.execute("UPDATE users SET name = %s, status = true, state = 'group', data_type= 'group' WHERE uid = %s", [name, uid])
        case "surname":
            cur.execute("UPDATE users SET name = %s, status = true, state = 'surname' data_type= 'teacher' WHERE uid = %s", [name, uid])
        case "data":
            data = message.text
            cur.execute("UPDATE users SET name = %s, status = true, state = 'timetable', data = %s WHERE uid = %s", [name, data, uid])

    base.commit()


async def schedule_data(message: types.Message, option, data):
    match option:
        case "save":
            cur.execute("SELECT * FROM timetable WHERE tid = %s", [data[0]])
            res = cur.fetchone()
            if res:
                data.append(data[0])
                cur.execute("""UPDATE timetable SET
                tid = %s,
                name = %s,
                type = %s,
                s_date = %s,
                e_date = %s,
                exist = %s,
                mon = %s,
                tue = %s,
                wed = %s,
                thu = %s,
                fri = %s,
                sat = %s,
                sun = %s,
                week = %s,
                n_mon = %s,
                n_tue = %s,
                n_wed = %s,
                n_thu = %s,
                n_fri = %s,
                n_sat = %s,
                n_sun = %s,
                n_week = %s
                WHERE tid = %s
                """, data)
            else:
                if data[5]:
                    cur.execute("""INSERT INTO timetable
                    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data)
                else:
                    cur.execute("INSERT INTO timetable VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)", data)    
    base.commit()
