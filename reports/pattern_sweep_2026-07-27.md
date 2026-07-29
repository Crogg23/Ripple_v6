# Broad Unbiased Pattern Sweep — Ripple v6 Entity Spine
**Date:** 2026-07-27 · **Mode:** autonomous discovery scan, no seed question · **Worker:** Fable (hunting lane)

## How this was produced
- Census of all 4 Library databases first: 3,197 objects (LIBRARY_RAW.LANDING alone holds 1,951 tables — the "~91 tables" in the mission packet matches the mart tier only).
- 11 parallel finder agents, one per method axis: distribution profiles (marts split 4 ways + raw split 2 ways), temporal discontinuities, spine join-key degrees, universe/missingness, threshold bunching, cross-source co-occurrence. 94 raw findings.
- Every candidate that mattered got an **independent adversarial verifier** told to kill it: re-derive the number with its own SQL, then hunt for loader caps, schema design, stale loads, population artifacts, documented causes, and column-meaning misreads. 28 verifications ran across two rounds.
- Score: **8 CONFIRMED, 11 WEAKENED (real but corrected), 8 REFUTED.** Every ranked item below shows the *verified* numbers, not the finder's first pass.
- Read-only throughout. Nothing built, nothing published. ~682+231 tool calls, ~2.25M agent tokens, a few hundred queries on COMPUTE_WH.

**Known traps honored:** ~60 RAW tables sit at exactly 500,000 rows (bulk-discovery loader cap) and were never treated as universes; `_RESTORE`/`_BAK`/`ZZ_RETIRED` backups, `FINDINGS` views (prior findings), and `LIBRARY_STAGING` (1:1 views over raw) were skipped.

---

## THE RANKED LIST (strongest signal first)

### 1. A tiny cluster of donors generates a fifth of all FEC contribution rows — at $23 a pop
- **Tables/fields:** `LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS` — DONOR_NAME, TRANSACTION_AMT, TRANSACTION_TYPE
- **Anomaly:** A hyper-frequent sliver of small-dollar donors — many reading as retirees — each has thousands to tens of thousands of separate recorded micro-contributions routed through conduit platforms (ActBlue/WinRed-style earmarks).
- **Magnitude (verified, strict name+city+state grain):** 7,052 person-cells (0.17% of ~4.2M donors) account for **17,672,814 rows = 21.0%** of the 84.2M-row table but only **$326.0M = 1.5%** of dollars (avg $23.18/txn). Extreme case verified: one Maryland donor, **75,946 contribution rows** averaging **$1.51**, 95% type-15E conduit earmarks across 116 committees, 2023–2026.
- **Mechanism guess:** Recurring/split micro-charge patterns on conduit platforms concentrating on a small set of habituated donors — same shape as documented donor-exploitation dark patterns.
- **Verification:** CONFIRMED (no dup loads, memo rows negligible, landing=mart counts). Caveat: rows are reported earmarked contributions; slate-split checkouts mean rows ≥ card charges.
- **Confidence: high.** Who gets hurt: elderly/small-dollar donors on recurring charge treadmills.

### 2. The OSHA inspection table was destroyed by *today's* load — and logged as success
- **Tables/fields:** `LIBRARY_RAW.LANDING.FED_DOL_OSHA_INSPECTION` — all columns
- **Anomaly:** A zip archive was ingested as if it were a CSV (PK zip magic bytes sit inside a column name; the zip member filename fused onto ACTIVITY_NR). Columns are shifted ~2 positions on effectively **100% of rows**; the run replaced a previously-good table via atomic swap this morning and the density gate passed it.
- **Magnitude (verified):** 5,190,513 rows, single run `d8acbb8e` dated **2026-07-27 20:49**, status success. 50.0% blank OPEN_DATE; 19.1% carry the constant bogus date 2026-07-23; 0 OPEN_DATE values parse under any date format; addresses sit in ESTAB_NAME; no clean ACTIVITY_NR column exists (breaks the dbt staging model). Repo docs say the opposite ("OSHA is NOT a data problem") — this is new breakage.
- **Mechanism guess:** Loader unzip step skipped or bypassed; density check validated row counts, not column sanity.
- **Verification:** CONFIRMED. **Confidence: high.** This is the one item with a clock on it: the good table is gone and the defect is invisible to the pipeline's own checks.

### 3. The MSHA marts silently report zero mine deaths and zero serious violations
- **Tables/fields:** `LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS / _ACCIDENTS / _MINES` — IS_SIGNIFICANT_AND_SUBSTANTIAL, IS_FATALITY, DAYS_LOST, NO_INJURIES, ACCIDENT_DATE, IS_ACTIVE, LATITUDE
- **Anomaly:** The raw MSHA CSVs kept literal quote characters inside text values (`"Y"`, `"FATALITY"`), so every typed severity/date/geo cast in the marts silently fails and returns FALSE/NULL.
- **Magnitude (verified):** 0 of 3,087,215 violations flagged S&S vs **814,390 (26.4%) actually S&S**; 0 fatalities flagged vs **1,208 real deaths**; DAYS_LOST, NO_INJURIES, ACCIDENT_DATE 100% NULL on all 273,623 accidents; IS_ACTIVE=false for all 91,906 mines (~6,631 truly active); mine LATITUDE 100% NULL.
- **Mechanism guess:** CSV quote-stripping missing in the loader; dbt predicates (`sig_sub='Y'` etc.) can never match.
- **Verification:** CONFIRMED. **Confidence: high.** Any mine-safety analysis on these marts hides 1,208 deaths.

### 4. EPA's penalty column stamps one settlement onto hundreds of facilities — $2.3B of phantom fines
- **Tables/fields:** `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO` — LAST_PENALTY_AMT, DATE_LAST_PENALTY (flows into EPA_PENALTY_GAP)
- **Anomaly:** Identical corporate settlement amounts repeat verbatim across huge facility blocks, so any sum over facilities multiplies single enforcement actions by up to ~650x.
- **Magnitude (verified, strictest same-amount + same-exact-date grain):** 40 groups / 5,675 rows implying **$2.27B** where the underlying actions total **$13.5M**; ~10-11% of the mart's entire $22.25B penalty mass. Proof it's case-level: mart-wide SUM(LAST_PENALTY_AMT)=$22.25B **exceeds** SUM(TOTAL_PENALTIES)=$10.9B, which is impossible for a facility-level field. Example: $468,600 stamped on 652 CELLCO/Verizon cell-site rows, all dated 2009-11-24.
- **Mechanism guess:** ECHO exporter semantics (case-level value carried per facility) inherited unlabeled into the mart — a loaded trap for every downstream penalty aggregate.
- **Verification:** CONFIRMED. **Confidence: high.**

### 5. The 13F table mixes two currencies-of-scale in one column — off by ~1000x across eras
- **Tables/fields:** `LIBRARY_RAW.LANDING.FED_SEC_13F_HOLDINGS` — VALUE, _SRC_FILE
- **Anomaly:** 2013–2022 files report holding values in **thousands of dollars**; 2024–2026 files report **whole dollars**; same TEXT column, no unit flag, no normalization anywhere in dbt (staging drops VALUE entirely). Any query spanning eras is wrong by ~1000x.
- **Magnitude (verified):** per-file median VALUE 534–1,205 for every 2013q2–2022q3 file vs 306,844–459,572 for every 2024–2026 file — clean separation, exact 1000x unit factor (SEC rule change effective Jan 2023). Bonus defects: **coverage hole 2021q3–2023q4** (no files), 51 rows claiming single positions >$200B, 5 rows claiming >100B shares, 1.89M zero-value rows.
- **Verification:** CONFIRMED. **Confidence: high.** Fix is mechanical (×1000 on pre-2023 files) since eras are file-separated.

### 6. Three-quarters of the 62M-row FAERS drug-safety corpus is column-shifted with its join key destroyed
- **Tables/fields:** `LIBRARY_RAW.LANDING.FED_FDA_FAERS_DRUG/_REAC/_INDI/_DEMO/_OUTC`
- **Anomaly:** For every legacy-era quarter (2004q1–2012q3), pandas promoted the first column (ISR — the case join key) to an index that `write_pandas` silently dropped, left-shifting every value one column. Outcome codes sit in the ISR column; genders sit in AGE_COD.
- **Magnitude (verified):** ~**47M of 62.3M rows (~75%)** across all five tables are shifted; 4,012,896 of 5,147,466 OUTC rows (78.0%) have no outcome code in either column; the case join key is unrecoverable without reload. Bug is documented nowhere; warnings sit unread in `logs/faers_err_*.log`. (The "stops at 2014q2" half of the original claim is *transient* — the checkpoint file shows an in-flight chronological backfill at 41/89 quarters, advancing daily.)
- **Mechanism guess:** Legacy AERS trailing `$` delimiter + `pd.read_csv` default `index_col` behavior in `scripts/fda_faers_load.py`; fix is `index_col=False` + reload of legacy quarters.
- **Verification:** CONFIRMED (corruption part). **Confidence: high.** Eight years of drug death/hospitalization outcomes currently can't be tied to any case or drug.

### 7. The federal debarment list is ≤9% loaded — and its status flags are fabricated
- **Tables/fields:** `LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS` (from raw `FED_SAM_EXCLUSIONS`)
- **Anomaly:** The SAM.gov exclusions pull truncates at a round 9,000 rows (~100k+ real universe); every date field is empty in raw (wrong JSON path), so IS_CURRENTLY_EXCLUDED=true on all 8,500 mart rows is an artifact of always-blank termination dates; the entity/individual flag can never fire (tests `last_name is null`, loader writes `''`); registry VOLUME literally says "0 rows"; all runs logged success. The 2026-07-24 re-pour hit the same 9,000 cap.
- **Magnitude (verified):** 9,000 raw / 8,500 mart rows vs ~100k+ universe; ACTIVATION_DATE null 8,500/8,500; IS_ENTITY_NOT_INDIVIDUAL true on 0 rows despite 1,401 'Firm' rows.
- **Verification:** CONFIRMED (row-cap was partially known from the 7-23 audit at its older 1,000-row state; the fabricated flags/dates are new). **Confidence: high.** Any "debarred but still getting federal money" check silently misses >90% of banned contractors.

### 8. CFPB complaints have become a single-purpose automated credit-dispute pipe
- **Tables/fields:** `LIBRARY_RAW.LANDING.FED_CFPB_COMPLAINTS` — Date received, Product, Company, Submitted via
- **Anomaly:** Complaint volume grew ~20x in six years while collapsing onto one product and three companies.
- **Magnitude (verified on distinct complaint IDs):** 277,243 complaints (2019) → **5,443,422 (2025)**, Jan–Jul 2026 already 4.49M (annualizing ~7.9M, ~28x); credit-reporting share 50.0% → **90.3%**; TransUnion+Equifax+Experian absorb **77.0%** of all 17.2M complaints ever; 99.4% arrive via web. (The finder's fourth pillar — narrative rate collapsing to 2% — was a publication-lag artifact; the true mature decline is ~42%→~26%.)
- **Mechanism guess:** Industrial credit-repair/template filing flooding the bureaus, drowning organic complaints.
- **Verification:** WEAKENED (3 of 4 pillars confirmed exactly). **Confidence: high.** Who gets hurt: consumers with real fraud/servicing complaints losing triage capacity.

### 9. A few nursing-home chains run near-uniformly one-star facilities at 4–6x the national fine rate
- **Tables/fields:** `LIBRARY_MARTS.DBT_CROGERS.HEALTH__FED_CMS_NURSING_HOME` — CHAIN_NAME, OVERALL_RATING, fines, turnover
- **Magnitude (verified, incl. per-bed normalization):** Reliant Care Management: 32 facilities, avg rating 1.19, 28/32 one-star, $126,704 fines/facility (4.5x per-bed), 61% nurse turnover. Arcadia Care: 22 facilities, avg 1.45, $175,951/facility (5.0x per-bed). Combined: **42 of 52 rated facilities one-star vs 19.8% base rate (~4.1x)**; CMS's own chain-average columns corroborate.
- **Mechanism guess:** Chain-level operating model (understaffing/turnover) reproducing deficient care across acquisitions; fines don't change the model.
- **Verification:** CONFIRMED. **Confidence: high.** ~5,000 residents live in these facilities. (Side find: the mart's date columns parse to NULL — staging format mismatch.)

### 10. Unpaid mine-safety fines concentrate on ~100 operators — after stripping out the boring two-thirds
- **Tables/fields:** `LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS` (+ raw controller history) — AMOUNT_DUE, AMOUNT_PAID, PROPOSED_PENALTY, CONTROLLER_ID
- **Anomaly:** The naive "30% of proposed penalties unpaid" claim is mostly legal reduction; what survives is still a concentrated delinquency pile.
- **Magnitude (verified):** True outstanding = **$191.4M of $1.463B finally assessed (13.1%)** — $357M of the naive gap is documented legal reduction, ~$30.5M is the normal 2025-26 billing pipeline, $20.9M is contested. **Top 100 of 43,276 violators hold ~51% of true outstanding**; Justice-family controller IDs hold $8.8M (4.6%) while overrepresented ~7x vs their share of assessed penalties; several top names are bankruptcy write-offs (Patriot, Alpha), but Justice and Hoops entities remain active through 2026.
- **Verification:** WEAKENED then corrected (both finder versions merged; every surviving number independently re-derived). **Confidence: high.** Miners at chronically delinquent operators face a gutted deterrent.

### 11. 44% of chronically noncompliant EPA facilities have no inspection on record — ever
- **Tables/fields:** `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP`
- **Magnitude (verified, with ECHO's 5-year-window semantics correctly applied):** of 93,808 active facilities noncompliant ≥4 of the last 12 quarters: **41,305 (44.0%) have no inspection date ever recorded**; 53,587 (57.1%) had none in the last 5 years; **86,963 (92.7%) paid zero penalty dollars** over a 5-year window that covers all their flagged noncompliance; median 9 of last 12 quarters noncompliant. Related unverified cut: facilities *missing demographic joins* are never-inspected at ~92% vs ~41% for mapped ones.
- **Mechanism guess:** Self-reported compliance status flows in with no enforcement follow-through. (Note: the mart was purpose-built to expose this gap — the number is the receipt, the mart choice is designed-in.)
- **Verification:** WEAKENED (window semantics corrected; core gap survives). **Confidence: high.**

### 12. 9,078 revoked nonprofits with $17.2B in assets still sit in the IRS master file as fully exempt
- **Tables/fields:** `LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_REVOCATION` × `ECONOMICS__FED_IRS_BMF` — EIN, WAS_REINSTATED, IRS_STATUS, RULING_DATE, ASSET_AMT
- **Anomaly:** The headline join (29,406 orgs / $42.7B) is two-thirds reinstatement-lag; the residual is the lead.
- **Magnitude (verified):** 20,328 of 29,406 have a BMF ruling date *after* revocation (reinstated; the revocation file's flag lags — known IRS sync issue). Unexplained residual: **9,078 orgs / $17.2B in assets** with pre-revocation ruling dates and no recorded reinstatement, spread across revocation years 2010–2024, asset-concentrated in foreign universities and 501(c)(14) credit-union group EINs (possibly group-ruling routes).
- **Verification:** WEAKENED (correctly shrunk). **Confidence:** high on the numbers, medium on meaning — needs case-level audit before it's a story.

### 13. The NHTSA investigations mart throws away 80% of its raw records on a wrong dedup grain
- **Tables/fields:** `LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS` (from raw)
- **Magnitude (verified):** 154,209 fully-distinct raw rows (one ingest run, zero load duplication) collapse to 30,748 mart rows (19.9%) because staging dedups on (action, make, model, year) while the true grain includes component and recall. The `resulted_in_recall` boolean survives intact (0 mixed groups), but **recall_number — the documented join key to the recalls mart — is an arbitrary pick in 2,317 groups** (up to 194 candidate recalls each) and the component dimension is lost in 8,326 groups (27%).
- **Verification:** WEAKENED (flag-corruption part dead; data-loss part solid; schema.yml itself says "grain not yet determined").
- **Confidence: high.** Defect-to-recall accountability trails are unreliable for ~7.5% of the mart.

### 14. ~150 long-excluded providers were still active enough in 2022 to be on pharma's payroll
- **Tables/fields:** `LIBRARY_META.CONNECT.ENTITY_INDEX` (LEIE × CMS Medicare Provider × Open Payments 2022)
- **Anomaly:** The finder's headline — "purged from Medicare (lift 0.17) yet over-represented in industry payments (lift 1.13), same population, opposite directions" — died on verification: the >1 lift is a denominator artifact (the 16.4M baseline includes ~6.8M non-NPI entities that can never match; in the correct 9.6M-NPI universe both lifts are <1: 0.10 vs 0.66), and 111 of the 112 Medicare overlaps are 2024+ exclusions hitting a CY2023 file — timing tautology, not measured purging.
- **What survives (verified):** **~150 of the 503 payment-overlap providers were excluded before or during 2022 (90 excluded pre-2020, zero reinstated) and still received 2022 industry payments** — a real cross-system gap, adjacent to the already-documented `banned_but_paid` pattern and extending it with the 2022 vintage.
- **Mechanism guess:** exclusion bars federal billing, not industry transfers; manufacturers don't screen payees against LEIE.
- **Verification:** WEAKENED (framing dead, residue solid). **Confidence: high** on the residue numbers. Patients are still being treated by practitioners barred from federal programs.

### 15. Six "included" sources are actually API sample stubs — and the freshness registry can't see it
- **Tables:** DBT_CROGERS marts for CFPB complaints (500 rows vs 17.2M in raw), ClinicalTrials (500 vs ~470k), FDA drug enforcement (5,000), HUDOC (2,000), IRS 990 (200 vs ~4-5M), HMDA (28,301 vs ~17-20M/yr) — vs `LIBRARY_META.REGISTRY` VOLUME fields
- **Anomaly:** All six sit at <1% of their own registry-documented universes, frozen at obvious API page caps (500/2,000/5,000), every one logged as a successful ingest — because nothing compares loaded rows to registry VOLUME, the platform's own freshness ledger certifies stubs as sources.
- **Magnitude:** 6 sources, all <1% of universe, all status=success, since June–July 2026.
- **Mechanism guess:** Dev-stub pulls promoted into mart schemas and never backfilled; the missing control is a row_count-vs-VOLUME check in the registry.
- **Verification:** unverified (numbers straight from catalog + INGEST_RUNS; low ambiguity). **Confidence: high** on the counts, and the *systemic* point — success-logging hides universe shortfall — is also what #2 and #7 exploited.

---

## Rediscoveries (real, but already in the repo's own record — not new leads)
- **Excluded providers paid by pharma after exclusion** ($363k/177 NPIs in 2023; $914k/377 across 2022-24): verified to the penny, but `lead_queue.sql` has a `banned_but_paid` detector and `outputs/PATTERN_MAP_2026-07-21.md` already publishes this exact pattern. Top case (Asfora/Medtronic royalties) is a known DOJ matter.
- **ARCOS Florida pill-mill concentration** (top 15 practitioner-buyers = 8.45% of channel MME, 13/15 in FL, #1 at 489x mean): every number reproduces, but the data window is 2006–2012 and this is the already-prosecuted, already-published WaPo-era story.
- **FJC IDB is 4.1M empty rows** (100% blank, all 20 columns): known — demoted to STATUS='empty' on 2026-07-12 by the density gate; never re-loaded, so the warehouse still holds ~zero usable federal civil dockets. Same family: **EOIR's 12.6M rows in one column** (recoverable in place via SPLIT on tab; already documented as FABLE_AUDIT item D12 with a queued re-pour) and **foreign assistance amounts 100% blank** (documented in `build_giant_aggs.py` as "BROKEN LOAD ... Flag for reload").

## Killed on verification (so nobody re-chases them)
- **"Epstein pages going dark Jan 2026"** — one 35-second Wayback 403 bot-block sweep; 91% of URLs back to 200 at next capture; 3 genuine 404s in the whole mart.
- **"OFAC-sanctioned vessels renamed in US waters"** — all four designations postdate the AIS snapshot by 16–28 months; the hulls were legitimately named, unsanctioned tankers on 2024-01-01.
- **"Entity spine does zero merging"** — true measurement, documented v1 design (hard-ID-only, zero-false-merge; fuzzy layer explicitly gated behind the Phase 6 eval).
- **"Match benchmark poisoned by sentinel NPIs"** — the 0.8764 precision was computed on a sentinel-free held-out split; sentinel generation already fixed 2026-06-28. Residue: warehouse GOLD_PAIRS/ENTITY_LINKS are stale pre-fix snapshots worth truncating.
- **"7 most-connected entities are all excluded providers"** — Open Payments vintage tables triple-count; six exclusions postdate the CMS file vintages; the seventh (Miranda) bills legally under a documented OIG sole-community waiver the finder didn't read (WAIVERDATE column).
- **"NHTSA recalls duplicated 6-9x in 2021/2025"** — native part-level grain of the NHTSA flat file (one giant tire recall = 19.3k rows), single ingest run. Live trap remains: the mart drops the part columns that reveal the grain, so naive unit sums inflate.
- **"635 false LEIE links in ENTITY_LINKS"** — real in the table, but pre-fix stale snapshot of a gated, no-consumer scratch table; code fixed 2026-06-28.

## Small-defect ledger (evidenced, unverified, worth one-line fixes)
- NEISS narratives 100% missing 2004–2025 — CPSC renamed the column to NARRATIVE_1 in 2004+ files; text exists in raw, mart maps the old name only.
- Open Payments 2022 truncated at exactly 13,250,000 rows (~1M+ short); propagated into both PUBLIC agg tables → every 2022-vs-2023/24 comparison biased low.
- USASpending: contracts table exactly 20,000,000 rows; assistance table has five years at exactly 1,000,000 rows and a 70x hole in 2012 — undocumented per-batch caps. Also uncorrected $344.7B typo-pair leaving ~$209M phantom in any sum.
- FEC contributions mart holds only 2023–2026 (99.98% of rows) while the name implies the full archive; undocumented scope.
- SEC insider marts stop at 2025-03-31, absent from the freshness registry (untracked staleness). Same family: MEDSL president returns end 2016, House 2018, Senate 2024.
- NOAA AIS: raw is the same single day loaded 8x (87% duplicate rows); the "maritime mart" is one calendar day (2024-01-01) of pings.
- USGS water: -999999 no-data sentinel passed through as real values in 62k rows (poisons any min/avg).
- Voteview votes mart includes the President's announced position as a phantom legislator (ICPSR 99912) — 478 rollcalls off by exactly +1, 25.5% of Senate rollcalls.
- POLITICS__MEMBER_PAC_MONEY: NULL-bioguide bucket is the single largest "member" ($29.3M PAC money, $394M outside spending).
- CONNECT_EDGES: BRIDGE CCN~NPI tier's MATCH_RATE averages 149% (max 860%) — wrong denominator on fan-out joins.
- FED_SEC_13F_SUBMISSION and FED_SEC_13F_POSITIONS are byte-identical twin loads of the same table under two names.
- FEC committee-to-candidate raw: ~25% of 24K-type rows carry unexplained negative amounts — needs cycle-baseline check.
- LEIE: 89.6% of excluded providers carry no real NPI (72% even for 2024 exclusions) — structurally caps every NPI-based "banned but operating" join at a floor.
- EPA FRS: facility dates parsed without a century (years 0–26); >half of facilities have impossible coordinates; ECHO has an inspection dated year 1016.
- EPA ECHO COMPLIANCE_STATUS null rates vary 30x by state (AL/GA/KY/FL mostly blank) — national compliance cuts silently drop whole states.

## Depth-limited leads (real numbers, no verification pass yet — candidates for the next mission)
1. SEC Form 4 lateness: 9.5% of insider filings filed beyond the 2-business-day deadline; 25,114 over 45 days, 5,412 over a year — clustered by specific filers.
2. UK Companies House: single postcodes hosting thousands of active companies with burst incorporation (one east-London postcode: 84% of its 7,507 active companies incorporated since Jan 2024); 2025 incorporations +53% YoY.
3. FEC: top 100 donor names hold 21.5% of all contribution dollars; organization-typed rows (0.036% of rows) inside the *individual* mart carry 16.3% of dollars.
4. Medicare provider utilization: 1,156 providers billing >500 services per beneficiary, largest cluster Nurse Practitioners (not pharmacies).
5. Open Payments 2024: teaching hospitals are 0.22% of records but 20.1% of dollars; single $91M "Acquisitions" payment to one Florida physician.
6. Part D: top 0.1% of prescribers = 5.5% of $288B; 132 prescribers at exactly 100% opioid rate. (Mega-prescriber outliers themselves verified as vaccine/LTC billing attribution — the residual question is whether standing-order NPIs obscure accountability.)
7. NHTSA investigations opened per year halved after 2015 (65 → ~30) while complaints stayed ≥90k/yr — regulator activity, not data artifact, if it survives verification.
8. WaPo fatal-force: race-unrecorded rate climbed 13x from 2015 to 2024; feed stops after 2024 (stale source?).
9. Federal Register: Oct-2025 output collapsed to 584 docs vs ~2,300/mo baseline (government shutdown fingerprint — excluded as externally caused, listed for completeness).

## Coverage notes (what this sweep did NOT do)
- LIBRARY_STAGING (1,031 views) untouched by design; ~60 exactly-500k-capped RAW tables profiled only as "capped" — their content distributions are load-order-biased samples.
- 13F filer/CUSIP concentration blocked by the unit break (#5) until normalized.
- No geographic clustering beyond value-range checks (AIS lat/lon, FRS coords).
- Small POLITICS reference tables (FJC judges, SCDB, FARA, Treasury/EDGAR minis) got sanity checks only.
- Co-occurrence lifts use whole-spine independence baselines; same-type clerical overlaps (CMS-family >600x) deliberately not reported. Item 14's verification showed whole-spine baselines overstate cross-type lifts — future co-occurrence work should compute lifts within the shared key-type universe.

## Provenance
- Run: 2 workflows, 39 agents total (11 finders, 28 verifiers), ~913 tool calls, ~2.25M agent tokens, read-only PAT-less ACCOUNTADMIN session on COMPUTE_WH (statement timeout 600s; a read-only runner script refused all writes).
- Finder→verifier protocol: every ranked item's numbers were re-derived by an independent agent instructed to refute it; verdicts and corrected magnitudes are shown in place of first-pass claims.
- Full raw material: 94 finder findings + all verdicts in session scratchpad (`all_findings.json`, workflow journals `wf_b460fa66-51b`, `wf_970873e3-7f5`).
