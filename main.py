import os
import logging
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Токенро аз GitHub Secrets мегирем
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Иваз кунед ба URL-и GitHub Pages-и худ
    web_app = types.WebAppInfo(url="https://yourusername.github.io/your-repo/")
    markup.add(types.KeyboardButton("🔍 Сканер", web_app=web_app))
    markup.add("📊 Ҳисобот", "📦 Қабули бор")
    await message.answer("Хуш омадед! Тугмаро пахш кунед:", reply_markup=markup)

@dp.message_handler(content_types=['document'])
async def handle_excel(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "stock.xlsx")
    df = pd.read_excel("stock.xlsx")
    await message.answer(f"Склад нав шуд! {len(df)} намуд мол илова шуд.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
