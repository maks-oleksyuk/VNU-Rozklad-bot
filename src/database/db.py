from datetime import date

from aiogram import types
from sqlalchemy import text, select
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
    conn.commit()


async def save_user_data(message: types.Message,
                         d_mode: str, d_date=date.today()):
    await insert_update_user(message)
    uid = message.from_user.id
    res = await get_data_id_and_name(f'{d_mode}s', message.text)
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
    conn.commit()


async def save_groups(data: dict):
    conn.execute(meta.tables['groups'].delete())
    query_data = []
    [(query_data.append({
        'id': i['ID'],
        'department': d['name'],
        'name': i['name'],
    })) for d in data for i in d['objects'] if i['ID'] != '']
    stmt = insert(meta.tables['groups']).values(query_data)
    conn.execute(stmt)
    conn.commit()


async def save_teachers(data: dict):
    conn.execute(meta.tables['teachers'].delete())
    query_data = []
    [(query_data.append({
        'id': i['ID'],
        'department': d['name'],
        'name': i['name'],
        'fullname': '{} {} {}'.format(i['P'], i['I'], i['B']),
        'P': i['P'],
        'I': i['I'],
        'B': i['B'],
    })) for d in data for i in d['objects'] if i['ID'] != '']
    stmt = insert(meta.tables['teachers']).values(query_data)
    conn.execute(stmt)
    conn.commit()


async def get_departments_by_mode(mode: str):
    table = meta.tables[mode]
    stmt = select(table.c.department).distinct()
    res = conn.execute(stmt).all()
    return [r for r, in res]


async def get_objects_by_department(mode: str, department: str):
    table = meta.tables[mode]
    name = table.c.name if mode == 'groups' else table.c.fullname
    stmt = select(name).where(table.c.department == department)
    res = conn.execute(stmt).all()
    return [r for r, in res]


async def search(mode: str, query: str):
    """ Search for matches in the database

    Args:
        mode (str): Search results of a specific type (groups or teacher)
        query (str): Text to search

    Returns:
        Array with search results
    """
    table = meta.tables[mode]
    name = table.c.name if mode == 'groups' else table.c.fullname
    # TODO: Fix search it next variants (Біо-11 - Біо-11з)
    stmt = select(name).filter(name.like(f'%{query}%'))
    res = conn.execute(stmt).all()
    return [r for r, in res]


async def get_data_id_and_name(mode: str, query: str):
    table = meta.tables[mode]
    name = table.c.name if mode == 'groups' else table.c.fullname
    stmt = select(table.c.id, table.c.name).where(name == query)
    res = conn.execute(stmt).first()
    return {'id': int(res[0]), 'name': res[1]}
