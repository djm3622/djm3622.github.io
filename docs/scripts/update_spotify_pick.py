#!/usr/bin/env python3
"""Select a daily track from one of the authenticated user's Spotify playlists."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import random
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Mapping, Sequence

ACCOUNTS_URL = "https://accounts.spotify.com/api/token"
API_ROOT = "https://api.spotify.com/v1"


class SpotifyError(RuntimeError):
    """Raised when Spotify returns an unusable response."""


class SpotifyClient:
    """Small Spotify Web API client using only the Python standard library."""

    def __init__(self, client_id: str, client_secret: str, refresh_token: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token: str | None = None

    def authenticate(self) -> None:
        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode("utf-8")
        ).decode("ascii")
        payload = urllib.parse.urlencode(
            {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        ).encode("ascii")
        response = self._request_json(
            ACCOUNTS_URL,
            data=payload,
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        token = response.get("access_token")
        if not isinstance(token, str) or not token:
            raise SpotifyError("Spotify did not return an access token")
        self.access_token = token

    def get(self, path_or_url: str) -> Mapping[str, Any]:
        if self.access_token is None:
            raise SpotifyError("Spotify client has not been authenticated")
        url = path_or_url if path_or_url.startswith("https://") else API_ROOT + path_or_url
        return self._request_json(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    def get_all(self, path: str) -> list[Mapping[str, Any]]:
        page: Mapping[str, Any] | None = self.get(path)
        items: list[Mapping[str, Any]] = []
        while page is not None:
            raw_items = page.get("items", [])
            if not isinstance(raw_items, list):
                raise SpotifyError("Spotify returned an invalid paginated response")
            items.extend(item for item in raw_items if isinstance(item, Mapping))
            next_url = page.get("next")
            page = self.get(next_url) if isinstance(next_url, str) and next_url else None
        return items

    @staticmethod
    def _request_json(
        url: str,
        *,
        data: bytes | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Mapping[str, Any]:
        request = urllib.request.Request(url, data=data, headers=dict(headers or {}))
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise SpotifyError(f"Spotify request failed ({error.code}): {detail}") from error
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            raise SpotifyError(f"Spotify request failed: {error}") from error
        if not isinstance(payload, Mapping):
            raise SpotifyError("Spotify returned an invalid JSON response")
        return payload


def _required_environment(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SpotifyError(f"Required environment variable {name} is not set")
    return value


def _load_existing(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SpotifyError(f"Could not read existing selection at {path}: {error}") from error
    return payload if isinstance(payload, Mapping) else {}


def _eligible_playlists(
    playlists: Sequence[Mapping[str, Any]], user_id: str
) -> list[Mapping[str, Any]]:
    eligible = []
    for playlist in playlists:
        owner = playlist.get("owner")
        item_summary = playlist.get("items") or playlist.get("tracks")
        owner_id = owner.get("id") if isinstance(owner, Mapping) else None
        total = item_summary.get("total", 0) if isinstance(item_summary, Mapping) else 0
        if (owner_id == user_id or playlist.get("collaborative") is True) and total > 0:
            eligible.append(playlist)
    return eligible


def _eligible_tracks(items: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    tracks = []
    for entry in items:
        track = entry.get("item") or entry.get("track")
        if not isinstance(track, Mapping):
            continue
        track_id = track.get("id")
        if (
            track.get("type") == "track"
            and isinstance(track_id, str)
            and track_id
            and track.get("is_local") is not True
            and track.get("is_playable") is not False
        ):
            tracks.append(track)
    return tracks


def _daily_random(selection_date: dt.date) -> random.Random:
    digest = hashlib.sha256(selection_date.isoformat().encode("ascii")).digest()
    return random.Random(int.from_bytes(digest, byteorder="big"))


def choose_selection(
    client: SpotifyClient,
    selection_date: dt.date,
    previous: Mapping[str, Any],
) -> Mapping[str, Any]:
    profile = client.get("/me")
    user_id = profile.get("id")
    if not isinstance(user_id, str) or not user_id:
        raise SpotifyError("Spotify profile did not include a user ID")

    playlists = _eligible_playlists(client.get_all("/me/playlists?limit=50"), user_id)
    if not playlists:
        raise SpotifyError("No non-empty owned or collaborative playlists were found")

    rng = _daily_random(selection_date)
    rng.shuffle(playlists)
    previous_playlist = previous.get("playlist")
    previous_playlist_id = (
        previous_playlist.get("id") if isinstance(previous_playlist, Mapping) else None
    )
    if len(playlists) > 1:
        playlists.sort(key=lambda playlist: playlist.get("id") == previous_playlist_id)

    selected_playlist: Mapping[str, Any] | None = None
    tracks: list[Mapping[str, Any]] = []
    for playlist in playlists:
        playlist_id = playlist.get("id")
        if not isinstance(playlist_id, str) or not playlist_id:
            continue
        items = client.get_all(f"/playlists/{playlist_id}/items?limit=50")
        tracks = _eligible_tracks(items)
        if tracks:
            selected_playlist = playlist
            break
    if selected_playlist is None:
        raise SpotifyError("No playable Spotify tracks were found in eligible playlists")

    rng.shuffle(tracks)
    previous_track = previous.get("track")
    previous_track_id = previous_track.get("id") if isinstance(previous_track, Mapping) else None
    if len(tracks) > 1:
        tracks.sort(key=lambda track: track.get("id") == previous_track_id)
    track = tracks[0]

    artists = track.get("artists", [])
    artist_names = [
        artist.get("name")
        for artist in artists
        if isinstance(artist, Mapping) and isinstance(artist.get("name"), str)
    ]
    playlist_id = str(selected_playlist["id"])
    track_id = str(track["id"])
    return {
        "enabled": True,
        "date": selection_date.isoformat(),
        "playlist": {
            "id": playlist_id,
            "name": selected_playlist.get("name") or "Spotify playlist",
            "url": f"https://open.spotify.com/playlist/{playlist_id}",
        },
        "track": {
            "id": track_id,
            "name": track.get("name") or "Spotify track",
            "artists": artist_names,
            "artist_label": ", ".join(artist_names),
            "url": f"https://open.spotify.com/track/{track_id}",
            "embed_url": f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator",
        },
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("_data/spotify_pick.json"),
        help="Jekyll data file to update",
    )
    parser.add_argument(
        "--date",
        type=dt.date.fromisoformat,
        default=dt.datetime.now(dt.timezone.utc).date(),
        help="selection date in YYYY-MM-DD format (defaults to the current UTC date)",
    )
    parser.add_argument("--force", action="store_true", help="replace an existing pick for the date")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    existing = _load_existing(args.output)
    if existing.get("enabled") is True and existing.get("date") == args.date.isoformat() and not args.force:
        print(f"Spotify selection for {args.date.isoformat()} already exists")
        return 0

    try:
        client = SpotifyClient(
            _required_environment("SPOTIFY_CLIENT_ID"),
            _required_environment("SPOTIFY_CLIENT_SECRET"),
            _required_environment("SPOTIFY_REFRESH_TOKEN"),
        )
        client.authenticate()
        selection = choose_selection(client, args.date, existing)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    except SpotifyError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(
        f"Selected {selection['track']['name']} from {selection['playlist']['name']} "
        f"for {selection['date']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
