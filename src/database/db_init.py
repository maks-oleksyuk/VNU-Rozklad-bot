from os import getenv

import mariadb

con = mariadb.connect(
    host='db',
    user=getenv('DB_USER', default=''),
    password=getenv('DB_PASS', default=''),
    database=getenv('DB_NAME', default=''),
)
cur = con.cursor()


async def db_init():
    if not await check_table_exists('users'):
        await create_table_users()
    if not await check_table_exists('users_data'):
        await create_table_users_data()


async def db_close():
    cur.close()
    con.close()


async def check_table_exists(name: str) -> bool:
    try:
        cur.execute(f"""
            SELECT EXISTS(
                SELECT *
                FROM information_schema.tables
                WHERE table_name = '{name}')
        """)
        return cur.fetchone()[0]
    except Exception as e:
        print(f'DB Error: {e}')
        return False


async def create_table_users():
    try:
        cur.execute("""
            CREATE TABLE users (
                uid      serial comment 'The Telegram user ID.',
                name     char(255) comment 'The name of this user.',
                username char(255) comment 'The Telegram pseudonym of this user.',
                status   boolean NOT NULL DEFAULT TRUE comment 'Whether the user is active or blocked.',
                login    timestamp DEFAULT CURRENT_TIMESTAMP comment 'The time that the user last logged in.'
            );
        """)
        con.commit()
    except Exception as e:
        print(f'DB Error: {e}')


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
