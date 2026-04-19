# DataCenterInsurance

Are North American data centers spatially correlated with severe convective
storm risk after controlling for the real siting drivers (power, fiber,
population, tax, water, competing hazards)? This project tests that question
with public data, pre-registered analysis, and an outcome-agnostic design.

## Reading order

1. `INBOX.md` — current project status
2. `CLAUDE.md` — agent operating instructions
3. `docs/dc_scs_execution_plan.md` — the binding execution plan
4. `docs/preregistration.md` — frozen analysis commitments
5. `docs/glossary.md` — abbreviations and domain terms
6. `docs/deviations.md` — logged changes from the plan

## Quickstart

```
make all        # full pipeline (placeholder; phase 1 in progress)
make fetch-raw  # download active Phase 1 sources (run on a networked machine)
make lint       # ruff check
make test       # pytest
```

### Fetching raw data

The agent sandbox cannot reach external hosts, so Phase 1 raw files are
fetched on a networked machine (e.g. a laptop) and committed. See
`docs/deviations.md` (2026-04-18) for the policy.

1. On a machine with network: `pip install -r requirements.txt`, then
   `make fetch-raw`. Each active entry in `scripts/raw_sources.yaml` is
   downloaded to its `local_path`, its SHA256 is computed, and a row is
   appended to `data/raw/manifest.csv`.
2. `git add data/raw/ && git commit && git push` to the current phase branch.
3. Re-running `make fetch-raw` is idempotent — cached files are not
   re-downloaded and manifest rows are not duplicated.

Sources under the `todo:` section of the YAML are scrapes, auth-gated APIs,
or sources with non-static filenames. They need per-source follow-up before
moving into `sources:`.

## Layout

```
src/                # pipeline code (package: dc_scs)
data/raw/           # cached source pulls (gitignored except manifest)
data/processed/     # intermediate artifacts (gitignored)
reports/            # human-readable outputs (audit, findings)
paper/              # academic writeup
substack/           # narrative drafts
docs/               # plan, preregistration, glossary, deviations, env
figures/            # generated PNGs with caption sidecars (gitignored)
tests/              # pytest suite
```
