# Ripple Library — Discovery Sweep
**Open-ended investigation across all 101 landed/modeled datasets · 2026-06-27**

## How this was produced
- **22 producers** (12 profiling batches covering every table + 10 targeted investigation tracks) ran concurrently, each finding then **adversarially re-checked by an independent skeptic** that re-ran the SQL and hunted for casting/definitional artifacts, then synthesized.
- **145 agents · 4.39M tokens · 1,799 SQL/tool calls · ~36 min.** All read-only (guarded helper refuses anything but SELECT/SHOW/DESCRIBE).
- **118 findings survived verification; 4 were rejected as artifacts.** Verdicts: 60 CONFIRMED as-stated, 58 DOWNGRADED (real but an overclaim trimmed / re-tiered). Tiers: 106 FACT, 12 LEAD.
- **I independently re-ran the 8 load-bearing headlines on my own connection — 100% reproduced.** Receipts (all 118 + SQL + verdicts): [discoveries_2026-06-27_findings.json](discoveries_2026-06-27_findings.json).

---

## TL;DR — the answer to "issues to fix, or garbage datasets?"
**Mostly neither-as-feared.** It sorts into four clean buckets:

| Bucket | Count | What it is |
|---|--:|---|
| 🔴 **INVESTIGATE** | ~25 | Real data, real stories — correlations, anomalies, beautiful signals worth publishing |
| 🟧 **HANDLE (dbt)** | ~20 | Real data with a query-trap (sentinels, grain, casts) — staging rules, not problems |
| 🟡 **FIX (loader)** | ~8 | Our loader fumbled a good source — re-run/re-parse |
| ⚫ **DROP / RE-SCOUT** | ~13 | Source captured page-chrome, not data — the only real "garbage" |

The **"76 landed" headline is inflated by ~13 dead scrapes.** And the four biggest assets (Open Payments, the vessel moat, the contractor spine, the sanctions list) each carry **one silent structural defect that makes the naive query wrong** — none are data *errors*, they're traps that look clean and fail quietly. That's the single most important takeaway.

---

## 🔴 THE FIVE THAT MATTER MOST (ranked by blast radius)
*All five independently re-verified by me on a fresh connection.*

**1. Half of CMS Open Payments is silently missing.** `FED_CMS_OPEN_PAYMENTS` is **2024-only** (15,385,047 rows); 2023 lives in a separate `_2023` table (14,700,786). Record-disjoint by `RECORD_ID`. **338 of our 353 existing leads ride the LEIE×Open-Payments edge** — any detector pointed at the unsuffixed table assuming "all years" is blind to ~51% of the data. *(FACT · #23 · STAGING)*

**2. The maritime moat sees exactly one day.** `FED_NOAA_AIS` "7.3M rows" is **a single 24-hour snapshot — 2024-01-01, 100% of rows.** Every "sanctioned vessel broadcasting" claim is one cross-section; loitering / port-calls / behavior-over-time are impossible until we land more AIS days. *(FACT · #2/#4 · SOURCE)*

**3. "Lockheed Martin" is 77 child UEIs / 26 *parent* UEIs / $75.0B that doesn't roll up.** The field meant to be the rollup key (`RECIPIENT_PARENT_UEI`) itself fragments into 26 UEIs. Every "top contractor" ranking is a floor, not the truth, until we build a normalization layer. *(FACT · #5 · DETECTOR/STAGING)*

**4. OpenSanctions catches 3× the broadcasting vessels OFAC does (6 vs 2)** on that one AIS day — and **5 of 6 broadcast a name with zero overlap to the sanctions listing.** Name-mismatch on a hard IMO match is a clean shadow-fleet-rename tell. *(FACT on the IMO identity · LEAD on "evasion" · #16/#17 · DETECTOR)*

**5. Two silent landmines in the primary sanctions table (LEIE).** `EXCLDATE` is `YYYYMMDD` text — `TRY_CAST(... AS DATE)` collapses all 83,464 rows into garbage 1970 dates (integer overflow); use `TO_DATE(col,'YYYYMMDD')`. And NPI is the literal string `'0000000000'` on **89.6% of rows** — a naive `[0-9]{10}` regex *passes* it, falsely FACT-grading 90% of name-only matches. *(FACT · #1 · STAGING)*

---

## 🔴 INVESTIGATIVE GOLD — real data, real stories
The findings that are about *the world*, not our pipeline. FACT unless tagged LEAD.

### Money & contractors
- **Brutal concentration: top 100 of 92,833 contractor UEIs capture 46.3% of $778.3B; top 1,000 capture 76.8%.** Stable on gross dollars. *(#51)*
- **$124.99 meal-cap fingerprint:** 20,666 Open Payments transfers priced at *exactly* $124.99, 99.7% Food & Beverage — a ~6–10× cliff one cent under $125, **across every major pharma maker, in both 2023 and 2024.** Behavioral economics showing up in regulated transfers. *(#8/#40 → meal-cap detector)*
- **The $91M endodontist:** largest single 2024 Open Payments transfer — $91.08M "Acquisitions" to Dr. Charles Goodis (NPI 1821157041) from physician-owned Edge Endo. **Caveat: a company buyout, not graft** — frame as mega-transfers. *(#34)*
- **EIN bridges the for-profit and tax-exempt worlds:** Caterpillar & VF Corp appear in *both* SEC EDGAR and the IRS revocation list on the same 9-digit EIN. n=2 proof-of-concept. *(#50 → EIN bridge detector once IRS BMF/990 lands)*

### US social panels (FIPS — the cleanest key in the warehouse)
- **Eastern Kentucky is the overdose + incarceration double-extreme epicenter:** 20 of 50 counties in the top decile of *both* metrics, despite KY being 3.9% of US counties (~10× over-representation). Robust to year alignment. **WV is the mirror image** — worst overdose, ~half KY's jail rate. *(#20/#7 → county_double_burden detector)*
- **Black residents jailed at a higher rate than White in 96% of measurable counties** (612/637 with ≥5k Black working-age pop); median ratio 3.16× (2019). The extreme outliers are *Northern-urban* (Staten Island 45.6×), which defies the "Southern" expectation. *(#54 → racial_jail_disparity detector)*

### Conflict (UCDP)
- **2024 set the all-time record for conflict *events* (28,816, ~11× 1989) — but deaths peaked in 2022, and the deadliest single year remains 1994** (824,156, of which Rwanda was 772,463 = 93.7%). Deaths-per-event collapsed ~26 → ~5.6. *(#19/#28)*
- **Civilians are ≥37% of all conflict deaths (1989–2024);** one-sided/civilian-targeting violence is 15% of events but 30% of deaths (~2.3× as lethal per event). *(#30)*

### Cyber, courts, geopolitics
- **Perimeter appliances (NAS/VPN/firewall) are disproportionate ransomware on-ramps:** 37% ransomware-linked in CISA KEV vs 16% for OS/browser; QNAP ~75–82%, SonicWall 67%, vs Microsoft 27%, Cisco 6%. *(#36)*
- **Ransomware leak-site posts grew ~29× from 2020 (270) to 2025 (7,939);** US is 45% of victims-with-known-country. Growth is *flattening* (H1-2026 only +8.5% YoY). *(#70/#94)*
- **Anthony Kennedy was empirically the swing justice** — in the majority on 76.4% of 5-4 decisions (409/535), the highest of any justice with ≥100 close votes (1946–2024). SCOTUS liberal-decision share: 68.5% (1960s Warren) → ~44% post-1970. *(#56/#57)*
- **Israel is the single most reliable US UN ally** (mean agreement 0.881 since 2010, #1 of 192); the US agrees with the *average* member only 46% of the time. *(#35, LEAD-flavored on the "2024 peak" sub-claim)*
- **US police killings rose ~12% after 2020** (985/yr 2015-19 → 1,101/yr 2020-24; 2021-24 each a new record, peak 1,175 in 2024); body cameras recorded only 17.2% of the 10,430 deaths. *(#76)*
- **Leiden "Russian ops in Europe" nearly tripled in 2024** (24 → 69). **AI incidents (OWID/AIID) climbed ~45× from 2012 (8) to 2025 (362)** — biggest doubling was 2020, not the post-ChatGPT kink. *(#86/#115)*

### Cross-country correlations *(LEAD — observational, small-n country-years, ISO3-normalized; UCDP name-joins are fuzzy)*
- **Life expectancy vs fertility = −0.81** (n=236, 2020); the biggest negative residuals are the **HIV belt** (Lesotho −15.9yr, Eswatini −10.9, South Africa −8.7) where AIDS decoupled lifespan from the demographic transition. *(#110)*
- **Corruption vs life expectancy +0.73; Gini vs homicide +0.53** — both robust and stable, but the "top-6 most murderous all high-Gini" anecdote is cherry-picked and false. *(#88/#89)*
- **World Bank IDS carries real forward-looking debt-service schedules out to 2032** (~12k future-year values) — a repayment-cliff finder waiting to be built. *(#25)*

---

## 🟧 HANDLE IN DBT — real data, query-traps (staging rules)
These are **not problems** — they're how raw public data behaves. Bake the rule into staging once.

| Source | Trap | The rule |
|---|---|---|
| LEIE | `EXCLDATE` epoch-overflow; NPI=`'0000000000'` (90%) | `TO_DATE(col,'YYYYMMDD')`; treat `'0000000000'`/blank NPI as null → name-match = LEAD only *(#1)* |
| USASpending | one row per **transaction**, not contract (9.6% excess, one key ×174) | dedup to award grain; `SUM` only `FEDERAL_ACTION_OBLIGATION`, never the cumulative cols *(#10)* |
| USASpending | "Lockheed" = 77 UEIs / 26 parent UEIs | parent-UEI + name-normalization layer before any ranking *(#5)* |
| OFAC SDN | `SDN_TYPE` = `'-0- '` (trailing space!) for 9,785 orgs | global `TRIM` + map `-0-`→NULL before any join *(#9)* |
| AIS↔OFAC | AIS stores `IMO8851273`, OFAC stores `8508462` | `REGEXP_REPLACE(IMO,'^IMO','')` + validity filter, or join on MMSI *(#3)* |
| AIS | `HEADING`=511 sentinel on 52% of rows | filter `<360` or AVG returns 356.9 instead of 186.8 *(#66)* |
| CDC injury/violence | `RATE=-999` sentinel (6,549 rows); `COUNT_SUP='1-9'` text | filter sentinels or `AVG(RATE)` = −38.5 instead of +11.6 *(#12/#33)* |
| Vera incarceration | prison series **dead-ends 2019**, blank≠0; 2025-26 empty stubs | prison only `YEAR='2019'`; jail usable through 2024; blanks ≠ decarceration *(#13/#32)* |
| Ember / FDIC banks | literal `'nan'` text → IEEE NaN that **poisons** aggregates | `NULLIF(col,'nan')` before cast *(#41/#78)* |
| CDC drug-poisoning | "rate" is **binned TEXT ranges**, not numeric | treat as ordinal categories *(#68)* |
| SEC EDGAR tickers | grain is per-**ticker** — 10,414 rows / 8,018 CIK (BMO=27 tickers) | dedup to CIK; CIK joins fan out *(#71)* |
| OWID milspend | absolute current US$, no GDP/pop, 644 SIPRI regional aggregates | normalize per-GDP; drop no-ISO aggregate rows before summing *(#74/#90)* |
| NOAA storm | `DAMAGE_PROPERTY` = bucketed 1/2/5×10ⁿ estimates, 57% flat $0 | treat as ordinal, never precise currency *(#61)* |
| FHFA HPI | latest year (2026) is Q1-only; `INDEX_SA` empty on 48% | `MAX(YR)` logic fakes a price crash; SA only on purchase-only flavor *(#81/#118)* |
| CMS pos_other | 270 foreign (CN/MX) + 230 territory rows in `STATE_CD` | exclude before any 50-state/FIPS crosswalk *(#99)* |

---

## 🟡 FIX — loader fumbled a good source
Re-run / re-parse; the source itself is fine.

- **DPRK missile tests** — loader **swallowed the header row** (all cols → `COL_N`, row 1 *is* the headers). Re-load. *(#109)*
- **Freedom House** — landed with the **xlsx title row as headers** (`FREEDOM_IN_THE_WORLD_2013_2025_RAW_DATA`); the real 44-field header sits in data row 1. Re-parse with correct header row. *(#62)*
- **Spain BORME** — company names/IDs landed in the **wrong column** (`ACT_DESCRIPTION`); mis-mapped, not hollow. *(#108)*
- **VA suicide appendix** — flattened PDF, 2 stacked sub-tables, positional `COL_n`. Needs a structured parse. *(#87)*
- **Open Payments naming** — rename unsuffixed → `_2024` or build a unioned all-years view, then audit every detector's table reference. *(#23)*
- Minor: FDIC `'nan'` text, Mapping-Inequality grade needs `TRIM/UPPER`, Treasury 4 blank shadow `_YR/_QTR` cols. *(#78/#85/#111)*

---

## ⚫ DROP / RE-SCOUT — the dead-scrape pile (the only real garbage)
**13 "landed" sources captured page-chrome, not data** — and several carry join keys in the catalog that silently return nothing. **The "76 landed" count is inflated by these.**

`fed_fdic_enforcement` (nav URLs) · `intl_ie_cro` (cookie-consent table) · `fed_nara_aad` (finding-aid pages) · `intl_gr_gemi` (UI/footer strings) · `fed_naag_multistate_settlements` (menu chrome) · `fed_slavevoyages_intraamerican` (empty HTML) · `fed_doj_fca_settlements` (nav + scraper errors) · `fed_doj_crt_cases` (1 nav row) · `fed_va_allcause_mortality` (PDF list-of-figures) · `intl_ch_zefix` (homepage chrome) · `fed_oyez` (25-row hollow stub) · `fed_wpa_slave_narratives` (mis-mapped — but names *are* in `TITLE`/`SUBJECTS`, salvageable) · `xc_nagix`/`intl_nti` DPRK (thin / stale).

**Action:** a **`degenerate_load` detector** — flag any landed source where every key column collapses to ≤1 distinct value — catches this whole class automatically.

---

## 🛠️ NEW DETECTORS this surfaced (the upside)
The existing 4 detectors put 338/353 leads on one edge. These are fresh, non-overlapping angles:

1. **`sanctioned_vessel_broadcasting` v2** — AIS × (OpenSanctions Vessel **∪** OFAC SDN, *not* replace — only 1,486/1,942 IMOs overlap), with a `name_mismatch` flag. *(#16)*
2. **`excluded_but_actively_billing`** — LEIE NPI × Part D / Medicare / facility, **date-gated on `EXCLDATE` < data year** and **waiver-aware** (the one survivor, NPI 1285673012, carries an OIG waiver → human-review LEAD, not auto-FACT). *(#27)*
3. **`county_double_burden`** — reusable p90∩p90 cross-axis extreme flag (overdose×jail today; any two county metrics tomorrow). *(#20)*
4. **`racial_jail_disparity`** — Black/White jail-rate ratio per county-year. *(#54)*
5. **`pharma_meal_cap_fingerprint`** — manufacturers with abnormal share of $124.xx F&B payments. *(#40)*
6. **`debt_repayment_cliff`** — WB IDS forward debt-service schedules to 2032. *(#25)*
7. **`degenerate_load`** + a **generic sentinel/NaN scanner** across all numeric-looking TEXT landing columns (catches `-999`, `'nan'`, `511`, `-0-` once). *(themes 2 & 4)*
8. **`EIN_bridge`** SEC↔IRS — once IRS BMF/990 is loaded. *(#50)*

## 📥 SOURCES / BACKFILLS worth loading
- **More NOAA AIS days** — turns the single-day snapshot into a surveillance series. *Biggest single moat unlock.* *(#4)*
- **Earlier Open Payments years** + the union view. *(#23)*
- **History backfills** for the snapshot-not-panel family: NOAA storm events (1950+), USGS earthquakes, Federal Register (beyond the 5,000-row API cap), SEC EDGAR financials (more quarters). *(#11/#42/#46/#58/#77)*
- **IRS BMF / Form 990** — activates the EIN bridge. *(#50)*

---

## 🧵 Cross-cutting themes
1. **Whole domains are data-poor or mis-shelved.** 6 domains have *zero* landed data (education, intl-procurement, crime_security, geo_demographics, elections_voting, immigration). And **49% of data-bearing sources sit in UNCLASSIFIED** — bigger than health_medicine — so a browse-by-domain hides ~half the moat and returns *false* holes (NICS, fatal-force, ransomware, CISA KEV are all landed under UNCLASSIFIED). **Catalog domain-tagging is the highest-leverage cleanup.** *(#24/#95)*
2. **Dead-scrape epidemic (13 sources)** — see DROP bucket. *(theme above)*
3. **"Looks like a panel, is a snapshot"** — AIS (1 day), HCRIS (1 cycle), SEC financials (1 quarter), CFPB (2 pulls), USGS (30-day rolling), storm events (2025), Federal Register / ClinicalTrials (API row-caps). **Registry needs a `SNAPSHOT` vs `PANEL` flag.** *(#4/#11/#26/#42/#46/#58/#77/#98)*
4. **TEXT-cast traps are systemic** — `-999`, literal `'nan'`→NaN, `511`, `-0-`, `YYYYMMDD` overflow, binned-text-as-number. One generic scanner pays for itself. *(theme 4)*
5. **The hard-ID edges are real; the name-only edges lie.** IMO/NPI/EIN/UEI/FIPS = FACT-grade and connect cleanly. Name-only joins (FARA country, UCDP↔OWID country-name) silently drop the biggest entities (DR Congo, "Bosnia"=Republika Srpska) — keep them **LEAD**. *(#22/#91/#96)*

---

## 🚫 Rejected (4) — killed by the skeptic pass, for honesty
- **IPC food-insecurity "every country carries 3 nested time-views"** — false; only 10 of 50 had all 3. Artifact.
- **NARA WRA "every column empty"** — cherry-picked 8 blank cols, omitted 2 populated ones.
- **HCRIS "26% cost-to-charge ratio > 1.0"** — 1,490 of 1,614 were the literal string `'nan'`; `TRY_CAST('nan')`→NaN > 1 is true. Pure casting artifact.
- **`excluded_but_actively_billing` as a clean FACT detector** — the single date-gated survivor has an OIG **waiver**; kept as a LEAD (#27), rejected as an auto-FACT.

---

## ⚠️ What I did NOT check (limitations)
- **I personally re-ran 8 of 118 SQLs.** The other 110 rest on the in-workflow adversarial verifier (which did re-run each one) — not a second independent pass by me.
- **Big tables were profiled by aggregate/sample, not exhaustively** — row-level anomalies in Open Payments (15.4M), NPPES (9.6M), AIS (7.3M), USASpending (6.3M), EPA ECHO (3.16M) could be missed.
- **Barely mined:** EPA ECHO (3.16M, untouched), the two Wayback DOJ-Epstein tables (1.5M + 25k, barely poked), FAOSTAT food security (279k), Istat (213k), ClinicalTrials (only a 500-row sample), FEC bulk beyond party, most OWID climate panels (CO2/temp/fossil) beyond profiling.
- **Correlations are associational** — observational, small-n country-years, no causal claim, no multiple-comparison correction (with 118 findings, expect a few chance "anomalies" — which is exactly why every entity claim is tiered FACT vs LEAD).
- **Country joins** normalized to ISO3 for OWID/WB; **UCDP is name-based and fuzzy** — those cross-country joins are LEAD only and drop unmatched names.
- **Read-only run** — nothing in the warehouse was modified.

---

## Appendix — all 118 verified findings, ranked (surprise/importance)
Full SQL + verifier notes for each: [discoveries_2026-06-27_findings.json](discoveries_2026-06-27_findings.json).

| # | Tier | Tag | S/I | Verify | Finding |
|--:|:--|:--|:--|:--|:--|
| 1 | FACT | data-quality | 7/8 | CONFIRMED | LEIE EXCLDATE is YYYYMMDD text: TRY_CAST(... AS DATE) silently collapses all 83,464 rows into 7 garbage 1970 dates (use TO_DATE(...,'YYYYMMDD')); and NPI is the placeholder '0000000000' on 89.6% of rows, not blank |
| 2 | FACT | coverage-gap | 7/8 | CONFIRMED | NOAA AIS '7.3M rows' is a single calendar day (2024-01-01) -- a vessel-tracking snapshot, not a longitudinal panel |
| 3 | FACT | data-quality | 6/8 | CONFIRMED | IMO normalization is mandatory: AIS stores 100% 'IMO'-prefixed values (and 2.24M placeholder-junk pings), OFAC stores bare 7-digit — naive string join returns exactly 0 matches; correct regex join finds 2 sanctioned vessels broadcasting |
| 4 | FACT | coverage-gap | 6/8 | CONFIRMED | FED_NOAA_AIS is a single 24-hour US-AIS snapshot (2024-01-01 only) — the entire OFAC<->AIS sanctioned-vessel bridge sees one calendar day, not a surveillance time series |
| 5 | FACT | data-quality | 6/8 | CONFIRMED | 'Lockheed Martin' is one prime fragmented across 77 child UEIs, 26 parent UEIs and 6 parent-name spellings - $75.0B of obligations; even the exact name 'LOCKHEED MARTIN CORPORATION' carries 42 distinct UEIs |
| 6 | FACT | trend | 6/8 | CONFIRMED | 1.21M IRS tax-exempt revocations are an administrative posting stream: 274,997 orgs auto-revoked on the 15-MAY-2010 Pension Protection Act purge (22.8%), every posting lands on the 15th, 14.9% later reinstated |
| 7 | FACT | contradiction | 7/7 | DOWNGRADED | West Virginia has the worst overdose but jails at ~half Kentucky's rate: WV contributes 0 to the OD+jail double-extreme set while Kentucky (lower OD) contributes 20 — same epidemic, divergent carceral response |
| 8 | FACT | beautiful | 7/6 | CONFIRMED | Open Payments 2024: 20,733 physician payments priced at exactly $124.99 (99.7% Food & Beverage) -- a 10x spike one cent under $125, across every major pharma company |
| 9 | FACT | data-quality | 6/7 | CONFIRMED | OFAC SDN_TYPE is OFAC's null token '-0- ' (trailing space) for 9,785 of 19,115 rows -- the sanctioned ORGANIZATIONS; WHERE SDN_TYPE='-0-' returns zero without a TRIM |
| 10 | FACT | data-quality | 5/8 | CONFIRMED | USASpending CONTRACT_AWARD_UNIQUE_KEY is one-row-per-transaction, not per-contract - 9.6% excess rows, one award appears up to 174 times; naive SUM overcounts ~90x |
| 11 | FACT | coverage-gap | 6/7 | CONFIRMED | HCRIS is a single most-recent-cost-report snapshot, not a panel: 99.9% of rows are FY2023-2024 |
| 12 | FACT | data-quality | 6/7 | CONFIRMED | CDC injury/violence county RATE hides a -999 sentinel (6,549 rows) and COUNT_SUP is the string '1-9' in 70,549 rows (53%) -- naive AVG(RATE) returns -38.5 instead of +11.6 |
| 13 | FACT | coverage-gap | 6/7 | CONFIRMED | Vera incarceration panel splices two windows: prison series DEAD-ENDS at 2019, jail runs to 2026 — all 11,914 post-2019 rows carry a BLANK (not zero) prison population |
| 14 | FACT | anomaly | 6/7 | CONFIRMED | Vera panel runs through future year (MAX=2026) and coverage collapses: 2,282 counties in 2021 to 597 rows across only 5 states in 2026 — recent cross-county trends are a shrinking non-representative subset |
| 15 | FACT | coverage-gap | 5/8 | DOWNGRADED | LEIE carries a real NPI on only 10.4% of rows (8,684 / 83,464) and records ZERO reinstatements — caps any NPI-based exclusion detector; gap is NOT mainly pre-2007 (42,077 blank-NPI rows are post-2007) |
| 16 | FACT | anomaly | 6/7 | DOWNGRADED | On 2024-01-01 AIS, OpenSanctions catches 6 broadcasting sanctioned ships vs OFAC's 2 (4 extra Australia/Switzerland Russia-shadow-fleet) — but OpenSanctions is NOT an OFAC superset (1,486 of OFAC's 1,942 vessel IMOs overlap) |
| 17 | FACT | beautiful | 6/7 | DOWNGRADED | All 6 sanctioned vessels broadcasting in AIS hard-match OpenSanctions on IMO; 5 of 6 broadcast a name with zero overlap to the listing; 3 sit near-stationary at Galveston/Beaumont TX approaches |
| 18 | FACT | anomaly | 6/7 | DOWNGRADED | ~$24B of foreign-OWNED federal contract obligations are ~85% hidden behind US recipient addresses; the $29.8B 'FY2025' figure actually mixes FY2024+FY2025 |
| 19 | FACT | trend | 6/7 | CONFIRMED | 2024 set the all-time record for conflict EVENTS (28,816, ~11x since 1989) while deaths peaked in 2022 (309,636) and the deadliest single year remains 1994 (824,156) |
| 20 | FACT | correlation | 6/7 | CONFIRMED | Eastern Kentucky is the overdose+jail double-extreme epicenter: 20 of 50 counties in the top decile of BOTH despite KY being 3.9% of 2,801 counties (~10x) — robust to year alignment |
| 21 | FACT | data-quality | 6/7 | CONFIRMED | Open Payments tables are consecutive program years, not dups: main=2024 (15.39M), _2023=2023 (14.7M), RECORD_ID globally unique with ZERO cross-year overlap |
| 22 | LEAD | anomaly | 7/6 | DOWNGRADED | FARA country ranking is dominated by 'Informational Materials' (propaganda logs), not lobbying; by actual registrations Japan/Canada/Korea lead, Saudi #7; the durable finding is the country-aggregation trap ('Bosnia' ~99% Republika Srpska) |
| 23 | FACT | data-quality | 5/8 | CONFIRMED | FED_CMS_OPEN_PAYMENTS is 2024-only (15.4M); the '_2023' table is 2023-only (14.7M) -- record-disjoint by RECORD_ID, so the unsuffixed name is a half-the-data trap |
| 24 | FACT | coverage-gap | 6/7 | CONFIRMED | 49% of data-bearing sources (49 of 101) sit in UNCLASSIFIED with no secondary domain or themes -- and 6 whole domains have zero landed data |
| 25 | FACT | beautiful | 6/6 | CONFIRMED | World Bank IDS carries real forward-looking debt-service SCHEDULES out to 2032 -- ~12k numerically-valid future-year values in TDS/AMT/INT series (134 countries each) |
| 26 | FACT | coverage-gap | 6/6 | DOWNGRADED | fed_cfpb_complaints is two 250-row 'most-recent' API pulls (May 15 + May 29 2026), 500 rows total; DATE_RECEIVED/DATE_SENT are INGESTION timestamps, not complaint dates |
| 27 | LEAD | anomaly | 6/6 | DOWNGRADED | Excluded oncologist Eduardo Miranda (NPI 1285673012) appears in three CY2023 CMS billing datasets ~8 years post-exclusion — but his LEIE row carries an OIG WAIVER (1 of only 3); human review, not a clean 'exclusion failed' fact |
| 28 | FACT | anomaly | 5/7 | DOWNGRADED | Rwanda 1994 = 772,463 deaths in one country-year, 93.7% of the deadliest year on record (824,156), ~3x the next-worst year |
| 29 | FACT | data-quality | 6/6 | DOWNGRADED | 92 UCDP events carry death tolls that are exact multiples of 1,000 (540,000 deaths = 13.6% of 3.96M total); round estimates concentrate in older uncountable conflicts, above all 1994 Rwanda |
| 30 | FACT | beautiful | 5/7 | CONFIRMED | Civilians are >=37% of all conflict deaths (1989-2024); one-sided/civilian-targeting violence is 15% of events but 30% of deaths and ~2.3x as lethal per event |
| 31 | LEAD | anomaly | 7/5 | DOWNGRADED | Menominee County WI shows the highest 2023 county OD rate at 284/100k -- but it rests on just 12 deaths, a tiny-denominator estimate, not a robust #1 |
| 32 | FACT | coverage-gap | 5/7 | CONFIRMED | Vera: prison and total-incarceration rates flatline to blank after 2019; only JAIL survives 2020-2024; 2025-2026 are empty placeholder rows |
| 33 | FACT | data-quality | 5/7 | DOWNGRADED | CDC injury panel RATE=-999 suppression sentinel (panel-wide 6549, all COUNT_SUP='1-9'); Vera 2025/26 rows are population-only stubs -- both need filtering |
| 34 | FACT | anomaly | 6/6 | CONFIRMED | Largest single 2024 Open Payments transfer: $91.08M 'Acquisitions' to endodontist Dr. Charles Goodis (NPI 1821157041, FL) from Edge Endo LLC (physician-owned) — 99.94% of that maker's total spend |
| 35 | FACT | beautiful | 5/7 | DOWNGRADED | Israel is the most reliable US ally at the UN (mean agreement 0.881 since 2010, #1 of 192); US agrees with the average member only 46%; 2024=0.92 (2nd-highest, under the 0.934 2009 peak) |
| 36 | FACT | correlation | 6/6 | CONFIRMED | Perimeter appliances (NAS/VPN/firewall) run 37% ransomware-linked in CISA KEV vs 16% for OS/browser; QNAP ~75-82%, SonicWall 67%, Microsoft 27%, Cisco 6% |
| 37 | FACT | contradiction | 6/6 | DOWNGRADED | CISA KEV ransomware-flag rate ~22-24% (2021-2024) drops to ~10-11% (2025-2026) -- a labeling-lag artifact (retroactive flagging), NOT a real decline; single-source caveat, not a cross-source contradiction |
| 38 | FACT | data-quality | 5/6 | CONFIRMED | FED_FDIC_ENFORCEMENT is 14 rows of FDIC.gov navigation chrome -- zero enforcement actions, yet cataloged 'landed' as "FDIC Enforcement Decisions and Orders" |
| 39 | FACT | data-quality | 6/5 | CONFIRMED | intl_ie_cro holds 0 company records -- its 3 rows are the opendata.cro.ie cookie-consent table |
| 40 | FACT | anomaly | 6/5 | DOWNGRADED | Open Payments 2023 has a sharp pile-up of meal payments JUST BELOW $125 (124.99 x19,883...), 6.4x the just-above side -- industry-wide threshold fingerprint, not one manufacturer |
| 41 | FACT | data-quality | 6/5 | DOWNGRADED | intl_ember_elec VALUE has 8,418 literal 'nan' strings that TRY_CAST converts to IEEE NaN (not NULL); only 10 genuine rows exceed 100% |
| 42 | FACT | coverage-gap | 5/6 | DOWNGRADED | SEC EDGAR financials is a single quarterly drop: 100% of 6,491 filings filed in 2024-Q4; one-quarter snapshot, not a panel |
| 43 | FACT | data-quality | 5/6 | CONFIRMED | fed_cms_home_health: 35.8% of agencies (4,431/12,392) have NO quality star rating — '-' is the most common value (low-volume suppression) |
| 44 | FACT | beautiful | 5/6 | DOWNGRADED | CMS star-rates only Acute Care + Critical Access; five facility types are 100% unrated; 41% carry 'Not Available' as a coverage RULE, not noise |
| 45 | FACT | coverage-gap | 6/5 | CONFIRMED | XC_NAGIX_DPRK is a 23-row year-index, not an event log: each row is one year holding a JSON array (340 launches hidden behind 23 rows; 2022=69) |
| 46 | FACT | coverage-gap | 5/6 | CONFIRMED | fed_usgs_earthquakes is a 30-day rolling snapshot (May 15-Jun 14 2026), not a seismic history (176 of 9890 are non-earthquakes) |
| 47 | FACT | anomaly | 6/5 | DOWNGRADED | 7,183 Medicare providers have avg patient age under 50; the absolute-youngest (avg 7-10) are pediatric specialists, but the under-50 cohort is dominated by NPs and Psychiatry |
| 48 | FACT | data-quality | 5/6 | CONFIRMED | SCOTUS (FED_SCDB) has 121 cases where MAJVOTES <= MINVOTES — all tie votes (118 4-4, 3 3-3), equally-divided affirmances that break the naive winner test |
| 49 | FACT | data-quality | 6/5 | DOWNGRADED | OWID nuclear-warhead estimates for 8 smaller states are heavily round (70% multiples of 5 vs ~23% for the US) — flags intelligence estimates; headline 84% double-counts 318 pre-program zeros |
| 50 | FACT | beautiful | 6/5 | DOWNGRADED | Caterpillar & VF Corp appear in BOTH SEC EDGAR and the IRS revocation list under the exact same 9-digit EIN — clean but small (n=2) proof EIN can bridge SEC and IRS |
| 51 | FACT | beautiful | 4/7 | CONFIRMED | Contractor concentration: top 100 of 92,833 UEIs capture 46% of $778B net obligated; top 1,000 capture 77% (45%/76% on gross) |
| 52 | FACT | data-quality | 5/6 | DOWNGRADED | #1 contractor by award COUNT (AmerisourceBergen, 516k rows) is routine pharma fulfillment, not a mega-award - rank by dollars not row count |
| 53 | FACT | coverage-gap | 5/6 | CONFIRMED | 30,021 UCDP events (7.8%) have a best-estimate of ZERO deaths — two-thirds state-based clashes (30,018 still carry a positive HIGH estimate) |
| 54 | FACT | beautiful | 4/7 | CONFIRMED | Black residents jailed at higher rate than White in 96% of measurable counties (612/637 with >=5k Black working-age pop); median ratio 3.16x (2019) |
| 55 | LEAD | anomaly | 6/5 | DOWNGRADED | 7 high-volume opioid prescribers (>=1,000 claims, >=90% opioid) carry a NON-pain NPPES specialty (incl a Hospitalist 96.1%, a Pharmacist 91.3%) -- a review flag, not proven over-prescribing |
| 56 | FACT | beautiful | 5/6 | CONFIRMED | Anthony Kennedy was empirically the swing justice: in the majority on 76.4% of 5-4 decisions (409/535), highest of any justice with >=100 close votes (1946-2024) |
| 57 | FACT | trend | 5/6 | CONFIRMED | SCOTUS liberal-decision share peaked at 68.5% in the 1960s (Warren), settled near 44% post-1970 (with a 2010s bump to ~50%) |
| 58 | FACT | coverage-gap | 4/7 | CONFIRMED | Federal Register table is a thin ~9.5-week snapshot (2026-04-10 to 06-16), 80% Notices, truncated at the 5,000-row API ceiling |
| 59 | FACT | contradiction | 6/5 | DOWNGRADED | The two DPRK missile sources agree EXACTLY on all 21 shared years (claimed deltas were a brace-counting artifact); the real story is NTI going stale, missing all 37 tests of 2025-2026 that Nagix has |
| 60 | FACT | anomaly | 5/5 | CONFIRMED | USASpending FY2026 top-tier agency budget shares sum to 95.5% (not 100%) and include one negative (FCC -0.073%) because the denominator is a fixed $13.40T total > the 111 agencies' $12.79T |
| 61 | FACT | data-quality | 4/6 | CONFIRMED | NOAA storm DAMAGE_PROPERTY is bucketed estimates: ~87% of nonzero are round 1/2/5x10^n, 57% of rows flat $0 -- ordinal, never precise currency |
| 62 | FACT | data-quality | 4/6 | CONFIRMED | intl_freedomhouse landed with the xlsx title row as headers (col named FREEDOM_IN_THE_WORLD_2013_2025_RAW_DATA); the real 44-field header sits in data row 1 |
| 63 | FACT | coverage-gap | 5/5 | DOWNGRADED | fed_nara_aad landed AAD series-description pages, not records -- 554 rows, all record-level keys null, JSON holds page metadata + 4 HTTP 404s |
| 64 | FACT | anomaly | 6/4 | DOWNGRADED | intl_opensanctions has 5 sanctioned Persons with impossible future birth dates (2064-2068), all from the Belgian feed -- consistent with 2-digit-year rollover, mechanism unproven |
| 65 | FACT | data-quality | 4/6 | CONFIRMED | INTL_GR_GEMI is a failed scrape: all 40 rows have every business field blank; the only populated column holds 7 Greek UI/footer strings |
| 66 | FACT | data-quality | 4/6 | CONFIRMED | NOAA AIS HEADING is the sentinel 511 ('not available') in 52.46% of 7.30M rows; naive AVG returns 356.86 vs 186.80 filtered |
| 67 | FACT | anomaly | 5/5 | CONFIRMED | OWID temperature anomaly carries a 2026 partial-year value (wide CI) alongside settled means — World tail reads as cooling 2024-2026 |
| 68 | FACT | data-quality | 5/5 | CONFIRMED | CDC drug-poisoning county rate is a binned TEXT range (16 bins, 0 numeric), not a death rate; the 3139/3141/3140 wobble is 3 FIPS boundary-change counties |
| 69 | FACT | data-quality | 4/6 | CONFIRMED | fed_naag_multistate_settlements is a FAILED SCRAPE: all 26 rows are NAAG website chrome, zero settlements |
| 70 | FACT | trend | 4/6 | DOWNGRADED | Ransomware-victims feed is live and exploding: 18,864 of 29,193 dated rows (65%) in 2024-2026; H1-2026 (4,607) already beats all of 2022 |
| 71 | FACT | data-quality | 4/6 | CONFIRMED | SEC EDGAR company_tickers grain is one-row-per-TICKER: 10,414 rows / 8,018 distinct CIK; BANK OF MONTREAL=27 tickers; CIK joins fan out |
| 72 | FACT | data-quality | 4/6 | CONFIRMED | fed_slavevoyages_intraamerican is a FAILED SCRAPE: 201 rows of HTML chrome, all 13 real columns 100% empty |
| 73 | FACT | coverage-gap | 4/6 | CONFIRMED | fed_federal_register_documents is a 'most-recent 5000' API-capped pull; SIGNIFICANT + PRESIDENT columns 100% empty (incl all 49 Presidential Documents) |
| 74 | FACT | data-quality | 4/6 | DOWNGRADED | OWID milspend: 644 of 9,112 rows are SIPRI regional aggregates (no ISO code) that double-count if summed; panel runs to 2025 |
| 75 | FACT | trend | 5/5 | DOWNGRADED | Open Payments amounts cluster on caps/flat fees: $125 (48,825x) and $124.99 (20,733x) both ~98% Food & Beverage meal-cap; $1k/$1.5k/$4k are consulting/education fees |
| 76 | FACT | beautiful | 4/6 | DOWNGRADED | US police killings ROSE ~12% after 2020: 985/yr (2015-19) to 1,101/yr (2020-24), 2021-2024 each a record (peak 1,175 in 2024); body cameras recorded only 17.2% of 10,430 deaths |
| 77 | FACT | coverage-gap | 3/6 | CONFIRMED | fed_noaa_storm_events is a single-year snapshot: all 72,360 rows are 2025 (NOAA's DB goes back to 1950) |
| 78 | FACT | data-quality | 4/5 | DOWNGRADED | fed_fdic_failed_banks: loader wrote pandas NaN as literal 'nan' (CERT 488, COST 638, QBFASSET 154); the 488 CERT='nan' are pre-1977 failures with no FDIC cert; ID is a clean alternate PK |
| 79 | FACT | data-quality | 4/5 | DOWNGRADED | FARA dates are MM/DD/YYYY text; TRY_CAST AS DATE works; only 51,575 of 221,900 rows carry a REGISTRATION_DATE |
| 80 | FACT | data-quality | 4/5 | CONFIRMED | All Guttmacher #WeCount abortion estimates rounded to nearest 10 (MEDIAN/LOWER/UPPER each 100% divisible by 10); the NOTES field says so |
| 81 | FACT | coverage-gap | 4/5 | CONFIRMED | FHFA 'all-transactions' flavor (89,265 rows, 48%) has a structurally EMPTY INDEX_SA, so SA is only 52% populated table-wide |
| 82 | FACT | beautiful | 6/3 | CONFIRMED | 11 long-term-care hospitals share certification date 07/01/1966 -- the day Medicare's hospital insurance launched -- and are the oldest LTCHs in the table |
| 83 | FACT | data-quality | 4/5 | CONFIRMED | Oyez 'modeled' source is a 25-row hollow stub: DECISION/DISPOSITION/MAJORITY_AUTHOR/CITATION 100% blank; 5 scattered terms (1966-1971) |
| 84 | FACT | data-quality | 5/4 | CONFIRMED | DOJ FCA settlements is a failed scrape: 19 rows of DOJ nav/boilerplate + scraper errors; SETTLEMENT_AMOUNT unparseable free-text, defendant/relator 0/19 |
| 85 | FACT | data-quality | 4/5 | DOWNGRADED | Mapping Inequality HOLC grade needs TRIM/UPPER + A-D whitelist: 10 raw buckets collapse to 6 (A/B/C/D + E/F) + 817 blanks; YEAR_MAPPED 100% empty |
| 86 | FACT | trend | 4/5 | CONFIRMED | Leiden Russian-ops-in-Europe: documented incidents nearly triple in 2024 (24 -> 69), then 40 in a partial 2025 (data ends Oct) |
| 87 | FACT | data-quality | 4/5 | DOWNGRADED | FED_VA_SUICIDE_APPENDIX is a flattened PDF: 2 stacked sub-tables, embedded-newline headers, positional COL_1..12 so the header never became the schema |
| 88 | LEAD | beautiful | 4/5 | DOWNGRADED | Corruption vs life expectancy correlates strongly (Pearson +0.73, n=179, stable 2018-2022) -- but it saturates; low-CPI survivors (Lebanon/Venezuela/Syria/NK/Libya) are the tail of a wide corrupt-state band, not a unique signal |
| 89 | LEAD | correlation | 4/5 | DOWNGRADED | Gini vs homicide is a robust positive panel correlation (Pearson +0.53, n=254 country-years, 2017-2020, stable) -- but the 'top 6 murderous all high-Gini' anecdote is cherry-picked and false |
| 90 | FACT | data-quality | 3/6 | DOWNGRADED | INTL_OWID_MILSPEND is absolute current US$ with NO GDP/pop -- raw correlations are economy-size artifacts (CORR with life-exp ~0.055 not 0.13); normalize first |
| 91 | LEAD | correlation | 4/5 | DOWNGRADED | Refugees are a lagging stock, not a mirror of current deaths: Syria deaths peak 2014 while refugees climb to 6.85M (2021) -- but the UCDP×OWID name-join silently drops the #1 country (DR Congo, 139k deaths) |
| 92 | FACT | lead | 4/5 | DOWNGRADED | 1,390 physicians self-disclosed an ownership stake in a manufacturer in 2024 -- a clean NPI-joinable COI cohort -- but the headline $113.2M is 84% one-time M&A; recurring conflict money ~$18.6M, median physician $160 |
| 93 | FACT | data-quality | 4/5 | CONFIRMED | fed_doj_crt_cases is CATALOG lifecycle='landed' but holds exactly 1 row that is a scraped nav-header, not a case |
| 94 | FACT | trend | 4/5 | DOWNGRADED | Ransomware leak-site posts grew ~29x from 2020 (270) to 2025 (7,939); US is 45% of victims-with-known-country. Growth flattening: H1-2026 vs H1-2025 only +8.5% |
| 95 | FACT | contradiction | 3/6 | DOWNGRADED | crime_security and elections_voting report 0 landed by DOMAIN_PRIMARY, but the data is landed under UNCLASSIFIED -- a browse-by-domain false hole (catalog backlog, not deception) |
| 96 | LEAD | correlation | 4/5 | DOWNGRADED | UCDP conflict deaths ~30-34% of an *estimated* Mexican homicide total (OWID has only a RATE) -- internally coherent, exposes a real UCDP parenthetical-country-name join hole |
| 97 | FACT | beautiful | 4/4 | DOWNGRADED | fed_fbi_nics_checks is a perfectly balanced 55-jurisdiction monthly panel (16,445 = 55 x 299, gap-free: 50 states + DC + 4 territories) |
| 98 | FACT | anomaly | 4/4 | DOWNGRADED | ClinicalTrials 500-row sample: 236 of 296 completed/terminated trials have NO posted results, ENROLLMENT clusters on round targets (+14 zero-enrollment) |
| 99 | FACT | anomaly | 4/4 | DOWNGRADED | fed_cms_pos_other STATE_CD carries 270 FOREIGN rows (CN=263, MX=7) + 230 territory rows — legit CMS codes but they break any 50-state/FIPS crosswalk |
| 100 | FACT | beautiful | 4/4 | DOWNGRADED | SERCOP (Ecuador): OCID is a flawless unique release key (132,995/132,995) but the table is a single window (2025-01 to 2026-06), and OCID is per-RELEASE, not per-contract |
| 101 | FACT | data-quality | 3/5 | CONFIRMED | FED_VA_ALLCAUSE_MORTALITY is a broken scrape of a PDF list-of-figures page: 244 rows, 227 fully blank, only 16 figure captions + 8 'Go to Top' nav links |
| 102 | FACT | beautiful | 3/5 | DOWNGRADED | FED_CMS_NADAC is a clean weekly drug-price panel: 1.5M rows, 32.9k 11-digit NDCs, 52 weekly snapshots (all 2024), zero bad prices, NDC+AS_OF a perfect grain |
| 103 | FACT | data-quality | 4/4 | CONFIRMED | intl_ch_zefix is a dead source: all 18 rows are scraped Zefix homepage nav/footer chrome (6 UI labels x 3 cantons), zero companies |
| 104 | LEAD | beautiful | 5/3 | DOWNGRADED | Coincidence: total CMS GENERAL payments flat YoY ($3.3140B vs $3.3138B) only because +$104M physician is offset by -$132M teaching-hospital; physician-only payments actually ROSE +4.5% |
| 105 | LEAD | contradiction | 4/4 | DOWNGRADED | SCOTUS unanimity rose to a 2010s peak of 47.5% then fell to 42.4% in the 2020s, and 6-3 rulings are now a record 24.1% -- the modern court is NOT at a unanimity high |
| 106 | LEAD | contradiction | 4/3 | DOWNGRADED | fed_wpa_slave_narratives has a column-mapping defect -- FULL_TEXT holds the photo caption and PERSON_NAME/STATE_FIPS are blank, but the named people ARE present in TITLE and SUBJECTS |
| 107 | FACT | data-quality | 3/4 | DOWNGRADED | intl_it_istat (213k rows, 3 SDMX cubes): UNIT_MEASURE and UNIT_MULT 100% blank, and dataflow 101_1033 mixes annual + monthly -- OBS_VALUE needs DIMENSION_KEYS/FREQ decoded |
| 108 | FACT | data-quality | 4/3 | DOWNGRADED | INTL_ES_BORME (25 rows): COMPANY_ID/NAME/SECTION 100% blank -- but the names+registry IDs landed in the wrong column (ACT_DESCRIPTION); mis-parsed, not hollow |
| 109 | FACT | data-quality | 3/4 | CONFIRMED | DPRK missile-tests load swallowed its own header row: all 19 cols are COL_N and row 1 IS the column names |
| 110 | FACT | correlation | 3/4 | CONFIRMED | Life expectancy vs fertility = -0.81 (R2 0.65, n=236, 2020); largest negative residuals are the HIV belt -- Lesotho -15.9yr, Eswatini -10.9, South Africa -8.7 |
| 111 | FACT | data-quality | 3/3 | CONFIRMED | Treasury Debt-to-Penny ships 4 fully-blank shadow columns (_YR/_QTR) duplicating the populated _YEAR/_QUARTER fields |
| 112 | FACT | beautiful | 3/3 | DOWNGRADED | fed_cdc_suicide_rates is a tidy long panel (6,390 rows, 1950-2018) -- but YEAR_NUM is a year-ordinal, spacing is irregular (1950/60/70 then annual), 14% of rows suppressed/blank |
| 113 | FACT | anomaly | 3/3 | DOWNGRADED | fed_cms_irf CERTIFICATION_DATE is an administrative effective-date (62% land on the 1st); 3 FL facilities carry future dates (Sep/Oct 2026) that break 'days since certification' |
| 114 | FACT | data-quality | 3/3 | DOWNGRADED | FEC party-affiliation is blank for 53% of committees ONLY because PACs have no party by design; for candidate committees it is 97% populated |
| 115 | FACT | beautiful | 3/3 | CONFIRMED | Reported AI incidents (OWID/AIID) climbed near-monotonically from 8 (2012) to 362 (2025), ~45x -- biggest doubling is 2020 (43->90), not the post-ChatGPT 2022 kink |
| 116 | FACT | data-quality | 3/3 | DOWNGRADED | FED_DOJ_CRT_CASES is a 1-row nav-page scrape with zero cases -- but it is correctly tagged 'landed' (NOT 'modeled') |
| 117 | LEAD | data-quality | 2/3 | DOWNGRADED | Wayback DOJ deep-pages: 2,542 rows = 653 URLs x multiple captures each (one row per snapshot, not duplicates) - use DISTINCT url for distinct pages |
| 118 | FACT | anomaly | 2/3 | DOWNGRADED | FHFA HPI latest year (2026) is Q1-only (1,198 rows vs ~4,792 full) -- so MAX(YR) 'latest year' logic lands on one quarter and can fake a price crash |

---
*Read-only run. No warehouse mutations. Generated by the `ripple-discovery-sweep` workflow (run `wf_2a40fd00-fae`), 8 headlines independently re-verified.*
