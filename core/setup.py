import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from .config import TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
disp = Dispatcher()


@disp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f'Greetings! My purpose is to convert your Youtube video to an mp3 file. Please send the link to the video :)')


async def main():
    await disp.start_polling(bot)


def initialize():
    asyncio.run(main())