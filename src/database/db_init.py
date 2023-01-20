from os import getenv

import mariadb
from sqlalchemy import create_engine, inspect, MetaData, Table, Column
from sqlalchemy.dialects.mysql import BOOLEAN, SMALLINT, INTEGER, BIGINT, \
    VARCHAR, DATE, TIMESTAMP
from sqlalchemy.sql import func

engine = create_engine(
    'mariadb+mariadbconnector://{}:{}@db:3306/{}'.format(
        getenv('DB_USER', default=''),
        getenv('DB_PASS', default=''),
        getenv('DB_NAME', default='')
    )
)
meta = MetaData()
meta.reflect(bind=engine)
inspector = inspect(engine)

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
            Column('status', BOOLEAN, nullable=False, server_default='1',
                   comment='Whether the user is active or blocked.'),
            Column('login', TIMESTAMP, nullable=False, default=func.utcnow(),
                   comment='The time that the user last logged in.')
        )
    if not inspector.has_table('users_data'):
        Table(
            'users_data', meta,
            Column('uid', BIGINT(unsigned=True), unique=True, primary_key=True,
                   comment='The Telegram user ID.'),
            Column('d_id', INTEGER, nullable=False, comment='The Data ID.'),
            Column('d_type', VARCHAR(65), nullable=False,
                   comment='Type of user in the system.'),
            Column('d_name', VARCHAR(65), nullable=False,
                   comment='The name of the received data.'),
            Column('d_date', DATE, nullable=False,
                   comment='The Last date of requested data.')
        )
    if not inspector.has_table('timetable'):
        Table(
            'timetable', meta,
            Column('id', SMALLINT(unsigned=True), nullable=False,
                   comment='The timetable data ID.'),
            Column('mode', VARCHAR(255), nullable=False,
                   comment='The data mode.'),
        )
    meta.create_all(engine)


async def db_close():
    engine.dispose()
    # @todo Remove close mariadb connect when finish refactor code to orm
    cur.close()
    con.close()
