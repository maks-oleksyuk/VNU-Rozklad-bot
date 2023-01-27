from os import getenv

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
conn = engine.connect()


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
            Column('d_mode', VARCHAR(65), nullable=False,
                   comment='Type of user in the system.'),
            Column('d_name', VARCHAR(65), nullable=False,
                   comment='The name of the received data.'),
            Column('d_date', DATE, nullable=False,
                   comment='The Last date of requested data.')
        )
    if not inspector.has_table('groups'):
        Table(
            'groups', meta,
            Column('id', SMALLINT(unsigned=True), nullable=False,
                   comment='The group ID.'),
            Column('department', VARCHAR(128), nullable=False,
                   comment='The group department.'),
            Column('name', VARCHAR(32), nullable=False,
                   comment='The group name.'),
        )
    if not inspector.has_table('teachers'):
        Table(
            'teachers', meta,
            Column('id', SMALLINT(unsigned=True), nullable=False,
                   comment='The teacher ID.'),
            Column('department', VARCHAR(128), nullable=False,
                   comment='The teacher department.'),
            Column('name', VARCHAR(32), nullable=False,
                   comment='The teacher shortname form .'),
            Column('fullname', VARCHAR(255), nullable=False,
                   comment='The teacher fullname form.'),
            Column('P', VARCHAR(32), nullable=False,
                   comment='The teacher surname.'),
            Column('I', VARCHAR(32), nullable=False,
                   comment='The teacher name.'),
            Column('P', VARCHAR(32), nullable=False,
                   comment='The teacher middle name.'),
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
    conn.close()
    engine.dispose()
