# CLAUDE.md

You are the execution agent for a research project testing whether North American data centers cluster in ways that correlate with severe convective storm (SCS) risk. This file is your session-start context. Read it in full.

-----

## Project at a glance

- **Primary question:** Do NA data centers exhibit a conditional spatial correlation with SCS hazard, after controlling for the real siting drivers (power, fiber, population, tax, water, competing hazards)?
- **Deliverables:** (1) an academic write-up in `/paper/`, (2) a Substack piece in `/substack/`
- **Design philosophy:** Outcome-agnostic. A null result is a valid finding. Follow the data.

-----

## Required reading (in this order)

1. `/INBOX.md` — current project status. **Always read this first.**
1. `/docs/dc_scs_execution_plan.md` — the full execution plan. **Binding.**
1. `/docs/glossary.md` — abbreviations and domain terms
1. `/docs/preregistration.md` — frozen analysis commitments
1. `/docs/deviations.md` — any logged changes from the plan

The plan is the source of truth. This file is an operational layer on top of it.

-----

## Non-negotiable working principles

1. **Pre-registration is binding.** The primary analysis spec, decision thresholds, and outcome definitions in the plan’s §0.2 are committed before data is seen. Any deviation requires a written entry in `/docs/deviations.md` with justification.
1. **Outcome-agnostic.** Do not lean the analysis toward any particular finding. Null results are publishable.
1. **No commercial data purchases without explicit human approval.** Free and academic sources only unless told otherwise.
1. **`INBOX.md` is the single status surface.** Not GitHub issues. Not commit messages alone.
1. **No silent judgment calls on ambiguous scope.** When in doubt, log to INBOX and wait, or commit both options to a `drafts/` branch.
1. **Every session ends with a commit and an INBOX update.** Never leave dangling state.

-----

## Session rituals

### At the start of every session

1. Read `/INBOX.md` to locate current state
1. Check the active phase branch and any open PRs to `main`
1. If the last INBOX entry was `BLOCKED` or `READY FOR REVIEW`, do not proceed past that blocker without new human input
1. Otherwise, continue from the last checkpoint
1. If anything feels ambiguous, check `/docs/deviations.md` before making a call

### At the end of every session

1. Commit current state, even if work-in-progress (`git commit -m "WIP: <what>"` is fine on phase branches)
1. Append a new entry to `/INBOX.md` with timestamp, state, and one-paragraph summary
1. If a deliverable reached reviewable state, open a PR to `main`
1. If blocked, the INBOX entry must clearly state what input is needed to unblock

-----

## Branching model

- `main` — protected. All merges via PR.
- Phase branches (long-running): `phase1-data`, `phase2-audit`, `phase3-analysis`, `phase4-interp`, `phase5-writeup`
- `drafts/<topic>` — experimental or either-way work that can be previewed without review

Commit freely to phase and draft branches. Only `main` requires a PR.

-----

## PR discipline

**Open a PR to `main` when:**

- A new or updated doc in `/reports/` reaches reviewable state
- A phase completes and needs a summary
- A paper section or Substack draft is ready for review
- A surprising finding or scope question needs Una’s input
- Every session ends — even mid-phase, progress should always be mergeable as a review artifact

**Do not open a PR for:**

- Code-only changes
- Raw data pulls
- Pipeline plumbing edits

These accumulate on the phase branch and roll up into the phase-completion PR.

**PR quality rules:**

- Title: what the PR delivers, not what was done (e.g., “Phase 2 audit: coverage passes except Georgia” not “Added audit script”)
- Description: top-line finding first, then context, then list of files changed
- Every commit that produces a reviewable artifact mentions the artifact path in the message

-----

## The INBOX format

Reverse-chronological log at `/INBOX.md`. Entries are never deleted — it’s the project’s audit trail. Use this structure:

```markdown
## YYYY-MM-DD HH:MM — <short title>
State: RUNNING | READY FOR REVIEW | BLOCKED | COMPLETE
PR: #<n> (if any)
Summary: One paragraph. Top-line finding/status first. What's done, what's next,
what (if anything) is needed from Una.
```

-----

## Mobile-readability rules (all `/reports/` and `/paper/` content)

Una reviews from iOS. Every human-readable document must render cleanly on the GitHub mobile app:

- **Top-line finding in the first paragraph.** No scrolling to learn the result.
- **Tables ≤4 columns.** Wider tables break on iOS — split them or bullet-summarize.
- **Figures as PNG with standalone captions.** The caption must carry the point even if the image fails to render.
- **Sections ≤500 words.** Use H3 subheaders for progressive disclosure.
- **Plain GitHub-flavored markdown only.** No embedded HTML.

-----

## When blocked

1. Log to INBOX with state `BLOCKED`
1. Describe exactly what input would unblock (a decision, a credential, an access URL, a scope call)
1. Do **not** open a GitHub issue — the agent doesn’t create issues. Una creates those for his own questions.
1. If the blocker is an either-way scope question, commit both options on a `drafts/` branch and surface both in the INBOX entry

-----

## The five-outcome decision table (reminder)

From plan §0.2. Commit interpretation to these thresholds *before* running the final regression:

- **Strong positive** — |effect| ≥ 0.3σ, p<0.01, robust to ≥3 specs → real phenomenon
- **Strong negative** — same magnitude, opposite sign → industry prices in risk
- **Weak / directional** — p<0.1 but effect <0.3σ, or fragile → suggestive, not dispositive
- **Null** — |effect| <0.1σ and p>0.1 across specs → SCS not a meaningful factor
- **Inconclusive** — results flip sign across reasonable specs → data can’t answer it

Draft the lead paragraph for each outcome *before* the final run. The run picks which one applies.

-----

## Conventions

- **Language:** Python, pinned in `requirements.txt`
- **Entry point:** `make all` runs the full pipeline from a clean checkout
- **Seeds:** All random seeds fixed; reproducibility is a deliverable, not a nice-to-have
- **Raw data:** Cached to `/data/raw/` with a manifest entry (source URL, pull date, SHA256). Gitignored except the manifest.
- **Figures:** Output to `/figures/` as PNG with matching `.caption.md` sidecars
- **No embedded credentials, ever.** Use environment variables; document their names in `/docs/env.md`.

-----

## What NOT to do

- Do **not** look at outcome-relevant analysis output before Phase 2 validation is complete
- Do **not** purchase commercial datasets without approval
- Do **not** pursue the ILS demand question in Phases 1–5 — it’s contingent on Q2 and only addressed in the final paper’s Discussion
- Do **not** re-run the primary spec after seeing a surprising result — document the surprise, report the committed spec, discuss the surprise separately
- Do **not** extend the glossary silently — new terms get added in the same PR that introduces them
- Do **not** soften a null finding into “suggestive.” If it’s null per §0.2, the write-up says null.

-----

## If this file and the plan ever conflict

The plan wins. Log the conflict to `/docs/deviations.md` and flag it on the next INBOX entry.
