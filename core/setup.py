import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile, InputMediaAudio
from aiogram.filters import Command

from .config import TOKEN
from .download import get_video_title, download_audio


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
disp = Dispatcher()


@disp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f'Greetings! My purpose is to convert your Youtube video to an mp3 file. Please send me the link to the video.')


@disp.message()
async def message_handler(message: types.Message):
    if message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
        title = get_video_title(message.text)

        if title == 'Unknown Title':
            await message.answer(f'No such video was found on Youtube. Try again, please.')
            return 0

        await message.answer(f'Found "{title}".')
        
        path = download_audio(message.text)


        
    else:
        await message.answer(f'Please send me a valid Youtube link. {message.chat.id}')




async def main():
    await disp.start_polling(bot)


def initialize():
    asyncio.run(main())