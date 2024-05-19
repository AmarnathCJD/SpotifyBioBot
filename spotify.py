from aiohttp import ClientSession, ClientTimeout
from os import getenv
import base64
import dotenv
import time
import logging

spotify_logger = logging.getLogger("spotify")

dotenv.load_dotenv()

meta = {
    "LAST_UPDATED": time.time(),
    "IS_PLAYING": False,
    "CURRENT_TRACK_TITLE": None,
}

ACTIVE_ACCESS_TOKEN = None
EXPIRATION_TIME = None

UPDATE_INTERVAL = 10

CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = getenv("SPOTIFY_REFRESH_TOKEN")

BASE_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
}

async def refresh_token():
    spotify_logger.info("<- Refreshing token ->")
    async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        async with session.post(
            "https://accounts.spotify.com/api/token",
            headers=BASE_HEADERS,
            data={
                "grant_type": "refresh_token",
                "refresh_token": REFRESH_TOKEN,
                "client_id": CLIENT_ID,
            },
        ) as response:
            response = await response.json()
            global ACTIVE_ACCESS_TOKEN
            global EXPIRATION_TIME
            ACTIVE_ACCESS_TOKEN = response["access_token"]
            EXPIRATION_TIME = int(response["expires_in"]) + int(time.time())
    
    spotify_logger.info("<- Token refreshed ->")    

async def get_current_playing():
    async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        async with session.get(
            "https://api.spotify.com/v1/me/player/currently-playing",
            headers={
                "Authorization": f"Bearer {ACTIVE_ACCESS_TOKEN}",
            },
        ) as response:
            # if status code is 204, no content is playing
            if response.status == 204:
                meta["IS_PLAYING"] = False
                meta["CURRENT_TRACK_TITLE"] = None
                spotify_logger.info("Not currently playing.")
                return
            
            # if not 200, refresh token
            if response.status != 200:
                await refresh_token()
                return await get_current_playing()
            try:
                data = await response.json()
                if data["is_playing"]:
                    meta["IS_PLAYING"] = True
                    artists = [artist["name"] for artist in data["item"]["album"]["artists"]]
                    artists_fmt = ", ".join(artists)
                    artists_fmt = artists_fmt[:100]
                    meta["CURRENT_TRACK_TITLE"] = data["item"]["name"] + " (" + artists_fmt + ")"
                    spotify_logger.info(f"Currently playing: {meta['CURRENT_TRACK_TITLE']}")
                else:
                    meta["IS_PLAYING"] = False
                    meta["CURRENT_TRACK_TITLE"] = None
                    spotify_logger.info("Not currently playing.")
            except:
                meta["IS_PLAYING"] = False
                meta["CURRENT_TRACK_TITLE"] = None
                spotify_logger.error("Error parsing JSON response/Not currently playing.")
                
                