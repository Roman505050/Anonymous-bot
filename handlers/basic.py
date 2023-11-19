from aiogram import Bot
from aiogram.types import Message

import os
from dotenv import load_dotenv

load_dotenv()
ADMIN = os.getenv('ADMIN')

async def start_bot(bot:Bot):
    await bot.send_message(ADMIN,'Бот запущений!')

async def stop_bot(bot:Bot):
    await bot.send_message(ADMIN,'Бот зупинився!')
