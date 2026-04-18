# INBOX

Running project status log. Reverse-chronological. Most recent entry at the top. Entries are never deleted.

Format for each entry:

```
## YYYY-MM-DD HH:MM — <short title>
State: RUNNING | READY FOR REVIEW | BLOCKED | COMPLETE
PR: #<n> (if any)
Summary: One paragraph.
```

-----

## 2026-04-18 — Phase 1 BLOCKED on outbound network

State: BLOCKED
PR: —
Branch: `phase1-data`
Summary: Phase 1 cannot proceed from this sandbox. Both `curl` and `WebFetch` to `noaa.gov` return HTTP 403 with `x-deny-reason: host_not_allowed`. The same restriction will apply to every Phase 1 source (datacentermap.com, eia.gov, fcc.gov, fema.gov, usgs.gov, census.gov, packet-clearing-house, etc.). The scaffolding is in place and `make lint` / `make test` pass (4 tests), so the pipeline is ready the moment data can be fetched. **Unblock options for Una to choose between:** (1) allowlist the relevant external hosts in the sandbox config (cleanest — agent runs the fetchers as designed); (2) pre-fetch the raw files locally and commit them under `data/raw/` with manifest rows so the agent processes pre-cached data; (3) run Phase 1 fetchers on a machine with network, push the resulting `data/raw/` cache + populated `manifest.csv`. Recommendation: option (1), with an initial allowlist of `*.noaa.gov`, `www.spc.noaa.gov`, `www1.ncdc.noaa.gov`, `datacentermap.com`, `www.eia.gov`, `broadbandmap.fcc.gov`, `hazards.fema.gov`, `earthquake.usgs.gov`, `data.census.gov`. No data pulled, no manifest rows added.

## 2026-04-18 — Phase 1 scaffolding

State: RUNNING
PR: —
Branch: `phase1-data`
Summary: Pipeline scaffolding laid down on `phase1-data`: `Makefile` with phase targets, `src/dc_scs/` package with raw-data manifest helper (`sha256_file`, `append_manifest_row`), `data/raw/manifest.csv` (header only), `data/raw/README.md` documenting the manifest schema, `pyproject.toml` with ruff config, pinned `requirements.txt`, `.gitignore`, `docs/env.md`, and `README.md`. `make lint` and `make test` both pass (4 tests). No data pulled yet — next session picks the first sub-track (1.1 DC inventory or 1.2 SCS hazard) and begins fetching through the manifest helper. Per plan, scaffolding is "pipeline plumbing" so no PR opened.

## 2026-04-18 — Project kickoff

State: READY FOR AGENT START
PR: —
Summary: Repo scaffolded with CLAUDE.md, plan, glossary, preregistration, and deviations log. Awaiting first agent session to begin Phase 1 (data collection). No data pulled yet.
