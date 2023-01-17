from os import getenv

import mariadb
from sqlalchemy import create_engine, inspect, MetaData, Table, Column
from sqlalchemy.dialects.mysql import BOOLEAN, BIGINT, VARCHAR, TIMESTAMP
from sqlalchemy.sql import func

engine = create_engine(
    'mariadb+mariadbconnector://{}:{}@db:3306/{}'.format(
        getenv('DB_USER', default=''),
        getenv('DB_PASS', default=''),
        getenv('DB_NAME', default='')
    )
)
inspector = inspect(engine)
meta = MetaData()

con = mariadb.connect(
    host='db',
    user=getenv('DB_USER', default=''),
    password=getenv('DB_PASS', default=''),
    database=getenv('DB_NAME', default=''),
)
cur = con.cursor()


async def db_init():
    if not inspector.has_table('users'):
        Table(
            'users', meta,
            Column('uid', BIGINT(unsigned=True), unique=True, primary_key=True,
                   comment='The Telegram user ID.'),
            Column('name', VARCHAR(255),
                   comment='The name of this user.'),
            Column('username', VARCHAR(255),
                   comment='The Telegram pseudonym of this user.'),
            Column('status', BOOLEAN, nullable=False, default=True,
                   comment='Whether the user is active or blocked.'),
            Column('login', TIMESTAMP, nullable=False, default=func.utcnow(),
                   comment='The time that the user last logged in.')
        )
    if not inspector.has_table('users_data'):
        await create_table_users_data()
    if not inspector.has_table('timetable'):
        await create_table_timetable()
    meta.create_all(engine)


async def db_close():
    cur.close()
    con.close()


async def create_table_users_data():
    try:
        cur.execute("""
        CREATE TABLE users_data (
            uid    serial comment 'The Telegram user ID.',
            d_id   integer  NOT NULL comment 'The Data ID.',
            d_type char(65) NOT NULL comment 'Type of user in the system.',
            d_name char(65) NOT NULL comment 'The name of the received data.',
            d_date date     NOT NULL comment 'The Last date of requested data.'
        );
    """)
        con.commit()
    except Exception as e:
        print(f'DB Error: {e}')


async def create_table_timetable():
    try:
        cur.execute("""
        create table timetable (
            id   smallint unsigned not null comment 'The timetable data ID.',
            mode varchar(255)         not null comment 'The data mode.'
        );
    """)
        con.commit()
    except Exception as e:
        print(f'DB Error: {e}')
