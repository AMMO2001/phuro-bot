import sqlite3
from utils.database import Database

# Создаем базу и проверяем
db = Database()

# Проверяем структуру базы
conn = sqlite3.connect('data/bot.db')
cursor = conn.cursor()

print("=== ПРОВЕРКА СТРУКТУРЫ БАЗЫ ===")

# Какие таблицы есть?
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("📊 Таблицы в базе:", tables)

# Содержимое таблицы users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("👥 Пользователи в базе:", users)

# Содержимое таблицы messages  
cursor.execute("SELECT * FROM messages")
messages = cursor.fetchall()
print("💬 Сообщения в базе:", messages)

conn.close()