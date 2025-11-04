from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
import aiofiles
import os
import datetime

from config import ADMIN_IDS

router = Router()

def is_admin(user_id: int) -> bool:
    """Проверяет, является ли пользователь администратором"""
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к этой команде")
        return
    
    admin_text = """
🛠️ <b>Админ панель</b>

📊 <b>Команды:</b>
/admin_logs - Получить логи
/admin_stats - Статистика  
/admin_clean - Очистить логи
/server_info - Инфо о сервере

💡 <b>Совет:</b> /admin_logs 10 - покажет последние 10 строк
"""
    await message.answer(admin_text)


@router.message(Command("admin_logs"))
async def cmd_admin_logs(message: types.Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    
    if not os.path.exists('data/messages.log'):
        await message.answer("📊 Логи пусты")
        return
    
    try:
        async with aiofiles.open('data/messages.log', 'r', encoding='utf-8') as f:
            logs = await f.read()
        
        if not logs.strip():
            await message.answer("📊 Логи пусты")
            return
            
        # Если указано количество строк
        if command.args and command.args.isdigit():
            lines = logs.strip().split('\n')
            lines = lines[-int(command.args):]
            logs = '\n'.join(lines)
            
            if len(logs) > 4000:
                logs = logs[-4000:]
                await message.answer(f"<pre>{logs}</pre>", parse_mode="HTML")
                await message.answer(f"⚠ Показаны последние 4000 символов из {command.args} строк")
            else:
                await message.answer(f"<pre>{logs}</pre>", parse_mode="HTML")
            return
        
        # Если логов много, покажем только последние 20 строк
        if len(logs) > 4000:
            lines = logs.strip().split('\n')
            lines = lines[-20:]  # последние 20 строк
            logs = '\n'.join(lines)
            await message.answer(f"<pre>{logs}</pre>", parse_mode="HTML")
            await message.answer("⚠ Логов много! Показаны последние 20 строк. Используй /admin_logs 10 для другого количества")
        else:
            await message.answer(f"<pre>{logs}</pre>", parse_mode="HTML")
            
    except Exception as e:
        await message.answer(f"❌ Ошибка чтения логов: {e}")

@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    bot_stats = db.get_bot_stats()
    
    # ЗАКОММЕНТИРУЙ ЭТИ СТРОКИ:
    # top_users = db.get_top_users(3)  # Топ-3 для админки
    # top_text = ""
    # for i, (user_id, username, first_name, message_count) in enumerate(top_users, 1):
    #     user_display = f"@{username}" if username else first_name or f"User_{user_id}"
    #     top_text += f"{i}. {user_display} - {message_count} сообщ.\n"
    
    stats_text = f"""
📈 <b>Статистика бота (из БАЗЫ ДАННЫХ)</b>

👥 <b>Пользователи:</b>
• Всего: <b>{bot_stats['total_users']}</b>
• Активных: <b>{bot_stats['active_users']}</b>

💬 <b>Сообщения:</b>
• Всего: <b>{bot_stats['total_messages']}</b>

⚙️ <b>Система:</b>
• Админов: <b>{len(ADMIN_IDS)}</b>
• Ваш ID: <code>{message.from_user.id}</code>
"""
    await message.answer(stats_text)

@router.message(Command("admin_clean"))
async def cmd_admin_clean(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        if os.path.exists('data/messages.log'):
            async with aiofiles.open('data/messages.log', 'w', encoding='utf-8') as f:
                await f.write("")
            await message.answer("✅ Логи успешно очищены")
        else:
            await message.answer("📊 Логи и так пусты")
    except Exception as e:
        await message.answer(f"❌ Ошибка очистки логов: {e}")

#################################################### тут команда сервер инфо

@router.message(Command("server_info"))
async def cmd_server_info(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        import platform
        import psutil  # ⭐ ВРЕМЕННО КОММЕНТИРУЕМ
        
        system_info = f"""
🖥️ <b>Информация о сервере</b>

<b>Система:</b>
• OS: {platform.system()} {platform.release()}
• Архитектура: {platform.machine()}
• Python: {platform.python_version()}

<b>Память и диск:</b>
• Информация временно недоступна
• Установи psutil: pip install psutil

<b>База данных:</b>
• Файл: data/bot.db
• Таблицы: users, messages, bot_settings
"""
        await message.answer(system_info)
    except Exception as e:
        await message.answer(f"❌ Ошибка получения информации: {e}")

#################################################### с ней были траблы




