## # Spotify Bio Bot for Telegram 🎵🤖

Automatically update your Telegram bio to reflect the song you're currently playing on Spotify. This bot synchronizes your Spotify activity with your Telegram bio, ensuring your friends always know what you're vibing to!

## Features ✨

- **Real-time Bio Updates**: Syncs your Telegram bio with your current Spotify track.
- **Customizable Default Bio**: Reverts to a default bio when not listening to music.
- **Easy Setup**: Simple environment variable configuration.
- **Secure Authentication**: Uses OAuth to securely connect to your Spotify account.
- **Lightweight**: Powered by the Aiohttp and Telethon libraries.
- **Refresh Token Support**: Automatically refreshes your Spotify access token every hour.

## Getting Started 🚀

### Prerequisites 📋

- Python 3.9 or higher
- A **[Spotify Developer Account](https://developer.spotify.com/dashboard/applications)**


### Installation 🛠️

1. **Clone the repository**:
    ```bash
    git clone https://github.com/AmarnathCJD/spotifybiobot.git
    cd spotifybiobot
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration ⚙️

1. **Set up your environment variables**:
    Create a `.env` file in the root of your project and fill it with the following:

    ```dotenv
    SPOTIFY_CLIENT_ID=your-spotify-client-id
    SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
    SPOTIFY_REFRESH_TOKEN=your-spotify-refresh-token
    STRING_SESSION=your-string-session
    API_ID=tg-api-id
    API_HASH=tg-api-hash
    DEFAULT_BIO=~
    ```

2. **Obtain Spotify tokens**:
    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create a new app.
    - Set `http://localhost:3000` as the Redirect URI in the app settings.
    - Copy the `Client ID` and `Client Secret` to your `.env` file.
    - Use the `auth_token.py` script to generate your refresh token:
      ```bash
      python auth_token.py
      ```
    - Copy the refresh token to your `.env` file.

### Running the Bot ▶️

Start the bot by running:
```bash
python main.py
```

## Contributing 🤝

Contributions are welcome! Feel free to open an issue or submit a pull request if you have any improvements to suggest.

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

