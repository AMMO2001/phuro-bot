from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

# ✅ Обработчики команд - ВЫСОКИЙ ПРИОРИТЕТ
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    print(f"✅ /start от пользователя {message.from_user.id}")
    await message.answer(f"✅ Бот работает! Твой ID: {message.from_user.id}")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    print(f"✅ /help от пользователя {message.from_user.id}")
    await message.answer("📝 Помощь: Используй /start, /profile, /my_id")

@router.message(Command("my_id"))
async def cmd_my_id(message: types.Message):
    print(f"✅ /my_id от пользователя {message.from_user.id}")
    await message.answer(f"🆔 Твой ID: {message.from_user.id}")

@router.message(Command("about"))
async def cmd_about(message: types.Message):
    print(f"✅ /about от пользователя {message.from_user.id}")
    await message.answer("🤖 PHURO v1.0")

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Показывает статистику пользователя из базы данных"""
    print(f"✅ /profile от пользователя {message.from_user.id}")
    
    from utils.database import Database
    db = Database()
    
    user_id = message.from_user.id
    
    stats = db.get_user_stats(user_id)
    
    if not stats:
        await message.answer("📊 Статистика пока недоступна")
        return
    
    registered = stats['registered_at'][:16]
    last_active = stats['last_activity'][:16] if stats['last_activity'] else "только что"
    
    profile_text = f"""
👤 <b>Профиль пользователя</b>

📛 <b>Имя:</b> {stats['first_name'] or 'Не указано'}
🔗 <b>Username:</b> @{stats['username'] or 'Не указан'}
🆔 <b>ID:</b> <code>{user_id}</code>

📊 <b>Статистика:</b>
💬 Сообщений: <b>{stats['message_count']}</b>
📅 Зарегистрирован: <b>{registered}</b>
🕐 Последняя активность: <b>{last_active}</b>

💡 <i>Продолжай общаться чтобы увеличить статистику!</i>
"""
    await message.answer(profile_text)

# ⛔ УДАЛИТЕ ЭТОТ ОБРАБОТЧИК - он блокирует все сообщения!
# @router.message()
# async def log_message_only(message: types.Message):
#     """Только логирует сообщение, но НЕ отвечает на него"""
#     print(f"📝 Логирование: User {message.from_user.id} сказал: {message.text}")
#     
#     # Логируем в файл (опционально)
#     import aiofiles
#     import os
#     import datetime
#     
#     log_entry = f"{datetime.datetime.now()} - {message.from_user.id}: {message.text}\n"
#     os.makedirs('data', exist_ok=True)
#     
#     async with aiofiles.open('data/messages.log', 'a', encoding='utf-8') as f:
#         await f.write(log_entry)