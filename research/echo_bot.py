import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# Load .env file from the project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Get Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Validate token
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not found. Please check your .env file."
    )

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    Handle /start and /help commands.
    """
    await message.reply(
        "👋 Hi!\n"
        "I'm KuttuBot!\n"
        "Powered by AI DEV Panto "
    )


@dp.message_handler(commands=["clear"])
async def clear_context(message: types.Message):
    """
    Dummy clear command.
    """
    await message.reply("✅ Conversation context cleared.")


@dp.message_handler()
async def echo(message: types.Message):
    """
    Echo every user message.
    """
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)