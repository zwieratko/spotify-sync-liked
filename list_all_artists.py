# /// script
# dependencies = [
#   "spotipy",
#   "python-dotenv",
# ]
# ///

from collections import Counter

from config import get_spotify_client


def main():
    sp = get_spotify_client("user-library-read")

    print("--- Fetching your artist list ---")

    all_artists = []
    results = sp.current_user_saved_tracks(limit=50)

    def extract_artists(items):
        """Extract the primary artist name from each track item."""
        return [item['track']['artists'][0]['name'] for item in items]

    all_artists.extend(extract_artists(results['items']))

    while results['next']:
        results = sp.next(results)
        all_artists.extend(extract_artists(results['items']))

    # Count occurrences and sort alphabetically (case-insensitive)
    artist_counts = Counter(all_artists)
    sorted_artists = sorted(artist_counts.items(), key=lambda x: x[0].lower())

    print(f"\n--- ALPHABETICAL ARTIST LIST ({len(sorted_artists)} artists) ---")
    print(f"{'Artist':<30} | {'Track count':<15}")
    print("-" * 48)

    for artist, count in sorted_artists:
        print(f"{artist:<30} | {count:<15}")

    print("-" * 48)
    print(f"Total tracks in library: {len(all_artists)}")


if __name__ == "__main__":
    main()
