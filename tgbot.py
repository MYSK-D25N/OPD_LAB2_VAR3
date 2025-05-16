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

PICTURES_DIRECTORY = 'pictures/'

def get_random_picture():
    picture_files = [f for f in listdir(PICTURES_DIRECTORY) if path.isfile(path.join(PICTURES_DIRECTORY, f))]
    
    if not picture_files:
        return None
    
    random_picture = random.choice(picture_files)
    return path.join(PICTURES_DIRECTORY, random_picture)

TOKEN = getenv("TOKEN")
if not TOKEN:
    print("Error: TOKEN environment variable not set!")
    exit(1)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎲 Get Random Picture", callback_data="random_picture")
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(lambda c: c.data == "random_picture")
async def send_random_picture(callback_query: CallbackQuery):
    picture_path = get_random_picture()
    if picture_path:
        photo = FSInputFile(picture_path)
        await callback_query.message.answer_photo(photo)
    else:
        await callback_query.message.answer("No pictures available!")
    await callback_query.answer()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
