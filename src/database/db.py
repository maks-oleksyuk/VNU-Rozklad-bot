from aiogram import types

from .db_init import con, cur


async def insert_update_user(message: types.Message):
    uid = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username
    try:
        cur.execute(f"""
            INSERT INTO users VALUES ({uid}, '{name}', '@{username}', default, default)
                ON DUPLICATE KEY UPDATE name = '{name}', username = '@{username}', status = default, login = default;  
        """)
        con.commit()
    except Exception as e:
        print(f'DB Error: {e}')
