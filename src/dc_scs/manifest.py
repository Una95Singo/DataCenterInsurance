"""Raw-data manifest helpers.

Every file written under data/raw/ must have a matching row in
data/raw/manifest.csv. This module provides the append helper and the
hashing primitive so all phase-1 fetchers go through one code path.
"""

from __future__ import annotations

import csv
import hashlib
from datetime import UTC, datetime
from pathlib import Path

MANIFEST_FIELDS = (
    "pull_id",
    "source_name",
    "source_url",
    "pulled_at",
    "sha256",
    "bytes",
    "local_path",
    "notes",
)

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"
MANIFEST_PATH = RAW_DIR / "manifest.csv"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_manifest_row(
    *,
    pull_id: str,
    source_name: str,
    source_url: str,
    local_path: Path,
    notes: str = "",
) -> dict:
    local_path = Path(local_path)
    row = {
        "pull_id": pull_id,
        "source_name": source_name,
        "source_url": source_url,
        "pulled_at": utc_now_iso(),
        "sha256": sha256_file(local_path),
        "bytes": local_path.stat().st_size,
        "local_path": str(local_path.relative_to(REPO_ROOT)),
        "notes": notes,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not MANIFEST_PATH.exists() or MANIFEST_PATH.stat().st_size == 0
    with MANIFEST_PATH.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return row
