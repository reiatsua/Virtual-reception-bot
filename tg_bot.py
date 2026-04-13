import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

load_dotenv()

# --- НАСТРОЙКИ ---
BOT_DIR = Path(__file__).resolve().parent
FILE_PATH = BOT_DIR / os.getenv('ADMIN_CHAT_ID_FILE')
TOKEN = os.getenv("RECEPTION_BOT_TOKEN") # Токен бота из .env
ALLOWED_PHONE = os.getenv("ALLOWED_PHONE") # Укажи номер директора или секретаря
# -----------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем кнопку для запроса номера телефона
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Подтвердить номер телефона", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Здравствуйте! Нажмите кнопку ниже, чтобы подтвердить, что вы являетесь администратором приемной комиссии.",
        reply_markup=contact_keyboard
    )

@dp.message(F.contact)
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number
    
    # Нормализуем номер (Телеграм иногда отдает номер без плюса)
    if not phone.startswith('+'):
        phone = '+' + phone

    if phone == ALLOWED_PHONE:
        # Сохраняем ID чата в текстовый файл, чтобы Django знал, куда писать
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(str(message.chat.id))
            
        await message.answer("✅ Аккаунт приемной комиссии привязан успешно.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("❌ Вы не являетесь приемной комиссией.", reply_markup=ReplyKeyboardRemove())

async def main():
    print("Бот запущен и ждет привязки...")
    # Запуск асинхронного поллинга
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())