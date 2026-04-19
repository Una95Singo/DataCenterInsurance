"""End-to-end build of facilities.jsonl from cached metro HTML."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from dc_scs.inventory.build import build_facilities_jsonl

REPO_ROOT = Path(__file__).resolve().parents[1]
MANASSAS_HTML = (
    REPO_ROOT
    / "data"
    / "raw"
    / "datacentermap"
    / "samples"
    / "usa_virginia_manassas.html"
)


def _stage_metros(root: Path, mapping: dict[str, str]) -> Path:
    """Build tmp `metros/{state}/{metro}.html` from copies of MANASSAS_HTML.

    `mapping` is {state: metro} — every staged file is the Manassas fixture
    under a different (state, metro) name, so duplicate IDs across 'metros'
    exercise the de-dup logic.
    """
    metros_dir = root / "metros"
    for state, metro in mapping.items():
        state_dir = metros_dir / state
        state_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(MANASSAS_HTML, state_dir / f"{metro}.html")
    return metros_dir


def test_build_single_metro(tmp_path: Path):
    metros_dir = _stage_metros(tmp_path, {"virginia": "manassas"})
    out = tmp_path / "facilities.jsonl"
    result = build_facilities_jsonl(metros_dir, out)

    assert result.metros_processed == 1
    assert result.records_written == 96
    assert result.duplicates_dropped == 0
    assert result.output_path == out
    assert out.exists()

    records = [json.loads(line) for line in out.read_text().splitlines()]
    assert len(records) == 96
    assert {r["source_state"] for r in records} == {"virginia"}
    assert {r["source_metro"] for r in records} == {"manassas"}


def test_build_dedupes_across_metros(tmp_path: Path):
    # Same roster staged under two metro slugs -> 96 unique IDs kept,
    # 96 dropped as duplicates.
    metros_dir = _stage_metros(tmp_path, {"virginia": "manassas", "maryland": "baltimore"})
    out = tmp_path / "facilities.jsonl"
    result = build_facilities_jsonl(metros_dir, out)

    assert result.metros_processed == 2
    assert result.records_written == 96
    assert result.duplicates_dropped == 96


def test_build_handles_missing_metros_dir(tmp_path: Path):
    # Nothing fetched yet: build is a no-op, not an error.
    result = build_facilities_jsonl(tmp_path / "metros", tmp_path / "facilities.jsonl")
    assert result.metros_processed == 0
    assert result.records_written == 0
