import telebot
from telebot import types
import os
import json

TOKEN = '8560757080:AAFXJLy71LZTPKMmCiscpe1mWKmj3lC-hDE'
# Ссылкаи GitHub Pages-и шумо (баъди фаъол кардан)
URL = "https://oson-savdo.github.io/magoza-bot/"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo(url=URL)
    markup.add(types.KeyboardButton("📷 Сканер", web_app=web_app))
    bot.send_message(message.chat.id, "Хуш омадед! Барои фурӯш 'Сканер'-ро пахш кунед:", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    data = json.loads(message.web_app_data.data)
    bot.send_message(message.chat.id, f"Фурӯхта шуд: {data}")

bot.infinity_polling()
