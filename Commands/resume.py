# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db
from pyrogram import Client, filters

from config import YETKILI

@Client.on_message(filters.command("resume") & ~filters.private)
async def resume_song(client, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "call" not in db[chat_id]:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "paused" in db[chat_id] and db[chat_id]["paused"] == False:
        return await message.reply_text("**Zaten Oynuyor**")

    db[chat_id]["paused"] = False

    vc = db[chat_id]["call"]
    vc.resume_playout()

    await message.reply_text("**Sürdürüldü, Müziği Duraklatmak İçin `/pause` Gönderin.**", quote=False)