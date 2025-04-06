import telebot
from secret_data import secret_data

token = secret_data.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)