#!/usr/bin/env python3
"""Build a compact, reproducible analytics snapshot from public Spotify pages.

Spotify's public playlist page exposes playlist totals and a variable public window
with play counts. Its public embed exposes up to 100 tracks with durations and
explicit labels. This script combines those views without account credentials.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import json
import re
import statistics
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

PLAYLIST_URL = "https://open.spotify.com/playlist/{playlist_id}"
EMBED_URL = "https://open.spotify.com/embed/playlist/{playlist_id}"
USER_AGENT = "Mozilla/5.0 (compatible; personal-site-music-analytics/1.0)"


class AnalyticsError(RuntimeError):
    """Raised when the public Spotify payload cannot be interpreted."""


def _load_json_script(page: str, script_id: str, *, encoded: bool) -> Mapping[str, Any]:
    match = re.search(
        rf'<script id="{re.escape(script_id)}"[^>]*>(.*?)</script>',
        page,
        flags=re.DOTALL,
    )
    if match is None:
        raise AnalyticsError(f"Spotify page did not contain {script_id}")
    payload = html.unescape(match.group(1))
    if encoded:
        payload = base64.b64decode(payload).decode("utf-8")
    decoded = json.loads(payload)
    if not isinstance(decoded, Mapping):
        raise AnalyticsError(f"Spotify {script_id} payload was not an object")
    return decoded


def _fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _read_page(cache_dir: Path | None, playlist_id: str, *, embed: bool) -> str:
    prefix = "spotify_embed_" if embed else "spotify_"
    cached = cache_dir / f"{prefix}{playlist_id}.html" if cache_dir else None
    if cached is not None and cached.exists():
        return cached.read_text(encoding="utf-8")
    url = (EMBED_URL if embed else PLAYLIST_URL).format(playlist_id=playlist_id)
    return _fetch(url)


def _track_id(uri: object) -> str | None:
    if not isinstance(uri, str) or not uri.startswith("spotify:track:"):
        return None
    return uri.rsplit(":", 1)[-1]


def _primary_artist(label: str) -> str:
    # Spotify separates credited artists with a comma followed by a nonbreaking space.
    return re.split(r",(?:\u00a0|\s)", label, maxsplit=1)[0].strip()


def _public_playlist(page: str, playlist_id: str) -> Mapping[str, Any]:
    state = _load_json_script(page, "initialState", encoded=True)
    entity = state.get("entities", {}).get("items", {}).get(
        f"spotify:playlist:{playlist_id}"
    )
    if not isinstance(entity, Mapping):
        raise AnalyticsError(f"Public data was unavailable for playlist {playlist_id}")

    public_tracks: list[dict[str, Any]] = []
    content = entity.get("content", {})
    items = content.get("items", []) if isinstance(content, Mapping) else []
    for wrapper in items:
        if not isinstance(wrapper, Mapping):
            continue
        item = wrapper.get("itemV2", {})
        track = item.get("data", {}) if isinstance(item, Mapping) else {}
        if not isinstance(track, Mapping):
            continue
        identifier = _track_id(track.get("uri"))
        if identifier is None:
            continue
        artists_block = track.get("artists", {})
        artist_items = (
            artists_block.get("items", []) if isinstance(artists_block, Mapping) else []
        )
        artists = []
        for artist in artist_items:
            profile = artist.get("profile", {}) if isinstance(artist, Mapping) else {}
            name = profile.get("name") if isinstance(profile, Mapping) else None
            if isinstance(name, str) and name:
                artists.append(name)
        playcount = track.get("playcount")
        public_tracks.append(
            {
                "id": identifier,
                "title": track.get("name") or "Untitled",
                "artists": artists,
                "playcount": int(playcount) if str(playcount).isdigit() else None,
            }
        )

    images = entity.get("images", {}).get("items", [])
    image_url = None
    if images and isinstance(images[0], Mapping):
        sources = images[0].get("sources", [])
        if sources and isinstance(sources[0], Mapping):
            image_url = sources[0].get("url")
    return {
        "name": entity.get("name") or "Untitled playlist",
        "owner": entity.get("ownerV2", {}).get("data", {}).get("name") or "Spotify user",
        "total": int(content.get("totalCount", 0)),
        "followers": int(entity.get("followers", 0)),
        "image_url": image_url,
        "tracks": public_tracks,
    }


def _embedded_tracks(page: str) -> list[dict[str, Any]]:
    payload = _load_json_script(page, "__NEXT_DATA__", encoded=False)
    entity = (
        payload.get("props", {})
        .get("pageProps", {})
        .get("state", {})
        .get("data", {})
        .get("entity", {})
    )
    if not isinstance(entity, Mapping):
        raise AnalyticsError("Spotify embed data did not contain an entity")
    tracks: list[dict[str, Any]] = []
    for track in entity.get("trackList", []):
        if not isinstance(track, Mapping):
            continue
        identifier = _track_id(track.get("uri"))
        if identifier is None:
            continue
        artist_label = str(track.get("subtitle") or "Unknown artist")
        tracks.append(
            {
                "id": identifier,
                "title": str(track.get("title") or "Untitled"),
                "artist_label": artist_label,
                "primary_artist": _primary_artist(artist_label),
                "duration_ms": int(track.get("duration") or 0),
                "explicit": bool(track.get("isExplicit")),
            }
        )
    return tracks


def _track_link(track_id: str) -> str:
    return f"https://open.spotify.com/track/{track_id}"


def _duration_label(duration_ms: int) -> str:
    total_seconds = round(duration_ms / 1000)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}:{seconds:02d}"


def _compact_count(count: int) -> str:
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def _track_card(track: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": track["id"],
        "title": track["title"],
        "artist": track["artist_label"],
        "url": _track_link(str(track["id"])),
        "duration_ms": track["duration_ms"],
        "duration_label": _duration_label(int(track["duration_ms"])),
    }


def _rounded_percentage(numerator: int, denominator: int) -> float:
    return round(100 * numerator / denominator, 1) if denominator else 0.0


def build_snapshot(playlist_ids: Iterable[str], cache_dir: Path | None) -> Mapping[str, Any]:
    playlists: list[dict[str, Any]] = []
    unavailable_playlists: list[dict[str, str]] = []
    slots: list[dict[str, Any]] = []
    playcounts: dict[str, int] = {}
    exact_artists: dict[str, list[str]] = {}

    for playlist_id in playlist_ids:
        try:
            public = _public_playlist(
                _read_page(cache_dir, playlist_id, embed=False), playlist_id
            )
            tracks = _embedded_tracks(_read_page(cache_dir, playlist_id, embed=True))
        except AnalyticsError:
            unavailable_playlists.append(
                {
                    "id": playlist_id,
                    "url": PLAYLIST_URL.format(playlist_id=playlist_id),
                    "reason": "Private or unavailable to Spotify's signed-out public pages",
                }
            )
            continue
        for track in public["tracks"]:
            if track["playcount"] is not None:
                playcounts[track["id"]] = track["playcount"]
            if track["artists"]:
                exact_artists[track["id"]] = track["artists"]
        for track in tracks:
            track["playlist_id"] = playlist_id
            slots.append(track)

        durations = [track["duration_ms"] for track in tracks if track["duration_ms"] > 0]
        artist_counts = Counter(track["primary_artist"] for track in tracks)
        playlists.append(
            {
                "id": playlist_id,
                "name": public["name"],
                "owner": public["owner"],
                "url": PLAYLIST_URL.format(playlist_id=playlist_id),
                "image_url": public["image_url"],
                "total_tracks": public["total"],
                "sampled_tracks": len(tracks),
                "sample_coverage_pct": _rounded_percentage(len(tracks), public["total"]),
                "duration_hours": round(sum(durations) / 3_600_000, 1),
                "median_duration_ms": int(statistics.median(durations)) if durations else 0,
                "median_duration_label": (
                    _duration_label(int(statistics.median(durations))) if durations else "0:00"
                ),
                "explicit_pct": _rounded_percentage(
                    sum(track["explicit"] for track in tracks), len(tracks)
                ),
                "distinct_primary_artists": len(artist_counts),
                "top_artist": artist_counts.most_common(1)[0][0] if artist_counts else "—",
                "top_artist_tracks": artist_counts.most_common(1)[0][1] if artist_counts else 0,
            }
        )

    by_track: dict[str, dict[str, Any]] = {}
    playlist_memberships: defaultdict[str, set[str]] = defaultdict(set)
    for track in slots:
        by_track.setdefault(track["id"], track)
        playlist_memberships[track["id"]].add(track["playlist_id"])

    artist_counts = Counter(track["primary_artist"] for track in slots)
    durations = [track["duration_ms"] for track in slots if track["duration_ms"] > 0]
    unique_tracks = list(by_track.values())
    repeated = sorted(
        (track for track in unique_tracks if len(playlist_memberships[track["id"]]) > 1),
        key=lambda track: (-len(playlist_memberships[track["id"]]), track["title"].casefold()),
    )
    repeated_cards = []
    playlist_names = {playlist["id"]: playlist["name"] for playlist in playlists}
    for track in repeated[:10]:
        card = _track_card(track)
        card["playlist_count"] = len(playlist_memberships[track["id"]])
        card["playlists"] = [
            playlist_names[playlist_id]
            for playlist_id in sorted(playlist_memberships[track["id"]])
        ]
        repeated_cards.append(card)

    rarity_pool = [
        track
        for track in unique_tracks
        if track["id"] in playcounts and playcounts[track["id"]] > 0
    ]
    rarity_pool.sort(key=lambda track: (playcounts[track["id"]], track["title"].casefold()))
    underrated = []
    for track in rarity_pool[:12]:
        card = _track_card(track)
        card["playcount"] = playcounts[track["id"]]
        card["playcount_label"] = _compact_count(playcounts[track["id"]])
        card["playlist_count"] = len(playlist_memberships[track["id"]])
        underrated.append(card)

    lower_titles = [
        track for track in unique_tracks if track["title"].isalpha() and track["title"].islower()
    ]
    punctuation_titles = [
        track
        for track in unique_tracks
        if any(mark in track["title"] for mark in ("?", "!", "(", ")", "[", "]"))
    ]
    duration_sorted = sorted(unique_tracks, key=lambda track: track["duration_ms"])
    title_sorted = sorted(unique_tracks, key=lambda track: len(track["title"]), reverse=True)

    total_catalog_slots = sum(playlist["total_tracks"] for playlist in playlists)
    return {
        "generated_on": dt.datetime.now(dt.timezone.utc).date().isoformat(),
        "methodology": {
            "playlist_count": len(playlists),
            "requested_playlist_count": len(playlists) + len(unavailable_playlists),
            "catalog_slots": total_catalog_slots,
            "sampled_slots": len(slots),
            "coverage_pct": _rounded_percentage(len(slots), total_catalog_slots),
            "playcount_sample": len(playcounts),
            "note": (
                "Public Spotify embeds expose up to the first 100 tracks per playlist; "
                "public playlist pages expose play counts for a variable visible window. "
                "Statistics describe those visible windows, not private listening history."
            ),
        },
        "overview": {
            "unique_tracks": len(unique_tracks),
            "distinct_primary_artists": len(artist_counts),
            "sampled_hours": round(sum(durations) / 3_600_000, 1),
            "median_duration_ms": int(statistics.median(durations)) if durations else 0,
            "median_duration_label": (
                _duration_label(int(statistics.median(durations))) if durations else "0:00"
            ),
            "explicit_pct": _rounded_percentage(sum(track["explicit"] for track in slots), len(slots)),
            "under_two_minutes_pct": _rounded_percentage(
                sum(track["duration_ms"] < 120_000 for track in slots), len(slots)
            ),
            "over_six_minutes_pct": _rounded_percentage(
                sum(track["duration_ms"] > 360_000 for track in slots), len(slots)
            ),
            "repeat_track_count": len(repeated),
            "lowercase_title_pct": _rounded_percentage(len(lower_titles), len(unique_tracks)),
            "punctuation_title_pct": _rounded_percentage(
                len(punctuation_titles), len(unique_tracks)
            ),
        },
        "playlists": playlists,
        "unavailable_playlists": unavailable_playlists,
        "top_artists": [
            {"name": name, "tracks": count}
            for name, count in artist_counts.most_common(12)
        ],
        "underrated": underrated,
        "repeat_offenders": repeated_cards,
        "oddities": {
            "shortest": [_track_card(track) for track in duration_sorted[:5]],
            "longest": [_track_card(track) for track in duration_sorted[-5:][::-1]],
            "longest_titles": [
                {**_track_card(track), "characters": len(track["title"])}
                for track in title_sorted[:5]
            ],
        },
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--playlists",
        type=Path,
        default=Path("_data/spotify_playlists.json"),
        help="JSON playlist allowlist",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("_data/music_analytics.json"),
        help="Generated analytics snapshot",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="Optional directory containing spotify_<id>.html cache files",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    config = json.loads(args.playlists.read_text(encoding="utf-8"))
    playlist_ids = config.get("playlist_ids", [])
    if not playlist_ids or not all(isinstance(item, str) for item in playlist_ids):
        raise AnalyticsError("Playlist config must contain playlist_ids")
    snapshot = build_snapshot(playlist_ids, args.cache_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
