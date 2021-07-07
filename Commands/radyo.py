# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters

from config import YETKILI, DEFAULT_SERVICE
from Music import available_services

@Client.on_message(filters.command("radyo") & ~filters.private)
async def help(client, message):
    if str(message.from_user.id) not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    await message.reply_text(f"""**Sesli Sohbette Müzik Çalabilirim**

**/skip** __Çalmakta olan Müziği Atla.__
**/play** __Hizmet Veya Varsayılan (Hizmetler: {'/'.join(list(available_services.keys()))}, Varsayılan: {DEFAULT_SERVICE}) Şarkı Adı | Sese Yanıt Ver__
**/joinvc** __Sesli Sohbete Katılın.__
**/leavevc** __Sesli Sohbetten Çıkın.__
**/listvc** __Katılan Sesli Sohbetleri Listeleyin.__
**/volume [1-200]** __Sesi Ayarla.__
**/pause** __Müziği Duraklat.__
**/resume** __Müziği Sürdür.__
**/dur** __Müziği Durdurun.__
**/basla** __Son Müziği Çal.__
**/replay** __Mevcut Müziği Tekrar Çal.__
**/theme** __Şu Anda Yürütülen Temayı Değiştir.__
**/kuyruk** __Sıra Listesini gösterir. `format` komutu ile gönderirseniz, çalma listesi formatında alırsınız.__
**/temizle** __Sıra Listesini ve Çalma Listesini Siler.__
**/playlist** __Oynatma Listesini Oynatmaya Başlayın.__
**/lyric** __Şu Anda Çalan Müzik Sözlerini Alın. Yanlış şarkı sözleri almak mümkündür. Gerçeklik olasılığını artırmak için deezer veya saavn kullanın__""", quote=False)