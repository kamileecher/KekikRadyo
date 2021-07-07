# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram.types import Message
from Core import arq, db
from Lib import convert_seconds, generate_cover, download_and_transcode_song, pause_skip_watcher
import asyncio, os

async def deezer(requested_by, query, message: Message):
    mesaj = await message.reply_text(f"**Deezer'da `{query}` aranıyor.**", quote=False)
    songs = await arq.deezer(query, 1)

    if not songs.ok:
        return await mesaj.edit(songs.result)

    songs     = songs.result
    title     = songs[0].title
    duration  = convert_seconds(int(songs[0].duration))
    thumbnail = songs[0].thumbnail
    artist    = songs[0].artist
    chat_id   = message.chat.id

    global db
    db[chat_id]["currently"] = {
        "artist": artist,
        "song": title,
        "query": query,
    }

    url = songs[0].url

    await mesaj.edit("**İndirme ve Kod Dönüştürme.**")
    cover, _ = await asyncio.gather(
        generate_cover(requested_by, title, artist, duration, thumbnail, chat_id),
        download_and_transcode_song(url, chat_id),
    )
    await mesaj.delete()

    caption = (
        f"🏷 **Başlık:** [{title[:45]}]({url})\n⏳ **Süre:** {duration}\n"
        + f"🎧 **İsteyen:** {message.from_user.mention}\n📡 **Platform:** Deezer"
    )
    mesaj = await message.reply_photo(
        photo=cover,
        caption=caption,
    )
    os.remove(cover)

    duration = int(songs[0]["duration"])

    await pause_skip_watcher(mesaj, duration, chat_id)
    await mesaj.delete()