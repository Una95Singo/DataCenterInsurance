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

## 2026-04-18 — Phase 1 scaffolding

State: RUNNING
PR: —
Branch: `phase1-data`
Summary: Pipeline scaffolding laid down on `phase1-data`: `Makefile` with phase targets, `src/dc_scs/` package with raw-data manifest helper (`sha256_file`, `append_manifest_row`), `data/raw/manifest.csv` (header only), `data/raw/README.md` documenting the manifest schema, `pyproject.toml` with ruff config, pinned `requirements.txt`, `.gitignore`, `docs/env.md`, and `README.md`. `make lint` and `make test` both pass (4 tests). No data pulled yet — next session picks the first sub-track (1.1 DC inventory or 1.2 SCS hazard) and begins fetching through the manifest helper. Per plan, scaffolding is "pipeline plumbing" so no PR opened.

## 2026-04-18 — Project kickoff

State: READY FOR AGENT START
PR: —
Summary: Repo scaffolded with CLAUDE.md, plan, glossary, preregistration, and deviations log. Awaiting first agent session to begin Phase 1 (data collection). No data pulled yet.
