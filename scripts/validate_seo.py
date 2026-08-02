#!/usr/bin/env python3
"""Validate generated SEO metadata for the David Millard research site."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET


SITE_URL = "https://djm3622.github.io"
PROFILE_IMAGE = f"{SITE_URL}/assets/images/my_pfp.jpg"
PROFILE_URLS = [
    "https://github.com/djm3622",
    "https://scholar.google.com/citations?user=LEs7ELgAAAAJ&hl=en",
    "https://www.linkedin.com/in/david-millard-77b214243/",
]


class GeneratedPageParser(HTMLParser):
    """Collect the metadata and semantic elements used by the checks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.titles: List[str] = []
        self.h1s: List[str] = []
        self.metas: List[Dict[str, Optional[str]]] = []
        self.links: List[Dict[str, Optional[str]]] = []
        self.anchors: List[Dict[str, Optional[str]]] = []
        self.images: List[Dict[str, Optional[str]]] = []
        self.jsonld: List[str] = []
        self.ids: set[str] = set()
        self._title: Optional[List[str]] = None
        self._h1: Optional[List[str]] = None
        self._jsonld: Optional[List[str]] = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(str(attributes["id"]))
        if tag == "title":
            self._title = []
        elif tag == "h1":
            self._h1 = []
        elif tag == "meta":
            self.metas.append(attributes)
        elif tag == "link":
            self.links.append(attributes)
        elif tag == "a":
            self.anchors.append(attributes)
        elif tag == "img":
            self.images.append(attributes)
        elif tag == "script" and attributes.get("type") == "application/ld+json":
            self._jsonld = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self._title is not None:
            self.titles.append("".join(self._title).strip())
            self._title = None
        elif tag == "h1" and self._h1 is not None:
            self.h1s.append(" ".join("".join(self._h1).split()))
            self._h1 = None
        elif tag == "script" and self._jsonld is not None:
            self.jsonld.append("".join(self._jsonld).strip())
            self._jsonld = None

    def handle_data(self, data: str) -> None:
        if self._title is not None:
            self._title.append(data)
        if self._h1 is not None:
            self._h1.append(data)
        if self._jsonld is not None:
            self._jsonld.append(data)


def parse_page(path: Path) -> GeneratedPageParser:
    parser = GeneratedPageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def meta_values(parser: GeneratedPageParser, key: str, value: str) -> List[str]:
    return [
        str(item.get("content") or "")
        for item in parser.metas
        if item.get(key) == value
    ]


def canonical_values(parser: GeneratedPageParser) -> List[str]:
    return [
        str(item.get("href") or "")
        for item in parser.links
        if "canonical" in str(item.get("rel") or "").split()
    ]


def validate_all_html(site_dir: Path) -> Dict[Path, GeneratedPageParser]:
    html_paths = sorted(site_dir.rglob("*.html"))
    if not html_paths:
        raise AssertionError("No generated HTML files found")

    required_meta = [
        ("name", "description"),
        ("property", "og:title"),
        ("property", "og:description"),
        ("property", "og:url"),
        ("property", "og:site_name"),
        ("property", "og:type"),
        ("property", "og:image"),
        ("name", "twitter:card"),
        ("name", "twitter:title"),
        ("name", "twitter:description"),
        ("name", "twitter:image"),
    ]
    parsed: Dict[Path, GeneratedPageParser] = {}
    for path in html_paths:
        page = parse_page(path)
        parsed[path] = page
        assert len(page.titles) == 1, f"{path}: expected one title, got {page.titles}"
        descriptions = meta_values(page, "name", "description")
        assert len(descriptions) == 1 and descriptions[0].strip(), (
            f"{path}: expected one nonempty description"
        )
        canonicals = canonical_values(page)
        assert len(canonicals) == 1, f"{path}: expected one canonical, got {canonicals}"
        canonical = canonicals[0]
        assert canonical.startswith(f"{SITE_URL}/"), f"{path}: bad canonical {canonical}"
        assert not any(part in canonical for part in ("/docs/", "/_site/", "index.html"))
        assert "//" not in canonical[len("https://") :], f"{path}: duplicate slash"
        for key, value in required_meta:
            values = meta_values(page, key, value)
            assert len(values) == 1 and values[0].strip(), (
                f"{path}: expected one nonempty {value}, got {values}"
            )
        assert len(page.jsonld) == 1, f"{path}: expected one JSON-LD block"
        json.loads(page.jsonld[0])
    return parsed


def validate_major_pages(
    site_dir: Path, parsed: Dict[Path, GeneratedPageParser]
) -> None:
    expected = {
        site_dir / "index.html": (
            "David Millard | Machine Learning Researcher",
            f"{SITE_URL}/",
            "ProfilePage",
        ),
        site_dir / "about/index.html": (
            "About | David Millard",
            f"{SITE_URL}/about/",
            "WebPage",
        ),
        site_dir / "publications/index.html": (
            "Publications | David Millard",
            f"{SITE_URL}/publications/",
            "WebPage",
        ),
        site_dir / "presentations/index.html": (
            "Presentations | David Millard",
            f"{SITE_URL}/presentations/",
            "WebPage",
        ),
    }
    descriptions: List[str] = []
    for path, (title, canonical, schema_type) in expected.items():
        page = parsed[path]
        assert page.titles == [title], f"{path}: unexpected title {page.titles}"
        assert canonical_values(page) == [canonical], f"{path}: unexpected canonical"
        assert json.loads(page.jsonld[0])["@type"] == schema_type
        descriptions.append(meta_values(page, "name", "description")[0])
    assert len(set(descriptions)) == len(descriptions), "Major descriptions must be unique"


def validate_identity_and_regressions(
    site_dir: Path, parsed: Dict[Path, GeneratedPageParser]
) -> None:
    home = parsed[site_dir / "index.html"]
    assert home.h1s == ["David Millard"], f"Unexpected homepage H1s: {home.h1s}"
    profile = json.loads(home.jsonld[0])["mainEntity"]
    assert profile["@type"] == "Person"
    assert profile["name"] == "David Millard"
    assert profile["image"] == PROFILE_IMAGE
    assert profile["jobTitle"] == "Ph.D. Student in Electrical and Computer Engineering"
    assert profile["affiliation"]["name"] == "University of Rochester"
    assert profile["sameAs"] == PROFILE_URLS

    about = parsed[site_dir / "about/index.html"]
    profile_images = [
        image for image in about.images if image.get("src") == "/assets/images/my_pfp.jpg"
    ]
    assert len(profile_images) == 1 and profile_images[0].get("alt") == "David Millard"

    hrefs = {str(anchor.get("href") or "") for anchor in home.anchors}
    for href in [
        "/",
        "/about/",
        "/publications/",
        "/presentations/",
        "mailto:david.millard@rochester.edu",
        "/assets/davidmillard_resume.pdf",
    ]:
        assert href in hrefs, f"Missing homepage link {href}"
    for href in PROFILE_URLS:
        matches = [anchor for anchor in home.anchors if anchor.get("href") == href]
        assert len(matches) == 1, f"Missing or duplicate identity link {href}"
        rel = set(str(matches[0].get("rel") or "").split())
        assert {"me", "noopener"} <= rel and matches[0].get("target") == "_blank"

    home_text = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "theme-toggle" in home.ids
    assert "prefers-color-scheme: dark" in home_text
    assert "david-millard-theme" in home_text

    publication_text = (site_dir / "publications/index.html").read_text(encoding="utf-8")
    for href in [
        "https://arxiv.org/abs/2501.10750",
        "https://openreview.net/forum?id=0twOHJg60V",
        "https://proceedings.mlr.press/v331/millard26a.html",
    ]:
        assert href in publication_text, f"Missing publication link {href}"

    presentation_text = (site_dir / "presentations/index.html").read_text(
        encoding="utf-8"
    )
    for href in [
        "/assets/presentations/maad_week3.pdf",
        "/assets/presentations/maad_week3.pptx",
    ]:
        assert href in presentation_text, f"Missing presentation link {href}"
        assert (site_dir / href.lstrip("/")).is_file(), f"Missing asset {href}"
    assert (site_dir / "assets/davidmillard_resume.pdf").is_file()
    assert (site_dir / "assets/images/my_pfp.jpg").is_file()


def validate_post(site_dir: Path, parsed: Dict[Path, GeneratedPageParser]) -> None:
    path = (
        site_dir
        / "conference/research/update/2026/06/17/presented-federated-irl-work-at-l4dc.html"
    )
    post = parsed[path]
    assert post.titles == ["Presented Federated IRL Work at L4DC 2026 | David Millard"]
    assert json.loads(post.jsonld[0])["@type"] == "BlogPosting"


def validate_discovery_files(site_dir: Path) -> int:
    robots = (site_dir / "robots.txt").read_text(encoding="utf-8")
    assert robots == (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )

    root = ET.parse(site_dir / "sitemap.xml").getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = {node.text or "" for node in root.findall("sm:url/sm:loc", namespace)}
    for url in [
        f"{SITE_URL}/",
        f"{SITE_URL}/about/",
        f"{SITE_URL}/publications/",
        f"{SITE_URL}/presentations/",
        f"{SITE_URL}/conference/research/update/2026/06/17/"
        "presented-federated-irl-work-at-l4dc.html",
    ]:
        assert url in locations, f"Missing sitemap URL {url}"
    assert not any(
        "/assets/" in url
        or "/docs/" in url
        or "/_site/" in url
        or "index.html" in url
        for url in locations
    ), f"Unexpected sitemap URL: {locations}"
    return len(locations)


def validate_rendering(site_dir: Path) -> None:
    for path in site_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html", ".xml", ".txt"}:
            text = path.read_text(encoding="utf-8")
            assert "{{" not in text and "{%" not in text, f"Unrendered Liquid in {path}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", type=Path, help="Generated Jekyll destination")
    args = parser.parse_args()
    site_dir = args.site_dir.resolve()
    parsed = validate_all_html(site_dir)
    validate_major_pages(site_dir, parsed)
    validate_identity_and_regressions(site_dir, parsed)
    validate_post(site_dir, parsed)
    sitemap_count = validate_discovery_files(site_dir)
    validate_rendering(site_dir)
    print(f"PASS: validated {len(parsed)} generated HTML pages")
    print(f"PASS: validated {sitemap_count} sitemap URLs")
    print("PASS: metadata, canonicals, JSON-LD, H1, discovery, links, and theme checks")


if __name__ == "__main__":
    main()
