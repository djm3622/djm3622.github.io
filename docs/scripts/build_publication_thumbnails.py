#!/usr/bin/env python3
"""Build content-aware square thumbnails for publication figures."""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


TARGET_SIZE = 512
CANVAS_MARGIN = 20
TRIM_FUZZ = "2%"
SAFETY_MARGIN_RATIO = 0.02
GEOMETRY_PATTERN = re.compile(
    r"^(?P<width>\d+)x(?P<height>\d+)\+(?P<x>\d+)\+(?P<y>\d+)$"
)


@dataclass(frozen=True)
class ThumbnailAsset:
    source: str
    output: str


@dataclass(frozen=True)
class Geometry:
    width: int
    height: int
    x: int
    y: int


ASSETS = (
    ThumbnailAsset("policy_3_flat.png", "policy_3_flat.png"),
    ThumbnailAsset("trajectory_instance_0.gif", "trajectory_instance_0.gif"),
    ThumbnailAsset("pearl2025.png", "pearl2025.png"),
    ThumbnailAsset("ams2025.png", "ams2025.png"),
    ThumbnailAsset("bigdata2024-1.gif", "bigdata2024-1.gif"),
    ThumbnailAsset("bigdata2024-2.gif", "bigdata2024-2.gif"),
    ThumbnailAsset(
        "val_target_potential_centered_mse_vs_ratio.png",
        "val_target_potential_centered_mse_vs_ratio.png",
    ),
    ThumbnailAsset("fig_cnn_vs_adv.png", "fig_cnn_vs_adv.png"),
    ThumbnailAsset("panel3_risk_barycenter.png", "panel3_risk_barycenter.png"),
    ThumbnailAsset(
        "Specific Humidity H600_Ensemble_Spread.gif",
        "specific_humidity_h600_ensemble_spread.gif",
    ),
)


def parse_geometry(value: str) -> Geometry:
    match = GEOMETRY_PATTERN.fullmatch(value.strip())
    if match is None:
        raise ValueError(f"Invalid ImageMagick geometry: {value!r}")
    return Geometry(**{name: int(number) for name, number in match.groupdict().items()})


def expand_geometry(
    geometry: Geometry, image_width: int, image_height: int
) -> Geometry:
    margin = math.ceil(max(geometry.width, geometry.height) * SAFETY_MARGIN_RATIO)
    left = max(0, geometry.x - margin)
    top = max(0, geometry.y - margin)
    right = min(image_width, geometry.x + geometry.width + margin)
    bottom = min(image_height, geometry.y + geometry.height + margin)
    return Geometry(width=right - left, height=bottom - top, x=left, y=top)


def run(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def image_size(magick: str, source: Path) -> tuple[int, int]:
    output = run([magick, "identify", "-format", "%w %h", f"{source}[0]"])
    width, height = output.split()
    return int(width), int(height)


def content_geometry(magick: str, source: Path) -> Geometry:
    output = run(
        [
            magick,
            str(source),
            "-coalesce",
            "-background",
            "white",
            "-alpha",
            "remove",
            "-evaluate-sequence",
            "min",
            "-fuzz",
            TRIM_FUZZ,
            "-format",
            "%@",
            "info:",
        ]
    )
    return parse_geometry(output)


def build_thumbnail(magick: str, source: Path, output: Path) -> None:
    width, height = image_size(magick, source)
    crop = expand_geometry(content_geometry(magick, source), width, height)
    crop_spec = f"{crop.width}x{crop.height}+{crop.x}+{crop.y}"
    content_size = TARGET_SIZE - 2 * CANVAS_MARGIN

    command = [
        magick,
        str(source),
        "-coalesce",
        "-background",
        "white",
        "-alpha",
        "remove",
        "-crop",
        crop_spec,
        "+repage",
        "-resize",
        f"{content_size}x{content_size}",
        "-gravity",
        "center",
        "-extent",
        f"{TARGET_SIZE}x{TARGET_SIZE}",
    ]
    if output.suffix.lower() == ".gif":
        command.extend(["-layers", "Optimize"])
    command.append(str(output))
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "images",
    )
    parser.add_argument(
        "--asset",
        action="append",
        choices=[asset.output for asset in ASSETS],
        help="Build only the named output asset; may be specified more than once.",
    )
    args = parser.parse_args()

    magick = shutil.which("magick")
    if magick is None:
        raise SystemExit("ImageMagick is required; install the `magick` executable.")

    output_dir = args.images_dir / "publication_thumbnails"
    output_dir.mkdir(parents=True, exist_ok=True)
    selected_assets = (
        [asset for asset in ASSETS if asset.output in args.asset]
        if args.asset
        else ASSETS
    )
    for asset in selected_assets:
        source = args.images_dir / asset.source
        output = output_dir / asset.output
        build_thumbnail(magick, source, output)
        print(f"Built {output.relative_to(args.images_dir.parent.parent)}", flush=True)


if __name__ == "__main__":
    main()
