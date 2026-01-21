import logging
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# 1. ТОКЕНИ ХУДРО ДАР БАЙНИ НОХУНАКҲО ГУЗОРЕД
TOKEN = "8560757080:AAFXJLy71LZTPKMmCiscpe1mWKmj3lC-hDE"

# Линки шумо аз GitHub Pages (аллакай илова шудааст)
WEB_APP_URL = "https://oson-savdo.github.io/magoza-bot/" 

# Танзимоти бот
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Фармони /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Тугмаи асосӣ барои Сканер (WebApp)
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    scan_btn = types.KeyboardButton("🚀 Сканер ва Фурӯш", web_app=web_app)
    
    markup.add(scan_btn)
    markup.add(types.KeyboardButton("📦 Қабули бор"), types.KeyboardButton("📊 Ҳисобот"))
    
    await message.answer(
        f"Салом {message.from_user.full_name}!\n"
        "Системаи 'Oson Savdo' омода аст. Барои оғози фурӯш тугмаи Сканерро пахш кунед.",
        reply_markup=markup
    )

# Қабули файлҳои Excel (Қабули бор)
@dp.message_handler(content_types=['document'])
async def handle_excel(message: types.Message):
    if message.document.file_name.endswith(('.xlsx', '.xls')):
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        
        # Файлро бо номи stock.xlsx захира мекунем
        await bot.download_file(file.file_path, "stock.xlsx")
        
        try:
            df = pd.read_excel("stock.xlsx")
            await message.answer(f"✅ Файл қабул шуд!\nДар склад {len(df)} намуд маҳсулот илова гардид.")
        except Exception as e:
            await message.answer(f"❌ Хатогӣ ҳангоми хондани файл: {e}")
    else:
        await message.answer("⚠️ Лутфан танҳо файлҳои Excel-ро (.xlsx) фиристед.")

# Қабули маълумот аз WebApp пас аз фурӯш
@dp.message_handler(content_types=['web_app_data'])
async def get_webapp_data(message: types.Message):
    # Маълумоте, ки аз саҳифаи сканер меояд
    sale_details = message.web_app_data.data
    
    report_text = (
        "✅ **Фурӯш тасдиқ шуд!**\n\n"
        f"📝 Маҳсулот: {sale_details}\n"
        "---------------------------\n"
        "Маълумот ба базаи фурӯш илова шуд."
    )
    await message.answer(report_text, parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
