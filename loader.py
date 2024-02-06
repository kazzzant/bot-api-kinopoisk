import os
import telebot
from telebot.storage import StateMemoryStorage
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

storage = StateMemoryStorage()

token = os.getenv('BOT_TOKEN')
site_api_key = os.getenv('SITE_API_KEY')
bot = telebot.TeleBot(token, state_storage=storage)
