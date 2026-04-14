import asyncio
import os
import aiohttp  # <-- Новая библиотека для асинхронных запросов
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

load_dotenv()

# --- НАСТРОЙКИ ---
TOKEN = os.getenv("RECEPTION_BOT_TOKEN") 
ALLOWED_PHONE = os.getenv("ALLOWED_PHONE")

# Новые переменные для связи с сайтом (которые мы пропишем в Railway)
API_URL = os.getenv("WEBHOOK_API_URL") # например: https://flyceum-prod.up.railway.app/api/update-reception-id/
SECRET_KEY = os.getenv("BOT_SECRET_KEY")
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
    # Проверка: человек скинул свой контакт или переслал чужой?
    if message.contact.user_id != message.from_user.id:
        await message.answer("❌ Пожалуйста, отправьте свой собственный контакт через кнопку.", reply_markup=ReplyKeyboardRemove())
        return

    phone = message.contact.phone_number
    
    # Нормализуем номер
    if not phone.startswith('+'):
        phone = '+' + phone

    if phone == ALLOWED_PHONE:
        chat_id = message.chat.id
        
        # --- ОТПРАВЛЯЕМ ID НА САЙТ ---
        payload = {
            "chat_id": chat_id,
            "secret_key": SECRET_KEY
        }
        
        try:
            # Асинхронно стучимся на твой сайт
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, json=payload) as response:
                    if response.status == 200:
                        await message.answer("✅ Отлично! Ваш аккаунт привязан. Теперь обращения с сайта будут приходить сюда.", reply_markup=ReplyKeyboardRemove())
                    else:
                        error_text = await response.text()
                        print(f"Ошибка от сайта: {error_text}")
                        await message.answer("⚠️ Вы подтвердили номер, но произошла ошибка связи с сайтом. Обратитесь к разработчику.", reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            print(f"Не смогли достучаться до сайта: {e}")
            await message.answer("❌ Сервер сайта сейчас недоступен.", reply_markup=ReplyKeyboardRemove())
            
    else:
        await message.answer("❌ Извините, этот номер не зарегистрирован как номер приемной комиссии.", reply_markup=ReplyKeyboardRemove())

async def main():
    print("Бот запущен и ждет привязки...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())