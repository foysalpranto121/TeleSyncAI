import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# Load .env file
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Get Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not found. Please check your .env file."
    )

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start", "help"))
async def send_welcome(message: Message):
    """
    Handle /start and /help commands.
    """
    await message.answer(
        "👋 Hi!\n"
        "I'm KuttuBot!\n"
        "Powered by AI DEV Panto"
    )


@dp.message(Command("clear"))
async def clear_context(message: Message):
    """
    Clear conversation context.
    """
    await message.answer("✅ Conversation context cleared.")


@dp.message()
async def echo(message: Message):
    """
    Echo every user message.
    """
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())