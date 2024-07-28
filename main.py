import os
import random
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.filters.command import Command, CommandStart

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.reply("Progress started...")
    asyncio.create_task(do_some_long_task(message.chat.id))


async def do_some_long_task(chat_id):
    progress_message = await bot.send_message(chat_id, "Progress: [0%]")
    progress = 0

    while progress < 100:
        await asyncio.sleep(1)  # Simulate a long task
        progress += random.uniform(10, 30)
        if progress > 100:
            progress = 100

        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=progress_message.message_id,
                text=f"Progress: [{int(progress)}%]"
            )
        except Exception as e:
            print(f"Error updating message: {e}")

    await bot.send_message(chat_id, "Completed")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
