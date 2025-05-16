import asyncio
import logging
import sys
import random
from os import getenv, path, listdir

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Директория, где хранятся изображения
PICTURES_DIRECTORY = 'pictures/'

def get_random_picture():
    """
    Получает случайное изображение из указанной директории.
    
    Returns:
        str or None: Полный путь к случайному изображению или None, если директория пуста
    """
    # Получаем список файлов в директории (только файлы, исключая поддиректории)
    picture_files = [f for f in listdir(PICTURES_DIRECTORY) if path.isfile(path.join(PICTURES_DIRECTORY, f))]
    
    # Если нет файлов, возвращаем None
    if not picture_files:
        return None
    
    # Выбираем случайный файл из списка и возвращаем путь
    random_picture = random.choice(picture_files)
    return path.join(PICTURES_DIRECTORY, random_picture)

# Получаем токен бота из переменной окружения
TOKEN = getenv("TOKEN")
if not TOKEN:
    print("Error: TOKEN environment variable not set!")
    exit(1)

# Диспетчер для обработки входящих сообщений
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start. Отправляет приветственное сообщение с кнопкой.
    
    Args:
        message (Message): Входящее сообщение с командой /start
    """

    builder = InlineKeyboardBuilder()
    # Добавляем кнопку
    builder.button(text="🎲 Get Random Picture", callback_data="random_picture")

    # Ответное приветственное сообщение
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(lambda c: c.data == "random_picture")
async def send_random_picture(callback_query: CallbackQuery):
    """
    Обработчик нажатия на inline-кнопку. Отправляет случайное изображение.
    
    Args:
        callback_query (CallbackQuery): Объект callback запроса от inline-кнопки
    """
    # Получаем путь к случайному изображению
    picture_path = get_random_picture()
    if picture_path:
        # Создание и отправка объекта файла
        photo = FSInputFile(picture_path)
        await callback_query.message.answer_photo(photo)
    else:
        await callback_query.message.answer("No pictures available!")

    # Подтверждение окончание обработку callback (убираем эффект загрузки на кнопке)
    await callback_query.answer()

async def main() -> None:
    """
    Основная асинхронная функция для запуска бота.
    """
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Настройка базовое логирование (уровень INFO, вывод в stdout)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Запуск основной функции в асинхронном цикле событий
    asyncio.run(main())
