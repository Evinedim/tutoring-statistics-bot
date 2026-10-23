import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import settings


dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

async def main():
    bot = Bot(token=settings.bot_token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())