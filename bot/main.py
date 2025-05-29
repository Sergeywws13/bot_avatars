import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN, LOG_LEVEL
from handlers import user_handlers, callback_handlers, admin_handlers



logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(user_handlers.router)
    dp.include_router(callback_handlers.router)
    dp.include_router(admin_handlers.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
