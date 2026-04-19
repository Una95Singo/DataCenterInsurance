"""Enumerate (state, metro) pairs from the cached sitemap shards.

Uses the real `data/raw/datacentermap/sitemap/dcs_*.xml` files committed
to the repo per §1.1 recon. No network. The expected 5,192 US facility
URLs → 490 unique (state, metro) pairs number is the recon-report
commitment; if the sitemaps are re-pulled and these counts drift, the
scrape scope has changed and the report needs updating.
"""

from __future__ import annotations

from pathlib import Path

from dc_scs.inventory.metros import (
    METRO_URL_TEMPLATE,
    Metro,
    enumerate_metros,
    extract_us_metros,
    iter_sitemap_urls,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SITEMAP_DIR = REPO_ROOT / "data" / "raw" / "datacentermap" / "sitemap"


def test_sitemap_shards_present():
    shards = sorted(SITEMAP_DIR.glob("dcs_*.xml"))
    assert len(shards) == 13, f"expected 13 dcs_*.xml shards, found {len(shards)}"


def test_total_sitemap_urls_worldwide():
    assert sum(1 for _ in iter_sitemap_urls(SITEMAP_DIR)) == 13_000


def test_us_facility_universe_is_5192():
    # Matches the §1.1 acceptance-gate number in the recon report.
    us_urls = [u for u in iter_sitemap_urls(SITEMAP_DIR) if "/usa/" in u]
    assert len(us_urls) == 5_192


def test_unique_metros_is_490():
    metros = enumerate_metros(SITEMAP_DIR)
    assert len(metros) == 490
    # Virginia/Manassas is in the recon sample — assert it round-trips.
    assert Metro("virginia", "manassas") in metros


def test_metros_sorted_deterministically():
    metros = enumerate_metros(SITEMAP_DIR)
    assert metros == sorted(metros)


def test_metro_url_shape():
    m = Metro("virginia", "manassas")
    assert m.url == METRO_URL_TEMPLATE.format(state="virginia", metro="manassas")
    assert m.url == "https://www.datacentermap.com/usa/virginia/manassas/"


def test_metro_pull_id_and_local_path(tmp_path: Path):
    m = Metro("texas", "dallas")
    assert m.pull_id == "dcm_metro_texas_dallas"
    assert m.local_path(tmp_path) == tmp_path / "datacentermap" / "metros" / "texas" / "dallas.html"


def test_extract_us_metros_ignores_non_us_and_malformed():
    urls = [
        "https://www.datacentermap.com/usa/virginia/manassas/10051-brickyard-wy/",
        "https://www.datacentermap.com/canada/toronto/100-gough-road/",
        "https://www.datacentermap.com/usa/virginia/",  # state listing, no metro
        "",
        "not-a-url",
    ]
    assert extract_us_metros(urls) == [Metro("virginia", "manassas")]
