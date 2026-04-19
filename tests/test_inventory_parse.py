"""Parse + flatten a real datacentermap.com metro page.

Fixture: `data/raw/datacentermap/samples/usa_virginia_manassas.html` —
the committed recon sample. The Manassas metro has 97 features in
`mapdata.dcs` (statistics.dcs = 96 real + 1 `market-unmapped` sentinel).
After filtering to `maptype in {dc, dc-unmapped}`, we expect 96 records.
"""

from __future__ import annotations

from pathlib import Path

from dc_scs.inventory.parse import (
    FACILITY_MAPTYPES,
    extract_next_data,
    flatten_features,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MANASSAS_HTML = (
    REPO_ROOT
    / "data"
    / "raw"
    / "datacentermap"
    / "samples"
    / "usa_virginia_manassas.html"
)


def _load():
    return extract_next_data(MANASSAS_HTML.read_text())


def test_extract_next_data_returns_page_props():
    data = _load()
    assert "props" in data
    assert "pageProps" in data["props"]
    assert "mapdata" in data["props"]["pageProps"]


def test_extract_next_data_raises_on_missing_tag():
    import pytest

    with pytest.raises(ValueError):
        extract_next_data("<html><body>no script here</body></html>")


def test_manassas_has_97_raw_features():
    data = _load()
    features = data["props"]["pageProps"]["mapdata"]["dcs"]
    assert len(features) == 97


def test_flatten_drops_market_unmapped_sentinel():
    records = list(
        flatten_features(_load(), source_state="virginia", source_metro="manassas")
    )
    # 97 raw features - 1 market-unmapped sentinel = 96 facility records,
    # matching `mapdata.statistics.dcs`.
    assert len(records) == 96
    assert all(r["maptype"] in FACILITY_MAPTYPES for r in records)


def test_flatten_lifts_all_expected_fields():
    records = list(
        flatten_features(_load(), source_state="virginia", source_metro="manassas")
    )
    # The "9905 Godwin Drive (IAD53)" record was the inspected example in
    # the recon report — pin its shape.
    target = next(r for r in records if r["id"] == 10818)
    assert target["name"] == "9905 Godwin Drive (IAD53)"
    assert target["companyname"] == "Digital Realty"
    assert target["companylink"] == "digital-realty-trust"
    assert target["listingtype"] == "Facility"
    assert target["capacitytype"] == "Colocation"
    assert target["maptype"] == "dc"
    assert target["address"] == "9905 Godwin Dr"
    assert target["city"] == "Manassas"
    assert target["state"] == "Virginia"
    assert target["country"] == "USA"
    assert target["postal"] == "20110"
    assert target["latitude"] == 38.7404104
    assert target["longitude"] == -77.5040386
    assert target["source_state"] == "virginia"
    assert target["source_metro"] == "manassas"


def test_flatten_retains_dc_unmapped_as_real_facilities():
    records = list(
        flatten_features(_load(), source_state="virginia", source_metro="manassas")
    )
    unmapped = [r for r in records if r["maptype"] == "dc-unmapped"]
    # Three QTS Manassas DC* listings are flagged dc-unmapped on the
    # Manassas fixture (real facilities, synthetic coords).
    assert len(unmapped) == 3
    assert all(r["companyname"] == "QTS Data Centers" for r in unmapped)


def test_facility_id_uniqueness_within_metro():
    records = list(
        flatten_features(_load(), source_state="virginia", source_metro="manassas")
    )
    ids = [r["id"] for r in records if r["id"] is not None]
    assert len(ids) == len(set(ids))
