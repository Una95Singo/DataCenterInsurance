"""Scrape datacentermap.com metro pages → facility JSONL.

Run this on a networked machine (the agent sandbox blocks egress). Two
phases:

  1. Enumerate unique (state, metro) pairs from the already-cached
     sitemap shards under `data/raw/datacentermap/sitemap/dcs_*.xml`.
  2. For each metro: GET `https://www.datacentermap.com/usa/{state}/{metro}/`
     with a browser UA and a 2 s per-request politeness gap, save the
     raw HTML under `data/raw/datacentermap/metros/{state}/{metro}.html`,
     and append one manifest row per metro.

Output: `data/processed/datacentermap/facilities.jsonl`, built by
parsing the saved metro HTML (pure local step — safe to re-run offline).

Flags:
  --subset N      only fetch the first N metros (alphabetical by
                  state/metro; use for smoke tests before the full run).
  --skip-build    fetch only; do not rebuild the JSONL.
  --build-only    skip the network phase; just rebuild the JSONL from
                  whatever metro HTML is already on disk.
  --delay SEC     override the 2 s politeness gap.

Idempotency: already-cached metros (file on disk, non-empty) are skipped;
manifest rows are de-duped by pull_id. Re-running after a successful pull
is effectively a no-op.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from dc_scs.inventory.build import build_facilities_jsonl  # noqa: E402
from dc_scs.inventory.fetch import DEFAULT_DELAY_S, scrape_metros  # noqa: E402
from dc_scs.inventory.metros import enumerate_metros  # noqa: E402

SITEMAP_DIR = REPO_ROOT / "data" / "raw" / "datacentermap" / "sitemap"
RAW_ROOT = REPO_ROOT / "data" / "raw"
OUT_JSONL = REPO_ROOT / "data" / "processed" / "datacentermap" / "facilities.jsonl"


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--subset", type=int, default=None,
                   help="only fetch the first N metros (smoke test)")
    p.add_argument("--skip-build", action="store_true",
                   help="fetch only; do not rebuild the JSONL")
    p.add_argument("--build-only", action="store_true",
                   help="skip the network phase; rebuild JSONL from cached HTML")
    p.add_argument("--delay", type=float, default=DEFAULT_DELAY_S,
                   help=f"per-request politeness gap in seconds (default {DEFAULT_DELAY_S})")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])

    metros = enumerate_metros(SITEMAP_DIR)
    print(f"scrape_datacentermap: {len(metros)} unique (state, metro) pairs from {SITEMAP_DIR.relative_to(REPO_ROOT)}")

    if args.subset is not None:
        metros = metros[: args.subset]
        print(f"  --subset: limited to first {len(metros)} metros")

    if not args.build_only:
        def _log(result):
            print(f"  [{result.pull_id}] {result.status}")
        results = scrape_metros(metros, RAW_ROOT, delay_s=args.delay, on_result=_log)
        failures = [r for r in results if r.status.startswith("FAIL")]
        if failures:
            print(f"\n{len(failures)} failure(s):")
            for r in failures:
                print(f"  {r.pull_id}: {r.status}")
            return 1

    if args.skip_build:
        print("\n--skip-build: not rebuilding JSONL")
        return 0

    print(f"\nBuilding {OUT_JSONL.relative_to(REPO_ROOT)} ...")
    result = build_facilities_jsonl(RAW_ROOT / "datacentermap" / "metros", OUT_JSONL)
    print(
        f"  {result.metros_processed} metros parsed, "
        f"{result.records_written} facility records written, "
        f"{result.duplicates_dropped} duplicates dropped"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
