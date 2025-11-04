import sys
print("Python executable:", sys.executable)
print("Python path:", sys.path)

try:
    from aiogram import Bot
    print("✅ Aiogram импортирован успешно!")
except ImportError as e:
    print(f"❌ Ошибка: {e}")

try:
    import dotenv
    print("✅ python-dotenv импортирован успешно!")
except ImportError as e:
    print(f"❌ Ошибка: {e}")