# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db
from pyrogram import Client, filters

from config import YETKILI

@Client.on_message(filters.command("leavevc") & ~filters.private)
async def leavevc(client, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id in db and "call" in db[chat_id]:
        vc = db[chat_id]["call"]
        del db[chat_id]["call"]
        await vc.leave_current_group_call()
        await vc.stop()

    await message.reply_text("**Sesli Sohbetten Ayrıldı**", quote=False)