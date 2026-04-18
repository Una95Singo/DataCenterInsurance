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
