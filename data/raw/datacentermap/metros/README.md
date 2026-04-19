# datacentermap.com metro scrape — partial (BLOCKED)

`make scrape-dcm` on 2026-04-19 fetched 490 metro pages. 489 came back
as a 10,114-byte `"Page View Limit Reached"` stub — datacentermap.com's
per-IP view cap. Only `virginia/manassas.html` (207 KB, 96 facility
records) landed inside the pre-cap window.

Files kept in this directory are the real metro pages. One cap-page
stub is preserved under `data/raw/datacentermap/evidence/` as proof
of the block. See `docs/deviations.md` entry
"§1.1 datacentermap.com spine pivot" and INBOX 2026-04-19 BLOCKED.

**Do not treat this as the §1.1 facility inventory.** Phase 1 spine
decision is pending — candidate paths are trickle-scrape, pivot to
OSM + Baxtel + hyperscaler region lists, or both.
