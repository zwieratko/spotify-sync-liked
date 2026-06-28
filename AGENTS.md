# AGENTS.md

## Project

Standalone Python scripts that manage/analyze a Spotify "Liked Songs" library via
[spotipy](https://spotipy.readthedocs.io/). Three entrypoints, all sharing `config.py`:

- `sync_spotify.py` — copies Liked Songs to a public playlist (dedup)
- `analyze_liked_songs.py` — top artists/genres/years, duplicate detection
- `list_all_artists.py` — alphabetical artist list with track counts

`config.py` builds the OAuth client from env vars and auto-recovers from Spotify's
6-month refresh-token expiration by deleting `.cache` and re-triggering the browser flow.

## Toolchain

- Python 3.9+, managed with **`uv`** (no `pyproject.toml`).
- Each script declares deps inline via PEP 723 (`# /// script`) metadata —
  `uv run <script>.py` resolves them automatically. Do not add a `requirements.txt`.
- Lint/format/typecheck use `uv tool run` against the repo defaults (no ruff/ty config files):
  - `uv tool run ruff check .`
  - `uv tool run ruff format . --check`
  - `uv tool run --with spotipy --with python-dotenv ty check .`
  - `ty` needs the runtime deps available (`--with spotipy --with python-dotenv`) because
    the project has no `pyproject.toml` and deps are declared only via PEP 723 inline
    metadata, which `ty` does not consume. Without `--with`, it reports false
    `unresolved-import` errors for `spotipy` and `dotenv`.
- No test suite. Verification order: **lint → format-check → type-check → run**.
  The `check-all` command in `opencode.json` codifies this.

## Running

- Requires `.env` (copy from `.env.example`) with `SPOTIPY_CLIENT_ID`,
  `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI`, `SPOTIFY_PUBLIC_PLAYLIST_ID`.
- First run opens a browser for OAuth; callback is `http://127.0.0.1:8888/callback`.
  Paste the redirected URL into the prompt. Token cached in `.cache` (gitignored).
- **Running the scripts hits the live Spotify API and can mutate the user's public
  playlist.** Do not run `sync_spotify.py` as a verification step unless the user
  asks. Prefer lint/format/typecheck for code validation; `analyze_liked_songs.py`
  and `list_all_artists.py` are read-only but still require valid credentials.

## Conventions

- All code (names, comments, docstrings, log/output messages) must be English.
- Communication with the owner may be in Slovak when they write in Slovak.
- Keep this file in sync whenever project structure, entrypoints, deps, or run
  commands change.
