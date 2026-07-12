# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Project-Specific Guidelines

Standalone Python scripts that manage/analyze a Spotify "Liked Songs" library via
[spotipy](https://spotipy.readthedocs.io/). Three entrypoints, all sharing `config.py`:

- `sync_spotify.py` — copies Liked Songs to a public playlist (dedup)
- `analyze_liked_songs.py` — top artists/genres/years, duplicate detection
- `list_all_artists.py` — alphabetical artist list with track counts

`config.py` builds the OAuth client from env vars and auto-recovers from Spotify's
6-month refresh-token expiration by deleting `.cache` and re-triggering the browser flow.

### Toolchain

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

### Running

- Requires `.env` (copy from `.env.example`) with `SPOTIPY_CLIENT_ID`,
  `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI`, `SPOTIFY_PUBLIC_PLAYLIST_ID`.
- First run opens a browser for OAuth; callback is `http://127.0.0.1:8888/callback`.
  Paste the redirected URL into the prompt. Token cached in `.cache` (gitignored).
- **Running the scripts hits the live Spotify API and can mutate the user's public
  playlist.** Do not run `sync_spotify.py` as a verification step unless the user
  asks. Prefer lint/format/typecheck for code validation; `analyze_liked_songs.py`
  and `list_all_artists.py` are read-only but still require valid credentials.

## Conventions

- Keep this file in sync whenever project structure, entrypoints, deps, or run
  commands change.
