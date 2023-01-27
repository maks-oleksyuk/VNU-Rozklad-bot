from datetime import date

from aiogram import types
from services.storage import get_data_id_and_name
from sqlalchemy import text, delete
from sqlalchemy.dialects.mysql import insert

from .db_init import conn, meta


async def insert_update_user(message: types.Message):
    uid = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username
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


async def save_user_data(message: types.Message,
                         d_mode: str, d_date=date.today()):
    await insert_update_user(message)
    uid = message.from_user.id
    s_type = 'faculty' if d_mode == 'group' else 'chair'
    res = await get_data_id_and_name(message.text, s_type)
    stmt = insert(meta.tables['users_data']).values(
        uid=uid,
        d_id=res.get('id'),
        d_mode=d_mode,
        d_name=res.get('name'),
        d_date=d_date
    ).on_duplicate_key_update(
        d_id=res.get('id'),
        d_mode=d_mode,
        d_name=res.get('name'),
        d_date=d_date
    )
    conn.execute(stmt)


async def save_groups(data: dict):
    conn.execute(meta.tables['groups'].delete())
    for d in data:
        for i in d['objects']:
            stmt = insert(meta.tables['groups']).values(
                id=i['ID'],
                department=d['name'],
                name=i['name'],
            )
            conn.execute(stmt)
