# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import arq, db
from Lib import convert_seconds, generate_cover, download_and_transcode_song, pause_skip_watcher
import asyncio, os

async def saavn(requested_by, query, message):
    mesaj = await message.reply_text(f"**JioSaavn'da `{query}` aranıyor.**", quote=False)
    songs = await arq.saavn(query)

    if not songs.ok:
        return await mesaj.edit(songs.result)

    songs    = songs.result
    sname    = songs[0].song
    slink    = songs[0].media_url
    ssingers = songs[0].singers
    chat_id  = message.chat.id

    global db
    db[chat_id]["currently"] = {
        "artist": ssingers[0] if type(ssingers) == list else ssingers,
        "song": sname,
        "query": query,
    }

    sthumb = songs[0].image
    sduration = songs[0].duration
    sduration_converted = convert_seconds(int(sduration))

    await mesaj.edit("**İndirme ve Kod Dönüştürme.**")
    cover, _ = await asyncio.gather(
        generate_cover(requested_by, sname, ssingers, sduration_converted, sthumb, chat_id,),
        download_and_transcode_song(slink, chat_id),
    )

    await mesaj.delete()

    caption = (
        f"🏷 **Başlık:** {sname[:45]}\n⏳ **Süre:** {sduration_converted}\n"
        + f"🎧 **İsteyen:** {message.from_user.mention}\n📡 **Platform:** JioSaavn"
    )
    mesaj = await message.reply_photo(
        photo=cover,
        caption=caption,
    )

    os.remove(cover)
    duration = int(sduration)

    await pause_skip_watcher(mesaj, duration, chat_id)
    await mesaj.delete()