import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import Config
from app.handlers import register_all_handlers
from app.database.database import init_db
from app.core.bot import bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    await init_db()
    dp = Dispatcher()
    register_all_handlers(dp)
    logging.info("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
