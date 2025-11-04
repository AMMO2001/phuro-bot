from aiogram import Router, types, F
from aiogram.filters import Command
import aiofiles
import os
import datetime

router = Router()

@router.message(F.text == "привет")
async def echo_hello(message: types.Message):
    print(f"🎯 Обработчик 'привет' ВЫЗВАН! User: {message.from_user.id}")
    
    from utils.database import Database
    db = Database()
    
    try:
        db.add_user({
            'id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'language_code': message.from_user.language_code,
            'is_bot': message.from_user.is_bot
        })
        print("✅ Пользователь сохранен через add_user")
    except Exception as e:
        print(f"❌ Ошибка в add_user: {e}")
    
    db.log_message(message.from_user.id, message.text)
    print("✅ Сообщение залогировано")
    
    await message.answer("И тебе привет! 😊")

@router.message(Command("top"))
async def cmd_top(message: types.Message):
    """Показывает топ активных пользователей"""
    
    top_text = """
🏆 <b>Топ активных пользователей</b>

🚧 <i>Эта функция скоро появится!</i>

А пока можешь посмотреть свою статистику командой /profile
"""
    await message.answer(top_text)

# ✅ ОБНОВЛЕННЫЙ обработчик для ВСЕХ сообщений
@router.message()
async def echo_all_messages(message: types.Message):
    """Обрабатывает ВСЕ сообщения - логирует и отвечает эхом"""
    print(f"🎯 Echo handler: User {message.from_user.id} said: {message.text}")
    
    # Логируем в файл
    log_entry = f"{datetime.datetime.now()} - {message.from_user.id}: {message.text}\n"
    os.makedirs('data', exist_ok=True)
    
    async with aiofiles.open('data/messages.log', 'a', encoding='utf-8') as f:
        await f.write(log_entry)
    
    # Сохраняем в базу данных
    from utils.database import Database
    db = Database()
    
    try:
        db.add_user({
            'id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'language_code': message.from_user.language_code,
            'is_bot': message.from_user.is_bot
        })
        print("✅ User saved to database")
    except Exception as e:
        print(f"❌ Error saving user: {e}")
    
    db.log_message(message.from_user.id, message.text)
    print("✅ Message logged to database")
    
    # Отвечаем эхом
    if message.text:
        await message.answer(f"🔁 Эхо: {message.text}")