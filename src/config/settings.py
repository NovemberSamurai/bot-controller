import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
EXTERNAL_API_SAVE_URL = os.getenv('EXTERNAL_API_SAVE_URL')
EXTERNAL_API_CREATE_URL = os.getenv('EXTERNAL_API_CREATE_URL')
PORT = int(os.getenv('HEALTH_PORT', 8080))
