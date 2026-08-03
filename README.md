# David Millard

Source for [David Millard's research website](https://djm3622.github.io/), covering research in machine learning, scientific computing, control systems, and audio at the University of Rochester.

The website is built with Jekyll and published from the [`docs/`](docs/) directory through GitHub Pages.

## Daily Spotify selection

The home page can display one track selected each day from a randomly chosen
Spotify playlist owned by, or collaborative with, the authenticated account.
Playback is always opt-in. Internal page navigation keeps the active embed
mounted so music can continue without interruption.

To connect the automation:

1. Create a Spotify developer app and add
   `http://127.0.0.1:8765/callback` as an allowed redirect URI. Spotify
   Development Mode currently requires the app owner to have Premium.
2. From `docs/`, run `python3 scripts/spotify_authorize.py`. Supply the app's
   client ID and client secret, authorize the account, and copy the refresh
   token printed at the end.
3. Add `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and
   `SPOTIFY_REFRESH_TOKEN` as repository Actions secrets.
4. Run the **Update daily Spotify pick** workflow once from the Actions tab.

The workflow then runs at 5:15 a.m. America/New_York each day. A failed Spotify
request leaves the previous day's working selection unchanged.
