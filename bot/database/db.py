import logging
from datetime import date

from aiogram import types
from sqlalchemy import create_engine, inspect, MetaData, text, \
    Table, Column, UniqueConstraint
from sqlalchemy import select, func
from sqlalchemy.dialects.mysql import BOOLEAN, SMALLINT, INTEGER, BIGINT, \
    VARCHAR, TEXT, DATE, TIMESTAMP, insert

# Define global variables.
DB_PORT = 3306
DB_HOST = 'localhost'


class Database:
    """
    A class for managing a database.

    # TODO Update docblock when finish bot.v3
    Attributes:
        __engine: a SQLAlchemy engine object for connecting to a database.
        __meta: a SQLAlchemy metaData object for reflecting on database metadata.
        __inspector: a SQLAlchemy Inspector object for inspecting database objects.
        _conn: a database connection object.

    Methods:
        __init__: a constructor method that initializes the database connection
                  and reflects on database metadata.
        _create_tables: a method that creates tables if they do not exist.
        insert_update_user: inserts or updates a user record in the database.
    """

    def __init__(self, db_name: str, db_user: str, db_pass: str):
        """
        Initializes a Database object.

        Args:
            db_name (str): name of the database.
            db_user (str): username for accessing the database.
            db_pass (str): password for accessing the database.
        """
        self.log = logging.getLogger('bot')

        # Create database __engine with provided parameters.
        self.__engine = create_engine(
            f'mariadb+mariadbconnector://{db_user}:{db_pass}@{DB_HOST}:{DB_PORT}/{db_name}'
        )

        # Initialize metadata and inspector objects.
        self.__meta = MetaData()
        self.__meta.reflect(bind=self.__engine)
        self.__inspector = inspect(self.__engine)
        self._conn = self.__engine.connect()

        # Create database tables if they do not exist.
        self._create_tables()

        # Get table objects.
        self._users = self.__meta.tables['users']
        self._users_data = self.__meta.tables['users_data']
        self._groups = self.__meta.tables['groups']
        self._teachers = self.__meta.tables['teachers']
        self._timetable = self.__meta.tables['timetable']

    def _create_tables(self) -> None:
        """Creates tables in a database if they do not already exist."""
        if not self.__inspector.has_table('users'):
            Table(
                'users', self.__meta,
                Column('uid', BIGINT(unsigned=True), unique=True, primary_key=True,
                       comment='The Telegram user ID.'),
                Column('fullname', VARCHAR(255),
                       comment='The name of this user.'),
                Column('username', VARCHAR(255),
                       comment='The Telegram pseudonym of this user.'),
                Column('status', BOOLEAN, nullable=False, server_default='1',
                       comment='Whether the user is active or blocked.'),
                Column('login', TIMESTAMP, nullable=False, server_default=text(
                    'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                       comment='The time that the user last logged in.')
            )
            self.log.info('The `users` table was not found, it has been created')
        if not self.__inspector.has_table('users_data'):
            Table(
                'users_data', self.__meta,
                Column('uid', BIGINT(unsigned=True), unique=True, primary_key=True,
                       comment='The Telegram user ID.'),
                Column('d_id', INTEGER, nullable=False,
                       comment='The Data ID.'),
                Column('d_mode', VARCHAR(65), nullable=False,
                       comment='Type of user in the system.'),
                Column('d_name', VARCHAR(65), nullable=False,
                       comment='The name of the received data.'),
                Column('d_date', DATE, nullable=False,
                       comment='The Last date of requested data.')
            )
            self.log.info('The `users_data` table was not found, it has been created')
        if not self.__inspector.has_table('groups'):
            Table(
                'groups', self.__meta,
                Column('id', SMALLINT(unsigned=True), unique=True, nullable=False,
                       comment='The group ID.'),
                Column('department', VARCHAR(128), nullable=False,
                       comment='The group department.'),
                Column('name', VARCHAR(32), nullable=False,
                       comment='The group name.'),
            )
            self.log.info('The `groups` table was not found, it has been created')
        if not self.__inspector.has_table('teachers'):
            Table(
                'teachers', self.__meta,
                Column('id', SMALLINT(unsigned=True), unique=True, nullable=False,
                       comment='The teacher ID.'),
                Column('department', VARCHAR(128), nullable=False,
                       comment='The teacher department.'),
                Column('name', VARCHAR(32), nullable=False,
                       comment='The teacher shortname form .'),
                Column('fullname', VARCHAR(128), nullable=False,
                       comment='The teacher fullname form.'),
                Column('P', VARCHAR(32), nullable=False,
                       comment='The teacher surname.'),
                Column('I', VARCHAR(32), nullable=False,
                       comment='The teacher name.'),
                Column('B', VARCHAR(32), nullable=False,
                       comment='The teacher middle name.'),
            )
            self.log.info('The `teachers` table was not found, it has been created')
        if not self.__inspector.has_table('timetable'):
            Table(
                'timetable', self.__meta,
                Column('id', SMALLINT(unsigned=True), nullable=False,
                       comment='The timetable data ID.'),
                Column('mode', VARCHAR(32), nullable=False,
                       comment='The data mode.'),
                Column('name', VARCHAR(128), nullable=False,
                       comment='The data name.'),
                Column('date', DATE, nullable=False,
                       comment='The timetable date.'),
                Column('lesson_number', SMALLINT(unsigned=True), nullable=False,
                       comment='The lesson number.'),
                Column('lesson_time', VARCHAR(16), nullable=False,
                       comment='The lesson time.'),
                Column('room', VARCHAR(16),
                       comment='The lesson room.'),
                Column('type', VARCHAR(8), nullable=False,
                       comment='The lesson type.'),
                Column('title', TEXT, nullable=False,
                       comment='The lesson title.'),
                Column('teacher', VARCHAR(64),
                       comment='The lesson teacher.'),
                Column('group', VARCHAR(128),
                       comment='The lesson group(s).'),
                Column('replacement', VARCHAR(255)),
                Column('reservation', VARCHAR(255)),
                UniqueConstraint('id', 'mode', 'date', 'lesson_number', 'teacher', 'group')
            )
            self.log.info('The `timetable` table was not found, it has been created')
        self.__meta.create_all(self.__engine)

    async def _table_is_empty(self, name: str) -> bool:
        """Check if a table is empty.

        Args:
            name: The name of the table to check.

        Returns:
            bool: True if the table is empty, False otherwise.
        """
        table = self.__meta.tables[name]
        stmt = select(func.count(table.c.id)).group_by(table.c.id)
        return not self._conn.execute(stmt).scalar()

    async def insert_update_user(self, message: types.Message) -> None:
        """
        Inserts or updates a user record in the database.

        Args:
            message (types.Message): A message object from the Telegram API
                                    containing user information.
        """
        self._conn.execute(insert(self._users).values(
            uid=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
        ).on_duplicate_key_update(
            fullname=message.from_user.full_name,
            username=message.from_user.username,
            status=True,
            login=text('default')
        ))
        self._conn.commit()
        self.log.debug(f'User {message.from_user.full_name} - created/updated')

    async def save_user_data(self, message: types.Message,
                             d_mode: str, d_date: date = date.today()) -> None:
        """Saves user data to the database.

        Args:
            message: Telegram Message object.
            d_mode: string indicating the data mode (group or teacher).
            d_date: optional date object representing the date of the data (default is today).
        """
        await self.insert_update_user(message)
        res = await self.get_data_id_and_name(f'{d_mode}s', message.text)
        stmt = insert(self._users_data).values(
            uid=message.from_user.id,
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
        self._conn.execute(stmt)
        self._conn.commit()

    async def save_groups(self, data: dict) -> None:
        """Saves groups data to the database.

        Args:
            data: a dictionary containing groups data.
        """

        # Delete existing data in the `groups` table.
        self._conn.execute(self._groups.delete())

        query_data = []
        # Iterate through the data and add each group to the query data list.
        [(query_data.append({
            'id': i['ID'],
            'department': d['name'],
            'name': i['name'],
        })) for d in data for i in d['objects'] if i['ID'] != '']

        # Insert the query data into the `groups` table and commit it.
        self._conn.execute(insert(self._groups).values(query_data))
        self._conn.commit()

        # Log a message indicating the `groups` table was successfully updated.
        self.log.info('Table `groups` updated successfully')

    async def save_teachers(self, data: dict) -> None:
        """Saves teachers data to the database.

        Args:
            data: a dictionary containing teachers data.
        """

        # Delete existing data in the `teachers` table.
        self._conn.execute(self._teachers.delete())

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

        # Insert the query data into the `teachers` table and commit it.
        self._conn.execute(insert(self._teachers).values(query_data))
        self._conn.commit()

        # Log a message indicating the `teachers` table was successfully updated.
        self.log.info('Table `teachers` updated successfully')

    async def get_departments_by_mode(self, mode: str) -> list:
        """Gets a list of departments for a specific type ('groups' or 'teacher').

        Args:
            mode: The table name to retrieve objects in departments.

        Returns:
            A list of departments in the specified table.
        """
        table = self.__meta.tables[mode]
        stmt = select(table.c.department).distinct()
        res = self._conn.execute(stmt).all()
        return [r for r, in res]

    async def get_objects_by_department(self, mode: str, department: str) -> list:
        """Retrieves all objects belong to a certain department from the database.

        Args:
            mode: The mode of the objects to retrieve.
            department: The department to filter the objects by.

        Returns:
            A list of objects that belong to the specified department.
        """
        table = self.__meta.tables[mode]
        name = table.c.name if mode == 'groups' else table.c.fullname
        stmt = select(name).where(table.c.department == department).order_by(name)
        res = self._conn.execute(stmt).all()
        return [r for r, in res]

    async def get_data_id_and_name(self, mode: str, query: str) -> dict:
        """Retrieves data id and name based on the given query string.

        Args:
            mode: A string representing the table name.
            query: A string representing the query.

        Returns:
            dict: A dictionary containing the id and name of the data.
        """
        table = self.__meta.tables[mode]
        name = table.c.name if mode == 'groups' else table.c.fullname
        stmt = select(table.c.id, table.c.name).where(name == query)
        res = self._conn.execute(stmt).first()
        return {'id': int(res[0]), 'name': res[1]}

    async def search(self, mode: str, query: str) -> list:
        """Searches for matches in the specified table of the database.

        Args:
            mode: The name of the table to search for objects.
            query: The text to search for.

        Returns:
            An array of search results.
        """
        table = self.__meta.tables[mode]
        name = table.c.name if mode == 'groups' else table.c.fullname
        stmt = select(name).filter(name.like(f'%{query}%')).order_by(name)
        try:
            if self._conn.execute(stmt).first()[0] == query:
                return [query]
            else:
                res = self._conn.execute(stmt).all()
                return [r for r, in res]
        except TypeError:
            return []

    async def db_close(self) -> None:
        """Close the connection with the database"""
        self._conn.close()
        self.__engine.dispose()
