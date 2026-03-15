import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load variables from .env file if it exists.
# In production, environment variables can be set directly in the OS instead.
load_dotenv()


def _get_required_env(key: str) -> str:
    """Load a required environment variable. Exit with a clear error message if missing."""
    value = os.getenv(key)
    if not value:
        print(f"❌ Missing required environment variable: {key}")
        print(f"   Copy .env.example to .env and fill in your values.")
        sys.exit(1)
    return value


def get_spotify_client(scope: str) -> spotipy.Spotify:
    """Return an authorized Spotify client for the given scope."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=_get_required_env("SPOTIPY_CLIENT_ID"),
        client_secret=_get_required_env("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=_get_required_env("SPOTIPY_REDIRECT_URI"),
        scope=scope
    ))


def get_playlist_id() -> str:
    """Return the target public playlist ID from environment variables."""
    return _get_required_env("SPOTIFY_PUBLIC_PLAYLIST_ID")
