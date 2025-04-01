import asyncio
import logging
import os

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
            return

        await message.answer(f'Found "{title}". Downloading audio...')

        # Download the audio file
        path = await asyncio.to_thread(download_audio, message.text)
        print('------------------ THE PATH IS ' + path)

        # Check if the file exists
        if not os.path.exists(path):
            await message.answer("The audio file could not be found. Please try again.")
            return

        # Send the audio file
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=FSInputFile(path=path),
            caption=f'Here is your audio file: "{title}"',
            reply_to_message_id=message.message_id
        )
    else:
        await message.answer(f'Please send me a valid Youtube link.')


async def main():
    await disp.start_polling(bot)


def initialize():
    asyncio.run(main())