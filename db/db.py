import logging
from datetime import date, datetime, timedelta

from aiogram import types
from sqlalchemy import (
    create_engine, inspect, MetaData, Table, Column, UniqueConstraint,
    select, update, delete, text, func
)
from sqlalchemy.dialects.mysql import (
    BOOLEAN, SMALLINT, INTEGER, BIGINT, VARCHAR, TEXT, DATE, TIMESTAMP, insert
)


class Database:
    """A class for managing a database.

    Attributes:
        __engine: a SQLAlchemy engine object for connecting to a database.
        __meta: a SQLAlchemy metaData object for reflecting on database metadata.
        __inspector: a SQLAlchemy Inspector object for inspecting database objects.
    """

    def __init__(self, db_name: str, db_user: str, db_pass: str,
                 db_host: str = 'localhost', db_port: int = 3306):
        """Initializes a Database object.

        Args:
            db_name: Name of the database.
            db_user: Username for accessing the database.
            db_pass: Password for accessing the database.
            db_host: Host name or IP address of the database server.
            db_port: Port number of the database server.
        """
        self.log = logging.getLogger('bot')

        # Create database engine with provided parameters.
        self.__engine = create_engine(
            f'mariadb+mariadbconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}',
            pool_pre_ping=True,
            pool_recycle=21600,
            pool_size=20,
        )

        # Initialize metadata and inspector objects.
        self.__meta = MetaData()
        self.__meta.reflect(bind=self.__engine)
        self.__inspector = inspect(self.__engine)

        # Create database tables if they do not exist.
        self._create_tables()

        # Get table objects.
        self._users = self.__meta.tables['users']
        self._users_data = self.__meta.tables['users_data']
        self._groups = self.__meta.tables['groups']
        self._teachers = self.__meta.tables['teachers']
        self._timetable = self.__meta.tables['timetable']
        self._audiences = self.__meta.tables['audiences']

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
                Column('room', VARCHAR(32),
                       comment='The lesson room.'),
                Column('type', VARCHAR(8), nullable=False,
                       comment='The lesson type.'),
                Column('title', TEXT, nullable=False,
                       comment='The lesson title.'),
                Column('teacher', VARCHAR(64),
                       comment='The lesson teacher.'),
                Column('group', VARCHAR(255),
                       comment='The lesson group(s).'),
                Column('replacement', VARCHAR(255)),
                Column('reservation', VARCHAR(255)),
                UniqueConstraint('id', 'mode', 'date', 'lesson_number', 'teacher', 'group')
            )
            self.log.info('The `timetable` table was not found, it has been created')
        if not self.__inspector.has_table('audiences'):
            Table(
                'audiences', self.__meta,
                Column('id', SMALLINT(unsigned=True), nullable=False),
                Column('block', VARCHAR(128), nullable=False),
                Column('room', VARCHAR(32), nullable=False),
                Column('type', VARCHAR(8)),
                Column('floor', SMALLINT(unsigned=True)),
                Column('places', SMALLINT(unsigned=True)),
            )
            self.log.info('The `audiences` table was not found, it has been created')
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
        with self.__engine.connect() as conn:
            return not conn.execute(stmt).scalar()

    async def insert_update_user(self, message: types.Message) -> None:
        """Inserts or updates a user record in the database.

        Args:
            message: The message sent by the user.
        """
        with self.__engine.connect() as conn:
            conn.execute(insert(self._users).values(
                uid=message.from_user.id,
                fullname=message.from_user.full_name,
                username=message.from_user.username,
            ).on_duplicate_key_update(
                fullname=message.from_user.full_name,
                username=message.from_user.username,
                status=True,
                login=text('default')
            ))
            conn.commit()
        self.log.debug(f'User {message.from_user.full_name} - created/updated')

    async def save_user_data(self, message: types.Message,
                             d_mode: str, d_date: date = date.today()) -> None:
        """Saves user data to the database.

        Args:
            message: The message sent by the user.
            d_mode: String indicating the data mode (group or teacher).
            d_date: Optional date object representing the date of the data (default is today).
        """
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
        with self.__engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    async def get_users_data_by_id(self, uid: int) -> dict | None:
        """Get user data by user id.

        Args:
            uid: User id, received from the message.

        Returns:
            A dictionary of user data, or None if the user is not found.
        """
        stmt = select(self._users_data).where(self._users_data.c.uid == uid)
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).first()
            return res._asdict() if res else None

    async def update_user_data_date(self, id: int, date: date) -> None:
        """Updates a user's data with a new date.

        Args:
            id: The ID of the user whose data is being updated.
            date: The new date to update the user's data with.
        """
        stmt = (update(self._users_data)
                .values(d_date=date)
                .where(self._users_data.c.uid == id))
        with self.__engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    async def save_groups(self, data: dict) -> None:
        """Saves groups data to the database.

        Args:
            data: a dictionary containing groups data.
        """
        query_data = []
        # Iterate through the data and add each group to the query data list.
        [(query_data.append({
            'id': i['ID'],
            'department': d['name'],
            'name': i['name'],
        })) for d in data for i in d['objects'] if i['ID'] != '']

        # Delete existing data in the `groups` table, and
        # Insert the query data into the `groups` table and commit it.
        with self.__engine.connect() as conn:
            conn.execute(self._groups.delete())
            conn.execute(insert(self._groups).values(query_data))
            conn.commit()

        # Log a message indicating the `groups` table was successfully updated.
        self.log.info('Table `groups` updated successfully')

    async def save_teachers(self, data: dict) -> None:
        """Saves teachers data to the database.

        Args:
            data: a dictionary containing teachers data.
        """
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

        # Delete existing data in the `teachers` table, and
        # Insert the query data into the `teachers` table and commit it.
        with self.__engine.connect() as conn:
            conn.execute(self._teachers.delete())
            conn.execute(insert(self._teachers).values(query_data))
            conn.commit()

        # Log a message indicating the `teachers` table was successfully updated.
        self.log.info('Table `teachers` updated successfully')

    async def save_audiences(self, data: dict) -> None:
        """Saves audiences data to the database.

        Args:
            data: a dictionary containing audiences data.
        """
        query_data = []
        # Iterate through the data and add each group to the query data list.
        [(query_data.append({
            'id': i['ID'],
            'block': d['name'],
            'room': i['name'],
        })) for d in data for i in d['objects']]

        # Delete existing data in the `audiences` table, and
        # Insert the query data into the `audiences` table and commit it.
        with self.__engine.connect() as conn:
            conn.execute(self._audiences.delete())
            conn.execute(insert(self._audiences).values(query_data))
            conn.commit()

        self.log.info('The `audiences` table has been successfully updated ')

    async def update_additions_to_audiences(self, data: dict) -> None:
        """Update additional data of audiences in the database.

        Args:
            data: A dictionary of data containing the additional data to update.
        """
        with self.__engine.connect() as conn:
            for i in data:
                stmt = (update(self._audiences)
                        .where(self._audiences.c.room == i['name'])
                        .values(type=i['type'], floor=i['floor'], places=i['places']))
                conn.execute(stmt)
            conn.commit()

        self.log.info('The `audiences` table has been successfully updated with additional data')

    async def get_departments_by_mode(self, mode: str) -> list:
        """Gets a list of departments for a specific type ('groups' or 'teacher').

        Args:
            mode: The table name to retrieve objects in departments.

        Returns:
            A list of departments in the specified table.
        """
        table = self.__meta.tables[mode]
        stmt = select(table.c.department).distinct()
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).all()
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
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).all()
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
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).first()
            return {'id': int(res[0]), 'name': res[1]}

    async def get_audience_blocks(self) -> list:
        stmt = select(self._audiences.c.block).distinct()
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).all()
            return [r for r, in res]

    async def get_block_floors(self, block: str) -> list | None:
        """Retrieve a list of unique floors for a given block.

        Args:
            block: The name of the block to retrieve floors for.

        Returns:
            list or None: A list of integers representing the floors for the
            given block, or None if no floors
        """
        stmt = (select(self._audiences.c.floor)
                .where(self._audiences.c.block == block)
                .filter(self._audiences.c.floor.isnot(None))
                .group_by(self._audiences.c.floor)
                .order_by(self._audiences.c.floor))
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).all()
            return [r for r, in res] if res else None

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
        with self.__engine.connect() as conn:
            try:
                if conn.execute(stmt).first()[0] == query:
                    return [query]
                else:
                    res = conn.execute(stmt).all()
                    return [r for r, in res]
            except TypeError:
                return []

    async def get_teacher_full_name(self, name: str):
        stmt = select(self._teachers.c.fullname).where(func.instr(name, self._teachers.c.name))
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).first()
            return res._asdict() if res else None

    async def save_timetable(self, id: int, mode: str, data: dict,
                             s_date: date, e_date: date) -> None:
        with self.__engine.connect() as conn:
            # Currently, there is no functionality to track deleted rows
            # from the API query result, so all are overwritten.
            conn.execute(delete(self._timetable)
                         .where(self._timetable.c.id == id)
                         .where(self._timetable.c.mode == mode)
                         .where(self._timetable.c.date >= s_date)
                         .where(self._timetable.c.date <= e_date))
            for i in data:
                # We look for matches in groups so as not to store unnecessary data.
                # For example: general (Group, name, ...) to general.
                g = i['group'].find('І (')
                stmt = insert(self._timetable).values(
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

    async def get_timetable(self, id: int, mode: str,
                            s_date: date = date.today(),
                            e_date: date = date.today()) -> list:
        """Get the timetable data from the database.

        Args:
            id: ID of the schedule.
            mode: Schedule mode (teacher or group).
            s_date: Start date of the schedule. Defaults to today.
            e_date: End date of the schedule. Defaults to today.

        Returns:
            list: List of timetable data matching the query.
        """
        from loader import api
        if schedule := await api.get_schedule(id, mode, s_date):
            await self.save_timetable(id, mode, schedule, s_date, s_date + timedelta(weeks=2))
        stmt = (select(self._timetable.c)
                .where(self._timetable.c.id == id)
                .where(self._timetable.c.mode == mode)
                .where(self._timetable.c.date >= s_date)
                .where(self._timetable.c.date <= e_date))
        with self.__engine.connect() as conn:
            res = conn.execute(stmt).all()
            return [r._asdict() for r in res]

    async def _close(self) -> None:
        """Close the connection with the database"""
        self.__engine.dispose()
