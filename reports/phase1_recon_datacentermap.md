# Phase 1 §1.1 recon — datacentermap.com

**Top-line: 5,192 US facility URLs — ~10× the plan's ≥500 acceptance gate. State distribution matches the plan's expected top-10. The facility URL space clears §1.1 by an order of magnitude; the open question is now which schema fields we can extract per page, not whether the universe exists.**

## Source structure

datacentermap.com publishes a sitemap index at `/sitemap.xml` pointing at 29 sub-sitemaps. The 13 `dcs_*.xml` shards carry all facility URLs (13,000 worldwide). Only the `/usa/*` subset is in scope per plan §0.3 CONUS; Alaska/Hawaii removal will trim < 1%. No authentication, no rate limiting beyond an anti-bot filter on default `python-requests` user agents (now handled).

## Top-10 US states by facility count

| State | Count |
|---|---|
| Virginia | 743 |
| Texas | 540 |
| California | 387 |
| Illinois | 296 |
| Georgia | 255 |
| Ohio | 234 |
| Arizona | 195 |
| New York | 170 |
| Florida | 150 |
| Oregon | 148 |

All five of the plan's expected leaders (VA, TX, CA, IL, NY, GA) appear in the top 6. Virginia is ~14% of US facility count — lower than the 40% MW-share threshold in plan §2.1, though MW-weighted analysis is likely to push NoVa dominance above that threshold once per-facility MW data lands.

## URL structure

Facility URL pattern: `/usa/{state}/{city}/{facility-slug}/`. State listing pages at `/usa/{state}/`; metro pages at `/usa/{state}/{city}/`. The pattern is consistent, which means (a) US filtering is trivial, (b) state/metro attribution is available pre-scrape.

## Scrape scale — two candidate approaches

A facility-level scrape of 5,192 pages at 2 s polite delay = ~3 hours. A state-level scrape of ~50 listings is seconds; if the listings carry operator + address, that covers Phase 2 acceptance and we only descend to facility pages for MW or coordinates. The choice is empirical — it depends on what each page type actually contains.

## Data access: no scraping needed

The site is a Next.js SPA. Each page embeds a full JSON payload in a `<script id="__NEXT_DATA__">` tag — `props.pageProps.dc` on a facility page is a structured object, not HTML to parse. Per-facility access is a single HTTP GET + one regex + one `json.loads`.

## What the JSON exposes, vs. the plan's schema

| Plan field | Accessible? |
|---|---|
| facility_id, name | `dc.id`, `dc.name` — yes |
| address, city, state, country | `dc.address`, `dc.city`, `dc.state`, `dc.country` — yes (structured, not just a single string) |
| lat, lon | `dc.latitude`, `dc.longitude` — yes |
| metro | `dc.market` — yes |
| type (colo/hyperscaler/wholesale) | `dc.capacitytype` + `dc.listingtype` — yes |
| status (operational/construction/planned) | `dc.status` + `dc.stage` — yes (numeric codes, need mapping) |
| operator | `props.owners[]` — partial (empty in the Brickyard sample; may be richer on operator-owned listings) |
| **it_mw_estimate** | `dc.meta_power` — **null on free tier**; must come from Baxtel / hyperscaler cross-ref |

MW absence is expected per plan §1.1 (Baxtel / hyperscaler disclosure were already slated as MW sources). No change to the schema; downstream MW confidence flags (H/M/L) were designed for exactly this.

## Scrape scale — resolved

Metro pages carry all facility records for their metro, with full schema (address, coords, operator, type). The Manassas page embeds 97 records in `mapdata.dcs`, each a GeoJSON Feature whose `properties` dict includes `id`, `name`, `address`, `postal`, `city`, `state`, `companyname`, `companylink` (operator), `listingtype`, `capacitytype`. Operator is actually **better-populated on metro pages than facility pages** (it was empty on the Brickyard facility sample).

The 5,192 US facility URLs map to **490 unique `(state, metro)` pairs**. Biggest metros: dallas (229), chicago (217), atlanta (187), phoenix (185), ashburn (159). 490 GETs × 2 s polite delay = **~16 minutes laptop time** for the full US universe.

## Scrape design (commitment)

1. Parse `data/raw/datacentermap/sitemap/dcs_*.xml` → extract unique `(state, metro)` tuples for `/usa/` URLs.
2. For each metro: `GET /usa/{state}/{metro}/` with the browser UA and 2 s per-host delay; save raw HTML to `data/raw/datacentermap/metros/{state}/{metro}.html` and append one manifest row.
3. Post-process: parse `__NEXT_DATA__` from each saved HTML, flatten `mapdata.dcs[*].properties` (plus geometry) to JSONL at `data/processed/datacentermap/facilities.jsonl`.
4. Phase 2 audit reconciles facility counts against the sitemap totals (should recover ~5,192 US records, modulo the minor sitemap-vs-metro off-by-one seen in Manassas: 99 vs 97).

MW is still null on the free tier. MW confidence-H/M rows will come from Baxtel + hyperscaler region lists (plan §1.1.2 / 1.1.4) in a separate pull.

## For Una

§1.1 is ready to scrape. The raw+processed split keeps provenance intact (metro HTML is the source of truth; JSONL is a derivation that can be regenerated). No scope calls required unless you want the scraper to run against a subset (e.g., top-10 states only) for faster iteration — it defaults to all 490.
