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

## 2026-04-19 05:15 — §1.1 BLOCKED: datacentermap.com serves a "Page View Limit Reached" cap
State: BLOCKED
PR: —
Branch: `claude/phase1-datacentermap-scrape-hNCrD`
Summary: **Una ran `make scrape-dcm` on his laptop; 489 of 490 metro GETs returned a 10,114-byte "Page View Limit Reached" stub. Only `virginia/manassas.html` (207 KB, 96 facility records) got through. Final JSONL: 127 records vs. the ≥500 §1.1 gate.** The stub is explicit site policy (`<title>Page View Limit Reached</title>`), not a scraper bug — 2 s politeness does not clear it and we will not try to bypass it. Scraper infrastructure (enumerate→fetch→parse→JSONL, 31 tests passing) is correct and reusable; the source is the problem. Committed on this branch: the scraper module, the real Manassas metro HTML, one cap-page stub under `data/raw/datacentermap/evidence/` for reference, and `docs/deviations.md` entry "§1.1 datacentermap.com spine pivot". **Needs Una's decision next session** between: (a) trickle-scrape 30–50/day over ~10 days from residential IP; (b) pivot the §1.1 spine to OSM `man_made=data_center` (Overpass) + Baxtel + hyperscaler region pages, per the plan's own §1.1.2–§1.1.4 (datacentermap becomes an enrichment cross-ref); (c) combine — start (b) now so Phase 2/3 aren't blocked, run (a) in the background. Recommendation: (c). No commercial license pursued per CLAUDE.md policy. **No push to `phase1-data` yet** — the scraper code is ready but §1.1 data is not.

## 2026-04-19 04:30 — §1.1 scraper written; ready for laptop run
State: READY FOR REVIEW (waiting on `make scrape-dcm` on a networked machine)
PR: —
Branch: `claude/phase1-datacentermap-scrape-hNCrD` (off `phase1-data`)
Summary: Sandbox allowlist probe: `.claude/settings.json` lists `datacentermap.com` and `*.noaa.gov` but both hosts still return `HTTP/2 403 x-deny-reason: host_not_allowed` — the settings file is present but not effective for this sandbox. Staying on the laptop-fetch pattern. Built the §1.1 scraper per the locked design: `src/dc_scs/inventory/{metros,parse,build,fetch}.py` (enumerate → GET → parse `__NEXT_DATA__` → flatten → JSONL) and `scripts/scrape_datacentermap.py` as the CLI entrypoint with `--subset N`, `--skip-build`, `--build-only`, `--delay` flags. Manifest integration reuses `dc_scs.manifest.append_manifest_row`; per-metro `pull_id = dcm_metro_{state}_{metro}`. Added `make scrape-dcm`. Gitignore whitelist updated: committed metro HTML lives at `data/raw/datacentermap/metros/{state}/{metro}.html`; derived `data/processed/datacentermap/facilities.jsonl` is NOT committed (rebuildable via `--build-only`). Tests: **31 pass** (up from 8) — the three new test modules exercise sitemap enumeration (490 unique metros, 5192 US URLs, 13000 worldwide), parser on the Manassas fixture (96 records after dropping the `market-unmapped` sentinel; all 96 have operator populated; AWS=46/96 = 48% of NoVa's Manassas metro), build (de-dup across metros), and fetcher (patched requests; verifies politeness-gap sleep is skipped on cache hits). `ruff check` clean. **Ask of Una**: `git pull && make scrape-dcm && git add data/raw/datacentermap/metros && git commit -m "§1.1 metro scrape: 490 pages" && git push`. Smoke-test first if you want: `python scripts/scrape_datacentermap.py --subset 3`. Next session: Phase 2 audit will reconcile the JSONL record count against the sitemap's 5,192 US URLs and flag the gap; also flag any metros where operator coverage drops below Manassas's 100%.

## 2026-04-19 03:40 — §1.1 scrape design locked: 490 metro GETs, ~16 minutes
State: READY FOR REVIEW
PR: —
Branch: `phase1-data`
Summary: Metro sample (`/usa/virginia/manassas/`) confirms the optimization. Each metro page's `__NEXT_DATA__` carries the full facility roster for that metro — 97 GeoJSON Features on the Manassas page, each with `id`, `name`, `address`, `postal`, `city`, `state`, `latitude`, `longitude`, `companyname`, `companylink` (operator), `listingtype`, `capacitytype`. Operator is *better populated* on metros than on facility detail pages (empty on the Brickyard facility sample). 5,192 US facility URLs reduce to **490 unique `(state, metro)` pairs** — confirmed by parsing all 13 sitemap shards. At 2 s polite delay: ~16 minutes to cover the entire US §1.1 universe vs. ~3 hours for per-facility. `reports/phase1_recon_datacentermap.md` updated with the committed scrape design (raw metro HTML → `__NEXT_DATA__` parse → JSONL). **Next session**: write `scripts/scrape_datacentermap.py` + `src/dc_scs/inventory/` module (enumerate metros, fetch+manifest, flatten to JSONL, unit tests on the Manassas fixture). Smoke-test on a small subset before the full 490 run.

## 2026-04-19 03:20 — §1.1 recon: Next.js app, no HTML scraping needed
State: READY FOR REVIEW
PR: —
Branch: `phase1-data`
Summary: **Facility pages on datacentermap.com embed a full structured JSON payload in a `__NEXT_DATA__` script tag — no HTML scraping needed.** Per-facility `dc` object exposes id, name, address, city/state/country, lat/lon, market (metro), listingtype, capacitytype, status, stage, parent, description. Plus `owners[]` (operators — empty on the Brickyard sample but may populate on operator-owned listings). MW is null on the free tier, as expected; cross-reference with Baxtel / hyperscaler disclosures handles MW per plan §1.1. State listings (`/usa/virginia/`) carry metro-level aggregates only (e.g., Manassas=69, Ashburn=130+), not facility records — so the scrape has to go per-facility unless a metro-listing shortcut exists. Queued one more sample (`/usa/virginia/manassas/`) to check that. Recon report (`reports/phase1_recon_datacentermap.md`) updated with the JSON finding, a plan-field-accessibility table, and revised scale estimate (~3 hours for the full 5,192-URL run at 2s politeness, or seconds if metro pages suffice). **Ask of Una**: one more `git pull && make fetch-raw && git add data/raw/ && git commit && git push`. Next session: read the metro sample, write the scraper.

## 2026-04-19 03:00 — §1.1 gate CLEARED: 5,192 US facilities on datacentermap.com
State: READY FOR REVIEW
PR: —
Branch: `phase1-data`
Summary: **Top-line: datacentermap.com exposes 5,192 US facility URLs — ~10× the plan's ≥500 §1.1 acceptance gate.** State distribution matches the plan's expectations cleanly (VA 743, TX 540, CA 387, IL 296, GA 255, ..., all top-5 leaders present). 13 `dcs_*.xml` sub-sitemaps carry 13,000 facility URLs worldwide; US filter is trivial via the `/usa/` URL prefix. Full writeup in `reports/phase1_recon_datacentermap.md` (mobile-readable, ≤500 words). The open question is no longer whether the universe exists — it's whether facility-page HTML exposes enough schema fields (operator, address, MW, coordinates) or whether state listings suffice for a first pass. Queued two sample pages (`/usa/virginia/` + one Manassas facility) in `scripts/raw_sources.yaml` so next session's first move is HTML inspection, not guesswork. Scrape scale estimate: 5,192 facility pages at 2s polite delay = ~3 hours laptop time; ~50 state listings = seconds. **Ask of Una**: read `reports/phase1_recon_datacentermap.md` when convenient and flag if the "listings first, facility pages for missing fields" approach needs a different default. Otherwise, `git pull && make fetch-raw && git add data/raw/ && git commit && git push` pulls the two HTML samples and I'll propose the scrape plan next session.

## 2026-04-19 02:35 — §1.1 kickoff: datacentermap recon queued
State: READY FOR NEXT SESSION (small laptop fetch pending)
PR: —
Branch: `phase1-data`
Summary: Probed the sandbox before starting §1.1 — datacentermap.com, Baxtel, Cloudscene, Overpass, GCP ip-ranges all still 403; only `ip-ranges.amazonaws.com` is reachable (appears to be on a baseline allowlist, not from `.claude/settings.json`). WebFetch to datacentermap.com also 403s, so no in-sandbox path to scope the scrape exists yet. Queued two tiny recon fetches in `scripts/raw_sources.yaml` under `sources:` — `datacentermap_robots` and `datacentermap_sitemap` — which Una can pull via the same `make fetch-raw` flow he used for SPC. Next session reads `robots.txt` (crawl policy, rate-limit hints, actual sitemap paths) and `sitemap.xml` (facility URL space), then designs the paginated scraper. .gitignore whitelisted `data/raw/datacentermap/`. Registry is now 51 active / 23 todo; 8 tests pass. **Ask of Una**: on a networked machine, `git pull && make fetch-raw && git add data/raw/ && git commit && git push`. If sitemap.xml 404s, robots.txt almost certainly points to the real URL — paste the robots.txt content and I'll update the YAML.

## 2026-04-19 02:20 — Merged SPC work into phase1-data; pivoting to §1.1 DC inventory
State: READY FOR NEXT SESSION
PR: —
Branch: `phase1-data` (claude/verify-spc-endpoint-pBdvG fast-forwarded in cleanly)
Summary: Una made two decisions: (1) merge the SPC sub-track into `phase1-data` — done, both branch tips now point at `c96ea10`; (2) pivot to §1.1 DC inventory before continuing §1.2. Rationale for the pivot: §1.1 is the fragile track where the plan's fallback ("if <500 facilities, drop from facility-level to metro-level") is a real risk; better to discover that early. Next session should: (a) check whether `.claude/settings.json` allowlist is now effective in a fresh agent shell — if yes, scraping can happen in-sandbox; if no, continue the laptop-fetch pattern; (b) start on datacentermap.com as the primary spine — this is an HTML scrape with pagination and rate limiting, not a static GET, so `fetch_raw.py` is not the right tool; a dedicated scraper module under `src/dc_scs/scrape/` is. §1.2 remaining work (NOAA Storm Events DB, SWDI/MESH, SPC hail climatology grid, ERA5 CAPE) is deferred until §1.1 has a first-cut facility list.

## 2026-04-19 02:00 — Phase 1 §1.2 SPC pulls landed
State: RUNNING
PR: —
Branch: `claude/verify-spc-endpoint-pBdvG`
Summary: All 49 SPC WCM files are on the branch with matching manifest rows (103 MB total in `data/raw/spc/`). Coverage: tornado 1950-2024 (consolidated), hail 1955-2024 (5 decade + 2 multi-year + 17 yearly), wind 1955-2024 (same split). Provenance: each row has a SHA256 + pulled_at timestamp written by `scripts/fetch_raw.py`. Discovery note for Phase 2 audit: SPC publishes a consolidated CSV only for tornadoes; hail/wind are split across 24 files each — the `_actual` tornado file name pattern doesn't apply to hail/wind. Phase 1 §1.2 still needs NOAA Storm Events DB (variable filename), SWDI/MESH (API), SPC hail climatology grid, and ERA5 CAPE (auth). §1.1 DC inventory and §1.3 covariates are untouched. **Next**: (a) cherry-pick/merge `claude/verify-spc-endpoint-pBdvG` → `phase1-data` (need Una's permission to push there), (b) decide whether to keep pushing on §1.2 (Storm Events next) or pivot to §1.1 DC inventory (first big payoff). Sandbox still can't reach external hosts from this agent session; fetches keep going via Una's laptop until a fresh session picks up the `.claude/settings.json` allowlist.

## 2026-04-18 22:45 — fetch_raw.py ready for Una to run locally
State: BLOCKED (waiting on Una to run `make fetch-raw` on a networked machine)
PR: —
Branch: `claude/verify-spc-endpoint-pBdvG`
Summary: Probed the sandbox egress — ALL ten Phase 1 hosts I tested return `403 x-deny-reason: host_not_allowed` (SPC, NCEI, datacentermap, EIA, FCC, FEMA, USGS, Census, PCH, OSM). The earlier INBOX extrapolation was correct: every source is walled off. Rather than have Una hand-upload 20+ files, built a single-shot fetcher he runs on his laptop: `scripts/fetch_raw.py` + `scripts/raw_sources.yaml` registry + `make fetch-raw` target. Active registry currently covers the SPC trio (tornado, hail, wind) — CSVs at `spc.noaa.gov/wcm/data/` that follow a consistent naming pattern. Everything else from plan §1.1 / §1.2 / §1.3 is enumerated under `todo:` in the YAML with a one-line note on what's needed to activate it (scrape, auth, variable filename, etc.). Fetcher is idempotent (skips cached files and dedupes manifest rows), reports failures without crashing, writes rows via `dc_scs.manifest.append_manifest_row` so the hash/byte/timestamp path is identical to what phase-1 scripts will use. Tests: 8 pass (4 existing + 4 new registry sanity checks); ruff clean. Unblock: (1) cherry-pick/merge this branch into `phase1-data` (or grant me permission), (2) `pip install -r requirements.txt && make fetch-raw` on a networked machine, (3) commit `data/raw/` + the updated `manifest.csv` and push. Subsequent sources get added by extending `sources:` in the YAML as URLs are verified.

## 2026-04-18 22:15 — Hand-upload path prepped for SPC tornado CSV
State: BLOCKED (waiting on Una's upload)
PR: —
Branch: `claude/verify-spc-endpoint-pBdvG`
Summary: Switched to option (4) from the earlier unblock menu: Una hand-uploads the SPC tornado CSV via the GitHub web UI. Prepped on this branch: `.gitignore` exception for `data/raw/spc/**`, empty `data/raw/spc/.gitkeep`, deviation entry at `docs/deviations.md` documenting the temporary raw-files-in-git policy, and a hand-upload procedure appended to `data/raw/README.md` with a pre-filled manifest row template (only `<SHA256>` and `<BYTES>` need filling in). Scope note: this unblocks only §1.2 SCS tornado; full Phase 1 needs ~20–25 files across §1.1 / §1.2 / §1.3. Awaiting Una to (a) merge/cherry-pick this branch into `phase1-data` or grant permission to push it there directly, (b) upload the CSV to `data/raw/spc/`, and (c) fill in the manifest row.

## 2026-04-18 22:01 — SPC endpoint re-check: still blocked
State: BLOCKED
PR: —
Branch: `claude/verify-spc-endpoint-pBdvG`
Summary: Una reported the Phase 1 sandbox allowlist is live and asked to verify via `curl -sSI https://www.spc.noaa.gov/wcm/data/1950-2023_actual_tornadoes.csv`. The response is still `HTTP/2 403` with `x-deny-reason: host_not_allowed` (content-type `text/plain`, 21 bytes) — identical to the previous block. The allowlist change has not taken effect in this sandbox, so per plan §1.2 the precondition (200/302) is not met and I did not start the SPC fetcher. **Unblock options for Una:** (1) confirm the allowlist was actually applied to the environment this agent runs in, and that `www.spc.noaa.gov` is on it; (2) if it is, check whether a cache/restart is needed for the sandbox to pick up the new policy; (3) re-trigger an agent session after verification. No files changed besides this INBOX entry.

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
