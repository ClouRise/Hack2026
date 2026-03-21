# test_db.py — положи в папку backend/
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="h26_user",
        password="123123",
        database="h26_db",
    )
    print("OK:", await conn.fetchval("SELECT version()"))
    await conn.close()

asyncio.run(main())