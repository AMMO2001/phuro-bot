import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.admin import router as admin_router
from handlers.echo import router as echo_router

logging.basicConfig(level=logging.INFO)

async def main():
    # ✅ ПРАВИЛЬНО: инициализация внутри async функции
    from utils.database import Database
    db = Database()
    
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # ⚡ ПРАВИЛЬНЫЙ ПОРЯДОК:
    dp.include_router(start_router)   # ← ПЕРВЫЙ! (команды и логирование)
    dp.include_router(admin_router)   # ← ВТОРОЙ (админ команды)  
    dp.include_router(echo_router)    # ← ПОСЛЕДНИЙ! (эхо и ответы на сообщения)
    
    print("🚀 БОТ ЗАПУЩЕН!!!...")
    print("✅ Роутеры подключены, ожидаем сообщения...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        print("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())