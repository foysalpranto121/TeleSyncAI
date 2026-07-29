import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from openai import AsyncOpenAI

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not found in .env")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")

MODEL_NAME = "gpt-4.1-mini"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# ----------------------------------------------------
# Conversation Memory
# ----------------------------------------------------

conversation_history = {}


def clear_history(chat_id: int):
    conversation_history[chat_id] = []


# ----------------------------------------------------
# Commands
# ----------------------------------------------------


@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "👋 **Welcome!**\n\n"
        "I'm **KuttuBot**, your AI assistant.\n\n"
        "Ask me anything about programming, writing, studying, or general knowledge.\n\n"
        "Type /help to see available commands.",
        parse_mode="Markdown",
    )


@dp.message(Command("help"))
async def help_command(message: Message):

    text = """
🤖 **Available Commands**

/start - Start the bot

/help - Show help

/clear - Clear conversation history

Simply send me any message and I'll reply using OpenAI.
"""

    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("clear"))
async def clear(message: Message):

    clear_history(message.chat.id)

    await message.answer("✅ Conversation history cleared.")


# ----------------------------------------------------
# Chat
# ----------------------------------------------------


@dp.message()
async def chat(message: Message):

    chat_id = message.chat.id

    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    conversation_history[chat_id].append(
        {
            "role": "user",
            "content": message.text,
        }
    )

    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    try:

        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are KuttuBot, a friendly, helpful AI assistant. "
                        "Answer clearly, accurately, and concisely."
                    ),
                },
                *conversation_history[chat_id],
            ],
        )

        answer = response.choices[0].message.content

        conversation_history[chat_id].append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        await message.answer(answer)

    except Exception as e:

        logger.exception(e)

        await message.answer(
            "❌ Sorry, something went wrong while contacting OpenAI."
        )


# ----------------------------------------------------
# Main
# ----------------------------------------------------


async def main():

    logger.info("🤖 Bot started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())