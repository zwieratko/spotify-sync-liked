import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
from dotenv import load_dotenv

# Load variables from .env file if it exists.
# In production, environment variables can be set directly in the OS instead.
load_dotenv()


def _get_required_env(key: str) -> str:
    """Load a required environment variable. Exit with a clear error message if missing."""
    value = os.getenv(key)
    if not value:
        print(f"❌ Missing required environment variable: {key}")
        print("   Copy .env.example to .env and fill in your values.")
        sys.exit(1)
    return value


def _build_auth_manager(scope: str) -> SpotifyOAuth:
    """Create a SpotifyOAuth manager with credentials from environment variables."""
    return SpotifyOAuth(
        client_id=_get_required_env("SPOTIPY_CLIENT_ID"),
        client_secret=_get_required_env("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=_get_required_env("SPOTIPY_REDIRECT_URI"),
        scope=scope,
    )


def get_spotify_client(scope: str) -> spotipy.Spotify:
    """Return an authorized Spotify client for the given scope.

    Handles Spotify's 6-month refresh token expiration policy: if the cached
    refresh token has expired (invalid_grant error), the stale cache is deleted
    automatically and the user is prompted to re-authorize within the same run.
    """
    auth_manager = _build_auth_manager(scope)

    # Eagerly validate any cached token so we can detect an expired refresh
    # token before the first real API call is made.
    try:
        cached_token = auth_manager.get_cached_token()
        if cached_token:
            auth_manager.validate_token(cached_token)
    except SpotifyOauthError as exc:
        if "invalid_grant" in str(exc).lower():
            cache_path = auth_manager.cache_handler.cache_path
            print(
                "⚠️  Your Spotify authorization has expired (6-month refresh token limit)."
            )
            print("   Clearing expired credentials and starting re-authorization...")
            if os.path.exists(cache_path):
                os.remove(cache_path)
            # Rebuild with a clean state so the OAuth browser flow is triggered
            # automatically on the first API call.
            auth_manager = _build_auth_manager(scope)
        else:
            raise

    return spotipy.Spotify(auth_manager=auth_manager)


def get_playlist_id() -> str:
    """Return the target public playlist ID from environment variables."""
    return _get_required_env("SPOTIFY_PUBLIC_PLAYLIST_ID")
