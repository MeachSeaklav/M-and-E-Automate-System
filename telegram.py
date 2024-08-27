import os
import requests
from dotenv import load_dotenv

load_dotenv()
# Set your Telegram bot token and chat ID
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = '-1002164741954'  # This can stay hardcoded or also be moved to an environment variable if needed

def send_to_telegram(file_path, caption):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendDocument"
    with open(file_path, 'rb') as file:
        response = requests.post(url, data={'chat_id': telegram_chat_id, 'caption': caption}, files={'document': file})
    return response