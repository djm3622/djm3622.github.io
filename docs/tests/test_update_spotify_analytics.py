from __future__ import annotations

import datetime as dt
import importlib.util
import sys
import unittest
from pathlib import Path
from typing import Any, Mapping


SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
MODULE_PATH = SCRIPTS_DIR / "update_spotify_analytics.py"
SPEC = importlib.util.spec_from_file_location("update_spotify_analytics", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
analytics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analytics)


def _track(identifier: str = "track-1") -> Mapping[str, Any]:
    return {
        "id": identifier,
        "type": "track",
        "name": "Night Drive",
        "duration_ms": 180_000,
        "explicit": False,
        "is_local": False,
        "is_playable": True,
        "artists": [{"id": "artist-1", "name": "Artist One"}],
        "album": {"images": [{"url": "https://example.com/cover.jpg"}]},
    }


class FakeClient:
    def get(self, path: str) -> Mapping[str, Any]:
        if path == "/me":
            return {"id": "david"}
        if path == "/me/player/recently-played?limit=50":
            return {
                "items": [
                    {"played_at": "2026-08-04T03:00:00Z", "track": _track()},
                    {"played_at": "2026-08-04T04:00:00Z", "track": _track()},
                ]
            }
        if path.startswith("/me/top/tracks"):
            return {"items": [_track()]}
        if path.startswith("/me/top/artists"):
            return {
                "items": [
                    {
                        "id": "artist-1",
                        "name": "Artist One",
                        "images": [{"url": "https://example.com/artist.jpg"}],
                    }
                ]
            }
        if path == "/artists?ids=artist-1":
            return {
                "artists": [
                    {
                        "id": "artist-1",
                        "images": [{"url": "https://example.com/catalog-artist.jpg"}],
                    }
                ]
            }
        raise AssertionError(f"Unexpected get path: {path}")

    def get_all(self, path: str) -> list[Mapping[str, Any]]:
        if path == "/me/playlists?limit=50":
            return [
                {
                    "id": "playlist-1",
                    "name": "Private Mix",
                    "owner": {"id": "david", "display_name": "David"},
                    "collaborative": False,
                    "items": {"total": 1},
                    "images": [{"url": "https://example.com/playlist.jpg"}],
                }
            ]
        if path == "/playlists/playlist-1/items?limit=50":
            return [{"item": _track()}]
        raise AssertionError(f"Unexpected get_all path: {path}")


class SpotifyAnalyticsTest(unittest.TestCase):
    def test_authenticated_snapshot_has_full_playlist_and_activity(self) -> None:
        snapshot = analytics.build_snapshot(
            FakeClient(),
            ["playlist-1"],
            {},
            now=dt.datetime(2026, 8, 4, 12, tzinfo=dt.timezone.utc),
        )

        self.assertEqual(snapshot["methodology"]["source"], "authenticated_spotify_api")
        self.assertEqual(snapshot["methodology"]["coverage_pct"], 100.0)
        self.assertEqual(snapshot["playlists"][0]["name"], "Private Mix")
        self.assertEqual(snapshot["activity"]["captured_plays"], 2)
        self.assertEqual(
            snapshot["activity"]["top_tracks"]["four_weeks"][0]["name"],
            "Night Drive",
        )
        self.assertEqual(snapshot["discovery_tracks"][0]["recent_play_count"], 2)
        self.assertEqual(snapshot["artists"][0]["image_kind"], "artist")
        self.assertEqual(
            snapshot["artists"][0]["image_url"],
            "https://example.com/catalog-artist.jpg",
        )

    def test_artist_images_fall_back_to_album_art(self) -> None:
        class MissingArtistImageClient(FakeClient):
            def get(self, path: str) -> Mapping[str, Any]:
                if path == "/artists?ids=artist-1":
                    return {"artists": [{"id": "artist-1", "images": []}]}
                return super().get(path)

        snapshot = analytics.build_snapshot(
            MissingArtistImageClient(),
            ["playlist-1"],
            {},
            now=dt.datetime(2026, 8, 4, 12, tzinfo=dt.timezone.utc),
        )

        self.assertEqual(snapshot["artists"][0]["image_kind"], "album")
        self.assertEqual(
            snapshot["artists"][0]["image_url"], "https://example.com/cover.jpg"
        )

    def test_artist_image_requests_are_batched(self) -> None:
        class BatchClient:
            def __init__(self) -> None:
                self.paths: list[str] = []

            def get(self, path: str) -> Mapping[str, Any]:
                self.paths.append(path)
                identifiers = path.removeprefix("/artists?ids=").split(",")
                return {
                    "artists": [
                        {"id": identifier, "images": [{"url": f"https://example.com/{identifier}.jpg"}]}
                        for identifier in identifiers
                    ]
                }

        client = BatchClient()
        identifiers = [f"artist-{index}" for index in range(51)]

        images = analytics._fetch_artist_images(client, identifiers)

        self.assertEqual(len(client.paths), 2)
        self.assertEqual(len(images), 51)
        self.assertEqual(images["artist-50"], "https://example.com/artist-50.jpg")

    def test_recent_history_deduplicates_and_expires_old_plays(self) -> None:
        now = dt.datetime(2026, 8, 4, tzinfo=dt.timezone.utc)
        current = {
            "id": "track-1",
            "played_at": "2026-08-03T12:00:00Z",
            "title": "Current",
        }
        old = {
            "id": "track-2",
            "played_at": "2026-01-01T12:00:00Z",
            "title": "Old",
        }

        merged = analytics._merge_recent_plays([current, old], [current], now)

        self.assertEqual(merged, [current])


if __name__ == "__main__":
    unittest.main()
