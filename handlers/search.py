from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from database import DataBase
import asyncio

import random

router = Router()


@router.message(CommandStart())
async def start(message: Message, db: DataBase):
    audit = await db.get(message.from_user.id)
    if audit is None:
        pattern = {
            'user_id': message.from_user.id,
            'is_looking': False,
            'chat_with': None
            }
        await db.insert(**pattern)
        await message.answer("Привіт я Тихий незнайомець! Створений для анонімного спілкування. Для того щоб розпочати анонімне спілкування використовуйте команду /search")
    else:
        await message.answer("Привіт я Тихий незнайомець! Створений для анонімного спілкування. Для того щоб розпочати анонімне спілкування використовуйте команду /search")

@router.message(Command('search'))
async def start_search(message: Message,bot:Bot, db: DataBase):
    audit_user = await db.user_id_exists(message.from_user.id)
    if audit_user is False:
        await message.answer("Вийшла якась помилка, я не можу вас згадати. Використай команду /start для індифікації")
        return None
    else:
        audit = await db.get(message.from_user.id)
        audit_chat = audit.chat_with
        if audit_chat is None and audit.is_looking == False:
            await db.user_update(message.from_user.id, is_looking=True)
            
            await message.answer("Чудово! Я розпочав пошук тобі пари для спілкування. "
                                 "Для скасування пошуку використовуй /stop")        
            async def find_companion():
                users_looking = await db.get_users_looking_for_chat()
                while len(users_looking) >= 1:
                    # Отримання інформації про користувачів, які шукають співрозмовників
                    users_looking = await db.get_users_looking_for_chat()
                    print(users_looking)        
                    # Вибір випадкового користувача для спілкування
                    if users_looking and len(users_looking) > 1:
                        
                        users_looking1 = users_looking.remove(message.from_user.id)
                        print(users_looking)
                        selected_user = random.choice(users_looking)
                        await db.user_update(user_id=selected_user, is_looking=False, chat_with=message.from_user.id)  # Позначення користувача як зайнятого
                        await db.user_update(message.from_user.id, is_looking=False, chat_with=selected_user)  # Позначення поточного користувача як зайнятого
                        await message.answer(f"Я знайшов тобі співрозмовника {selected_user}"
                                             "Для скасування чату використовуй /stopchat")
                        await bot.send_message(selected_user,f"Я знайшов тобі співрозмовника {message.from_user.id}"
                                             "Для скасування чату використовуй /stopchat")
                        break
                    else:
                        # Очікування і повторення пошуку через 3 секунди
                        await asyncio.sleep(3)        
            # Запуск асинхронної задачі для пошуку співрозмовника
            asyncio.create_task(find_companion())
        else:
            await message.answer("ОШИБКА. Ви пробуєте знайти співрозмовника в той момент, коли вже почали шукати або маєте поточний чат з співрозмовником.\n\nВикористовуйте наступні команди:\n/stop - скасування пошуку\n/stopchat - скасування поточного чату, якщо такий є") 

@router.message(Command('stop'))
async def stop_search(message: Message,db:DataBase):
    audit = await db.get(message.from_user.id)
    if audit.is_looking == True:
        await db.user_update(message.from_user.id, is_looking=False)
        await message.answer("Ти відмінив пошук. Для початку нового пошуку використовуй /search")
    else:
        await message.answer('ОШИБКА. Ви навіть не розчали пошук. Щоб розпочати використайте /search')

@router.message(Command('stopchat'))
async def stop_chat(message:Message,bot:Bot,db:DataBase):
    chat_1 = await db.get(message.from_user.id)
    chat_1_id = chat_1.chat_with
    if chat_1_id is not None:
        second_user =await db.get(message.from_user.id)
        second_user_id = second_user.chat_with
        await message.answer("УВАГА! Чат призупинено вами!")
        await bot.send_message(second_user_id,"УВАГА! Чат призупинено співрозмовником!")
        await db.user_update(user_id=second_user_id, is_looking=False, chat_with=None)
        await db.user_update(message.from_user.id, is_looking=False, chat_with=None)
    else:
        await message.answer("ОШИБКА. Можливо ви немаєте поточного чату!")