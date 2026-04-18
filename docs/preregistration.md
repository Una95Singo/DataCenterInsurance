# Preregistration — DC / SCS Clustering Study

**Committed:** 2026-04-18
**Status:** Frozen. Changes require a logged entry in `/docs/deviations.md`.

This document formalizes the analytical commitments of the study **before any data is examined**. It is extracted from §0.1–§0.3 of the execution plan and held here as the binding reference.

-----

## 1. Sharpened Primary Hypothesis

The loose question — “do data centers cluster in storm zones?” — is separated into two testable sub-questions:

- **Q1 (Clustering):** Do North American data centers exhibit statistically significant spatial clustering beyond what is expected from population density alone?
- **Q2 (Conditional SCS correlation):** After controlling for the legitimate siting drivers of data centers (power cost, fiber backbone, population, land cost, tax incentives, water, climate for cooling, competing nat-cat hazards), is there any residual relationship between data center density and severe-convective-storm exposure?

**Q2 is the primary question.** A raw overlay of DCs and SCS events will show a positive correlation because both cluster east of the Rockies for unrelated reasons. Only the conditional test is informative.

-----

## 2. Primary Specification

Poisson / negative binomial regression at the county level:

```
DC_MW_county ~ β₀ + β₁·SCS_exposure + β_controls·X + ε
```

Where:

- `DC_MW_county` = total installed MW in the county
- `SCS_exposure` = 30-year annual expected loss proxy combining tornado, hail, wind frequency (primary = H_reported)
- `X` = population density, industrial electricity price, fiber backbone density, IXP proximity, tax incentives, water/drought, cooling degree days, seismic PGA, flood zone coverage, land cost proxy

Residual spatial autocorrelation tested via Moran’s I; if present, re-fit with a spatial-lag or spatial-error model.

**β₁ is the coefficient of interest.** Its sign, magnitude, and confidence interval determine the study finding.

-----

## 3. Decision Thresholds (Pre-Committed)

|Finding           |Definition                                                       |Interpretation                           |
|------------------|-----------------------------------------------------------------|-----------------------------------------|
|Strong positive   |Standardized effect ≥ 0.3, p<0.01, robust to ≥3 sensitivity specs|DCs disproportionately sited in SCS zones|
|Strong negative   |Same magnitude/significance, opposite sign                       |Industry avoids SCS zones                |
|Weak / directional|p<0.1 but effect <0.3, or fragile                                |Suggestive, not dispositive              |
|Null              |                                                                 |effect                                   |
|Inconclusive      |Results flip sign across reasonable specs                        |Data cannot answer the question          |

These thresholds are committed before data is pulled. Any finding, including null, is publishable.

-----

## 4. Pre-Committed Sensitivity Specifications

All seven sensitivities run; finding is “robust” only if ≥5 of 7 agree in sign and approximate magnitude:

1. Substitute `H_reported` → `H_radar` (MESH-derived)
1. Substitute `H_reported` → `H_environment` (CAPE climatology)
1. Exclude Northern Virginia MSA (Loudoun, Fairfax, Prince William)
1. Hyperscaler-only subset
1. Metro-level (MSA) instead of county-level
1. Log(MW) vs. linear MW outcome
1. Recent construction (post-2015) only

-----

## 5. Scope Commitments

- **Geography:** CONUS only
- **Facility type:** Commercial colocation, hyperscaler, and wholesale data centers ≥1 MW IT load. Excluded: enterprise on-prem, edge compute <1 MW, crypto mining
- **Time horizon:** Facilities operational or under construction as of Q1 2026

-----

## 6. What Would Count as Falsification

To guard against motivated interpretation, these falsifiers are committed:

- If “DCs cluster in SCS zones,” the effect should be stronger for older / less-hardened builds. If it isn’t, the finding is suspect.
- If “DCs avoid SCS zones,” insurance pricing should show evidence of SCS risk being priced into siting decisions. If it isn’t, the avoidance may be coincidental.
- If “null,” β₁ should be consistently near zero across all seven sensitivity specs. Spec-fragile near-zero results are “inconclusive,” not “null.”

-----

## 7. Interpretation Lock-In

A one-paragraph “headline finding” draft is written for each of the five outcome categories **before the final regression is run.** The run picks which paragraph applies. This prevents post-hoc softening of null findings into “suggestive” or promotion of weak findings into “strong.”

-----

*This preregistration is binding. Deviations are logged in `/docs/deviations.md`.*
