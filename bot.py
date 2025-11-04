import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Импорты роутеров
from handlers.start import router as start_router
from handlers.admin import router as admin_router
from handlers.echo import router as echo_router

logging.basicConfig(level=logging.INFO)

async def main():
    # ✅ Берем токен из переменных окружения (для облака)
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    if not BOT_TOKEN:
        # ✅ Для локальной разработки
        from config import BOT_TOKEN as local_token
        BOT_TOKEN = local_token
    
    if not BOT_TOKEN:
        logging.error("❌ BOT_TOKEN не найден! Проверь переменные окружения.")
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(admin_router) 
    dp.include_router(echo_router)
    
    print("🚀 БОТ ЗАПУЩЕН В ОБЛАКЕ!")
    print("✅ Роутеры подключены, ожидаем сообщения...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        print("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())