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
