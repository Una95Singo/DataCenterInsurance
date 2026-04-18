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
make all     # full pipeline (placeholder; phase 1 in progress)
make lint    # ruff check
make test    # pytest
```

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
