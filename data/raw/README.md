# Raw Data

Source-of-truth pulls cached from upstream URLs. Files in this directory are
gitignored except `manifest.csv` and this README.

## Manifest format

`manifest.csv` records every raw pull. Columns:

- `pull_id` — short stable id for the pull (e.g. `spc_tornado_2026q1`)
- `source_name` — human-readable source name
- `source_url` — fetched URL
- `pulled_at` — ISO-8601 UTC timestamp
- `sha256` — hex digest of the file contents
- `bytes` — file size in bytes
- `local_path` — path under the repo root (e.g. `data/raw/spc/...`)
- `notes` — free-form

## Reproducibility rule

Every file under `data/raw/` must have a matching manifest row. Phase 2 audit
will enforce this; Phase 1 fetchers must use `dc_scs.manifest.append_manifest_row`
to register every pull.

## Hand-upload procedure (temporary, while sandbox egress is blocked)

See `docs/deviations.md` (2026-04-18). Until the agent sandbox can reach
external hosts, raw files are uploaded via the GitHub web UI. Per file:

1. Upload the file to `data/raw/<source>/` (a per-source `.gitignore`
   exception must be added first, e.g. `!/data/raw/spc/**`).
2. Append a row to `manifest.csv` with:
   - `pull_id` — short stable id (e.g. `spc_tornado_1950_2023`)
   - `source_name` — e.g. `NOAA SPC tornado database`
   - `source_url` — the URL the file was fetched from
   - `pulled_at` — ISO-8601 UTC timestamp of the download
   - `sha256` — hex digest (GitHub shows this on the file page; or `shasum -a 256 <file>`)
   - `bytes` — file size in bytes (GitHub shows this on the file page)
   - `local_path` — repo-relative path (e.g. `data/raw/spc/1950-2023_actual_tornadoes.csv`)
   - `notes` — e.g. `hand-uploaded via GitHub UI; sandbox egress blocked`

### Pre-filled row for the SPC tornado CSV

Paste this into `manifest.csv` after upload, then fill in `<SHA256>` and `<BYTES>`:

```
spc_tornado_1950_2024,NOAA SPC tornado database,https://www.spc.noaa.gov/wcm/data/1950-2024_actual_tornadoes.csv,2026-04-19T00:00:00Z,<SHA256>,<BYTES>,data/raw/spc/1950-2024_actual_tornadoes.csv,hand-uploaded via GitHub UI; sandbox egress blocked
```

## datacentermap.com metro scrape (§1.1)

Cached HTML layout:

```
data/raw/datacentermap/
  robots.txt                 # crawl policy
  sitemap.xml                # index of sub-sitemaps
  sitemap/dcs_*.xml          # 13 sharded facility URL lists
  sitemap/geos_*.xml         # 3 sharded geography URL lists
  samples/                   # recon samples (state, metro, facility)
  metros/{state}/{metro}.html    # 490 metro pages produced by scrape-dcm
```

Run from a networked machine:

```
make scrape-dcm                                   # full run (~16 min)
python scripts/scrape_datacentermap.py --subset 3 # smoke test
python scripts/scrape_datacentermap.py --build-only  # just rebuild JSONL
```

Each metro fetch writes one manifest row with `pull_id=dcm_metro_{state}_{metro}`.
The derived `data/processed/datacentermap/facilities.jsonl` is rebuilt from
the cached HTML and is NOT committed (regenerate offline at any time).
