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
