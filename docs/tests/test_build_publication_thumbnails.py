import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "build_publication_thumbnails.py"
)
SPEC = importlib.util.spec_from_file_location("build_publication_thumbnails", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PublicationThumbnailGeometryTests(unittest.TestCase):
    def test_parse_geometry(self):
        geometry = MODULE.parse_geometry("1659x738+225+15")
        self.assertEqual(
            geometry,
            MODULE.Geometry(width=1659, height=738, x=225, y=15),
        )

    def test_expand_geometry_preserves_image_bounds(self):
        geometry = MODULE.Geometry(width=905, height=866, x=0, y=0)
        expanded = MODULE.expand_geometry(geometry, 906, 866)
        self.assertEqual(
            expanded,
            MODULE.Geometry(width=906, height=866, x=0, y=0),
        )

    def test_expand_geometry_adds_safety_margin(self):
        geometry = MODULE.Geometry(width=370, height=369, x=143, y=58)
        expanded = MODULE.expand_geometry(geometry, 640, 480)
        self.assertEqual(
            expanded,
            MODULE.Geometry(width=386, height=385, x=135, y=50),
        )


if __name__ == "__main__":
    unittest.main()
