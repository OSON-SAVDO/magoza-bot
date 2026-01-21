import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import pandas as pd

# ТОКЕН-ро дар ин ҷо гузоред
TOKEN = "8560757080:AAFXJLy71LZTPKMmCiscpe1mWKmj3lC-hDE"
# Линки саҳифаи сканери шумо (баъди сохтани файли 2-юм)
WEB_APP_URL = "https://username.github.io/repository-name/" 

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Тугмаи сканер
    scan_btn = types.KeyboardButton("🚀 Сканер ва Фурӯш", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(scan_btn)
    markup.add("📦 Қабули бор", "📊 Ҳисобот")
    await message.answer("Хуш омадед! Барои фурӯш сканерро пахш кунед:", reply_markup=markup)

# Ин қисм маълумотро аз Сканер қабул мекунад
@dp.message_handler(content_types=['web_app_data'])
async def get_data(message: types.Message):
    # Маълумоте, ки аз сканер меояд (ном ва нарх)
    result = message.web_app_data.data
    await message.answer(f"✅ Фурӯш анҷом ёфт!\n\nРӯйхат:\n{result}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
