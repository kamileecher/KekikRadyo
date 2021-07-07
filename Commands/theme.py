# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import themes
from pyrogram import Client, filters

from config import YETKILI
from Lib import change_theme

@Client.on_message(filters.command("theme") & ~filters.private)
async def theme_func(_, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    usage = f"**Yanlış tema, aşağıdan birini seçin**\n{' | '.join(themes)}"
    if len(message.command) != 2:
        return await message.reply_text(usage)

    theme = message.text.split(None, 1)[1].strip()
    if theme not in themes:
        return await message.reply_text(usage)

    change_theme(theme, message.chat.id)
    await message.reply_text(f"**Tema Değiştirildi :** `{theme}`")