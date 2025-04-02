import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import FSInputFile
from aiogram.filters import Command

from .config import TOKEN
from .download import get_video_title, download_audio


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
disp = Dispatcher()
router = Router(name=__name__)


@disp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f'Greetings!\n\nMy purpose is to convert your Youtube video to an audio file.\n\nPlease send me the link to the video.')


@disp.message()
async def message_handler(message: types.Message):
    # checking whether the link is a Youtube link
    if message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
        title = get_video_title(message.text)

        # video doesn't exist on Youtube
        if title == 'Unknown Title':
            await message.answer(f'No such video was found on Youtube. Try again, please.')
            return 0

        await message.answer(f'Found requested video. Downloading audio...')

        # Download the audio file
        path = await asyncio.to_thread(download_audio, message.text)

        # Send the audio file
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=FSInputFile(path=path, filename=title),
            reply_to_message_id=message.message_id
        )

        # Remove the audio file after sending
        os.remove(path)
    else:
        await message.answer(f'Please send me a valid Youtube link.')


async def main():
    await disp.start_polling(bot)


def initialize():
    asyncio.run(main())