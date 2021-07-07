# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import app, db
from Commands.playlist import playlist

# Queue handler
async def start_queue(chat_id, message=None):
    global db
    while True:
        db[chat_id]["call"].set_is_mute(True)
        if ("queue_breaker" in db[chat_id] and db[chat_id]["queue_breaker"] != 0 ):
            db[chat_id]["queue_breaker"] -= 1

            if db[chat_id]["queue_breaker"] == 0:
                del db[chat_id]["queue_breaker"]
            break

        if db[chat_id]["queue"].empty():
            if "playlist" not in db[chat_id] or not db[chat_id]["playlist"]:
                db[chat_id]["running"] = False
                db[chat_id]["call"].set_is_mute(False)
                break
            else:
                await playlist(app, message, redirected=True)

        data = await db[chat_id]["queue"].get()
        service = data["service"]
        await service(data["requested_by"], data["query"], data["message"])