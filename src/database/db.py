from datetime import date, datetime

import api.timetable_api as api
from aiogram import types
from sqlalchemy import text, select, update, delete
from sqlalchemy.dialects.mysql import insert

from .db_init import conn, meta


# TODO: Create admin stats function
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


async def update_user_data_date(id: int, date: date):
    table = meta.tables['users_data']
    conn.execute(update(table).values(d_date=date).where(table.c.uid == id))
    conn.commit()


async def check_user_data_exist(message: types.Message):
    table = meta.tables['users_data']
    pass


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
    })) for d in data for i in d['objects'] if
        i['ID'] != ''
        and i['name'].find('Вакансія') == -1
        and i['name'].find('0,75') == -1]
    stmt = insert(meta.tables['teachers']).values(query_data)
    conn.execute(stmt)
    conn.commit()


async def save_timetable(id: str, mode: str, data: dict,
                         s_date: date, e_date: date):
    table = meta.tables['timetable']
    # Currently, there is no functionality to track deleted rows
    # from the API query result, so all are overwritten.
    conn.execute(delete(table)
                 .where(table.c.id == id)
                 .where(table.c.mode == mode)
                 .where(table.c.date >= s_date)
                 .where(table.c.date <= e_date))
    for i in data:
        # We look for matches in groups so as not to store unnecessary data.
        # For example: general (Group, name, ...) to general.
        g = i['group'].find('І (')
        stmt = insert(table).values(
            id=id,
            mode=mode,
            name=i['object'],
            date=datetime.strptime(i['date'], '%d.%m.%Y').date(),
            lesson_number=i['lesson_number'],
            lesson_time=i['lesson_time'],
            room=i['room'],
            type=i['type'],
            title=i['title'].replace(' (за професійним спрямуванням)', ''),
            teacher=i['teacher'],
            group=i['group'] if g == -1 else i['group'][:g + 1],
            replacement=i['replacement'],
            reservation=i['reservation'],
        )
        conn.execute(stmt)
    conn.commit()


async def get_timetable(id: str, mode: str,
                        s_date: date = date.today(),
                        e_date: date = date.today()):
    await api.get_timetable(id, mode, s_date)
    table = meta.tables['timetable']
    stmt = (select(table.c)
            .where(table.c.id == id)
            .where(table.c.mode == mode)
            .where(table.c.date >= s_date)
            .where(table.c.date <= e_date))
    res = conn.execute(stmt).all()
    return [r._asdict() for r in res]


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
    stmt = select(name).filter(name.like(f'%{query}%'))
    try:
        if conn.execute(stmt).first()[0] == query:
            return [conn.execute(stmt).first()[0]]
        else:
            res = conn.execute(stmt).all()
            return [r for r, in res]
    except TypeError:
        return []


async def get_data_id_and_name(mode: str, query: str):
    table = meta.tables[mode]
    name = table.c.name if mode == 'groups' else table.c.fullname
    stmt = select(table.c.id, table.c.name).where(name == query)
    res = conn.execute(stmt).first()
    return {'id': int(res[0]), 'name': res[1]}


async def get_users_data_by_id(uid: int):
    table = meta.tables['users_data']
    stmt = (select(table.c.d_id, table.c.d_mode,
                   table.c.d_name, table.c.d_date)
            .where(table.c.uid == uid))
    res = conn.execute(stmt).first()
    return res._asdict()
