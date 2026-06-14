import asyncio

from aiogram import Bot
from aiogram import Dispatcher

from config import BOT_TOKEN

from database import init_db

from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.referral import router as referral_router
from handlers.admin import router as admin_router
from handlers.mailing import router as mailing_router
from handlers.guide import router as guide_router


async def main():
    await init_db()

    bot = Bot(BOT_TOKEN)

    try:
        me = await bot.get_me()
        print(f"Бот запущен: @{me.username}")
    except Exception as e:
        print("Ошибка подключения к Telegram:")
        print(e)
        return

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(referral_router)
    dp.include_router(admin_router)
    dp.include_router(mailing_router)
    dp.include_router(guide_router)

    print("Polling started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())