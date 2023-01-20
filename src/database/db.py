from datetime import date

from aiogram import types
from services.storage import get_data_id_and_name
from sqlalchemy import text
from sqlalchemy.dialects.mysql import insert

from .db_init import con, cur, engine, meta


async def insert_update_user(message: types.Message):
    uid = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username
    conn = engine.connect()
    stmt = insert(meta.tables['users']).values(
        uid=uid,
        name=name,
        username=username,
    ).on_duplicate_key_update(
        name=name,
        username=username,
        status=True,
        login=text('default')
    )
    conn.execute(stmt)


async def save_user_data(message: types.Message, d_type: str,
                         d_date=date.today()):
    await insert_update_user(message)
    uid = message.from_user.id
    s_type = 'faculty' if d_type == 'group' else 'chair'
    res = await get_data_id_and_name(message.text, s_type)
    try:
        cur.execute(f"""
            INSERT INTO users_data VALUES ({uid}, {res.get('id')}, '{d_type}', '{res.get('name')}', '{d_date}')
                ON DUPLICATE KEY UPDATE
                    d_id = {res.get('id')},
                    d_type = '{d_type}',
                    d_name = '{res.get('name')}',
                    d_date = '{d_date}';
        """)
        con.commit()
    except Exception as e:
        print(f'DB Error: {e}')
