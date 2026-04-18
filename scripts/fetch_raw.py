"""Fetch Phase 1 raw sources listed in scripts/raw_sources.yaml.

Intended to be run on a machine that has outbound network access (the agent
sandbox does not). For each entry under `sources:` it downloads the URL to
`local_path`, computes SHA256, and appends a row to data/raw/manifest.csv
via dc_scs.manifest.append_manifest_row.

Idempotency: if local_path already exists and is non-empty, the download is
skipped. If a manifest row with the same pull_id already exists, no duplicate
row is written. Re-running after a successful pull is a no-op.

Exit codes:
  0 — every active source present locally (either freshly fetched or cached)
  1 — at least one source failed
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from dc_scs.manifest import MANIFEST_PATH, append_manifest_row  # noqa: E402

REGISTRY = REPO_ROOT / "scripts" / "raw_sources.yaml"
CHUNK = 1 << 16
TIMEOUT = 60


def existing_pull_ids() -> set[str]:
    if not MANIFEST_PATH.exists() or MANIFEST_PATH.stat().st_size == 0:
        return set()
    with MANIFEST_PATH.open() as f:
        return {row["pull_id"] for row in csv.DictReader(f)}


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        with tmp.open("wb") as f:
            for chunk in r.iter_content(chunk_size=CHUNK):
                if chunk:
                    f.write(chunk)
    tmp.replace(dest)


def fetch_one(entry: dict, already_logged: set[str]) -> tuple[str, str]:
    pull_id = entry["pull_id"]
    local_path = REPO_ROOT / entry["local_path"]

    if local_path.exists() and local_path.stat().st_size > 0:
        status = "cached"
    else:
        try:
            download(entry["url"], local_path)
        except Exception as e:  # noqa: BLE001
            return pull_id, f"FAIL: {e}"
        status = "fetched"

    if pull_id not in already_logged:
        append_manifest_row(
            pull_id=pull_id,
            source_name=entry["source_name"],
            source_url=entry["url"],
            local_path=local_path,
            notes=entry.get("notes", ""),
        )
        already_logged.add(pull_id)
        status += " + manifest"
    else:
        status += " (manifest row already present)"

    return pull_id, status


def main() -> int:
    with REGISTRY.open() as f:
        registry = yaml.safe_load(f)

    sources = registry.get("sources") or []
    todo = registry.get("todo") or []

    print(f"fetch_raw: {len(sources)} active sources, {len(todo)} TODO")
    print(f"           manifest -> {MANIFEST_PATH.relative_to(REPO_ROOT)}\n")

    already_logged = existing_pull_ids()
    results: list[tuple[str, str]] = []
    for entry in sources:
        pull_id, status = fetch_one(entry, already_logged)
        print(f"  [{pull_id}] {status}")
        results.append((pull_id, status))

    failures = [r for r in results if r[1].startswith("FAIL")]
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for pull_id, status in failures:
            print(f"  {pull_id}: {status}")
        return 1

    if todo:
        print(f"\n{len(todo)} source(s) still TODO (see scripts/raw_sources.yaml).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
