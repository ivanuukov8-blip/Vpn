import aiosqlite
from datetime import datetime

DB_NAME = "data/bot.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            referrer_id INTEGER,
            created_at TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS promocodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            discount INTEGER,
            uses INTEGER DEFAULT 0,
            max_uses INTEGER DEFAULT 1
        )
        """)

        await db.commit()


async def add_user(
        telegram_id,
        username,
        referrer_id=None
):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT telegram_id FROM users WHERE telegram_id=?",
            (telegram_id,)
        )

        exists = await cursor.fetchone()

        if exists:
            return False

        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (
                telegram_id,
                username,
                referrer_id,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                telegram_id,
                username,
                referrer_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        await db.commit()

        return True


async def get_user(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT * FROM users WHERE telegram_id=?",
            (telegram_id,)
        )

        return await cursor.fetchone()


async def get_referrals(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM users
            WHERE referrer_id=?
            """,
            (user_id,)
        )

        result = await cursor.fetchone()

        return result[0]


async def get_users_count():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        result = await cursor.fetchone()

        return result[0]


async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT telegram_id FROM users"
        )

        return await cursor.fetchall()