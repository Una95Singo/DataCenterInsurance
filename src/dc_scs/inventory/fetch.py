"""Polite metro-page fetcher for datacentermap.com.

Not importable inside the agent sandbox — network egress is blocked.
Runs on Una's laptop via `scripts/scrape_datacentermap.py`.

Idempotency: per-metro HTML is cached under
`data/raw/datacentermap/metros/{state}/{metro}.html`. A fetch is skipped
if the file already exists and is non-empty. Manifest rows are appended
exactly once per pull_id, de-duped against rows already on disk.
"""

from __future__ import annotations

import csv
import time
from dataclasses import dataclass
from pathlib import Path

import requests

from dc_scs.manifest import MANIFEST_PATH, append_manifest_row

from .metros import Metro

# Same UA fetch_raw.py uses — default python-requests/* is 403-blocked.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
HEADERS = {"User-Agent": BROWSER_UA}

DEFAULT_DELAY_S = 2.0  # per-host politeness gap; matches fetch_raw.py
DEFAULT_TIMEOUT_S = 60


@dataclass(frozen=True)
class FetchResult:
    pull_id: str
    status: str  # "cached" | "fetched" | f"FAIL: <msg>"


def _existing_pull_ids() -> set[str]:
    if not MANIFEST_PATH.exists() or MANIFEST_PATH.stat().st_size == 0:
        return set()
    with MANIFEST_PATH.open() as f:
        return {row["pull_id"] for row in csv.DictReader(f)}


def fetch_metro(
    metro: Metro,
    raw_root: Path,
    *,
    already_logged: set[str],
    session: requests.Session | None = None,
    timeout: float = DEFAULT_TIMEOUT_S,
) -> FetchResult:
    """Fetch one metro page and append its manifest row. Idempotent."""
    dest = metro.local_path(raw_root)

    if dest.exists() and dest.stat().st_size > 0:
        status = "cached"
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        try:
            client = session or requests
            resp = client.get(metro.url, headers=HEADERS, timeout=timeout)
            resp.raise_for_status()
            tmp.write_bytes(resp.content)
            tmp.replace(dest)
        except Exception as e:  # noqa: BLE001
            if tmp.exists():
                tmp.unlink()
            return FetchResult(pull_id=metro.pull_id, status=f"FAIL: {e}")
        status = "fetched"

    if metro.pull_id not in already_logged:
        append_manifest_row(
            pull_id=metro.pull_id,
            source_name=f"datacentermap.com metro ({metro.state}/{metro.metro})",
            source_url=metro.url,
            local_path=dest,
            notes="§1.1 metro scrape; __NEXT_DATA__ payload includes full facility roster",
        )
        already_logged.add(metro.pull_id)
        status += " + manifest"
    else:
        status += " (manifest row already present)"

    return FetchResult(pull_id=metro.pull_id, status=status)


def scrape_metros(
    metros: list[Metro],
    raw_root: Path,
    *,
    delay_s: float = DEFAULT_DELAY_S,
    session: requests.Session | None = None,
    on_result=None,
) -> list[FetchResult]:
    """Loop over metros with a polite delay between non-cached fetches.

    The delay is skipped when the previous result was `cached` — caching
    does not hit the network, so sleeping would only slow re-runs.
    """
    already_logged = _existing_pull_ids()
    results: list[FetchResult] = []
    last_hit_network = False
    for metro in metros:
        if last_hit_network:
            time.sleep(delay_s)
        result = fetch_metro(
            metro, raw_root, already_logged=already_logged, session=session
        )
        last_hit_network = result.status.startswith("fetched")
        results.append(result)
        if on_result is not None:
            on_result(result)
    return results
