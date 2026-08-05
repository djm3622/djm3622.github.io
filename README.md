# David Millard

Source for [David Millard's research website](https://notdavidmill.dev/), covering research in machine learning, scientific computing, control systems, and audio at the University of Rochester.

The website is built with Jekyll and published from the [`docs/`](docs/) directory through GitHub Pages.

## Spotify data automation

The home page displays one track selected each day from a randomly chosen
Spotify playlist owned by, or collaborative with, the authenticated account.
Playback is always opt-in. Internal page navigation keeps the active embed
mounted so music can continue without interruption.

The music page uses the same authenticated account to analyze complete private
and collaborative playlists. It also publishes a rolling 90-day sample of
recent listening activity and Spotify's private top-track and top-artist
rankings. The generated snapshot is public because it is committed to this
public website; credentials and tokens remain in repository Actions secrets.

To connect the automation:

1. Create a Spotify developer app and add
   `http://127.0.0.1:8765/callback` as an allowed redirect URI. Spotify
   Development Mode currently requires the app owner to have Premium.
2. From `docs/`, run `python3 scripts/spotify_authorize.py`. Supply the app's
   client ID and client secret, authorize the account, and copy the refresh
   token printed at the end.
3. Add `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and
   `SPOTIFY_REFRESH_TOKEN` as repository Actions secrets.
4. Run the **Update Spotify data** workflow once from the Actions tab.

The workflow then runs every two hours so it can accumulate recent listening
history without exposing Spotify credentials to the browser. A failed Spotify
request leaves the previous working site data unchanged.

The eligible playlist IDs are maintained in
[`docs/_data/spotify_playlists.json`](docs/_data/spotify_playlists.json). Only
non-empty entries in that allowlist that the authenticated account owns or
collaborates on are considered for the daily selection.
