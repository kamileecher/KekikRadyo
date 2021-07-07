# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db
from pyrogram import Client, filters

from config import YETKILI

@Client.on_message(filters.command("listvc") & ~filters.private)
async def list_vc(client, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    if len(db) == 0:
        return await message.reply_text("Aktif sesli sohbet yok..")

    chats = [int(chat) for chat in db if "call" in db[chat]]

    text = ""
    for count, chat_id in enumerate(chats, 1):
        try:
            chat = await client.get_chat(chat_id)
            chat_title = chat.title
        except Exception:
            chat_title = "Private"

        text += f"**{count}.** [`{chat_id}`]  **{chat_title}**\n"

    if not text:
        return await message.reply_text("Aktif sesli sohbet yok..")

    await message.reply_text(text)