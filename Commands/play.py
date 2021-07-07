# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db
from pyrogram import Client, filters

from config import YETKILI
from Lib import get_default_service, start_queue
import asyncio, traceback

from Music import available_services

@Client.on_message(filters.command("play") & ~filters.private)
async def play_song(client, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    try:
        if len(message.command) < 2 and (not message.reply_to_message or not message.reply_to_message.audio):
            return await message.reply_text("**Kullanım:**\n\n`/play Eypio - Dardayım`", quote=False)

        if chat_id not in db:
            db[chat_id] = {}

        if "call" not in db[chat_id]:
            return await message.reply_text("**Önce /joinvc !**")

        if message.reply_to_message:
            if not message.reply_to_message.audio:
                return await message.reply_text("**Ses dosyasına cevap verin veya alıntılamadan komut verin!**")

            service   = "telegram"
            song_name = message.reply_to_message.audio.title
        else:
            text = message.text.split("\n")[0]
            text = text.split(None, 2)[1:]
            service = text[0].lower()
            services = list(available_services.keys())
            if service in services:
                song_name = text[1]
            else:
                service   = get_default_service()
                song_name = " ".join(text)

        requested_by = message.from_user.first_name

        if chat_id not in db:
            db[chat_id] = {}

        if "queue" not in db[chat_id]:
            db[chat_id]["queue"] = asyncio.Queue()

        if not db[chat_id]["queue"].empty() or ("running" in db[chat_id] and db[chat_id]["running"]):
            await message.reply_text(f"`{song_name}` __Kuyruğa Eklendi.__", quote=False, disable_web_page_preview=True)

        await db[chat_id]["queue"].put(
            {
                "service"       : available_services[service],
                "requested_by"  : requested_by,
                "query"         : song_name,
                "message"       : message,
            }
        )

        if "running" not in db[chat_id]:
            db[chat_id]["running"] = False

        if not db[chat_id]["running"]:
            db[chat_id]["running"] = True
            await start_queue(chat_id)

    except Exception as e:
        await message.reply_text(str(e), quote=False)
        e = traceback.format_exc()
        print(e)