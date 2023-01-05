from ..config import cur


async def checkTableExists(name: str) -> bool:
    try:
        cur.execute(f"""
            SELECT EXISTS(
                SELECT *
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = '{name}')        
        """)
        cur.fetchone()
        print(cur.fetchone())
        return True
    except Exception as e:
        print(f'DB Error: {e}')
        return False
