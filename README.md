# 🛡️ Бот авторизации администрации | Reception Bot

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Telegram API](https://img.shields.io/badge/Telegram-Bot_API-2CA5E0?logo=telegram&logoColor=white)

Сервисный Telegram-бот, обеспечивающий безопасность системы виртуальной приемной. Является неотъемлемой частью цифровой экосистемы Первого IT-лицея. 

Его главная задача — провести первичную авторизацию уполномоченного лица (директора или секретаря) по номеру телефона, получить уникальный ID чата и безопасно передать его основному сайту для настройки рассылки обращений.

## 🔗 Зависимости
Этот бот генерирует конфигурационный файл `admin_chat_id.txt`, который необходим для работы **основного сайта лицея** (Django API).
* Репозиторий основного сайта: [First IT Lyceum](https://github.com/reiatsua/First_IT_Lyceum.git)

## 🛠 Технологии
* **Язык:** Python 3
* **Фреймворк:** `aiogram` 3.x (Асинхронный поллинг)
* **Окружение:** `python-dotenv`

## 🚀 Как запустить локально

### 1. Подготовка
Склонируйте репозиторий на свой компьютер и перейдите в папку бота (для корректной работы назовите ее `reception_bot`):
```bash
git clone https://github.com/reiatsua/Virtual-reception-bot.git
cd reception_bot
```

### 2. Виртуальное окружение
Создайте и активируйте виртуальное окружение:

Для Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Для Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Примечание: при ошибке выполнения на Windows попробуйте следующую команду:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Установка зависимостей
Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` в корневой папке бота и добавьте следующие ключи:
```env
RECEPTION_BOT_TOKEN=ваш_токен_бота_приемной_комиссии
ALLOWED_PHONE=+77XXXXXXXXX
ADMIN_CHAT_ID_FILE=admin_chat_id.txt
```
*Внимание: укажите в `ALLOWED_PHONE` реальный номер телефона администратора в международном формате с плюсом. Только с этого номера можно будет привязать аккаунт.*

### 5. Запуск и авторизация
Запустите скрипт бота:
```bash
python reception_bot.py
```

**После запуска:**
1. Найдите бота в Telegram и отправьте команду `/start`.
2. Нажмите появившуюся кнопку «📱 Подтвердить номер телефона».
3. Если номер совпадает с `ALLOWED_PHONE`, бот успешно создаст файл `admin_chat_id.txt` в своей корневой папке. 

*(После создания файла этот бот можно остановить, так как сайт будет читать ID напрямую из файла, а отправлять сообщения через собственный запрос к Telegram API).*