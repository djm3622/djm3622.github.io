from __future__ import annotations

import datetime as dt
import importlib.util
import unittest
from pathlib import Path
from typing import Any, Mapping

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "update_spotify_pick.py"
SPEC = importlib.util.spec_from_file_location("update_spotify_pick", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
spotify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(spotify)


class FakeClient:
    def __init__(self) -> None:
        self.responses: dict[str, Mapping[str, Any]] = {
            "/me": {"id": "david"},
        }
        self.pages: dict[str, list[Mapping[str, Any]]] = {
            "/me/playlists?limit=50": [
                {
                    "id": "followed",
                    "name": "Followed only",
                    "owner": {"id": "someone-else"},
                    "collaborative": False,
                    "items": {"total": 1},
                },
                {
                    "id": "owned",
                    "name": "My playlist",
                    "owner": {"id": "david"},
                    "collaborative": False,
                    "items": {"total": 2},
                    "images": [{"url": "https://example.com/playlist.jpg"}],
                },
            ],
            "/playlists/owned/items?limit=50": [
                {"item": {"id": None, "type": "track", "name": "Local"}},
                {
                    "item": {
                        "id": "track-1",
                        "type": "track",
                        "name": "Selected song",
                        "artists": [{"name": "Selected artist"}],
                        "album": {
                            "id": "album-1",
                            "name": "Selected album",
                            "images": [{"url": "https://example.com/album.jpg"}],
                        },
                        "is_local": False,
                        "is_playable": True,
                    }
                },
            ],
        }

    def get(self, path: str) -> Mapping[str, Any]:
        return self.responses[path]

    def get_all(self, path: str) -> list[Mapping[str, Any]]:
        return self.pages[path]


class ChooseSelectionTests(unittest.TestCase):
    def test_selects_owned_playlist_and_playable_track(self) -> None:
        selection = spotify.choose_selection(
            FakeClient(), dt.date(2026, 8, 2), {}, ["owned"]
        )

        self.assertTrue(selection["enabled"])
        self.assertEqual(selection["playlist"]["id"], "owned")
        self.assertEqual(selection["track"]["id"], "track-1")
        self.assertEqual(selection["track"]["artist_label"], "Selected artist")
        self.assertEqual(selection["playlist"]["image_url"], "https://example.com/playlist.jpg")
        self.assertEqual(
            selection["playlist"]["description"],
            "A 1-track collection centered on Selected artist.",
        )
        self.assertEqual(selection["track"]["image_url"], "https://example.com/album.jpg")
        self.assertEqual(selection["track"]["album"]["name"], "Selected album")

    def test_playlist_allowlist_is_strict(self) -> None:
        with self.assertRaisesRegex(spotify.SpotifyError, "None of the configured"):
            spotify.choose_selection(
                FakeClient(), dt.date(2026, 8, 2), {}, ["followed"]
            )

    def test_daily_seed_is_reproducible(self) -> None:
        first = spotify._daily_random(dt.date(2026, 8, 2)).random()
        second = spotify._daily_random(dt.date(2026, 8, 2)).random()

        self.assertEqual(first, second)

    def test_playlist_description_summarizes_content(self) -> None:
        tracks = [
            {"artists": [{"name": "Alpha"}, {"name": "Beta"}]},
            {"artists": [{"name": "Alpha"}]},
            {"artists": [{"name": "Gamma"}]},
            {"artists": [{"name": "Delta"}]},
        ]

        self.assertEqual(
            spotify._describe_playlist(tracks),
            "A 4-track mix spanning 4 artists, led by Alpha, Beta, and Gamma.",
        )


if __name__ == "__main__":
    unittest.main()
