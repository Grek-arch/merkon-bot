
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '7752598173:AAE8B2tXcnehDiAZX2-6HY0DlZO16xmHlRo'
MY_TELEGRAM_ID = 5943436254

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer("Здравствуйте! Давайте начнем. Напишите наименование товарного знака:")

@dp.message_handler(lambda message: message.from_user.id in user_data and 'name' not in user_data[message.from_user.id])
async def get_name(message: types.Message):
    user_data[message.from_user.id]['name'] = message.text
    await message.answer("Регион использования (страна, регион):")

@dp.message_handler(lambda message: 'region' not in user_data[message.from_user.id])
async def get_region(message: types.Message):
    user_data[message.from_user.id]['region'] = message.text
    await message.answer("Срок полезного использования (лет):")

@dp.message_handler()
async def collect_rest(message: types.Message):
    user_data[message.from_user.id]['other'] = message.text
    data = user_data[message.from_user.id]
    summary = "\n".join([f"{k}: {v}" for k, v in data.items()])
    await bot.send_message(MY_TELEGRAM_ID, f"Новая анкета:\n{summary}")
    await message.answer("Спасибо! Анкета отправлена оценщику.")
    del user_data[message.from_user.id]

if __name__ == '__main__':
    executor.start_polling(dp)
