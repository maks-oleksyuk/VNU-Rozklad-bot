from aiogram import types

from config import base, cur


async def user_data(message: types.Message, option, data):
    uid = message.from_user.id
    name = message.from_user.full_name
    match option:
        case "save":
            cur.execute("SELECT * FROM users WHERE uid = %s", [uid])
            res = cur.fetchone()
            if not res:
                cur.execute("INSERT INTO users (uid, name, status) VALUES (%s, %s, true)", [uid, name])
            else:
                cur.execute("UPDATE users SET name = %s, status = true WHERE uid = %s", [name, uid])
        case "data":
            data = [name] + data + [uid]
            cur.execute("""UPDATE users SET
                            name = %s,
                            status = true,
                            data_id = %s,
                            data_name = %s,
                            data_type  = %s,
                            data_date = %s
                            WHERE uid = %s""", data)
        case "get_data_id":
            cur.execute("SELECT data_id, data_name, data_type, data_date FROM users WHERE uid = %s", [uid])
            res = cur.fetchone()
            return res

    base.commit()


async def schedule_data(message: types.Message, option, data):
    match option:
        case "check":
            cur.execute("SELECT * FROM timetable WHERE tid = %s", [data[0]])
            res = cur.fetchone()
            return res
        case "save":
            if data[5]:
                cur.execute("""INSERT INTO timetable
                VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data)
            else:
                cur.execute("INSERT INTO timetable VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)", data)    
        case "update":
            data += [data.pop(0)]
            cur.execute("""UPDATE timetable SET
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
        case "week_update":
            cur.execute("""UPDATE timetable SET
            s_date = %s,
            e_date = %s,
            mon = n_mon,
            tue = n_tue,
            wed = n_wed,
            thu = n_thu,
            fri = n_fri,
            sat = n_sat,
            sun = n_sun,
            week = n_week,
            n_mon = default,
            n_tue = default,
            n_wed = default,
            n_thu = default,
            n_fri = default,
            n_sat = default,
            n_sun = default,
            n_week = default
            WHERE tid = %s
            """, [data[3], data[4], data[0]])
        case "get_col":
            cur.execute("SELECT " + data[0] + " FROM timetable WHERE tid = %s", [data[1]])
            res = cur.fetchone()
            return res
        case "get_date":
            cur.execute("SELECT S_date, e_date FROM timetable WHERE tid = %s", [data])
            res = cur.fetchone()
            return res
    base.commit()
