# Spotify Library Tools

A small collection of Python scripts for managing and analyzing your Spotify Liked Songs library.

## Features

| Script | Description |
|---|---|
| `sync_spotify.py` | Syncs your Liked Songs to a public playlist (no duplicates) |
| `analyze_liked_songs.py` | In-depth analysis: top artists, genres, release years, duplicates |
| `list_all_artists.py` | Alphabetical list of all artists in your library with track counts |

## Requirements

- Python 3.9+
- A [Spotify Developer App](https://developer.spotify.com/dashboard) (free)
- `uv` (recommended) or `pip`

## Setup

### 1. Create a Spotify Developer App

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) and create a new app.
2. In the app settings, add `http://127.0.0.1:8888/callback` as a **Redirect URI**.
3. Copy your **Client ID** and **Client Secret**.

### 2. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIFY_PUBLIC_PLAYLIST_ID=your_playlist_id_here
```

> **Finding your playlist ID:** Open the playlist in Spotify, click *Share → Copy link*.
> The ID is the string after `/playlist/` and before `?`.

### 3. Install dependencies

**With `uv` (recommended):**

```bash
uv run sync_spotify.py
```

`uv` reads inline dependency metadata and installs everything automatically.

**With `pip`:**

```bash
pip install spotipy python-dotenv
python sync_spotify.py
```

### 4. First run — browser authorization

On the first run, your browser will open and ask you to authorize the app.
After confirming, you will be redirected to `127.0.0.1:8888/callback`.
Copy the full URL from the browser and paste it into the terminal when prompted.
A `.cache` file will be created locally to store the token for future runs.

## Usage

```bash
# Sync Liked Songs to your public playlist
uv run sync_spotify.py

# Analyze your library
uv run analyze_liked_songs.py

# List all artists alphabetically
uv run list_all_artists.py
```

## Project structure

```
spotify-library-tools/
├── config.py               # Shared auth and config helpers
├── sync_spotify.py
├── analyze_liked_songs.py
├── list_all_artists.py
├── .env                    # Your secrets — never commit this
├── .env.example            # Template for .env — safe to commit
├── .gitignore
└── README.md
```

## Security note

The `.env` file contains sensitive credentials and is excluded from version control via `.gitignore`.
Never commit your actual `CLIENT_SECRET` to a repository.
If you accidentally expose it, revoke it immediately in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
