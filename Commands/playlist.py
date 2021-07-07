# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db
from pyrogram import Client, filters
from pyrogram.types import Message

from config import YETKILI

import asyncio
from Lib import start_queue

from Music import available_services

@Client.on_message(filters.command("playlist") & ~filters.private)
async def playlist(client: Client, message: Message, redirected=False):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if message.reply_to_message:
        raw_playlist = message.reply_to_message.text
    elif len(message.text) > 9:
        raw_playlist = message.text[10:]
    else:
        return await message.reply_text("**Kullanım:** /play ile aynı\n\n**Misal:**\n```/playlist Mary Jane - Mevsim Bahar\nFikri Karayel - Yol\nEypio - Dardayım```", quote=False)

    if chat_id not in db:
        db[chat_id] = {}

    if "call" not in db[chat_id]:
        return await message.reply_text("**Önce /joinvc !**")

    if "playlist" not in db[chat_id]:
        db[chat_id]["playlist"] = False

    if "running" in db[chat_id] and db[chat_id]["running"]:
        db[chat_id]["queue_breaker"] = 1

    db[chat_id]["playlist"] = True
    db[chat_id]["queue"] = asyncio.Queue()

    services = list(available_services.keys())

    for line in raw_playlist.split("\n"):
        if line.split()[0].lower() in services:
            service = line.split()[0].lower()
            song_name = " ".join(line.split()[1:])
        else:
            service = "youtube"
            song_name = line

        requested_by = message.from_user.first_name
        await db[chat_id]["queue"].put(
            {
                "service": available_services[service],
                "requested_by": requested_by,
                "query": song_name,
                "message": message,
            }
        )

    if not redirected:
        db[chat_id]["running"] = True
        await message.reply_text("**Oynatma Listesi Başladı.**")
        await start_queue(chat_id, message=message)