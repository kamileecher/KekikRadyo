# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db
from pyrogram import Client, filters

from config import YETKILI
import asyncio

@Client.on_message(filters.command("temizle") & ~filters.private)
async def clear_queue(client, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "call" not in db[chat_id]:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if ("queue" not in db[chat_id] or db[chat_id]["queue"].empty()) and ("playlist" not in db[chat_id] or not db[chat_id]["playlist"]):
        return await message.reply_text("**Kuyruk Zaten Boş**")

    db[chat_id]["playlist"] = False
    db[chat_id]["queue"]    = asyncio.Queue()

    await message.reply_text("**Kuyruk Başarıyla Temizlendi**", quote=False)