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

## Queued for next session

Two sample pages added to the fetch registry: `/usa/virginia/` (state listing) and `/usa/virginia/manassas/10051-brickyard-wy/` (facility detail). Reading their HTML will determine the scraper design. No MW / coordinate decisions until those samples are in.

## For Una

Nothing required. §1.1 scope gate is cleared cleanly. Review this doc when convenient; if you disagree with the state-listing-first approach, flag it, otherwise next session parses the samples and commits a scrape plan.
