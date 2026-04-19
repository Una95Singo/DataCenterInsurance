"""Enumerate the (state, metro) universe from datacentermap.com sitemaps.

The site publishes 13 `dcs_*.xml` sub-sitemaps listing every facility URL
worldwide. Each US facility URL has the shape
`https://www.datacentermap.com/usa/{state}/{metro}/{slug}/`. Collapsing on
(state, metro) reduces the ~5,192 US facility URLs to ~490 unique metro
listings — which is what §1.1's scrape iterates over.

This module has no network dependency; it only parses locally-cached
sitemap XML under `data/raw/datacentermap/sitemap/`.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import NamedTuple

SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# `/usa/{state}/{metro}/{facility-slug}/` — the four-segment facility URL
# shape. The alternatives (state-listing `/usa/{state}/` and metro-listing
# `/usa/{state}/{metro}/`) never appear in the dcs_*.xml shards, per the
# recon report, so we only need to recognise the facility shape here.
_FACILITY_URL = re.compile(r"^https?://[^/]+/usa/([^/]+)/([^/]+)/([^/]+)/?$")

METRO_URL_TEMPLATE = "https://www.datacentermap.com/usa/{state}/{metro}/"


class Metro(NamedTuple):
    state: str
    metro: str

    @property
    def url(self) -> str:
        return METRO_URL_TEMPLATE.format(state=self.state, metro=self.metro)

    @property
    def pull_id(self) -> str:
        return f"dcm_metro_{self.state}_{self.metro}"

    def local_path(self, raw_root: Path) -> Path:
        return raw_root / "datacentermap" / "metros" / self.state / f"{self.metro}.html"


def iter_sitemap_urls(sitemap_dir: Path) -> Iterator[str]:
    """Yield every `<loc>` URL across all dcs_*.xml shards in sitemap_dir."""
    for shard in sorted(sitemap_dir.glob("dcs_*.xml")):
        tree = ET.parse(shard)
        for loc in tree.getroot().findall(".//s:loc", SITEMAP_NS):
            if loc.text:
                yield loc.text.strip()


def extract_us_metros(urls: Iterable[str]) -> list[Metro]:
    """Collapse US facility URLs to unique (state, metro) pairs.

    Returns the list sorted by (state, metro) for deterministic ordering.
    Non-US URLs and any URL that doesn't match the four-segment facility
    shape are silently skipped.
    """
    seen: set[Metro] = set()
    for url in urls:
        m = _FACILITY_URL.match(url)
        if not m:
            continue
        state, metro, _slug = m.groups()
        seen.add(Metro(state=state, metro=metro))
    return sorted(seen)


def enumerate_metros(sitemap_dir: Path) -> list[Metro]:
    """End-to-end: sitemap_dir → sorted list of unique US metros."""
    return extract_us_metros(iter_sitemap_urls(sitemap_dir))
