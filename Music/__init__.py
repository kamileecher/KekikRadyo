# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Music.get_telegram import telegram
from Music.get_youtube  import youtube
from Music.get_deezer   import deezer
from Music.get_saavn    import saavn

available_services = {"telegram":telegram, "youtube":youtube, "deezer":deezer, "saavn":saavn}