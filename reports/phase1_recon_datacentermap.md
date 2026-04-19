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

## Revised scrape scale

At a 2-second per-host delay, 5,192 GETs × 2 s = **~3 hours laptop time**, output ~300–500 MB of HTML. If metro-listing pages embed full facility records (queued as a next-session check on `/usa/virginia/manassas/`), 100–200 metro pages suffice — seconds to minutes. The metro sample resolves this before any scraper code is written.

## Queued for next session

1. Read the Manassas metro sample to decide metro-vs-facility granularity.
2. Write a scraper module under `src/dc_scs/inventory/` that loops the sitemap URLs, extracts `__NEXT_DATA__`, validates schema, writes JSONL + one manifest row.
3. Run a 10-URL smoke batch before the full 5 k run.

## For Una

Nothing required. §1.1 scope gate is cleared and the extraction path is easier than anticipated (JSON, not HTML scraping). Review if convenient; otherwise next session proposes the scraper design on top of the metro sample.
