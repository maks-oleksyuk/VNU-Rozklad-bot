from os import getenv

import psycopg2 as ps

base = ps.connect(
    host="db",
    user=getenv("DB_USER", default=""),
    password=getenv("DB_PASS", default=""),
    database=getenv("DB_NAME", default=""),
)
cur = base.cursor()


async def db_init():
    if not await checkTableExists('users'):
        await createTableUsers()
    if not await checkTableExists('users_data'):
        await createTableUsersData()


async def checkTableExists(name: str) -> bool:
    try:
        cur.execute(f"""
            SELECT EXISTS(
                SELECT *
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = '{name}')
        """)
        return cur.fetchone()[0]
    except Exception as e:
        print(f'DB Error: {e}')
        return False


async def createTableUsers():
    try:
        cur.execute("""
            CREATE TABLE public.users (
                uid      bigserial NOT NULL,
                name     char(255),
                username char(255),
                type     char(65) NOT NULL,
                status   boolean NOT NULL DEFAULT TRUE,
                login    timestamp without time zone DEFAULT timezone('Europe/Kiev'::text, now())
            );
            comment on column users.uid      is 'The Telegram user ID.';
            comment on column users.name     is 'The name of this user.';
            comment on column users.username is 'The Telegram pseudonym of this user.';
            comment on column users.type     is 'Type of user in the system.';
            comment on column users.status   is 'Whether the user is active or blocked.';
            comment on column users.login    is 'The time that the user last logged in.';
        """)
        base.commit()
    except Exception as e:
        print(f'DB Error: {e}')


async def createTableUsersData():
    try:
        cur.execute("""
            CREATE TABLE public.users_data (
                uid    bigserial NOT NULL,
                d_id   integer   NOT NULL,
                d_date date      NOT NULL
            );
            comment on column users_data.uid    is 'The Telegram user ID.';
            comment on column users_data.d_id   is 'The Data ID.';
            comment on column users_data.d_date is 'The Last date of requested data.';
        """)
        base.commit()
    except Exception as e:
        print(f'DB Error: {e}')
