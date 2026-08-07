#!/usr/bin/env python3
"""Build the music-page snapshot from the authenticated Spotify account."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from zoneinfo import ZoneInfo

from build_music_analytics import (
    _catalog_duration_label,
    _duration_label,
    _rounded_percentage,
)
from update_spotify_pick import (
    SpotifyClient,
    SpotifyError,
    _eligible_playlists,
    _eligible_tracks,
    _first_image_url,
    _load_playlist_ids,
    _required_environment,
)

ACTIVITY_RETENTION_DAYS = 90
LOCAL_TIMEZONE = ZoneInfo("America/New_York")
TRACK_URL = "https://open.spotify.com/track/{track_id}"
ARTIST_URL = "https://open.spotify.com/artist/{artist_id}"
PLAYLIST_URL = "https://open.spotify.com/playlist/{playlist_id}"
ARTIST_BATCH_SIZE = 50


def _load_existing(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SpotifyError(f"Could not read existing analytics at {path}: {error}") from error
    return payload if isinstance(payload, Mapping) else {}


def _artist_names(track: Mapping[str, Any]) -> list[str]:
    artists = track.get("artists", [])
    if not isinstance(artists, list):
        return []
    return [
        str(artist["name"])
        for artist in artists
        if isinstance(artist, Mapping) and isinstance(artist.get("name"), str)
    ]


def _primary_artist_id(track: Mapping[str, Any]) -> str | None:
    artists = track.get("artists", [])
    if not isinstance(artists, list) or not artists or not isinstance(artists[0], Mapping):
        return None
    identifier = artists[0].get("id")
    return str(identifier) if isinstance(identifier, str) and identifier else None


def _normalise_track(track: Mapping[str, Any], playlist_id: str) -> dict[str, Any] | None:
    identifier = track.get("id")
    if not isinstance(identifier, str) or not identifier or track.get("type") != "track":
        return None
    names = _artist_names(track)
    album = track.get("album")
    album = album if isinstance(album, Mapping) else {}
    return {
        "id": identifier,
        "title": str(track.get("name") or "Untitled"),
        "artist_label": ", ".join(names) or "Unknown artist",
        "primary_artist": names[0] if names else "Unknown artist",
        "primary_artist_id": _primary_artist_id(track),
        "duration_ms": int(track.get("duration_ms") or 0),
        "explicit": bool(track.get("explicit")),
        "image_url": _first_image_url(album),
        "playlist_id": playlist_id,
    }


def _track_card(track: Mapping[str, Any], playlist_name: str) -> dict[str, Any]:
    identifier = str(track["id"])
    duration_ms = int(track["duration_ms"])
    return {
        "id": identifier,
        "title": track["title"],
        "artist": track["artist_label"],
        "primary_artist": track["primary_artist"],
        "playlist": playlist_name,
        "url": TRACK_URL.format(track_id=identifier),
        "duration_ms": duration_ms,
        "duration_label": _duration_label(duration_ms),
        "explicit": bool(track["explicit"]),
        "image_url": track.get("image_url"),
        "playcount": None,
    }


def _iso_datetime(value: object) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _recent_play(entry: Mapping[str, Any]) -> dict[str, Any] | None:
    track = entry.get("track")
    played_at = entry.get("played_at")
    if not isinstance(track, Mapping) or _iso_datetime(played_at) is None:
        return None
    normalised = _normalise_track(track, "")
    if normalised is None:
        return None
    return {
        "played_at": played_at,
        "id": normalised["id"],
        "title": normalised["title"],
        "artist": normalised["artist_label"],
        "primary_artist": normalised["primary_artist"],
        "duration_ms": normalised["duration_ms"],
        "image_url": normalised["image_url"],
        "url": TRACK_URL.format(track_id=normalised["id"]),
    }


def _merge_recent_plays(
    previous: Iterable[Mapping[str, Any]], new: Iterable[Mapping[str, Any]], now: dt.datetime
) -> list[dict[str, Any]]:
    cutoff = now.astimezone(dt.timezone.utc) - dt.timedelta(days=ACTIVITY_RETENTION_DAYS)
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for play in [*previous, *new]:
        played_at = _iso_datetime(play.get("played_at"))
        identifier = play.get("id")
        if played_at is None or played_at < cutoff or not isinstance(identifier, str):
            continue
        by_key[(played_at.isoformat(), identifier)] = dict(play)
    return sorted(
        by_key.values(), key=lambda play: str(play["played_at"]), reverse=True
    )[:2500]


def _top_item(item: Mapping[str, Any], rank: int, item_type: str) -> dict[str, Any] | None:
    identifier = item.get("id")
    if not isinstance(identifier, str) or not identifier:
        return None
    if item_type == "artists":
        return {
            "rank": rank,
            "id": identifier,
            "name": str(item.get("name") or "Unknown artist"),
            "image_url": _first_image_url(item),
            "url": ARTIST_URL.format(artist_id=identifier),
        }
    album = item.get("album")
    album = album if isinstance(album, Mapping) else {}
    return {
        "rank": rank,
        "id": identifier,
        "name": str(item.get("name") or "Untitled"),
        "artist": ", ".join(_artist_names(item)) or "Unknown artist",
        "image_url": _first_image_url(album),
        "url": TRACK_URL.format(track_id=identifier),
    }


def _fetch_top_items(client: SpotifyClient, item_type: str) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {}
    for key, time_range in (
        ("four_weeks", "short_term"),
        ("six_months", "medium_term"),
        ("one_year", "long_term"),
    ):
        page = client.get(f"/me/top/{item_type}?time_range={time_range}&limit=20")
        raw_items = page.get("items", [])
        items = raw_items if isinstance(raw_items, list) else []
        output[key] = [
            card
            for rank, item in enumerate(items, start=1)
            if isinstance(item, Mapping)
            and (card := _top_item(item, rank, item_type)) is not None
        ]
    return output


def _fetch_artist_images(
    client: SpotifyClient, artist_ids: Iterable[str]
) -> dict[str, str]:
    """Return available Spotify profile images keyed by artist ID.

    The Web API accepts at most 50 artist IDs per request. Missing images are
    intentionally omitted so callers can use the album-art fallback already
    present in the playlist snapshot.
    """

    identifiers = list(dict.fromkeys(identifier for identifier in artist_ids if identifier))
    images: dict[str, str] = {}
    for offset in range(0, len(identifiers), ARTIST_BATCH_SIZE):
        batch = identifiers[offset : offset + ARTIST_BATCH_SIZE]
        response = client.get("/artists?ids=" + ",".join(batch))
        raw_artists = response.get("artists", [])
        if not isinstance(raw_artists, list):
            raise SpotifyError("Spotify returned an invalid artist image response")
        for artist in raw_artists:
            if not isinstance(artist, Mapping):
                continue
            identifier = artist.get("id")
            image_url = _first_image_url(artist)
            if isinstance(identifier, str) and identifier and image_url:
                images[identifier] = image_url
    return images


def _activity_snapshot(
    client: SpotifyClient, existing: Mapping[str, Any], now: dt.datetime
) -> tuple[Mapping[str, Any], str | None]:
    try:
        recent_page = client.get("/me/player/recently-played?limit=50")
        raw_recent = recent_page.get("items", [])
        recent_entries = raw_recent if isinstance(raw_recent, list) else []
        new_plays = [
            play
            for entry in recent_entries
            if isinstance(entry, Mapping) and (play := _recent_play(entry)) is not None
        ]
        top_tracks = _fetch_top_items(client, "tracks")
        top_artists = _fetch_top_items(client, "artists")
    except SpotifyError as error:
        if "(403)" not in str(error):
            raise
        previous_activity = existing.get("activity")
        if isinstance(previous_activity, Mapping) and previous_activity.get("enabled") is True:
            return previous_activity, str(error)
        return {"enabled": False}, str(error)

    previous_activity = existing.get("activity")
    previous_plays = (
        previous_activity.get("recent_plays", [])
        if isinstance(previous_activity, Mapping)
        else []
    )
    previous_plays = previous_plays if isinstance(previous_plays, list) else []
    history = _merge_recent_plays(
        (item for item in previous_plays if isinstance(item, Mapping)), new_plays, now
    )

    hour_counts: collections.Counter[int] = collections.Counter()
    weekday_counts: collections.Counter[int] = collections.Counter()
    track_counts: collections.Counter[tuple[str, str, str, str | None]] = collections.Counter()
    artist_counts: collections.Counter[str] = collections.Counter()
    listening_ms = 0
    for play in history:
        timestamp = _iso_datetime(play["played_at"])
        if timestamp is None:
            continue
        local = timestamp.astimezone(LOCAL_TIMEZONE)
        hour_counts[local.hour] += 1
        weekday_counts[local.weekday()] += 1
        listening_ms += int(play.get("duration_ms") or 0)
        track_counts[
            (
                str(play["id"]),
                str(play["title"]),
                str(play["artist"]),
                str(play["image_url"]) if play.get("image_url") else None,
            )
        ] += 1
        artist_counts[str(play["primary_artist"])] += 1

    max_hour = max(hour_counts.values(), default=1)
    max_weekday = max(weekday_counts.values(), default=1)
    hours = [
        {
            "hour": hour,
            "label": dt.datetime(2000, 1, 1, hour).strftime("%-I %p"),
            "plays": hour_counts[hour],
            "height_pct": round(100 * hour_counts[hour] / max_hour),
        }
        for hour in range(24)
    ]
    weekdays = [
        {
            "label": label,
            "plays": weekday_counts[index],
            "width_pct": round(100 * weekday_counts[index] / max_weekday),
        }
        for index, label in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"))
    ]
    recent_top_tracks = [
        {
            "id": key[0],
            "name": key[1],
            "artist": key[2],
            "image_url": key[3],
            "url": TRACK_URL.format(track_id=key[0]),
            "plays": count,
        }
        for key, count in track_counts.most_common(8)
    ]
    recent_top_artists = [
        {"name": name, "plays": count}
        for name, count in artist_counts.most_common(8)
    ]
    timestamps = [
        timestamp
        for play in history
        if (timestamp := _iso_datetime(play.get("played_at"))) is not None
    ]
    return {
        "enabled": True,
        "history_days": ACTIVITY_RETENTION_DAYS,
        "captured_plays": len(history),
        "captured_hours": round(listening_ms / 3_600_000, 1),
        "distinct_tracks": len(track_counts),
        "distinct_artists": len(artist_counts),
        "history_start": min(timestamps).date().isoformat() if timestamps else None,
        "history_end": max(timestamps).date().isoformat() if timestamps else None,
        "last_played_at": history[0]["played_at"] if history else None,
        "hour_bins": hours,
        "weekday_bins": weekdays,
        "recent_top_tracks": recent_top_tracks,
        "recent_top_artists": recent_top_artists,
        "top_tracks": top_tracks,
        "top_artists": top_artists,
        "recent_plays": history,
    }, None


def build_snapshot(
    client: SpotifyClient,
    playlist_ids: Sequence[str],
    existing: Mapping[str, Any],
    *,
    now: dt.datetime | None = None,
) -> Mapping[str, Any]:
    generated_at = now or dt.datetime.now(dt.timezone.utc)
    profile = client.get("/me")
    user_id = profile.get("id")
    if not isinstance(user_id, str) or not user_id:
        raise SpotifyError("Spotify profile did not include a user ID")
    account_playlists = client.get_all("/me/playlists?limit=50")
    eligible = _eligible_playlists(account_playlists, user_id, playlist_ids)
    by_id = {str(playlist["id"]): playlist for playlist in eligible}
    unavailable = [identifier for identifier in playlist_ids if identifier not in by_id]

    playlists: list[dict[str, Any]] = []
    slots: list[dict[str, Any]] = []
    for playlist_id in playlist_ids:
        playlist = by_id.get(playlist_id)
        if playlist is None:
            continue
        raw_items = client.get_all(f"/playlists/{playlist_id}/items?limit=50")
        tracks = [
            normalised
            for track in _eligible_tracks(raw_items)
            if (normalised := _normalise_track(track, playlist_id)) is not None
        ]
        if not tracks:
            continue
        slots.extend(tracks)
        durations = [int(track["duration_ms"]) for track in tracks if track["duration_ms"]]
        artist_counts = collections.Counter(str(track["primary_artist"]) for track in tracks)
        leading_artist, leading_count = artist_counts.most_common(1)[0]
        playlists.append(
            {
                "id": playlist_id,
                "name": str(playlist.get("name") or "Untitled playlist"),
                "owner": str(
                    (playlist.get("owner") or {}).get("display_name")
                    if isinstance(playlist.get("owner"), Mapping)
                    else "Spotify user"
                ),
                "url": PLAYLIST_URL.format(playlist_id=playlist_id),
                "image_url": _first_image_url(playlist),
                "total_tracks": len(tracks),
                "sampled_tracks": len(tracks),
                "sample_coverage_pct": 100.0,
                "duration_hours": round(sum(durations) / 3_600_000, 1),
                "median_duration_ms": int(statistics.median(durations)) if durations else 0,
                "median_duration_label": _duration_label(
                    int(statistics.median(durations)) if durations else 0
                ),
                "explicit_pct": _rounded_percentage(
                    sum(bool(track["explicit"]) for track in tracks), len(tracks)
                ),
                "distinct_primary_artists": len(artist_counts),
                "top_artist": leading_artist,
                "top_artist_tracks": leading_count,
                "top_artist_share_pct": _rounded_percentage(leading_count, len(tracks)),
            }
        )

    if not playlists or not slots:
        raise SpotifyError("No readable tracks were found in the configured playlists")

    playlist_names = {playlist["id"]: playlist["name"] for playlist in playlists}
    playlist_images = {playlist["id"]: playlist["image_url"] for playlist in playlists}
    unique: dict[str, dict[str, Any]] = {}
    memberships: collections.defaultdict[str, set[str]] = collections.defaultdict(set)
    for track in slots:
        unique.setdefault(str(track["id"]), track)
        memberships[str(track["id"])].add(str(track["playlist_id"]))
    for track in unique.values():
        if not track.get("image_url"):
            track["image_url"] = playlist_images.get(str(track["playlist_id"]))

    activity, activity_error = _activity_snapshot(client, existing, generated_at)
    activity_plays = activity.get("recent_plays", []) if isinstance(activity, Mapping) else []
    recent_counts = collections.Counter(
        str(play["id"])
        for play in activity_plays
        if isinstance(play, Mapping) and isinstance(play.get("id"), str)
    )
    existing_discovery = existing.get("discovery_tracks", [])
    public_playcounts = {
        str(track["id"]): int(track["playcount"])
        for track in existing_discovery
        if isinstance(track, Mapping)
        and isinstance(track.get("id"), str)
        and isinstance(track.get("playcount"), int)
    } if isinstance(existing_discovery, list) else {}
    discovery = [
        _track_card(track, str(playlist_names[track["playlist_id"]]))
        for track in unique.values()
    ]
    for card in discovery:
        card["playcount"] = public_playcounts.get(str(card["id"]))
        card["recent_play_count"] = recent_counts[str(card["id"])]
    discovery.sort(
        key=lambda track: (
            str(track["title"]).casefold(),
            str(track["artist"]).casefold(),
        )
    )
    artist_counts = collections.Counter(str(track["primary_artist"]) for track in slots)
    artist_durations: collections.Counter[str] = collections.Counter()
    artist_explicit: collections.Counter[str] = collections.Counter()
    artist_fallback_images: dict[str, str | None] = {}
    artist_ids: dict[str, str] = {}
    for track in slots:
        name = str(track["primary_artist"])
        artist_durations[name] += int(track["duration_ms"])
        artist_explicit[name] += int(bool(track["explicit"]))
        fallback_image = track.get("image_url")
        if name not in artist_fallback_images or (
            artist_fallback_images[name] is None and fallback_image
        ):
            artist_fallback_images[name] = fallback_image
        if track.get("primary_artist_id"):
            artist_ids[name] = str(track["primary_artist_id"])

    artist_images = _fetch_artist_images(client, artist_ids.values())
    artists = [
        {
            "name": name,
            "tracks": count,
            "duration_ms": artist_durations[name],
            "duration_label": _catalog_duration_label(artist_durations[name]),
            "explicit_pct": _rounded_percentage(artist_explicit[name], count),
            "url": ARTIST_URL.format(artist_id=artist_ids[name]) if name in artist_ids else None,
            "image_url": artist_images.get(
                artist_ids.get(name, ""), artist_fallback_images[name]
            ),
            "image_kind": "artist"
            if artist_ids.get(name) in artist_images
            else "album",
        }
        for name, count in artist_counts.most_common()
    ]
    durations = [int(track["duration_ms"]) for track in slots if track["duration_ms"]]
    duration_sorted = sorted(unique.values(), key=lambda track: int(track["duration_ms"]))
    title_sorted = sorted(
        unique.values(), key=lambda track: len(str(track["title"])), reverse=True
    )
    repeated = [track for track in unique.values() if len(memberships[str(track["id"])]) > 1]
    existing_underrated = existing.get("underrated", [])
    underrated = existing_underrated if isinstance(existing_underrated, list) else []
    snapshot = {
        "generated_on": generated_at.date().isoformat(),
        "methodology": {
            "source": "authenticated_spotify_api",
            "playlist_count": len(playlists),
            "requested_playlist_count": len(playlist_ids),
            "catalog_slots": len(slots),
            "sampled_slots": len(slots),
            "coverage_pct": 100.0,
            "playcount_sample": len(underrated),
            "note": (
                "Playlist composition comes from Spotify's authenticated API, including "
                "configured private and collaborative playlists. Listening activity combines "
                "Spotify's recent-play history with private top-item affinity rankings."
            ),
        },
        "overview": {
            "unique_tracks": len(unique),
            "distinct_primary_artists": len(artist_counts),
            "sampled_hours": round(sum(durations) / 3_600_000, 1),
            "median_duration_ms": int(statistics.median(durations)) if durations else 0,
            "median_duration_label": _duration_label(
                int(statistics.median(durations)) if durations else 0
            ),
            "explicit_pct": _rounded_percentage(
                sum(bool(track["explicit"]) for track in slots), len(slots)
            ),
            "under_two_minutes_pct": _rounded_percentage(
                sum(int(track["duration_ms"]) < 120_000 for track in slots), len(slots)
            ),
            "over_six_minutes_pct": _rounded_percentage(
                sum(int(track["duration_ms"]) > 360_000 for track in slots), len(slots)
            ),
            "repeat_track_count": len(repeated),
        },
        "playlists": playlists,
        "unavailable_playlists": [
            {
                "id": identifier,
                "url": PLAYLIST_URL.format(playlist_id=identifier),
                "reason": "Unavailable to the authenticated account or missing required scope",
            }
            for identifier in unavailable
        ],
        "top_artists": [
            {"name": name, "tracks": count} for name, count in artist_counts.most_common(12)
        ],
        "artists": artists,
        "discovery_tracks": discovery,
        "underrated": underrated,
        "repeat_offenders": [
            {
                **_track_card(track, str(playlist_names[track["playlist_id"]])),
                "playlist_count": len(memberships[str(track["id"])]),
                "playlists": [
                    playlist_names[item]
                    for item in sorted(memberships[str(track["id"])])
                ],
            }
            for track in repeated[:10]
        ],
        "oddities": {
            "shortest": [
                _track_card(track, str(playlist_names[track["playlist_id"]]))
                for track in duration_sorted[:5]
            ],
            "longest": [
                _track_card(track, str(playlist_names[track["playlist_id"]]))
                for track in duration_sorted[-5:][::-1]
            ],
            "longest_titles": [
                {
                    **_track_card(track, str(playlist_names[track["playlist_id"]])),
                    "characters": len(str(track["title"])),
                }
                for track in title_sorted[:5]
            ],
        },
        "activity": activity,
    }
    if activity_error:
        snapshot["methodology"]["activity_warning"] = (
            "Listening activity is awaiting renewed Spotify authorization."
        )
        print(f"warning: activity data unavailable: {activity_error}", file=sys.stderr)
    return snapshot


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--playlists",
        type=Path,
        default=Path("_data/spotify_playlists.json"),
        help="JSON file containing the allowed playlist IDs",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("_data/music_analytics.json"),
        help="Jekyll data file to update",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        client = SpotifyClient(
            _required_environment("SPOTIFY_CLIENT_ID"),
            _required_environment("SPOTIFY_CLIENT_SECRET"),
            _required_environment("SPOTIFY_REFRESH_TOKEN"),
        )
        client.authenticate()
        snapshot = build_snapshot(
            client, _load_playlist_ids(args.playlists), _load_existing(args.output)
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    except SpotifyError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"Updated authenticated music analytics with {len(snapshot['playlists'])} playlists"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
