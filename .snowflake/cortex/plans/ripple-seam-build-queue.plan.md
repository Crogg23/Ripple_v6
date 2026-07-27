# Ripple Seam Build Queue

## What this is
A sequenced order of operations for building the seam map into real marts. Ranked by **harm-clarity x data-readiness**. Each finding mart is a LEAD (exact-ID or defensible match), never an auto-published claim — human review gates every one (per CLAUDE.md).

## The ordering is a RED call
Sequence below is a recommendation. "Where the light points first" is Chris's taste call — re-sort any wave by feel.

## Entity spine (the connective tissue)
NPI (health) · EIN (orgs) · FIPS/GEOID (place) · BIOGUIDE/CIK/UEI (politics/companies) · name+address (probabilistic fallback at scale).

---

## WAVE 0 — Infrastructure: the denominator
**Pour Census/ACS demographics (tract + county).**
You have the geographic skeleton (85K tracts, 3,222 counties, ZIP crosswalk) but NO population/demographic data. This is the denominator under Themes A, D, and I. It turns "50 overdoses" into "6x the national rate." Do this first; it unlocks the most downstream seams per unit effort.

---

## WAVE 1 — Health-money body count (build now, all data loaded)
Highest harm-clarity, cleanest joins, mission-core (who gets hurt is unambiguous).
- **A1 — Pharma to Prescriber to Overdose Death.** Open Payments (43M, 3yr) -> Part D opioid rate (1.4M) -> county overdose deaths. Join on NPI + FIPS. The flagship chain.
- **A2 — Excluded providers still working where patients are trapped.** LEIE -> Facility Affiliation (2.2M) -> Nursing Homes/Dialysis -> Shortage Areas. Extends the existing FINDINGS mart with the "no alternative" layer.
- **A5 — For-profit dialysis / nursing mortality premium.** Facility outcomes + ownership/chain + affiliated-doctor payments.
- **A6 — Drug markup.** NADAC acquisition cost (1.5M) vs. Part D reimbursement. Dollar harm.
- **A8 — Hospital financial-collapse forecast.** Cost reports (margins) + shortage areas + Medicaid dependence = closures not yet happened. Timely given Medicaid cuts.
- **I1 — Ghost economy of revoked nonprofits.** Already built as a FINDINGS candidate; harden and add the 990 index (5.5M) flow layer.

## WAVE 2 — Cheap re-pours that complete started chains
Each is a probe/sample today; each finishes a chain Wave 1 or the seam map already started.
- ClinicalTrials.gov full (500 -> ~400K): unlocks A3 buried-results -> FAERS.
- FDA drug recalls full (5K sample): unlocks A4 "how many bodies before a recall."
- DOJ False Claims full (19 rows): unlocks E4 repeat-fraud detection vs. Medicare billing + LEIE.
- DOJ Civil Rights cases (probe): unlocks E2 enforcement-decline.
- EOIR immigration court re-pour (12.6M rows, one usable column): unlocks F3 case-outcome-by-judge.
- Full HMDA (28K -> full): required for the redlining-echo seam in Wave 4.

## WAVE 3 — The money to power machine (data-ready, systemic)
Deep, clean, buildable today. Less "body count," more "how the machine works."
- **C1 — Money in to legislative inaction out.** FEC (84M) + PAC + voting/bill records.
- **C2 — Revolving door to enforcement cliff.** Appointees + Federal Register (94K) + EPA ECHO / FTC enforcement over time.
- **C3 — The invisible caucus.** Cosponsorship (367K) + shared donors network graph.
- **C4 — Foreign agents to money to votes.** FARA (21K) + FEC + votes.
- **B1 — Federal contractors who are active law-breakers.** USASpending (6.3M) + EPA ECHO (3.2M) + corporate crosswalk.
- **B5 — Insider selling before the collapse.** SEC insider (2.7M) + failed banks + complaint spikes.

## WAVE 4 — Geography of abandonment (needs Wave 0 ACS)
- **D1 — Compound death index.** Overdose + suicide + incarceration + shortage areas per-capita (needs ACS).
- **D2 — Redlining echo 1935->today.** HOLC (1,155 areas) + full HMDA (Wave 2) + ACS. The definitive version academics only do one city at a time.
- **D3 — Disaster meets bankrupt hospital.** NOAA Storm Events (1.8M, FIPS) + hospital financial health.

## WAVE 5 — Movement, global, frontier (mix of NOW and new pours)
Build-now: G1 sanctioned vessels in US waters (AIS 58M + sanctions + LEI) · G3 PPP to ineligible parties · F1 ICE to employment collapse (QCEW 3.6M) · F2 visa wage suppression (DOL 664K) · H1 US aid into conflict · H2 debt-cliff to violence · H3 environmental-defender killings to industries.
New pours (POUR+, not yet in warehouse): state Medicaid enrollment (A9 coverage-loss) · domestic Lobbying Disclosure (C6) · FEC expenditures-out (C5) · Medicare Advantage encounter data (A7) · Eviction Lab (D4) · property/deed records (D5) · ADS-B flight tracking (G2).

---

## Verification / definition of done per mart
- Built in LIBRARY_MARTS.FINDINGS (or a new marts schema) as a documented view/table with a COMMENT that states: what, who-gets-hurt, sources, join keys, caveats.
- Runs on plain SQL/dbt — no AI at runtime (AI is build-time only, per CLAUDE.md).
- Row count sanity-checked; libel-trap IDs excluded (e.g., NPI 0000000000, EIN 000000000).
- Flagged as LEAD, not published. Human sign-off required before any publication.
- Where a rate is claimed, ACS denominator is wired in (not raw counts mislabeled as rates).

## Critical files / objects
- `LIBRARY_MARTS.FINDINGS` - existing finding-candidate schema; new marts land here or alongside.
- `LIBRARY_MARTS.DBT_CROGERS` - dbt-built marts; the build target for durable tables.
- `LIBRARY_RAW.LANDING` - source tables (129 full sources + probes to re-pour).
- `THE_LIBRARY.GEOGRAPHY` - FIPS/tract/ZIP spine; ACS lands adjacent to power Wave 0.
- `LIBRARY_META` - catalog/wiring; register new sources here as poured.
