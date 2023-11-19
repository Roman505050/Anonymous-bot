from aiogram import Bot, F, Router
from aiogram.types import Message

from database import DataBase

router = Router()


@router.message(F.text)
async def synchronizer_for_text(message:Message,bot:Bot, db: DataBase):
    audit_user = await db.user_id_exists(message.from_user.id)
    if audit_user == True:
        send_user = await db.get(message.from_user.id)
        if send_user.chat_with is not None:
           text = message.text
           await bot.send_message(send_user.chat_with, text=text)

@router.message(F.photo)
async def synchronizer_for_text(message:Message,bot:Bot, db: DataBase):
    audit_user = await db.user_id_exists(message.from_user.id)
    if audit_user == True:
        send_user = await db.get(message.from_user.id)
        if send_user.chat_with is not None:
           photo = message.photo[-1].file_id
           text = message.caption
           await bot.send_photo(send_user.chat_with, photo=photo, caption= text)

@router.message(F.video)
async def synchronizer_for_text(message:Message,bot:Bot, db: DataBase):
    audit_user = await db.user_id_exists(message.from_user.id)
    if audit_user == True:
        send_user = await db.get(message.from_user.id)
        if send_user.chat_with is not None:
           photo = message.video.file_id
           text = message.caption
           await bot.send_video(send_user.chat_with, video=photo, caption= text)

@router.message(F.sticker)
async def synchronizer_for_text(message:Message,bot:Bot, db: DataBase):
    audit_user = await db.user_id_exists(message.from_user.id)
    if audit_user == True:
        send_user = await db.get(message.from_user.id)
        if send_user.chat_with is not None:
           photo = message.sticker.file_id
           await bot.send_sticker(send_user.chat_with, sticker=photo)
 
@router.message(F.animation)
async def synchronizer_for_text(message:Message,bot:Bot, db: DataBase):
    audit_user = await db.user_id_exists(message.from_user.id)
    if audit_user == True:
        send_user = await db.get(message.from_user.id)
        if send_user.chat_with is not None:
           animation = message.animation.file_id
           await bot.send_animation(send_user.chat_with, animation=animation)
 
