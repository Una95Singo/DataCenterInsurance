# Execution Plan — Do Data Centers Cluster in Convective Storm Risk Zones?

*An outcome-agnostic research design for autonomous execution.*

-----

## 0. Research Framing & Pre-Registration

Before any data is pulled, the analysis is pre-registered to prevent hypothesis creep. This document is committed to the repo at `/docs/preregistration.md` and any deviation is logged in `/docs/deviations.md` with a written justification.

### 0.1 Sharpened Primary Hypothesis

The loose question — “do data centers cluster in storm zones?” — is too weak to falsify. It is sharpened into two separable sub-questions:

- **Q1 (Clustering):** Do North American data centers exhibit statistically significant spatial clustering beyond what is expected from population density alone? *(This is almost certainly yes — the interesting question is the shape and scale of the clustering, not its existence.)*
- **Q2 (SCS correlation):** After controlling for the legitimate siting drivers of data centers (power cost, fiber backbone, population, land cost, tax incentives, water, climate for cooling), is there any residual relationship between data center density and severe-convective-storm (SCS) exposure?

**Q2 is the one that actually matters.** A raw overlay of data centers and tornadoes will show a strong positive correlation because both cluster in the eastern half of CONUS. That finding would be spurious and uninteresting. The real question is the *conditional* relationship.

### 0.2 Pre-Registered Decision Rules for “Proof” vs. “Inconclusive”

|Finding               |Definition                                                                          |Interpretation                                                                         |
|----------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
|**Strong positive**   |Conditional effect size ≥ 0.3 (standardized), p<0.01, robust to ≥3 sensitivity specs|DCs disproportionately sited in SCS zones → real phenomenon                            |
|**Strong negative**   |Same magnitude/significance, opposite sign                                          |Industry avoids SCS zones → siting prices in risk                                      |
|**Weak / directional**|p<0.1 but effect size <0.3, or significance fragile                                 |Suggestive, not dispositive; narrative-worthy but not publishable as a positive finding|
|**Null**              |                                                                                    |Effect                                                                                 |
|**Inconclusive**      |Results flip sign across reasonable specs                                           |Data can’t answer the question; document why                                           |

These thresholds are committed *before* the data is pulled. Any finding, including null, is a publishable result.

### 0.3 Scope Decisions (Committed Upfront)

- **Geography:** CONUS only. Canadian DC count is small and regulatory/insurance context differs; Mexican SCS data is sparse. Noted as a limitation, not a workaround.
- **Facility type:** Commercial colocation, hyperscaler, and wholesale data centers. Exclude: enterprise/on-prem server rooms (undefined population), edge compute nodes (<1 MW typically), crypto mining (different siting logic).
- **Minimum scale:** ≥ 1 MW of IT load. This is the colo/hyperscaler cutoff and is verifiable in most sources.
- **Time horizon:** Facilities operational or under construction as of Q1 2026.

### 0.4 Execution Workflow — GitHub & Async Mobile Review

Execution happens autonomously via Claude Code, reviewed asynchronously from iOS. Because review is on mobile and the agent runs without live oversight, the workflow is designed so readable content accumulates as standalone markdown documents that render cleanly on GitHub mobile, not as commit diffs.

**Repo structure (committed at project kickoff):**

```
/src/                # pipeline code
/data/raw/           # cached raw pulls (gitignored except manifest)
/data/processed/     # intermediate artifacts
/reports/            # human-readable outputs (audit, findings, memos)
/paper/              # academic writeup
/substack/           # narrative drafts
/docs/               # preregistration, deviations, glossary
/figures/            # generated PNGs with standalone captions
/INBOX.md            # running status log — the first file to read
/README.md           # project orientation
Makefile             # single entry point: `make all`
```

**Branching model:**

- `main` is protected; all merges go via PR.
- Each phase has a long-running branch: `phase1-data`, `phase2-audit`, `phase3-analysis`, `phase4-interp`, `phase5-writeup`.
- Experimental or half-formed work lives on `drafts/<topic>` branches that can be previewed without being reviewed.
- The agent commits freely to phase and draft branches. Only PRs to `main` require review.

**PR triggers — what warrants a PR to main:**

- A new or updated document in `/reports/` (audit, findings, unexpected-finding logs)
- A phase-completion summary
- A paper-section or Substack-piece draft reaching reviewable state
- A surprising finding or scope question that needs Una’s input
- End of every work session, even mid-phase, so progress is always mergeable

A PR is **not** opened for code-only changes, raw data pulls, or pipeline plumbing edits. Those accumulate on the phase branch and roll up into the phase-completion PR.

**The INBOX pattern (single status surface):**
`/INBOX.md` is the first file Una reads on every check-in. The agent maintains it as a reverse-chronological log:

```markdown
## 2026-04-18 14:30 — Phase 2 audit complete
State: READY FOR REVIEW
PR: #12
Summary: 583 facilities captured. Coverage passes except Georgia (-28%
vs Cushman total — flagged for investigation). H_reported vs H_radar
correlation 0.71. Recommend proceeding to Phase 3 with Georgia caveat.
Next: Awaiting review before Phase 3 kickoff.

## 2026-04-17 09:12 — Scrape complete
State: RUNNING
...
```

Every entry specifies: timestamp, state (`RUNNING` / `READY FOR REVIEW` / `BLOCKED` / `COMPLETE`), related PR, and a one-paragraph summary. Entries are never deleted; the log is the project’s audit trail.

**When the agent is blocked:**

- Log to INBOX with state `BLOCKED` and a clear description
- Do **not** open a GitHub issue — the agent doesn’t create issues (Una can, for his own questions)
- If the blocker is an either-way scope question, commit both options on a `drafts/` branch and let Una pick on review
- Never make silent judgment calls on ambiguous scope decisions — those are always escalated to INBOX

**Mobile-readability rules for everything in `/reports/` and `/paper/`:**

- Top-line finding in the first paragraph; no scrolling required to see the result
- Tables with >4 columns are split or converted to bullet summaries — wide tables break on iOS GitHub
- Figures are PNG with **standalone captions** — the caption must convey the point even if the image doesn’t render
- Sections ≤500 words; progressive disclosure via H3 subheaders
- Plain GitHub-flavored markdown only; no embedded HTML

**Checkpoint discipline:**
Every agent session ends with a commit and an INBOX update, even if the work is incomplete. A dangling uncommitted state forces Una to wait a full cycle to know where things stand.

**CI:**
A minimal GitHub Actions workflow runs `make lint` and `make test` on every PR. Deliberately lightweight — heavy compute stays local and doesn’t block review.

**Single source of truth for terminology:**
All abbreviations and technical terms used in this plan are defined in `/docs/glossary.md`. The glossary is updated whenever a new term is introduced in any report or paper section.

-----

## Phase 1 — Data Collection

### 1.1 Data Center Inventory

**Acceptance criterion:** ≥500 facilities with lat/long, operator, and MW estimate, with ≥90% of the estimated CONUS hyperscaler/colo universe by MW captured. It is better to have 500 facilities with MW and type than 2,000 with just names.

**Primary source ladder (try in order, merge where possible):**

1. **Data Center Map** (datacentermap.com) — free, global coverage, ~2,700 US facilities listed. Scrape with rate-limiting. Primary spine of the dataset.
1. **Baxtel** — cross-reference for operator/MW data.
1. **Cloudscene** — good for connectivity metadata; supplementary.
1. **Hyperscaler disclosures** — AWS regions/AZs, Azure regions, GCP regions, Meta, Apple, Oracle. Published, authoritative, but MW often estimated.
1. **OpenStreetMap** — `man_made=data_center` tag. Noisy but useful for cross-validation.
1. **dgtlinfra** — industry data; good aggregate MW estimates by metro.

**Fallback:** If ≥500-facility threshold is not met from free sources, escalate to *metro-level* analysis (DC MW aggregated by MSA) rather than *facility-level*. This preserves the primary question at a coarser resolution. Do **not** pay for commercial datasets (Synergy, 451) without human approval — cost not justified at this stage.

**Schema (committed):**

```
facility_id, operator, address, lat, lon, metro, state,
it_mw_estimate, mw_source, mw_confidence (H/M/L),
type (hyperscaler|colo|wholesale|unknown),
status (operational|construction|planned),
first_seen_date, source_list[]
```

**Deduplication rule:** Facilities within 100m of each other are treated as one campus. Operator + address string-matched with fuzzy distance ≥0.9.

**MW confidence flags:**

- **H** — disclosed by operator or regulatory filing
- **M** — estimated from reliable industry source
- **L** — inferred from building footprint / campus size

Sensitivity analyses in Phase 3 are run with and without L-confidence MW estimates.

### 1.2 SCS Hazard Data

**Acceptance criterion:** Gridded (≤25 km resolution) climatological frequency of tornado, hail (≥1”), and damaging wind events, covering CONUS for ≥25 years, with explicit documentation of reporting bias.

**Primary sources:**

1. **NOAA Storm Prediction Center (SPC) tornado database** — 1950-present, lat/lon of touchdowns, EF rating. Known bias: reporting density tracks population density (more spotters → more reports). This must be explicitly corrected for or at least mapped.
1. **NOAA Storm Events Database** — hail, wind, tornado from 1996 onward with better metadata.
1. **SPC hail climatology** — pre-computed annual frequency of ≥1” hail at 80 km grid.
1. **SWDI (Severe Weather Data Inventory)** — radar-derived hail signatures (MESH). Crucially, this is *not* population-biased because it’s radar-observed, not human-reported. Use as a bias-check against the SPC event database.
1. **ERA5 or NARR CAPE climatology** — atmospheric proxy for SCS potential, independent of human reporting. The “ground truth” physical layer.

**Construction:** Three versions of the hazard layer are built, not one:

- **H_reported** — from SPC event database (reporting-biased)
- **H_radar** — from SWDI/MESH (less population-biased)
- **H_environment** — from CAPE/shear climatology (no reporting bias at all)

If results are consistent across all three, the finding is robust. If they diverge, that divergence is itself the finding.

### 1.3 Covariates (the key to the conditional test)

The correlation between DCs and SCS is meaningless without these. Each is needed to isolate the SCS signal from confounders.

|Covariate                           |Source                         |Why it matters                            |
|------------------------------------|-------------------------------|------------------------------------------|
|Population density                  |US Census block groups         |Demand proxy; also confounds SCS reporting|
|Industrial electricity price ($/kWh)|EIA Form 861 by state/utility  |DCs chase cheap power                     |
|Fiber backbone density              |ITU / InterTubes / FCC Form 477|Latency-sensitive workloads need fiber    |
|Internet exchange points            |Packet Clearing House          |Peering matters for cloud                 |
|State/local tax incentives          |Good Jobs First Subsidy Tracker|VA, IA, TX incentives shaped the map      |
|Water availability / drought risk   |USGS, US Drought Monitor       |Cooling constraint                        |
|Cooling degree days                 |NOAA                           |Climate-driven cooling cost               |
|Seismic hazard (PGA 2%/50yr)        |USGS NSHM                      |Competing nat-cat confounder              |
|Flood (100-yr FEMA zones)           |FEMA NFHL                      |Competing nat-cat confounder              |
|Land cost proxy                     |Zillow / BLS                   |Scale constraint                          |

**Why seismic and flood are on this list:** California has low SCS risk and high seismic risk. If data centers avoid California for seismic reasons, that will *look* like SCS-seeking behavior in a naive model. Including competing hazards lets the model distinguish “avoiding seismic” from “tolerating SCS.”

-----

## Phase 2 — Validation & Bias Audit

Before any inferential analysis, the dataset gets a standalone audit. This phase produces `/reports/data_audit.md` and a go/no-go decision.

### 2.1 DC Inventory Quality Gates

- **Coverage check:** Does captured MW total reconcile (±20%) with published industry aggregates (e.g., Cushman & Wakefield US Data Center Trends, Synergy Research public figures)? If not, investigate the gap before proceeding.
- **Geographic representativeness:** Plot facility count by state against published state rankings (VA, TX, CA, IL, NY, GA should dominate). If the top-10 ranking is wrong, the scrape is broken.
- **Operator coverage:** Every top-20 hyperscaler and top-20 colo operator (Equinix, Digital Realty, CyrusOne, etc.) must have ≥80% of their known US footprint captured.
- **Source triangulation:** ≥60% of facilities must appear in ≥2 independent sources. Single-source facilities are flagged and run in a sensitivity analysis.

**Failure mode handling:**

- If coverage < 70% → continue at metro-level, not facility-level
- If coverage < 50% → stop and escalate; the question can’t be answered with this data
- If Virginia represents > 40% of MW → this is expected but the analysis must be run with and without NoVa (sensitivity to the single-cluster dominance problem)

### 2.2 Hazard Data Bias Audit

- **Population-reporting correlation:** Compute correlation between SPC tornado reports per km² and population density per km² at the county level. Expected strong positive. Document magnitude.
- **Reported vs. radar-derived hail:** For the period of overlap (2005-present), correlate H_reported with H_radar at 50 km grid. Divergence regions → flag.
- **Temporal stability:** Split the SPC record into 1990-2005 and 2005-2020. If climatology shifts materially (it has, for hail), use the more recent period and note.

### 2.3 The Bias Audit Itself Must Be Published

Every limitation found here appears in the final writeup. No surprises, no “we forgot to mention.” The audit doc is a deliverable, not an internal artifact.

-----

## Phase 3 — Spatial Analysis

Three analytical layers, run in order. Each has a pre-committed primary spec and at least two sensitivity specs.

### 3.1 Exploratory Visualization (Descriptive Only — No Inferential Claims)

- Kernel density maps of data center MW
- Chloropleth of tornado/hail/wind frequency by county
- Side-by-side and overlaid views at CONUS, region, and metro resolutions
- Scatter: county DC-MW vs. county SCS frequency (raw, uncontrolled)

**Decision rule:** These plots go in the paper as motivation, never as evidence. No statistical claims from this phase. If the raw overlay looks “dramatic,” that is a warning sign that the confounding is severe, not that the hypothesis is confirmed.

### 3.2 Is There Clustering at All? (Q1)

- **Ripley’s K-function** on facility point pattern, weighted by MW
- **Null model:** Complete spatial randomness weighted by population (not uniform — uniform null is trivially rejected and uninformative)
- **Edge correction:** Ripley’s isotropic correction
- **Scales tested:** 10 km, 50 km, 100 km, 500 km (covers campus, metro, region, macro)

Expected result: clustering at all scales, strongest at the metro scale. If this doesn’t appear, the data is broken.

### 3.3 Conditional Correlation with SCS Risk (Q2 — The Real Question)

**Primary specification:** Poisson/negative binomial regression at the county level:

```
DC_MW_county ~ β₀ + β₁·SCS_exposure + β_controls·X + ε
```

Where:

- `DC_MW_county` is total installed MW in the county
- `SCS_exposure` is 30-year annual expected loss proxy combining tornado, hail, wind frequency (primary = H_reported; sensitivity = H_radar, H_environment)
- `X` = all Section 1.3 covariates
- Spatial autocorrelation in residuals checked with Moran’s I; if present, re-fit with spatial lag or spatial error model

**The β₁ coefficient on SCS_exposure is the answer to the research question.** Its sign, magnitude, and confidence interval map directly onto the decision table in Section 0.2.

**Sensitivity specifications (all pre-registered):**

1. Substitute H_reported → H_radar
1. Substitute H_reported → H_environment (CAPE climatology)
1. Exclude Northern Virginia MSA (Loudoun + Fairfax + Prince William)
1. Hyperscaler-only subset
1. Metro-level (MSA) instead of county-level
1. Log MW vs. linear MW outcome
1. Recent construction (post-2015) only — tests whether behavior is changing

The finding is only reported as “robust” if ≥5 of 7 specs agree in sign and rough magnitude.

### 3.4 Falsifiers We’re Actively Looking For

To avoid motivated reasoning, pre-commit to evidence that would *disprove* each possible finding:

|If we find…             |We should also find…                                                           |Otherwise the finding is suspect               |
|------------------------|-------------------------------------------------------------------------------|-----------------------------------------------|
|DCs cluster in SCS zones|Effect stronger for ground-floor / older builds; weaker for new hardened builds|If not, maybe it’s not about SCS               |
|DCs avoid SCS zones     |Insurance premiums materially priced into known siting decisions               |If not, the “avoidance” may be coincidental    |
|Null finding            |Consistent near-zero β₁ across all specs                                       |If spec-fragile, it’s “inconclusive” not “null”|

-----

## Phase 4 — Findings Interpretation

### 4.1 The Interpretation Rulebook

Interpretation is pre-committed to the decision table in Section 0.2. A single paragraph draft of the “headline finding” is written for each of the five outcome types *before running the final regression*. The run picks which paragraph applies.

This prevents the almost-irresistible pull to soften a null result into “suggestive” or to promote a weak finding into a strong one.

### 4.2 Effect Size Translation (Do Not Skip)

A statistically significant β₁ with a tiny effect size is a null result in practical terms. Report:

- Standardized coefficient
- Predicted MW difference between 10th and 90th percentile SCS exposure counties, holding controls at means
- Share of DC MW “at risk” under the observed relationship

### 4.3 What to Do with Surprises

If the data shows something unexpected (e.g., strong clustering in *moderate* but not *extreme* SCS zones, or a nonlinear U-shape), the response is:

1. Document the surprise in `/reports/unexpected_findings.md`
1. Do not change the primary spec retroactively
1. Report the primary spec result as committed
1. Discuss the surprise in a separate “exploratory” section of the paper, clearly flagged

-----

## Phase 5 — Academic Write-Up

Structure (`/paper/main.md`):

1. **Abstract** — written last, contains the actual finding
1. **Introduction** — motivates the question (ILS context, hyperscaler growth, rising SCS losses). Does *not* preview the answer.
1. **Data** — full provenance, coverage, audit summary, limitations
1. **Methods** — pre-registered, including all sensitivity specs
1. **Results** — primary spec first, then sensitivities, then exploratory. In that order.
1. **Discussion** — what the result means, bounded by what the data can support
1. **Limitations** — a full section, not a single paragraph. Includes:
- Reporting bias in SCS data
- Unobserved siting factors (regulatory, executive preference, security)
- Cross-sectional design can’t show causal direction
- Facility-count vs. resilience-adjusted-count conflation
1. **Extensions** — what the next study would do if findings are inconclusive

### 5.1 Tension Between Academic and Substack Deliverables

The academic write-up is committed to the finding as specified. The Substack piece has narrative flexibility but **cannot contradict the academic write-up**. If the academic paper concludes “null,” the Substack cannot say “clear pattern.” The Substack is *framing flexibility*, not *finding flexibility*.

The resolution: the Substack can explore *why the finding is what it is* with more speculative range, while the academic paper stays bounded to what the regression can support.

-----

## Phase 6 — Substack Narrative Angles (All Five Outcomes)

Draft lead paragraphs for each outcome are prepared in advance so the writing doesn’t start from a predetermined angle.

**If strong positive:** *“Why is the cloud being built in Tornado Alley?”* — the industry’s revealed preference appears to tolerate SCS risk; examine whether this is explicit (pricing insurance in) or implicit (risk underweighted). The ILS angle becomes: if exposure concentration is real, it’s a reinsurance market looking for a structure.

**If strong negative:** *“The cloud knows where the weather is.”* — an underappreciated form of efficient markets; the siting process has quietly priced in SCS risk. The ILS angle inverts: low demand for SCS cover in DC space because siting already solves it.

**If weak / directional:** *“A small signal, possibly real.”* — honest framing; the data hints at something but can’t confirm. The value is methodological, and the piece becomes a template for this class of question.

**If null:** *“Data centers don’t care about storms — and maybe that’s the story.”* — the three things that actually drive siting (power, fiber, tax) dwarf everything else, including natural hazard. The ILS angle becomes structural: insurance demand from DC owners is not going to come from siting awareness, so it has to come from regulatory or counterparty pressure.

**If inconclusive:** *“The question we can’t yet answer, and why.”* — a piece about the data gaps in hyperscaler infrastructure disclosure and what it would take to close them. Frame as a call for better data rather than a failed study.

**Universal rule:** The Substack never overstates what the academic paper concluded. A reader of both should see consistent findings in different registers, not contradictory claims.

-----

## Reproducibility & Handoff

- Full pipeline in `/src/`, orchestrated by a single `Makefile` target `make all`
- Raw data cached to `/data/raw/` with a manifest recording source URL, pull date, SHA256
- All random seeds fixed
- `requirements.txt` pinned; environment containerized (Dockerfile committed)
- Another researcher running `make all` on a clean checkout should produce byte-identical tables and figures
- The preregistration, audit, deviation log, and unexpected-findings log are all part of the deliverable, not internal artifacts

-----

## What This Plan Deliberately Does Not Do

- **It does not pursue the ILS demand question in Phase 1–5.** That is a contingent secondary question; it is only addressed in the final paper’s Discussion and the Substack piece, conditional on Q2’s answer. Pursuing it in parallel would invite confirmation bias.
- **It does not buy commercial data.** Every step is runnable from free/academic sources. If those prove insufficient, that is itself a finding worth publishing.
- **It does not try to settle causality.** Cross-sectional observational data cannot. The plan produces a defensible conditional correlation claim and is explicit about that ceiling.

