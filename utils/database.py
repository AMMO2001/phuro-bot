import sqlite3
import datetime
import logging
from typing import Optional, List, Tuple

import sqlite3
import datetime
import logging
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_path: str = "data/bot.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Создает соединение с базой данных"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Инициализирует таблицы в базе данных"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language_code TEXT,
                    is_bot BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица сообщений (для статистики)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Таблица настроек бота
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bot_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            conn.commit()
        logging.info("✅ База данных инициализирована")

    def get_top_users(self, limit: int = 10):  # ⭐ ПЕРЕМЕСТИЛ ВНУТРЬ КЛАССА!
        """Возвращает топ активных пользователей"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    u.user_id,
                    u.username,
                    u.first_name,
                    COUNT(m.id) as message_count
                FROM users u
                LEFT JOIN messages m ON u.user_id = m.user_id
                GROUP BY u.user_id
                ORDER BY message_count DESC
                LIMIT ?
            ''', (limit,))
            
            return cursor.fetchall()
    
    
##############################################################################    

    def add_user(self, user_data: dict):
        """Добавляет или обновляет пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, language_code, is_bot, last_activity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['id'],
                user_data.get('username'),
                user_data.get('first_name'),
                user_data.get('last_name'),
                user_data.get('language_code'),
                user_data.get('is_bot', False),
                datetime.datetime.now()
            ))
            
            conn.commit()
    
    def log_message(self, user_id: int, text: str):
        """Логирует сообщение пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Сначала убедимся что пользователь существует
            cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
            if not cursor.fetchone():
                # Если пользователя нет, создаем базовую запись
                cursor.execute(
                    'INSERT INTO users (user_id, last_activity) VALUES (?, ?)',
                    (user_id, datetime.datetime.now())
                )
            
            # Логируем сообщение
            cursor.execute(
                'INSERT INTO messages (user_id, text) VALUES (?, ?)',
                (user_id, text)
            )
            
            # Обновляем время последней активности
            cursor.execute(
                'UPDATE users SET last_activity = ? WHERE user_id = ?',
                (datetime.datetime.now(), user_id)
            )
            
            conn.commit()
    
    def get_user_stats(self, user_id: int) -> dict:
        """Возвращает статистику пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Основная информация о пользователе
            cursor.execute('''
                SELECT username, first_name, created_at, last_activity 
                FROM users WHERE user_id = ?
            ''', (user_id,))
            user_data = cursor.fetchone()
            
            # Количество сообщений
            cursor.execute('''
                SELECT COUNT(*) FROM messages WHERE user_id = ?
            ''', (user_id,))
            message_count = cursor.fetchone()[0]
            
            if user_data:
                return {
                    'username': user_data[0],
                    'first_name': user_data[1],
                    'registered_at': user_data[2],
                    'last_activity': user_data[3],
                    'message_count': message_count
                }
            return None
    
    def get_bot_stats(self) -> dict:
        """Возвращает общую статистику бота"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Общее количество пользователей
            cursor.execute('SELECT COUNT(*) FROM users')
            total_users = cursor.fetchone()[0]
            
            # Количество активных пользователей (за последние 7 дней)
            week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
            cursor.execute('''
                SELECT COUNT(*) FROM users WHERE last_activity > ?
            ''', (week_ago,))
            active_users = cursor.fetchone()[0]
            
            # Общее количество сообщений
            cursor.execute('SELECT COUNT(*) FROM messages')
            total_messages = cursor.fetchone()[0]
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_messages': total_messages
            }