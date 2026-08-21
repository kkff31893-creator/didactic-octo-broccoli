import sys
from pathlib import Path
import os

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from database.db import init_db

# Import handlers
from handlers import start, deals, profile, reviews, admin, language

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="OK - Garant Bot is running!")

async def start_health_server(port: int):
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Health check web server started on port {port}")

async def main():
    logger.info("Initializing Database...")
    await init_db()
    logger.info("Database initialized successfully.")

    # Start dummy web server for Render.com Web Service healthcheck
    port = int(os.getenv("PORT", 10000))
    try:
        await start_health_server(port)
    except Exception as e:
        logger.warning(f"Could not start web health server: {e}")

    session = None
    if settings.PROXY_URL:
        logger.info(f"Using proxy: {settings.PROXY_URL}")
        session = AiohttpSession(proxy=settings.PROXY_URL)

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Register all routers
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(deals.router)
    dp.include_router(profile.router)
    dp.include_router(reviews.router)
    dp.include_router(language.router)

    logger.info("Starting Telegram Garant Bot Polling...")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        logger.warning(f"Could not delete webhook: {e}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
