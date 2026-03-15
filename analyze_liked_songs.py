# /// script
# dependencies = [
#   "spotipy",
#   "python-dotenv",
# ]
# ///

from collections import Counter
from datetime import datetime

from config import get_spotify_client


def main():
    sp = get_spotify_client("user-library-read")

    print("🚀 Starting in-depth analysis of your Liked Songs...\n")

    # --- Fetch all tracks (pagination handled) ---
    all_items = []
    results = sp.current_user_saved_tracks(limit=50)
    all_items.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        all_items.extend(results['items'])

    total_count = len(all_items)
    print(f"✅ Loaded {total_count} tracks in total.")

    # --- 1. LAST 5 ADDED TRACKS ---
    print("\n📅 LAST 5 ADDITIONS:")
    for item in all_items[:5]:
        track = item['track']
        added_at = datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ')
        print(f"  • {track['name']} - {track['artists'][0]['name']} ({added_at.strftime('%d.%m.%Y')})")

    # --- 2. TOP ARTISTS ---
    artist_names = [item['track']['artists'][0]['name'] for item in all_items]
    top_artists = Counter(artist_names).most_common(5)
    print("\n🏆 YOUR TOP 5 ARTISTS:")
    for artist, count in top_artists:
        print(f"  • {artist}: {count} tracks")

    # --- 3. DUPLICATE CHECK ---
    # Logic: a track is considered a duplicate if it shares the same title and primary artist.
    seen_tracks = {}  # (title, artist) -> count
    duplicates = []

    for item in all_items:
        name = item['track']['name'].lower().strip()
        artist = item['track']['artists'][0]['name'].lower().strip()
        key = (name, artist)

        if key in seen_tracks:
            if key not in duplicates:
                duplicates.append(key)
            seen_tracks[key] += 1
        else:
            seen_tracks[key] = 1

    print("\n🔍 DUPLICATE CHECK:")
    if duplicates:
        print(f"  ⚠️  Warning: Found {len(duplicates)} possible duplicate(s):")
        for name, artist in duplicates:
            print(f"  - {name.title()} ({artist.title()}) appears {seen_tracks[(name, artist)]}x")
    else:
        print("  ✅ Great! No duplicates found in your Liked Songs.")

    # --- 4. RELEASE YEAR ANALYSIS ---
    years = [item['track']['album']['release_date'].split('-')[0] for item in all_items]
    top_years = Counter(years).most_common(3)
    print("\n⏳ STRONGEST YEARS IN YOUR LIBRARY:")
    for year, count in top_years:
        print(f"  • {year}: {count} tracks")

    # --- 5. GENRE ANALYSIS ---
    # Artist details must be fetched separately to access genre data.
    artist_ids = list(set([item['track']['artists'][0]['id'] for item in all_items]))
    all_genres = []

    # Spotify API accepts a maximum of 50 artists per request.
    for i in range(0, len(artist_ids), 50):
        artists_data = sp.artists(artist_ids[i:i + 50])['artists']
        for artist in artists_data:
            all_genres.extend(artist['genres'])

    if all_genres:
        top_genres = Counter(all_genres).most_common(5)
        print("\n🎸 YOUR TOP GENRES:")
        for genre, count in top_genres:
            print(f"  • {genre.title()}: {count}x")

    print("\n--- Analysis complete ---")


if __name__ == "__main__":
    main()
