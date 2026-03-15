# /// script
# dependencies = [
#   "spotipy",
#   "python-dotenv",
# ]
# ///

from config import get_spotify_client, get_playlist_id


def main():
    sp = get_spotify_client("user-library-read playlist-modify-public")
    playlist_id = get_playlist_id()

    # --- Step 1: Fetch all Liked Songs ---
    print("--- Fetching your Liked Songs ---")
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)
    liked_songs.extend([item['track']['id'] for item in results['items']])

    while results['next']:
        results = sp.next(results)
        liked_songs.extend([item['track']['id'] for item in results['items']])

    print(f"Found {len(liked_songs)} tracks in your library.")

    # --- Step 2: Fetch tracks already in the public playlist ---
    print("--- Checking the public playlist ---")
    playlist_results = sp.playlist_items(playlist_id)
    existing_ids = [item['track']['id'] for item in playlist_results['items']]

    while playlist_results['next']:
        playlist_results = sp.next(playlist_results)
        existing_ids.extend([item['track']['id'] for item in playlist_results['items']])

    # --- Step 3: Filter — only add tracks not already in the playlist ---
    new_tracks = [t_id for t_id in liked_songs if t_id not in existing_ids]

    if not new_tracks:
        print("Everything is up to date. No new tracks to add.")
        return

    # --- Step 4: Add new tracks (Spotify API accepts max 100 per request) ---
    print(f"Adding {len(new_tracks)} new tracks...")
    for i in range(0, len(new_tracks), 100):
        sp.playlist_add_items(playlist_id, new_tracks[i:i + 100])

    print("Done! Your public playlist is now synchronized.")


if __name__ == "__main__":
    main()
