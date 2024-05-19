import asyncio
from aiohttp import ClientSession, ClientTimeout
import base64

# This script is used to authenticate with the Spotify API.


async def authenticate():
    print("Welcome to the Spotify authentication process.")
    print("Please enter your client ID, client secret, and redirect URI.")
    print("https://developer.spotify.com/")

    CLIENT_ID = input("Enter your client ID: ")
    CLIENT_SECRET = input("Enter your client secret: ")
    REDIRECT_URI = input("Enter your redirect URI (skip: http://localhost:3000): ")
    
    if not REDIRECT_URI:
        REDIRECT_URI = "http://localhost:3000"

    base64_encoded = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        async with session.post(
            "https://accounts.spotify.com/authorize",
            params={
                "client_id": CLIENT_ID,
                "response_type": "code",
                "redirect_uri": REDIRECT_URI,
                "scope": "user-read-currently-playing",
            },
        ) as response:
            print("Visit the following URL to authenticate:")
            print(response.url)
            print("After authenticating, paste the code from the URL here.")
            print("Example: http://localhost:3000?code=YOUR_CODE")
            print("copy the YOUR_CODE part.")
            code = input("Enter the code: ")

        async with session.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {base64_encoded}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
        ) as response:
            response = await response.json()
            print("Refresh Token:", response["refresh_token"])
            print("\n\nCopy the refresh token and paste it in your environment variables.")

asyncio.run(authenticate())
