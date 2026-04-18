# Glossary — DC / SCS Research Project

Reference definitions for abbreviations and domain terms used in the execution plan and subsequent reports. Kept flat and short by design — extended explanations live in the paper.

**Maintenance rule:** When any agent introduces a new term in a report, paper section, or INBOX entry, that term is added here in the same PR.

-----

## Severe Convective Storm (SCS) Meteorology

**SCS — Severe Convective Storm.** Umbrella term for thunderstorm-driven hazards: tornadoes, large hail (≥1”), damaging straight-line winds (≥58 mph). The primary hazard class under study.

**CAPE — Convective Available Potential Energy.** A measure of atmospheric instability (J/kg); higher CAPE means more energy available to fuel thunderstorms. Used as a reporting-bias-free proxy for SCS potential. Think of it as the “fuel load” in the atmosphere — a necessary but not sufficient condition for severe weather.

**MESH — Maximum Estimated Size of Hail.** Radar-derived hail size estimate from NEXRAD reflectivity profiles. Because it’s observed by radar rather than reported by humans, it avoids the population-density reporting bias that affects SPC event records.

**EF rating — Enhanced Fujita scale.** Tornado intensity rating from EF0 (weakest, >65 mph) to EF5 (strongest, >200 mph), estimated from damage surveys.

**Return period.** Average interval between events of a given severity — a “100-year event” has a 1% annual exceedance probability. Insurance/reinsurance terminology.

**Reanalysis.** A retrospective reconstruction of past atmospheric state by feeding historical observations into a modern weather model. Used to build physically consistent long-horizon climatologies.

- **ERA5** — European reanalysis (ECMWF), global, hourly, 1940-present
- **NARR** — North American Regional Reanalysis (NOAA), 1979-present, higher resolution over NA

-----

## SCS Data Sources

**NOAA — National Oceanic and Atmospheric Administration.** US agency; parent of SPC, NWS, the storm databases.

**SPC — Storm Prediction Center.** NOAA sub-agency maintaining the tornado and severe-weather event databases. Located in Norman, OK.

**SWDI — Severe Weather Data Inventory.** NOAA archive combining radar-derived and reported severe-weather products, including MESH.

**Storm Events Database.** NOAA’s human-curated record of severe weather events from 1996, with location, magnitude, and damage metadata. Reporting is population-biased.

-----

## Data Center Industry

**DC — Data center.** Purpose-built facility housing compute, storage, and networking equipment. Scope in this project: ≥1 MW IT load, commercial operation.

**Hyperscaler.** Operator of massive cloud/compute infrastructure at a global scale. Working list: AWS, Azure, GCP, Meta, Apple, Oracle. Characterized by bespoke, owner-operated facilities typically 50–500+ MW.

**Colocation (“colo”).** A facility where multiple customers rent space, power, and cooling for their own servers. Think of it as a shared warehouse for computing, with the operator providing the building and utilities.

**Wholesale data center.** Operator leases entire buildings or large suites to a single customer (often a hyperscaler). Sits between colo and hyperscaler-owned on the scale-of-commitment spectrum.

**Edge compute.** Small, distributed facilities close to end-users, typically <1 MW. **Excluded from this study** — undefined population and different siting logic.

**IT load.** The electrical power consumed by compute equipment itself, as distinct from cooling, lighting, and overhead. The standard way to measure DC capacity.

**MW — Megawatt.** The unit of DC capacity. 1 MW ≈ the power used by ~750 average US homes. A mid-size colo is ~10–30 MW; a hyperscaler campus can exceed 500 MW.

**kWh — Kilowatt-hour.** Unit of energy (power × time). Industrial electricity prices are quoted in $/kWh.

**Availability Zone (AZ).** A hyperscaler’s logical grouping of one or more physical data centers designed to fail independently. Multiple AZs form a cloud “region.”

**Internet Exchange Point (IXP).** Physical infrastructure where networks connect and exchange traffic (“peer”). Proximity to an IXP reduces latency and transit cost — a known DC siting factor.

**Fiber backbone.** Long-haul fiber-optic network. DCs need dense, redundant fiber access; this heavily shapes siting.

**Tax abatement / incentive.** State or local reduction of property, sales, or use tax to attract DC investment. A dominant siting factor in states like Virginia and Iowa.

**Cooling degree days (CDD).** Climatology measure of how much cooling a location requires over a year. Higher CDD = higher operating cost. A climate-based siting consideration.

-----

## Geographic / Administrative

**CONUS — Contiguous United States.** The lower 48 states. Study area for this project.

**MSA — Metropolitan Statistical Area.** US Census geography unit defining an urbanized region and its economically integrated surroundings. Used for metro-level analysis.

**NoVa — Northern Virginia.** Loudoun, Fairfax, and Prince William counties. Houses the largest DC cluster in the world (~70% of global internet traffic transits Ashburn, VA). A known outlier that must be analyzed both with and without.

**FCC — Federal Communications Commission.** Source of fiber/broadband data via Form 477.

**EIA — US Energy Information Administration.** Source of industrial electricity price data via Form 861.

**FEMA — Federal Emergency Management Agency.** Publisher of the National Flood Hazard Layer.

**USGS — United States Geological Survey.** Publisher of the National Seismic Hazard Model.

-----

## Competing Natural Hazards (Confounders)

**NFHL — National Flood Hazard Layer.** FEMA’s mapped flood zones (100-year, 500-year). Used to control for flood-avoidance in DC siting.

**NSHM — National Seismic Hazard Model.** USGS probabilistic map of earthquake shaking hazard.

**PGA — Peak Ground Acceleration.** Standard seismic hazard metric, typically expressed as a fraction of g (gravitational acceleration) at a given exceedance probability (e.g., 2% in 50 years).

-----

## Insurance / ILS

**ILS — Insurance-Linked Security.** An umbrella term for financial instruments transferring insurance risk to capital markets: cat bonds, sidecars, industry-loss warranties.

**Cat bond.** Catastrophe bond — a security where investors receive a coupon but lose part or all of principal if a defined catastrophe event meets a trigger (parametric, indemnity, or industry-loss-based).

**Reinsurance.** Insurance purchased by insurers to transfer portions of their risk. The downstream layer where catastrophe exposure accumulates.

**RMS / Moody’s RMS.** Risk Management Solutions, a dominant catastrophe-modeling vendor. Proprietary; not used in this project’s primary analysis.

-----

## Statistical Methods

**H0 / H1.** Null and alternative hypotheses. In this project: H0 = no conditional relationship between DC siting and SCS exposure; H1 = a relationship exists after controlling for siting covariates.

**β (beta) coefficient.** In a regression, the estimated effect of a predictor on the outcome. The sign and magnitude of β on SCS exposure is the answer to the primary research question.

**Ripley’s K-function.** Spatial statistic measuring whether points are clustered, randomly distributed, or dispersed at a given distance scale. Compared against a null model of complete spatial randomness — or, in this project, population-weighted randomness.

**Moran’s I.** Test for spatial autocorrelation — whether a variable’s value at one location is correlated with its values at nearby locations. Used to check regression residuals and, if present, correct with a spatial-lag or spatial-error model.

**Kernel density estimation (KDE).** Smoothed density map constructed from discrete point locations by summing kernel functions centered on each point.

**Poisson / negative binomial regression.** Count-data regression models. Poisson assumes mean = variance; negative binomial handles overdispersion (variance > mean), which is typical for geographic count data.

**Complete spatial randomness (CSR).** Null model in which points are placed uniformly at random over an area. Used as a baseline for clustering tests — though in this project, population-weighted randomness is a more informative null.

**Confounder.** A variable associated with both the predictor and the outcome, creating a spurious relationship if omitted from the model. Population density is the dominant confounder here: it drives both DC siting and SCS reporting.

**Pre-registration.** Committing the analysis plan to a timestamped document before looking at the data, to prevent post-hoc specification search (“p-hacking”). This plan is itself a pre-registration.

**Sensitivity analysis.** Re-running the primary analysis under alternate but defensible specifications to test whether the finding depends on arbitrary choices. A finding that flips sign across sensitivities is not a finding.

**Propensity weighting.** Reweighting observations so that predictor-variable distributions match between groups, used to approximate experimental balance in observational data.

**Standardized coefficient.** Regression coefficient expressed in standard-deviation units of the predictor and outcome, enabling comparison across variables on different scales.

-----

## Project-Internal Terminology

**H_reported / H_radar / H_environment.** The three parallel SCS hazard layers constructed in Phase 1.2 — from SPC event reports (population-biased), from radar-derived MESH (less biased), and from CAPE climatology (no human-reporting component). Agreement across the three is the robustness test.

**Coverage check.** The Phase 2 audit step that compares captured DC counts and MW to published industry aggregates (Cushman & Wakefield, Synergy). Gate threshold: ≥70% of expected MW captured.

**INBOX.** The running project status log at `/INBOX.md`. The single authoritative surface for “what’s happening now” and “what’s ready to read.” The first file to check on every mobile check-in.
