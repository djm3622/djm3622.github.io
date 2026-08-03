import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_music_analytics.py"
SPEC = importlib.util.spec_from_file_location("build_music_analytics", MODULE_PATH)
analytics = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(analytics)


class MusicAnalyticsHelpersTest(unittest.TestCase):
    def test_duration_label_rounds_to_nearest_second(self) -> None:
        self.assertEqual(analytics._duration_label(58_363), "0:58")
        self.assertEqual(analytics._duration_label(485_598), "8:06")

    def test_compact_count_uses_readable_suffixes(self) -> None:
        self.assertEqual(analytics._compact_count(18_265), "18.3K")
        self.assertEqual(analytics._compact_count(3_091_864), "3.1M")

    def test_primary_artist_uses_spotify_credit_separator(self) -> None:
        self.assertEqual(analytics._primary_artist("MOTL,\u00a0KUTE,\u00a0MUPP"), "MOTL")
        self.assertEqual(analytics._primary_artist("PinkPantheress"), "PinkPantheress")

    def test_percentage_handles_empty_samples(self) -> None:
        self.assertEqual(analytics._rounded_percentage(3, 8), 37.5)
        self.assertEqual(analytics._rounded_percentage(0, 0), 0.0)


if __name__ == "__main__":
    unittest.main()
