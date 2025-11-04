import os
from dotenv import load_dotenv

load_dotenv('token.env')


BOT_TOKEN = os.getenv('BOT_TOKEN') 
ADMIN_IDS = [7091567651]

if not BOT_TOKEN:
    load_dotenv('token.env')
    BOT_TOKEN = os.getenv('BOT_TOKEN')