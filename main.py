import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart,Command
from aiogram.types import ReplyKeyboardRemove,Message

from handlers.synchronizer import router
from handlers.search import router
from handlers.basic import start_bot,stop_bot
from database import DataBase

import handlers

load_dotenv()
TOKEN = os.getenv('TOKEN')

async def start():
    bot = Bot(token=TOKEN,parse_mode='HTML')
    dp = Dispatcher()
    db = DataBase()

    dp.startup.register(db.create)

    dp.include_routers(
        handlers.search.router,
        handlers.synchronizer.router
    )

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot,
                           db=db
                           )
    