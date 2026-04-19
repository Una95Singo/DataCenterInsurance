# Deviations Log

This file records every deviation from the preregistered plan (`/docs/preregistration.md`) with written justification.

**A deviation must be logged whenever:**

- The primary analysis specification changes
- A decision threshold in §0.2 is reinterpreted
- A scope decision in §0.3 is revised
- A data source is swapped or dropped
- A sensitivity spec is added, removed, or modified

Entries are append-only. Never edit or delete past entries.

Format:

```
## YYYY-MM-DD — <short title>
Changed: <what>
From: <original>
To: <new>
Reason: <written justification>
Approved by: <human> or <n/a — agent judgment>
```

-----

## 2026-04-18 — Committing raw files due to sandbox egress block
Changed: Raw data file storage policy (operational, not analytical)
From: `data/raw/` is gitignored except `manifest.csv` and `README.md`; all raw files are fetched by agent scripts at runtime and live locally only.
To: Per-source exceptions are added to `.gitignore` (starting with `data/raw/spc/`) so Una can hand-upload raw files via the GitHub web UI until sandbox egress is fixed. Manifest schema, SHA256 requirement, and reproducibility rule are unchanged.
Reason: The agent sandbox denies outbound HTTP to every Phase 1 host (`x-deny-reason: host_not_allowed`). A proxy allowlist change was attempted but has not taken effect in this environment. Hand-upload is the fastest path to unblock Phase 1 §1.2. Once network access is restored, new pulls should go back to the fetcher path and these exceptions can be removed; the hand-uploaded files stay in git as the source-of-truth cache for those pulls.
Approved by: Una (conversation, 2026-04-18)

## 2026-04-19 — §1.1 datacentermap.com spine pivot (BLOCKED pending decision)
Changed: §1.1 DC-inventory primary source
From: datacentermap.com metro-level scrape as the primary spine (490 metro GETs, ~16 minutes) per plan §1.1.
To: TBD. Full 490-metro scrape attempted at 2 s per-request politeness; the site returned a 10,114-byte "Page View Limit Reached" stub for ~489 of 490 URLs. Only `virginia/manassas.html` (207 KB, 96 facility records) landed in the pre-cap window. Net: 127 facility records vs. ≥500 §1.1 acceptance gate — source-level block, not a scraper bug.
Reason: The view cap is deliberate site policy; 2 s spacing does not clear it and we will not try to bypass it. The plan anticipates this kind of failure — §1.1 lists Baxtel, Cloudscene, OSM `man_made=data_center` via Overpass, and hyperscaler region pages as complementary sources. Candidate paths for next session: (a) trickle datacentermap at 30–50 metros/day over ~10 days from a residential IP, (b) pivot the spine to OSM + Baxtel + hyperscaler region lists, treating datacentermap as an enrichment cross-ref, (c) combine (a) and (b). Commercial license was not pursued (per CLAUDE.md "no commercial purchases without explicit human approval").
Approved by: pending — see INBOX 2026-04-19 BLOCKED entry

