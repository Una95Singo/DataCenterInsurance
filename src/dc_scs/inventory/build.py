"""Build the facility JSONL from saved metro HTML pages.

Inputs:  data/raw/datacentermap/metros/{state}/{metro}.html   (raw scrape)
Output:  data/processed/datacentermap/facilities.jsonl        (flat records)

The raw HTML is the committed source of truth; this step is a pure
transformation that can be regenerated on any machine from the cache.
Duplicate facility IDs are de-duplicated — a single facility can appear
on more than one metro page when the site's metro boundaries overlap
(e.g. ashburn/leesburg). The first occurrence wins and an audit count
of drops is returned.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from .parse import extract_next_data, flatten_features


@dataclass(frozen=True)
class BuildResult:
    metros_processed: int
    records_written: int
    duplicates_dropped: int
    output_path: Path


def _iter_metro_files(metros_dir: Path) -> Iterator[tuple[str, str, Path]]:
    """Yield (state, metro, path) for every `{state}/{metro}.html` under metros_dir."""
    if not metros_dir.exists():
        return
    for state_dir in sorted(p for p in metros_dir.iterdir() if p.is_dir()):
        state = state_dir.name
        for html in sorted(state_dir.glob("*.html")):
            yield state, html.stem, html


def build_facilities_jsonl(metros_dir: Path, out_path: Path) -> BuildResult:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seen_ids: set[int] = set()
    metros_processed = 0
    written = 0
    dupes = 0

    with out_path.open("w") as out:
        for state, metro, html_path in _iter_metro_files(metros_dir):
            metros_processed += 1
            next_data = extract_next_data(html_path.read_text())
            for record in flatten_features(
                next_data, source_state=state, source_metro=metro
            ):
                fid = record.get("id")
                if fid is not None and fid in seen_ids:
                    dupes += 1
                    continue
                if fid is not None:
                    seen_ids.add(fid)
                out.write(json.dumps(record, separators=(",", ":")) + "\n")
                written += 1

    return BuildResult(
        metros_processed=metros_processed,
        records_written=written,
        duplicates_dropped=dupes,
        output_path=out_path,
    )
