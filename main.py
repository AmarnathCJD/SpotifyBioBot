import asyncio
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.sessions import StringSession
from telethon import events
from spotify import refresh_token, get_current_playing, meta
from os import getenv

import logging as log

log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app_logger = log.getLogger("app")

APP_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
STRING = getenv("STRING_SESSION")

if not APP_ID or not API_HASH:
    if not STRING:
        print("Enter your AppID and API Hash")
        APP_ID = int(input("Enter APP ID: "))
        API_HASH = input("Enter API HASH: ")

if not STRING:
    client = TelegramClient('anon', APP_ID, API_HASH, base_logger=app_logger)
else:
    client = TelegramClient(StringSession(STRING), APP_ID,
                            API_HASH, base_logger=app_logger)

app_logger.info("<- Starting Spotify Telegram Bot ->")

DEFAULT_BIO = getenv("DEFAULT_BIO", "~")


@client.on(events.NewMessage(pattern='.curr', outgoing=True))
async def handler(event):
    await get_current_playing()
    await event.edit(meta["CURRENT_TRACK_TITLE"])


async def main():
    await refresh_token()
    await client.start()
    app_logger.info("<- Telegram client started ->")
    while True:
        prev = meta["CURRENT_TRACK_TITLE"]
        await get_current_playing()
        curr = meta["CURRENT_TRACK_TITLE"]
        if prev != curr and curr:
            try:
                new_bio = "Listening 🎧 " + meta["CURRENT_TRACK_TITLE"]
                if len(new_bio) > 96:
                    new_bio = new_bio[:96]

                await client(UpdateProfileRequest(about="Listening 🎧 " + meta["CURRENT_TRACK_TITLE"]))
            except Exception as e:
                app_logger.error(f"Error updating bio: {e}")
            app_logger.info(f"Updated bio to: Listening 🎧 {meta['CURRENT_TRACK_TITLE']}")
            prev = curr
        elif not curr:
            await client(UpdateProfileRequest(about=DEFAULT_BIO))
            app_logger.info("Updated bio to default.")
        await asyncio.sleep(30)

asyncio.run(main())
