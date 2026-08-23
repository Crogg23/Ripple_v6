# Wonder Wall — Ranking Pass

**Run:** 2026-08-22 · every data-readiness score below was verified with live queries against the warehouse this session (9 query batches). Nothing here is scored from table names.

**Scope:** all 75 wonders from `The_Wonder_Wall.md` plus 18 expansion wonders generated against verified-healthy tables. 93 ranked. Priority = M × D × C × E (max 625). Novelty is deliberately unscored — it belongs to the tabled "Pie in the Sky" project and has its own column so it can be joined in later.

**Axes:** **M** mechanism (5 = exposes a systemic dynamic, 1 = describes) · **D** data readiness (verified; broken upstream capped at 2) · **C** consequence to actual people · **E** effort (5 = one SQL + a chart, 1 = new pipeline / new math / animation engine).

---

## TOP 5 TO PROTOTYPE FIRST

Selection rule: highest priority score, with two adjustments stated openly — anything already built and run is excluded (see #26/#72 below), and where five wonders tied at 500 the tie was broken toward distinct source-and-mechanism coverage. Runners-up are named.

### 1. E1 — Which mine operators get the biggest discount between the penalty proposed and the penalty actually paid
**Score 625 (M5 · D5 · C5 · E5) · origin: expansion · lens: Surprise**

Every published violation count treats a citation as an event. This asks what the citation was actually worth after it was negotiated — enforcement that evaporates between assessment and collection, which no violation count anywhere shows.

- **Tables/columns:** `LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS` — `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`, `CONTROLLER_ID`, `CONTROLLER_NAME`, `MINE_ID`, `VIOLATION_OCCUR_DATE`, `SIG_SUB`, `NEGLIGENCE`.
- **The query:** `select controller_name, count(*), sum(proposed_penalty), sum(amount_paid), 100.0*sum(amount_paid)/sum(proposed_penalty) pct_paid ... group by 1 having sum(proposed_penalty) > threshold order by pct_paid asc`. Then repeat sliced by S&S flag, negligence level, and year to see whether the discount tracks severity.
- **Already measured this session:** $1.82B proposed vs $1.27B paid across 3.02M penalised violations — **69.9% collected, $548M assessed and never collected**. The worst-paying named operators land at 7.7%, 7.8%, 9.1%, 14.3%, 17.3%, 19.7%. One holds 1,801 violations, $5.62M proposed, $432,710 paid.
- **Effort:** under half a session for the core result. A second half-session to check whether the discount is contest-driven (appeals) versus non-collection, which changes what the number means.
- **Watch for:** `AMOUNT_PAID` is zero-not-null for uncollected rows, so a mean over all rows understates; use sums. Recent violations may still be in an appeal window — exclude the trailing 24 months before ranking.

### 2. E2 — Does the severity of a nursing-home citation depend on which state inspected it
**Score 625 (M5 · D5 · C5 · E5) · origin: expansion · lens: Surprise**

Same federal tag numbers, same federal law, 50 state survey agencies applying them. If severity assignment varies by state far more than facility conditions do, the regulator is the variable — and a resident's protection depends on their address.

- **Tables/columns:** `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES` — `STATE`, `SCOPE_SEVERITY_CODE`, `DEFICIENCY_TAG_NUMBER`, `SURVEY_DATE`, `CMS_CERTIFICATION_NUMBER_CCN`; joined to `HEALTH__FED_CMS_NURSING_HOME` for facility covariates (beds, staffing, ownership type, chain).
- **The query:** harm-level share per state = `sum(case when scope_severity_code in ('G','H','I','J','K','L') then 1 else 0 end) / count(*)`, grouped by state, then re-run holding the tag number fixed so you compare like citation to like citation.
- **Already measured this session:** harm-level share runs **12.50% (KY) and 12.07% (IL) down to 1.32% (NV) and 1.85% (MD)** — a **9.5x spread** across states with 2,000+ citations each. California, with 57,877 citations, sits at 2.54%.
- **Effort:** under half a session for the state ranking; one more session to hold tag, facility size and ownership type fixed, which is what turns it from a table into a finding.
- **Watch for:** real coverage is 2023–2026 (see readiness findings); state citation volumes differ 25x, so use rates and a minimum-volume floor.

### 3. #55 — Which mine's fatality-to-violation ratio breaks the pattern: deaths without a paper trail
**Score 500 (M5 · D5 · C5 · E4) · origin: wall · lens: Anomaly**

The highest-scoring wonder on the original wall. A death that generated no enforcement, or an enforcement record with no deaths behind it, is a mechanism with a body attached.

- **Tables/columns:** `LABOR__FED_MSHA_ACCIDENTS` (`IS_FATALITY`, `DEGREE_INJURY`, `MINE_ID`, `CONTROLLER_ID`, `ACCIDENT_DATE`, `NARRATIVE`) against `LABOR__FED_MSHA_VIOLATIONS` (`MINE_ID`, `CONTROLLER_ID`, `VIOLATION_OCCUR_DATE`, `SIG_SUB`), denominated by `LABOR__FED_MSHA_MINES` (`NO_EMPLOYEES`, `CURRENT_MINE_STATUS`).
- **The approach:** deaths per 1,000 violations and deaths per employee-year, per controller, over a fixed horizon — then rank the residual against the controller's own size and mine type. The 273,621 accident narratives are the receipt layer for whatever surfaces.
- **Verified:** 1,208 fatalities (`IS_FATALITY` and `DEGREE_INJURY='FATALITY'` agree exactly, and match the raw figure the July audit cited), 3.09M violations, 19,430 controllers with violations, 6,634 with accidents, 26 years of clean overlap.
- **Effort:** one session. Two aggregates, a ratio, and a size-adjusted residual.
- **Watch for:** raw ratios shrink toward the present (fixed-horizon rule); 48% of mines have null lat/lon so keep this non-geographic; `NO_EMPLOYEES` is null on 39,735 of 91,906 mines, so the employee denominator only covers active operations.

### 4. E7 — Do facilities in more-minority communities get inspected less while staying out of compliance longer
**Score 500 (M5 · D4 · C5 · E5) · origin: expansion · lens: Causal**

A finished mart nobody is using. It already carries compliance status, inspection counts, penalty totals, community racial composition and geography on one row.

- **Tables/columns:** `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP` — `PCT_MINORITY`, `QUARTERS_WITH_NONCOMPLIANCE`, `TOTAL_INSPECTION_COUNT`, `FORMAL_ACTION_COUNT`, `TOTAL_PENALTIES`, `CHRONIC_NO_PENALTY`, `NEVER_INSPECTED_NONCOMPLIANT`, `IN_MAJORITY_MINORITY_COMMUNITY`, `LATITUDE`/`LONGITUDE`, `STATE`, `POPULATION_DENSITY`.
- **The query:** decile facilities by `PCT_MINORITY`, then compare mean inspections, mean quarters-in-noncompliance and chronic-no-penalty share across deciles; repeat within state and within program type to strip out where-the-industry-is confounding.
- **Already measured this session:** inspections fall **2.90 → 1.46** from the whitest to the most-minority decile while quarters in noncompliance rise **8.24 → 8.85**. 86,963 of 93,808 facilities (92.7%) have zero penalties; 53,587 (57.1%) were never inspected while noncompliant.
- **Effort:** one session for the honest version — the raw gradient is one query, but the state/program controls are what make it defensible.
- **Watch for:** 29,702 rows (32%) are missing `PCT_MINORITY` and 5,653 are missing geography — check whether the missingness itself is patterned before reporting anything. Penalty dollars run the *other* way (higher in high-minority deciles), so the finding is about inspection, not fines; say so or it reads as overstated.

### 5. E8 — Does a nursing home's staffing level predict its next deficiency, holding size and state fixed
**Score 500 (M5 · D5 · C5 · E4) · origin: expansion · lens: Causal**

Staffing is the one lever a regulator can actually pull. Deficiencies are the harm it is supposed to prevent. Nobody has connected the two on this data yet.

- **Tables/columns:** `HEALTH__FED_CMS_NURSING_HOME` — seven reported staffing measures, five case-mix-adjusted ones, `TOTAL_NURSING_STAFF_TURNOVER`, `REGISTERED_NURSE_TURNOVER`, `NUMBER_OF_ADMINISTRATORS_WHO_HAVE_LEFT_THE_NURSING_HOME`, `NUMBER_OF_CERTIFIED_BEDS`, `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`, `OWNERSHIP_TYPE`, `CHAIN_NAME`, `STATE` — joined to `HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES` on CCN for the forward-looking outcome.
- **The approach:** staffing measured at time T, deficiency count and severity in the following window, with size, state and ownership type held fixed. Turnover is the sharper predictor to test first — it is the measure a facility can hide least.
- **Effort:** one to two sessions. The join is trivial; the care is all in the forward-window construction so you are predicting rather than describing.
- **Watch for:** the facility table is a snapshot, so staffing is "now" and the deficiencies are a 2023–2026 history — the forward window has to be built from `SURVEY_DATE` and the staffing snapshot treated as end-of-period, or the arrow points backwards.

**Tied runners-up at 500, both MSHA, both a session each:** **E10** (does a mine changing hands change its violation rate — roughly 9,500 mines have had two or more controllers, which is the ownership-change study nursing homes cannot support) and **E14** (does a death at one mine change violation rates at the same operator's other mines).

---

## THREE THINGS TO KNOW BEFORE READING THE TABLE

**The wall's own guess about which lenses were rich was wrong.** The handoff expected Density and Structure to be the deep quarries. Scored on M × D × C, they came out **second-worst and third-worst** of the ten single lenses above 25 (Structure 32.3, Density 31.9). The rich ones are **Surprise 52.4, Causal 47.8, Contagion 47.2** — so those are where the 18 expansion wonders were generated. The reason is structural, not accidental: density and structure are *display* lenses that mostly recover population and size, while surprise, causal and contagion are *mechanism* lenses, which is what the mission actually asks for. Full lens table below.

**Two wonders are already answered.** #26 and #72 (does a violation cascade to same-owner siblings; does it spread faster inside a clique) were built and run on **2026-08-21** with 20-draw control validation: nursing homes +13.3% over control, mines +34.3%, toxic-release sites +11.8%. They are excluded from the top 5 because prototyping them would be redoing yesterday's work. The live follow-on is **E13** — whether that co-spike survives controlling for the regulator's district office and calendar, which is the caveat that run flags about itself.

**MSHA is the healthiest source on this wall, by a distance.** 26 years of clean overlap between violations and accidents, a real ownership key stamped on every violation, penalty amounts proposed *and* paid, a fatality flag that reconciles exactly, and 273,621 rows of genuine prose narrative. Four of the top seven are MSHA and that is a finding, not a bias — most other sources on the wall turned out to be three-year windows.

### Lens ranking (original 75 only, M × D × C, effort ignored)

| Lens | Avg | n | Read |
|---|---:|---:|---|
| Cross-lens combos | 61.6 | 5 | Highest of all — combining two lenses genuinely adds mechanism, when both legs are sound |
| Surprise | 52.4 | 5 | **Expanded** — order-where-there-should-be-noise is the strongest mechanism family here |
| Causal | 47.8 | 5 | **Expanded** — highest mechanism scores on the wall, repeatedly killed by missing data |
| Contagion | 47.2 | 6 | **Expanded** — and the platform already has a rule engine for it |
| Anomaly | 45.8 | 5 | Bimodal: #55 is the wall's best wonder, #54 and #56 are its worst |
| Community | 45.6 | 5 | Solid; identity resolution is the recurring ceiling |
| Flow | 43.8 | 5 | Good mechanisms, repeatedly blocked by missing history |
| Prediction | 40.2 | 4 | Carried almost entirely by #59 |
| Structure | 32.3 | 7 | Expected to be rich; the domain taxonomy is too coarse to support it |
| Density | 31.9 | 7 | Expected to be rich; heat maps mostly recover population |
| Phase | 29.8 | 6 | Evocative framing, thin data |
| Compression | 25.6 | 5 | Mostly re-derives things already labelled |
| Narrative | 25.6 | 5 | See the special check below — half the lens is theoretical |
| Temporal | 24.4 | 5 | Killed by three-year windows across almost every source |

---

## SPECIAL CHECK — the Narrative lens (#66–70): half live, half theoretical

The brief asked whether free text actually exists. It does, but **not where the wall assumed**.

| Wonder | Text it assumed | What is actually there | Verdict |
|---|---|---|---|
| #66 inspection notes | CMS inspector notes | `DEFICIENCY_DESCRIPTION` is the canned federal tag label: **260 distinct values across 418,479 rows**, 277 tag numbers, avg 118 chars, repeated verbatim | **Dead as written** |
| #67 CFPB escalation phrases | complaint narratives | **Real: 3,825,161 narratives, avg 1,021 chars, max 35,984** — but no escalation outcome exists to predict (only response category / timely / closed) | **Half live** |
| #68 model legislation | state bill text | **No state legislation in the warehouse at all.** Federal bills carry only `TITLE` (avg 69 chars) | **Dead — needs a new ingest** |
| #69 FAERS dialects | adverse-event report text | FAERS has **no narrative column**, and the reporter-type field is one of the shifted columns | **Dead** |
| #70 enforcement sentiment | enforcement documents | Only short operational notes (EPA single-event violation comments, SDWA visit comments); no dated document corpus | **Dead as written** |

**The live free-text corpus, verified:** CFPB complaint narratives (3.83M, 2011–2026) · **MSHA accident narratives (273,621 real prose rows, avg 189 chars, 2000–2026, only 2 blank — the best long-run narrative corpus in the warehouse, with a hard fatality outcome attached)** · CPSC NEISS injury narratives (1.72M of 9.79M rows populated, 1999–2025) · NOAA storm event and episode narratives (1.78M rows, 39% blank).

So the Narrative lens is not dead — it is pointed at the wrong tables. The MSHA substitute is what #66 should have asked for.

## Cross-lens combos (#71–75) — flagged as instructed

| # | Score | Component check |
|---|---:|---|
| #72 | 300 | Both legs strong (#26 D4, #65 D4) — but **already answered**, see above |
| #75 | 320 | Both legs strong; this is #23 with a clock on it, and #23's evidence is already dramatic |
| #74 | 240 | Both legs verified end to end (the money→member→vote chain works) |
| #71 | 72 | Weak by construction — a presentation upgrade of #1/#2/#3, not a new question |
| **#73** | **72** | **FLAGGED: both components score low.** #8 is blocked (D2, broken domain taxonomy) and #52 is mechanism-poor (M2). Do not build. |

---

## DATA READINESS FINDINGS

Everything below was found while verifying the D axis. Bad news first.

### New defects found this session

1. **FAERS is column-shifted, and the shift is in the landing table too.** `FDA_DT` holds report codes `EXP` / `PER` / `DIR` on 4.27M rows where dates belong; `GNDR_COD` holds `Y`/`N` (E-sub values) on 4.28M rows against only 1.41M real F/M; `HEALTH__FED_FDA_FAERS_DRUG` shifts by one from `DRUG_SEQ` onward, so `ROLE_COD` holds drug names and `DRUGNAME` holds numbers. This confirms the July defect that was carried as unverified. It affects roughly 58M rows across the five FAERS tables and blocks four wonders outright (#5, #25, #49, #69). Because landing is shifted, it is an ingest defect, not a mart bug — a re-parse, not a rebuild.

2. **The nursing-home ownership-change flag is dead.** `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS` reads `'N'` on all 14,700 rows. CMS does not publish 14,700 facilities with zero ownership changes; this is almost certainly a load defect. It single-handedly blocks #17, #38 and #43 — three of the wall's highest-mechanism wonders.

3. **The portal dataset index is a capped crawl, not a census.** Five portals sit at exactly 25,000 rows (Canada, Australia, Virginia, HDX, UK) and two at exactly 10,000 — the round-count truncation signature. On top of that, 259,869 of 338,520 datasets (76.8%) expose no column metadata, and with-columns coverage is wildly uneven (Open Data DC 6,267 of 10,000; UK 0 of 25,000). Any "where is public data thin" reading measures the crawler. Blocks #6, #13, #35.

4. **OSHA ITA hours-worked has scale outliers.** `TOTAL_HOURS_WORKED` sums to 1,065 billion hours against 138.8M reported employees — about 7,672 hours per employee per year, which is impossible. Aggregate injury rates still come out BLS-plausible (delivery 6.3, air transport 5.34 days-away cases per 200k hours), so the corruption is in a tail that needs trimming before any per-establishment rate is trusted.

5. **OSHA ITA `EIN` is not a usable join key.** 43,260 blank of 398,620, and minimum length 1 on the non-blank values. Key on `ESTABLISHMENT_ID` instead. This is the same masked-ID trap as NPPES EIN and FCC ULS EIN.

6. **CFPB mart is 11,501 rows short of landing** (17,168,287 vs 17,179,788 — 0.067%). Small, but it is a gap, not a rounding artefact.

### Coverage limits that are not defects but change what is answerable

- **FEC individual contributions has no history.** 84.2M rows, and **99.99% of them fall in 2023–2026** (2023: 18.1M, 2024: 40.1M, 2025: 21.0M, 2026: 5.0M). Every year before 2021 combined is under 30 rows. Kills #50 outright and caps every FEC temporal wonder at three and a half years. Three rows carry a year-3312 date.
- **CMS deficiencies are really only 2023–2026.** The table spans 2017–2026 but the early years are a straggler tail: 273 rows in 2017 against 121,925 in 2024. CMS publishes a rolling window. Anything asking for "a decade" (#47) does not have one.
- **CMS penalties span 2023-06 to 2026-05 only**, with 2,470 of 16,180 (15%) carrying a null fine amount.
- **Congressional committee membership has no clock.** 3,879 rows with committee code, name, bioguide, party, rank and title — no congress number, no start date. It is a current snapshot, which kills #45's "money arriving *after* the seat" and caps #7 at correlation.
- **There is no OSHA violation data.** Only ITA injury summaries (2023/24/25) and case details. The inspections re-pull is mid-flight at roughly 300k of ~4.5M rows and rate-limited. Blocks #28.
- **There is no federal staffing or agency-headcount table anywhere** (nothing under OPM, FedScope, workforce, staffing or appropriations). USAspending agency aggregates are awards, not people. Kills #42, the wall's best causal question.
- **There is no MSHA inspector identifier.** Kills #4.
- **There is no state legislation, and federal bills carry title only.** Kills #68.
- **Cosponsorships and roll-call votes are congresses 118–119 only** (2023-01 to 2026-06). Fine for network work, but "career" questions (#56) have two terms to work with.
- **48% of mines have no coordinates** (44,356 of 91,906 null latitude) and 43% have no employee count. Keep MSHA work non-geographic and be careful with per-worker denominators.
- **NEISS narratives are 82.5% blank** (8,079,416 of 9,794,971) and average 64 characters where present.
- **NOAA storm events are 41% without coordinates** (736,104 of 1,780,730) and 39% without an event narrative.

### Surprises worth knowing

- **CFPB is 77% three credit bureaus.** TransUnion 4.60M + Equifax 4.51M + Experian 4.12M = 13.2M of 17.17M complaints. Any CFPB density, community or flow analysis that does not handle this just rediscovers the big three.
- **CFPB narratives are industrially templated.** The single most-repeated narrative text appears **27,510 times**; the next five appear 24,241 / 18,431 / 15,803 / 12,204 / 10,903 times. 2.57M distinct texts across 3.83M narratives. #23 is not a hypothesis — it is visible in one GROUP BY.
- **CFPB responses are near-canned too.** Experian answers 79.2% of 4.12M complaints with one response category; JPMorgan 79.4%, Wells Fargo 78.9%, Capital One 77.4%.
- **61.6% of FEC contribution rows say `RETIRED` or `NOT EMPLOYED`** — and the blank-occupation bucket, only 2.7M rows, carries the single largest dollar total at $5.2B. The occupation axis is emptiest exactly where the money is.
- **The politics money→member→vote chain is fully wired and verified.** 54,195,669 contributions ($6.86B) reach 695 sitting members through `POLITICS__MEMBER_FEC_ID` → `FEC_CAND_CMTE_LINKAGE`; 1,067,437 votes reach 635 members through ICPSR → bioguide; the windows overlap exactly. **This corrects a standing note that politics had zero verified cross-family joins** — that is no longer true.
- **Cross-domain entity bridging is nearly nonexistent.** Only 105,724 of 33.2M entities (0.32%) appear in two domains, none in three, and 78% of the index is labelled `other` across just five domain buckets. The useful axis is key-type reach instead: **EIN spans 34 source tables, NPI 32 (9.6M entities), CCN 23, CIK 19, FRS_ID 15 (5.4M entities)** — which is #12's answer, sitting in one GROUP BY.
- **The connection map is mostly weak-tier.** 4,910 edges: CORROBORATED 2,670 at an average 7.1% match rate, STEEL 1,386 at 52.8%, BRIDGE 496, GEO 353, STRONG 5.
- **`ENVIRONMENT__EPA_PENALTY_GAP` is a finished, unused, mission-shaped mart** — 93,808 facilities with compliance status, inspection counts, penalty totals, community racial composition and coordinates on one row. See E7.
- **MSHA ownership changes are directly observable**: 6,358 mines had 2 controllers, 2,091 had 3, one had 11. Roughly 9,500 mines changed hands. 6,082 controllers hold 2+ mines.
- **The nursing-home clinician graph is too sparse to use.** Only **273 facility pairs** share 5 or more clinicians (40,841 nursing-home links of 2.26M total, and no dates). E15 was killed by this check.
- **`ENTITY_INDEX` is 84.4M rows, not 12.88M** — the figure on the wall and in The Laboratory is stale by a factor of six.
- **The MSHA zero-deaths defect carried since July is not present.** `IS_FATALITY` and `DEGREE_INJURY = 'FATALITY'` both return exactly 1,208, matching the raw figure the audit cited. That item can come off the carried list.

---

## FULL RANKING — all 93

Sorted by priority score (M × D × C × E). `origin: wall` = one of the original 75. `origin: expansion` = generated this session against verified-healthy tables.

| Rank | ID | Origin | Lens | Restatement | M | D | C | E | Priority | Novelty | Justification | Blocking defects / caveats |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| 1 | E1 | expansion | Surprise | Which mine operators get the biggest discount between the penalty proposed and the penalty actually paid | 5 | 5 | 5 | 5 | **625** | unscored | Enforcement that evaporates after assessment is invisible in every violation count anyone publishes - and the gap is enormous. | None. Verified: $1.82B proposed vs $1.27B paid across 3.02M penalised violations = 69.9% collected, $548M assessed and never collected. Worst named operators pay 7.7%-19.7% (one at 1,801 violations / $5.62M proposed / $432,710 paid). |
| 2 | E2 | expansion | Surprise | Does the severity of a nursing-home citation depend on which state inspected it | 5 | 5 | 5 | 5 | **625** | unscored | Same federal tags, same federal law, wildly different state hands - the regulator becomes the variable instead of the facility. | None. Verified: share of citations at harm-level severity (G-L) runs 12.50% in KY and 12.07% in IL down to 1.32% in NV and 1.85% in MD - a 9.5x spread across state survey agencies with 2,000+ citations each. |
| 3 | 55 | wall | Anomaly | Which mine's fatality-to-violation ratio breaks the pattern - deaths without a paper trail | 5 | 5 | 5 | 4 | **500** | unscored | Deaths that generated no enforcement is a mechanism with a body attached, on the healthiest source on the wall. | None. Verified: 1,208 fatalities (IS_FATALITY and DEGREE_INJURY='FATALITY' agree exactly, matching the raw figure the July audit cited), 3.09M violations, 19,430 controllers with violations and 6,634 with accidents, 26-year overlap. |
| 4 | E10 | expansion | Causal | Does a mine changing hands change its violation rate | 5 | 5 | 5 | 4 | **500** | unscored | This is the ownership-change study nursing homes cannot support, and mines can - the controller is stamped on every violation across 26 years. | None. Verified: 6,358 mines saw 2 controllers, 2,091 saw 3, up to one with 11 - roughly 9,500 mines changed hands at least once. 6,082 controllers hold 2+ mines. |
| 5 | E14 | expansion | Contagion | Does a death at one mine change violation rates at the same operator's other mines | 5 | 5 | 5 | 4 | **500** | unscored | A different trigger from the 08-21 rule - a body, not a citation count - and the strongest ownership key in the warehouse. | None. Verified: 1,208 fatalities, 6,082 controllers with 2+ mines, 6,634 controllers with accidents, 26-year overlap on MINE_ID / CONTROLLER_ID. |
| 6 | E7 | expansion | Causal | Do facilities in more-minority communities get inspected less while staying out of compliance longer | 5 | 4 | 5 | 5 | **500** | unscored | Mechanism-first, harm-first, geography-ready, already built - and the gradient is already visible. | 32% (29,702 of 93,808) missing PCT_MINORITY; 5,653 missing geo; 44% null last-inspection date. Verified gradient: inspections fall 2.90 to 1.46 across minority deciles while quarters-in-noncompliance rise 8.24 to 8.85. |
| 7 | E8 | expansion | Causal | Does a nursing home's staffing level predict its next deficiency, controlling for size and state | 5 | 5 | 5 | 4 | **500** | unscored | Staffing is the lever a regulator can actually pull; deficiencies are the harm it is supposed to prevent. | 2023-2026 deficiency window. Seven reported plus five case-mix-adjusted staffing measures, turnover, and administrator departures all present across 14,700 facilities. |
| 8 | 2 | wall | Density | Nursing-home fines heat-mapped per owner instead of per location | 4 | 4 | 5 | 5 | **400** | unscored | 'Does harm follow ownership or geography' is a real mechanism test, and the chain axis is live. | CHAIN_NAME blank on 4,221 of 14,700 facilities (28.7%); penalties table covers 2023-06 to 2026-05 only. |
| 9 | 23 | wall | Surprise | Which company's CFPB narratives are too similar - templated robo-text | 4 | 5 | 4 | 5 | **400** | unscored | Not just answerable - already visibly true at a glance, and mass-produced complaints distort the signal for everyone reading it. | None. Verified: the single most-repeated narrative appears 27,510 times; the next five appear 24,241 / 18,431 / 15,803 / 12,204 / 10,903 times. 2.57M distinct texts across 3.83M narratives. |
| 10 | 26 | wall | Contagion | Does one nursing-home violation cascade to sister facilities under the same owner | 5 | 4 | 5 | 4 | **400** | unscored | ALREADY ANSWERED 2026-08-21: same-owner co-spike 76.8% vs a 20-draw control of 63.5% (+13.3%) across 2,524 spikes; mines +34.3%, TRI sites +11.8%. | Not a defect - this is built and run (scripts/ripples/neighbor_spike_rule.py). The open question is the report's own caveat: state inspector calendars vs owner management. |
| 11 | E11 | expansion | Causal | Do nursing homes lose stars after a fine, or do fines follow lost stars | 5 | 4 | 5 | 4 | **400** | unscored | A directional test with real dates on both sides settles which way the arrow points. | Penalties 2023-06 to 2026-05; rating-cycle survey dates present. 2,470 penalties (15%) carry a null fine amount. |
| 12 | E13 | expansion | Contagion | Does the same-owner co-spike survive controlling for the regulator's district office and calendar | 5 | 4 | 5 | 4 | **400** | unscored | This is the open follow-on the 2026-08-21 run names itself: sister sites in one district get visited together regardless of who owns them. | Needs a district or region field. MSHA violations carry no district column directly - it would be derived from mine state and county. The rule engine already exists. |
| 13 | E16 | expansion | Contagion | Does a complaint spike at one credit bureau appear at the other two within days | 4 | 5 | 4 | 5 | **400** | unscored | Isolates whether spikes are company events or filing-mill events - and the big three ARE the corpus. | None. Verified: TransUnion 4.60M, Equifax 4.51M, Experian 4.12M = 77% of 17.17M complaints, daily dates 2011-2026. |
| 14 | E3 | expansion | Surprise | Do self-reported OSHA injury counts bunch on round numbers, and does the bunching grow with employer size | 4 | 4 | 5 | 5 | **400** | unscored | Round-number piling in self-reported harm counts is an under-reporting signature, and the repo already has a bunching detector. | OSHA ITA has scale outliers: TOTAL_HOURS_WORKED sums to 1,065B hours against 138.8M reported employees (~7,672 hrs/employee - impossible), so the tail needs trimming. Aggregate rates come out BLS-plausible. |
| 15 | E4 | expansion | Surprise | Which companies answer nearly every CFPB complaint with the same canned response | 4 | 5 | 4 | 5 | **400** | unscored | A firm that answers 79% of four million complaints identically is not answering them. | Ceiling is bounded - only 6-8 response categories exist. Verified: Experian 79.2% one category across 4.12M complaints, JPMorgan 79.4%, Wells Fargo 78.9%, Capital One 77.4%. |
| 16 | E9 | expansion | Causal | Do OSHA establishments that reported a death change their reported hours or injuries the next year | 5 | 4 | 5 | 4 | **400** | unscored | Tests whether a fatality triggers a real safety change or a reporting change - and there is a genuine panel to test it on. | Verified: 219,860 establishments appear in both 2023 and 2024. Deaths fall 859 to 812 to 778 across the three years. EIN quality is poor (min length 1, 43,260 blank) so key on ESTABLISHMENT_ID. |
| 17 | 48 | wall | Temporal | Does mine inspection have a season, and do accidents cluster in the gaps | 4 | 5 | 4 | 4 | **320** | unscored | A seasonal enforcement gap that lines up with injuries is a mechanism with a named victim - and this is the longest verified overlap on the wall. | None. Violations 1994-2026 (3.09M, 31,277 mines) and accidents 2000-2026 (273,623) both carry real dates: 26 years of clean overlap. |
| 18 | 53 | wall | Anomaly | Which facility's inspection record is statistically impossible - too clean for its peers | 4 | 4 | 5 | 4 | **320** | unscored | 'Too clean' points at capture or non-inspection, which is a mechanism with residents on the other end. | Real window 2023-2026. Peer covariates (beds, staffing, ownership type, state) all present across 14,632 CCNs. |
| 19 | 75 | wall | Combo | Surprise + Narrative - entropy collapse in filing language over time | 4 | 5 | 4 | 4 | **320** | unscored | This is #23 with a clock on it, and #23's evidence is already dramatic. | None. 14 years (2011-2026) to watch templating arrive; the same credit-bureau concentration caveat applies. |
| 20 | E17 | expansion | Contagion | Do injury rates cluster within industry-and-state cells beyond what employer size explains | 4 | 4 | 5 | 4 | **320** | unscored | Same work, same state, different odds of getting hurt is a mechanism with a worker on the other end. | Same hours-outlier caveat as E3. 1,218 NAICS codes, 3 years, ~1.18M establishment-years. |
| 21 | 12 | wall | Structure | Which join key is secretly the most valuable in the whole warehouse | 4 | 5 | 3 | 5 | **300** | unscored | Tells you where to build next, which decides who gets found; the answer is already sitting in one GROUP BY. | None. Verified this session: EIN reaches 34 tables, NPI 32 (9.6M entities), CCN 23, CIK 19, FRS_ID 15 (5.4M entities). |
| 22 | 44 | wall | Causal | Does a fine actually change behaviour - trajectories before vs after, matched controls | 5 | 4 | 5 | 3 | **300** | unscored | The single most important question you can ask an enforcement dataset, and the pieces are all present. | 3-year window means short pre/post arms; 2,470 of 16,180 penalties (15%) have a null fine amount. 3,722 facilities have 2+ penalties; 14,700-facility control pool with covariates. |
| 23 | 59 | wall | Prediction | Predicted vs actual inspection outcomes - the confident misses are the story | 5 | 4 | 5 | 3 | **300** | unscored | Residuals-as-the-finding is genuinely mechanism-first; this is #53 with a model behind it. | Same 2023-2026 window and same feature set as #53. |
| 24 | 72 | wall | Combo | Community + Contagion - does a violation spread faster inside a clique than between | 5 | 4 | 5 | 3 | **300** | unscored | The wall is right that this is the smoking-gun shape - and it was already run on 2026-08-21. | ALREADY ANSWERED: nursing homes +13.3% over a 20-draw control, mines +34.3%, TRI +11.8%. Components #26 and #65 both score well, so this is not built on weak legs. Open follow-on: inspector calendar vs owner management. |
| 25 | E12 | expansion | Causal | Does the special-focus designation actually change facility behaviour | 5 | 3 | 5 | 4 | **300** | unscored | A designed natural experiment sitting unused in the data. | Small and snapshot-only: 88 current SFF and 440 candidates, with no designation DATE - entry and exit timing would have to be inferred. |
| 26 | 24 | wall | Surprise | Are some facilities' inspection outcomes suspiciously low-entropy | 4 | 4 | 4 | 4 | **256** | unscored | The same result regardless of conditions points at the inspection process, not the facility. | Real coverage is 2023-2026: the deficiency table's 2017-2022 rows are a straggler tail (273 rows in 2017 vs 121,925 in 2024). |
| 27 | E5 | expansion | Surprise | Do nursing-home surveys bunch at the end of the certification window rather than at risk | 4 | 4 | 4 | 4 | **256** | unscored | If inspection timing is administrative rather than risk-driven, the whole inspection record measures the calendar. | Real window 2023-2026 only; SURVEY_DATE and INSPECTION_CYCLE both present across 418,479 rows. |
| 28 | 14 | wall | Structure | Which donor appears in the most different networks - small everywhere, present everywhere | 4 | 4 | 3 | 5 | **240** | unscored | The ubiquitous small donor is a genuinely different actor type from the big one. | Verified: top donor (name+ZIP) gave to 268 distinct committees. Identity is name+ZIP (CORROBORATED tier, not a hard ID); 2023-2026 window. |
| 29 | 22 | wall | Surprise | Does donation timing entropy drop right before key votes | 5 | 4 | 4 | 3 | **240** | unscored | Randomness collapsing into pattern around votes is a textbook mechanism claim, and the chain is verified end to end. | Verified: 54.2M contributions ($6.86B) reach 695 sitting members; 1.07M votes reach 635 members; windows overlap exactly. Individual contributions only; 2 congresses. |
| 30 | 65 | wall | Community | Which facilities cluster by behaviour rather than ownership - acting like a chain without being one | 5 | 4 | 4 | 3 | **240** | unscored | A behavioural chain that is not a legal chain is exactly a hidden mechanism, and CHAIN_NAME gives you ground truth to check against. | 14,700 facilities x ~50 numeric features verified populated; 2023-2026 for the deficiency-derived features. |
| 31 | 74 | wall | Combo | Causal + Flow - money before votes vs after, as two overlaid rivers | 5 | 4 | 4 | 3 | **240** | unscored | Strong mechanism on a chain that is verified end to end. | 54.2M contributions ($6.86B) reach 695 members; 1.07M votes reach 635 members; exact 2023-2026 overlap. Two congresses only. |
| 32 | 18 | wall | Phase | The percolation curve of the edge map - how close is the warehouse to one component | 3 | 5 | 3 | 5 | **225** | unscored | About the platform rather than the world, but it directly sets the next build. | None. CONNECT_EDGES is 4,910 rows with tier/match-rate/confidence: CORROBORATED 2,670 (avg 7.1% match), STEEL 1,386 (52.8%), BRIDGE 496, GEO 353, STRONG 5. |
| 33 | 41 | wall | Flow | Complaint volume migrating between financial products over time | 3 | 5 | 3 | 5 | **225** | unscored | Clean, long, one query - but describes migration rather than explaining it. | None. 17.17M complaints, 23 products, 180 issues, 2011-2026. |
| 34 | E18 | expansion | Contagion | Does an enforcement action at one facility change inspection frequency at its neighbours | 5 | 3 | 5 | 3 | **225** | unscored | Deterrence spillover is a real regulatory mechanism. | The penalty-gap mart is a snapshot with counts, not an event stream - the timed version needs the underlying EPA ICIS action records wired in. |
| 35 | 30 | wall | Contagion | Do CFPB complaint surges propagate from one company to its competitors | 4 | 4 | 3 | 4 | **192** | unscored | Attention spreading through a sector is a real dynamic and the series is the longest clean one available. | 2011-12 to 2026-07 (14 years), 8,084 companies. 'Sector' must be defined carefully around the credit-bureau mass. |
| 36 | 40 | wall | Flow | Out-of-state money flooding small races | 4 | 4 | 3 | 4 | **192** | unscored | Outside money in low-attention races is a real, consequential dynamic and the chain works. | Same verified chain as #37 plus CAND_OFFICE_DISTRICT. 2023-2026 window. |
| 37 | 7 | wall | Density | Congressional fundraising density mapped onto committee assignments | 4 | 3 | 4 | 4 | **192** | unscored | Money pooling around specific seats is a genuine mechanism; the money half is fully wired. | Committee membership has NO date or congress column - it is a current snapshot (3,879 rows, 528 members, 228 committees). Comparison is possible; change is not. |
| 38 | 3 | wall | Density | CFPB complaints heat-mapped by company instead of place | 3 | 4 | 3 | 5 | **180** | unscored | Reframes the unit but 'firms as hotspots' largely tracks customer-base size. | 77% of the 17.17M complaints are three credit bureaus (TransUnion 4.60M, Equifax 4.51M, Experian 4.12M). |
| 39 | 33 | wall | Compression | Nursing homes in compressed space - do bad actors form a visible island | 3 | 5 | 4 | 3 | **180** | unscored | Descriptive, but on unusually rich features and trivial compute. | None. ~50 numeric features per facility across 14,700 rows, zero null lat/lon. |
| 40 | E6 | expansion | Surprise | Does contribution timing spike on filing-deadline eves rather than spreading evenly | 3 | 4 | 3 | 5 | **180** | unscored | Deadline-driven money is a known artefact; worth measuring so it can be subtracted from #22. | 2023-2026 window; TRANSACTION_DATE is a real DATE with only 583 nulls in 84.2M rows. |
| 41 | 17 | wall | Phase | Is there a fine threshold where nursing-home owners start restructuring | 5 | 2 | 5 | 3 | **150** | unscored | Behavioural phase change under enforcement pressure is exactly the shape Ripple wants - and the signal column is dead. | BLOCKED: PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS reads 'N' on all 14,700 rows (a dead column, near-certainly a load defect). No ownership-history table exists. |
| 42 | 37 | wall | Flow | Political money as literal rivers - donor regions into candidate regions | 3 | 4 | 3 | 4 | **144** | unscored | Out-of-state money is real, but the map largely restates population. | Chain verified: donor ZIP (99.94% usable) to CMTE_ID to CAND_CMTE_LINKAGE to CAND_OFFICE_ST. 2023-2026 window. |
| 43 | 67 | wall | Narrative | Which phrases in CFPB narratives predict escalation | 4 | 3 | 4 | 3 | **144** | unscored | The text exists; the outcome to predict does not, and the corpus is contaminated. | 3.83M narratives available, but the only outcome fields are COMPANY_RESPONSE / IS_TIMELY / IS_CLOSED - no litigation or referral flag. The 27,510-copy templated texts contaminate any text model. |
| 44 | 10 | wall | Structure | Which nursing-home parent company is the highest-centrality node | 2 | 4 | 4 | 4 | **128** | unscored | In a chain-to-facility star graph, 'centrality' IS facility count - the question answers itself. | Chain data is healthy (636 chains, 572 with 5+ facilities); the graph structure is the weak part, not the data. |
| 45 | 11 | wall | Structure | Which member of Congress is the bridge node in the cosponsorship network | 4 | 5 | 2 | 3 | **120** | unscored | Coalition-holders are a real structural mechanism, but nobody is harmed by the answer. | Clean: 367,735 cosponsorships, 635 members, 29,211 bills, dates present. Congress 118-119 only. |
| 46 | 29 | wall | Contagion | A bill spreading through the cosponsorship network - who catches it, who is immune | 4 | 5 | 2 | 3 | **120** | unscored | Clean diffusion data, but the outcome does not name a harmed person. | None. 367,735 cosponsorships with dates, original/withdrawn flags, 29,211 bills. |
| 47 | 45 | wall | Causal | Does committee assignment cause donation shifts - money arriving after the seat | 5 | 2 | 4 | 3 | **120** | unscored | There is no 'after the seat' to measure. | BLOCKED: committee membership has no dates and no congress number - a current snapshot only. |
| 48 | 47 | wall | Temporal | One facility's fine history as a plain line up-and-right for a decade | 2 | 3 | 4 | 5 | **120** | unscored | A single line is a receipt, not a map - and there is no decade. | Penalties span 3 years; deficiencies are only real from 2023 (273 rows in 2017 vs 121,925 in 2024). |
| 49 | 63 | wall | Community | Congressional voting communities ignoring party labels | 4 | 5 | 2 | 3 | **120** | unscored | Defection structure is real; nobody is harmed by the answer. | None. 945,523 votes, 3,364 rollcalls, 639 members, party present. |
| 50 | E15 | expansion | Contagion | Do nursing homes connected by shared clinicians behave alike | 5 | 2 | 4 | 3 | **120** | unscored | Good idea, verified too sparse to carry it. | BLOCKED: only 273 facility pairs share 5+ clinicians in the nursing-home slice (40,841 of 2.26M affiliation links), and the affiliation table has no dates. |
| 51 | 62 | wall | Community | Shell-company clusters as tight communities in the ownership graph | 4 | 3 | 3 | 3 | **108** | unscored | A real graph, disconnected from any US harm. | ICIJ relationships is 3,339,267 edges over 1,131,496 start nodes and 14 relationship types - but offshore-leaks only, mostly pre-2017, with no verified wire into a US harm dataset. |
| 52 | 64 | wall | Community | Do CFPB complainants form communities - organised campaigns | 4 | 3 | 3 | 3 | **108** | unscored | There is no complainant identity, so this collapses into #23. | CFPB publishes no filer ID; the only proxies are ZIP (36,538 values) and the narrative text itself. |
| 53 | 39 | wall | Flow | Executives moving between violating companies ahead of enforcement | 5 | 2 | 5 | 2 | **100** | unscored | Strong mechanism with no dated people-to-org history anywhere in the warehouse. | BLOCKED: only ICIJ officers (771,315, offshore-only), IRS 527 directors/officers (189,593), and CMS FACILITY_AFFILIATION (2.26M NPI-to-CCN links, NO dates - snapshot only). |
| 54 | 43 | wall | Causal | Do ownership changes cause fine-rate changes at nursing homes (diff-in-diff) | 5 | 2 | 5 | 2 | **100** | unscored | Textbook design, no treatment events to point it at. | BLOCKED: same dead ownership-change flag as #17/#38. See E10 - the identical study IS runnable on mines. |
| 55 | 66 | wall | Narrative | Inspection-note language as topics over time | 4 | 2 | 4 | 3 | **96** | unscored | The 'inspection notes' are not notes. | BLOCKED: 418,479 deficiency rows carry only 260 distinct DEFICIENCY_DESCRIPTION values across 277 tag numbers, avg 118 chars - it is the canned federal tag label, repeated. NOTE: MSHA accident NARRATIVE is the live substitute (273,621 real prose rows, avg 189 chars, 2000-2026, 2 blank). |
| 56 | 38 | wall | Flow | Ownership churn as a flow map - nursing homes moving between parents over a decade | 4 | 2 | 5 | 2 | **80** | unscored | There is no decade and there is no churn record. | BLOCKED: CHAIN_NAME is one snapshot; the change flag is dead ('N' on all 14,700 rows). Same blocker as #17/#43. |
| 57 | 20 | wall | Phase | At what date does the politics spine percolate into one mesh | 3 | 3 | 2 | 4 | **72** | unscored | The answer is already known and it is an artefact: money, votes and cosponsorships all start in 2023 because that is when the loaders pulled. | Not a defect, but the finding would describe the ingest, not the institution. |
| 58 | 21 | wall | Surprise | The whole warehouse coloured by entropy - noisy chaos vs suspiciously orderly regions | 3 | 3 | 2 | 4 | **72** | unscored | Maps the warehouse, not the harm. | COLUMN_HEALTH covers 8,613 columns across only 247 of ~4,800 tables (5%), from a stale 2026-07-28 run. |
| 59 | 27 | wall | Contagion | Removing one parent company - the trophic cascade, what dies downstream | 3 | 3 | 4 | 2 | **72** | unscored | As written it is a simulation without a dependency structure; nothing actually 'dies' when a chain is deleted. | No structural blocker, but no downstream-dependency data to cascade through either. |
| 60 | 34 | wall | Compression | Members of Congress plotted by voting behaviour alone | 3 | 4 | 2 | 3 | **72** | unscored | DW-NOMINATE already exists and is literally a column in the members table; this re-treads it. | 945,523 votes, 3,364 rollcalls, 639 members. NOMINATE dims present but population unverified (modern rows sampled as empty strings). |
| 61 | 57 | wall | Prediction | A facility's projected trajectory as a dotted line | 2 | 3 | 3 | 4 | **72** | unscored | Extrapolation is not a mechanism. | 3-year window is thin for projection. |
| 62 | 61 | wall | Community | The donor network as visible cliques - coordinated blocks, not individuals | 4 | 3 | 3 | 2 | **72** | unscored | Coordination is a real mechanism; identity and scale are the problem. | Donor identity is name+ZIP (CORROBORATED tier, not a hard ID); pairwise co-giving over 84.2M rows is the real cost. |
| 63 | 71 | wall | Combo | Density + Temporal - a heatmap that breathes | 2 | 4 | 3 | 3 | **72** | unscored | A presentation upgrade of #1/#2/#3, not a new question. | Inherits the 2023-2026 window from its components. |
| 64 | 73 | wall | Combo | Anomaly + Structure - is the weirdest record also a high-centrality node | 4 | 2 | 3 | 3 | **72** | unscored | FLAGGED per brief: both components score low - #8 is blocked (D=2) and #52 is mechanism-poor (M=2). | Inherits #8's broken domain taxonomy for the centrality half. |
| 65 | 8 | wall | Structure | Which single entity is the hidden bridge between two domains nobody connects | 4 | 2 | 3 | 3 | **72** | unscored | The premise does not survive contact with the taxonomy. | BLOCKED: ENTITY_INDEX has only 5 domain labels and 78% is 'other'; just 105,724 of 33.2M entities (0.32%) span two domains and none span three. |
| 66 | 1 | wall | Density | FEC donor money as a national heat surface | 2 | 4 | 2 | 4 | **64** | unscored | Where giving is thick mostly recovers where people and money already are; population is the confound. | Money window is 2023-2026 only (99.99% of 84.2M rows); 3 rows carry a year-3312 date. |
| 67 | 28 | wall | Contagion | Do OSHA violations spread through industries like an epidemic | 4 | 2 | 4 | 2 | **64** | unscored | Good shape, wrong dataset present. | BLOCKED: there are NO OSHA violations in the warehouse - only ITA injury summaries (2023/24/25) and case details. The inspections re-pull is mid-flight at roughly 300k of ~4.5M rows and rate-limited. |
| 68 | 52 | wall | Anomaly | Which one donor visibly pops out of an otherwise normal cluster | 2 | 4 | 2 | 4 | **64** | unscored | One dot is a receipt, not a map - this is the scope-law failure mode in wonder form. | Data fine; the question is the problem. |
| 69 | 25 | wall | Surprise | Where does FDA adverse-event reporting become uniform - the batch-filed signature | 4 | 1 | 5 | 3 | **60** | unscored | Would be a strong finding on an intact corpus. | BLOCKED: FAERS column shift verified live - FDA_DT holds report codes 'EXP'/'PER'/'DIR' on 4.27M rows, GNDR_COD holds Y/N on 4.28M rows, and FAERS_DRUG shifts from DRUG_SEQ onward. The shift is in LANDING too, so it is an ingest defect. |
| 70 | 36 | wall | Compression | Do donor giving patterns compress into a small set of archetypes | 3 | 3 | 2 | 3 | **54** | unscored | The occupation axis is mostly empty exactly where the money is. | 61.6% of the 84.2M rows say RETIRED or NOT EMPLOYED; the blank-occupation bucket is only 2.7M rows but carries the largest dollar total ($5.2B). |
| 71 | 58 | wall | Prediction | Which companies the model flags as next to appear in CFPB data | 3 | 3 | 3 | 2 | **54** | unscored | 'Lookalikes' need attributes to look alike on. | CFPB carries company NAME only - no EIN, no LEI. A firm-attribute crosswalk would have to be built first. |
| 72 | 9 | wall | Structure | Which ZIP codes are load-bearing across domains | 3 | 3 | 2 | 3 | **54** | unscored | Geography as connector is real, but ZIP-level bridging mostly restates population density. | No ZIP-keyed edge tier exists; the GEO tier is 353 edges, mostly state grain. |
| 73 | 42 | wall | Causal | Regulator staffing cuts lined up against the violation rate right after | 5 | 1 | 5 | 2 | **50** | unscored | The best causal question on the wall, and the warehouse has no staffing data at all. | DEAD: nothing under OPM / FedScope / workforce / staffing / appropriations. USAspending agency aggregates are awards, not headcount. |
| 74 | 15 | wall | Phase | Watching MSHA + OSHA + CFPB become one regulatory system | 4 | 2 | 3 | 2 | **48** | unscored | Compelling frame, no seam to sew it on. | BLOCKED: no verified key joins the three. MSHA keys on MINE_ID/CONTROLLER_ID, OSHA ITA on EIN (64% populated, min length 1 = junk), CFPB on company NAME only (no EIN, no LEI). |
| 75 | 4 | wall | Density | MSHA violations clustering around inspectors' territories | 4 | 1 | 4 | 3 | **48** | unscored | Good mechanism, no data: territory-following heat would be a strong finding if it could be measured. | DEAD: no inspector identifier exists in any MSHA table (violations carry EVENT_NO / VIOLATION_NO / MINE_ID / CONTROLLER_ID / VIOLATOR_ID only). |
| 76 | 46 | wall | Causal | Do CFPB spikes cause policy changes, or just precede press releases | 4 | 2 | 3 | 2 | **48** | unscored | The effect side of the causal claim has no data. | BLOCKED: no corporate policy-change or press-release corpus exists in the warehouse. |
| 77 | 6 | wall | Density | The 338K portal datasets as a density map by topic - where are the data deserts | 3 | 2 | 2 | 4 | **48** | unscored | Absence-as-evidence is a real meta-mechanism, but this would measure the crawler, not the world. | BLOCKED: the index is a capped crawl - five portals sit at exactly 25,000 rows and two at exactly 10,000; 259,869 of 338,520 (76.8%) expose no column metadata. |
| 78 | 60 | wall | Prediction | Which open lead-queue items a scoring model would rank first | 2 | 4 | 2 | 3 | **48** | unscored | Points at the platform's own backlog, not the world. | Verified: LIBRARY_MARTS.REVIEW.LEAD_QUEUE holds 17,306 rows. |
| 79 | 32 | wall | Compression | All the spine tables squashed to 2D - do entities collapse into unnamed types | 3 | 3 | 2 | 2 | **36** | unscored | The features are too thin to embed meaningfully. | ENTITY_INDEX is 84.4M rows now (the 12.88M figure on the wall is stale) but carries only entity_type, key_type, source_table, domain, row_count. |
| 80 | 49 | wall | Temporal | One drug's adverse-event line across its whole market life | 2 | 1 | 4 | 4 | **32** | unscored | Descriptive, and on the corrupted corpus. | BLOCKED: FAERS column shift (see #25). |
| 81 | 50 | wall | Temporal | A member's fundraising rhythm across a whole career | 2 | 2 | 2 | 4 | **32** | unscored | There is no career in this data. | BLOCKED: FEC individual contributions are 99.99% inside 2023-2026 (2023: 18.1M rows, 2024: 40.1M, 2025: 21.0M, 2026: 5.0M). Every prior year combined is under 9,000 rows. |
| 82 | 69 | wall | Narrative | Do patient-filed and company-filed adverse-event reports use different dialects | 4 | 1 | 4 | 2 | **32** | unscored | Two blockers at once. | BLOCKED: FAERS has no narrative text at all, and the reporter-type column (OCCP_COD) is one of the displaced columns. |
| 83 | 5 | wall | Density | FDA adverse-event density per drug class over time | 3 | 1 | 5 | 2 | **30** | unscored | Consequential question sitting on a corrupted corpus with no class mapping. | BLOCKED x2: FAERS is column-shifted (verified live in landing AND marts), and no drug-class lookup table exists. |
| 84 | 31 | wall | Contagion | A single enforcement action propagating through the spine, as animation | 3 | 3 | 3 | 1 | **27** | unscored | The animation is the deliverable here, not the finding. | No blocker; needs an engine that does not exist. |
| 85 | 16 | wall | Phase | At what similarity threshold does the donor network snap into one continent | 4 | 3 | 2 | 1 | **24** | unscored | Real percolation question; the cost is pairwise over 84.2M rows. | Data present; scale is the blocker, not readiness. |
| 86 | 35 | wall | Compression | The 96 portals compressed by what they publish - which are near-duplicates | 2 | 2 | 2 | 3 | **24** | unscored | Would compress crawl coverage, not publishing behaviour. | BLOCKED: same crawl caps and 76.8% missing column metadata as #6/#13. |
| 87 | 70 | wall | Narrative | The sentiment arc of enforcement documents across an administration | 3 | 2 | 2 | 2 | **24** | unscored | No dated document corpus to arc. | The candidates (EPA NPDES single-event violation comments, SDWA visit comments) are short operational notes, not documents; cross-administration coverage unverified. |
| 88 | 68 | wall | Narrative | Bill-text similarity across states - model legislation spreading | 5 | 1 | 4 | 1 | **20** | unscored | A first-class systemic mechanism with zero data behind it. | DEAD: no state legislation exists in the warehouse at all, and federal bills carry only TITLE (avg 69 chars) plus LATEST_ACTION_TEXT - not bill text. Requires a new ingest. |
| 89 | 19 | wall | Phase | Would TDA find a hole in the political money network | 3 | 3 | 2 | 1 | **18** | unscored | A 'void' needs a defined metric space and an interpretation; high risk of an unreadable result. | No blocker, but new math and no guarantee of a legible answer. |
| 90 | 54 | wall | Anomaly | Which single FEC filing is the weirdest in the whole corpus | 1 | 4 | 1 | 4 | **16** | unscored | Explicitly 'just to see' - no mechanism, no person. | None; the question has no destination. |
| 91 | 13 | wall | Structure | Which of the 96 portals is the centrality king of the portal index | 2 | 2 | 1 | 3 | **12** | unscored | Would measure crawl luck, not publishing behaviour. | BLOCKED: same crawl caps as #6; with-columns coverage is wildly uneven (Open Data DC 6,267/10,000 vs UK 0/25,000). |
| 92 | 56 | wall | Anomaly | Which member's single most out-of-character vote of their career | 1 | 4 | 1 | 3 | **12** | unscored | One dot off a line; no mechanism. | Congress 118-119 only, so 'career' is two terms. |
| 93 | 51 | wall | Temporal | The warehouse itself over time - the organism growing | 1 | 2 | 1 | 4 | **8** | unscored | The curve would measure rebuild history, not growth. | Table CREATED dates span only 2026-06 / 07 / 08 (793 / 1,281 / 847 tables) and reset on rebuild. TABLE_VITALS is a single 2026-07-28 run, not a series. |

---

## Method note

- Data readiness was verified with 9 batches of live queries against `LIBRARY_MARTS`, `LIBRARY_RAW`, `LIBRARY_META` and `LIBRARY_META.REGISTRY` on 2026-08-22 — row counts, null and blank rates, distinct-value counts, date ranges, key-coverage joins, and value samples. No D score was assigned from a table name.
- Per the standing rule, no column was accepted as a real key on a null check alone; every key claim here is paired with a distinct count and a value sample.
- Novelty is deliberately left `unscored` on every row so the tabled "Pie in the Sky" project can join on it later.
- Expansion wonders were generated only in the three lenses that scored highest on M × D × C among the original 75 (Surprise, Causal, Contagion), and only against tables verified healthy during the readiness pass.

*Generated 2026-08-22.*
