# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db
from pyrogram import Client, filters

from config import YETKILI, DEFAULT_SERVICE

from os import popen
from pytgcalls import GroupCall
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.raw.types import InputPeerChannel
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired

@Client.on_message(filters.command("joinvc") & ~filters.private)
async def joinvc(client, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        db[chat_id] = {}

    if "call" in db[chat_id]:
        return await message.reply_text("**Bot Zaten Sesli Sohbette**")

    popen(f"cp etc/sample_input.raw input{chat_id}.raw")

    vc = GroupCall(client, f"input{chat_id}.raw")

    db[chat_id]["call"] = vc

    try:
        await db[chat_id]["call"].start(chat_id)
    except Exception:
        peer = await client.resolve_peer(chat_id)
        print(peer)
        start_voice_chat = CreateGroupCall(
            peer        = InputPeerChannel(
                channel_id  = peer.channel_id,
                access_hash = peer.access_hash,
            ),
            random_id   = client.rnd_id() // 9000000000,
        )
        try:
            await client.send(start_voice_chat)
            await db[chat_id]["call"].start(chat_id)
        except ChatAdminRequired:
            del db[chat_id]["call"]
            return await message.reply_text("Mesaj silme ve sesli sohbet yönetme izniyle beni yönetici yap")

    await message.reply_text(f"**Sesli Sohbet'e katıldı.**\n\n__Varsayılan Servis :__ `{DEFAULT_SERVICE}`")