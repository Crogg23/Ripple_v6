# Connectivity Audit — The Library

**Date:** 2026-06-21
**Type:** Join-density audit (NOT a "find more data" exercise)
**Win condition:** the sources that weave the **existing** tables into one dense web — ranked by connection count, not row count or source count.

---

## ⚠️ Read this first — provenance & caveats

This audit is honest about what was and wasn't confirmed this session.

- **The wishlist Excel was not found.** No `.xlsx/.xls/.csv` exists anywhere in the repo or its git history, and `.gitignore` isn't hiding one. The Google Drive MCP (its likely home) was **token-expired** this session, so it couldn't be checked. Per Chris's call, this became a **scout-what's-available** audit instead of scoring a supplied list. If the wishlist resurfaces, fold it in and cross-check against this.
- **The existing-warehouse map is repo-derived, not live.** This container has **no Snowflake credentials** (no `.env`, no `SNOWFLAKE_PAT`), so the Snowflake MCP never came up. The "what exists" inventory below was built from the repo's **dbt models/`schema.yml`** (read this session) + the **`build-state.md` ledger** + targeted verification. It is **not** verified against the live `LIBRARY_RAW.LANDING` tables or the live `LIBRARY_META.REGISTRY.SOURCE_REGISTRY` (901 rows). Treat counts as documented-state, not live-state.
- **"Catalog" naming:** the task referenced `CATALOG.SOURCES`/`CATALOG.COLUMNS`. Those names don't exist in this repo — the catalog is **`LIBRARY_META.REGISTRY.SOURCE_REGISTRY`**, and per-source columns live in dbt `schema.yml` (live: `INFORMATION_SCHEMA`).
- **Candidate sources were web-confirmed (June 2026)** by four domain scouts (geo, health, corporate, legal). Dead/gated/changed endpoints are flagged.
- **One scout claim was overturned on verification** (NPPES→EIN) — see *Corrections* at the bottom. This is why connection counts here differ from the raw scout output.

---

## Top-line summary

- **~31 candidate sources scored** across four domains, each graded on how many **existing** tables it connects to (by a usable join key), plus a **HUB** flag for sources that anchor a future cluster.
- **12 landed in Tier A** (ingest now — they light up the existing web today).
- **Headline:** **ingesting the ~12 Tier-A sources weaves ~30 of your existing key-bearing tables into one connected graph** — three dense clusters (**geographic**, **healthcare-provider**, **judicial**) stitched together by entity bridges.
- **Reframe you should know:** **most of the top hubs are already in your day-one queue (`sources_queue.py`, 37 sources) — just never run.** So this audit is really a **prioritization of what you already planned, by join density**, plus the net-new finds the queue under-specified (CMS Open Payments, IRS EO BMF bulk, the Medicare utilization files, SEC Financial Statement Data Sets, FEMA, CDC PLACES). `[Q]` = already in your queue · `[NEW]` = net-new find.

---

## The existing warehouse — what you're connecting TO

Key-bearing tables already landed (from dbt models + `build-state.md`; `*` = inferred from a landing-only source with no dbt model). This is the scoring denominator.

| Join key | Existing tables that carry it |
|---|---|
| **FIPS / county_fips** | `fed_fdic_failed_banks`, `fed_mapping_inequality`, `fed_nara_wra_aad`, `fed_wpa_slave_narratives` (state), `fed_hhs_taggs`, `fed_cms_nursing_home`, `fed_usaspending_subawards`* |
| **zip_code** | `fed_cfpb_complaints`, `fed_hhs_taggs`, `fed_cms_nppes`, `fed_cms_nursing_home`, `fed_cms_hcris`* |
| **lat/lon** | `fed_noaa_ais`, `fed_mapping_inequality`, `fed_usgs_earthquakes`, `fed_cms_nursing_home` |
| **NPI** | `fed_cms_nppes`, `fed_clinicaltrials`, `fed_cms_nursing_home`, `fed_hhs_oig_leie`* |
| **CCN (provider)** | `fed_cms_hcris`, `fed_cms_nursing_home` |
| **NDC (drug)** | `fed_fda_drug_enforcement` |
| **CIK / ticker** | `fed_sec_edgar_company_tickers` |
| **EIN** | `fed_hhs_taggs` (NPPES EIN is phantom — see corrections) |
| **UEI / DUNS / ALN** | `fed_usaspending_subawards`*, `fed_hhs_taggs` (ALN) |
| **docket / case_id / court / judge** | `fed_fjc_idb`, `fed_scdb`, `fed_oyez`, `fed_doj_fca_settlements`, `fed_fdic_enforcement`, `fed_doj_crt_cases`, `intl_hudoc` (ECHR) |
| **MMSI / IMO (vessel)** | `fed_noaa_ais`* |
| **country ISO** | `intl_ember_elec`, `intl_it_istat` |
| **company-reg number (intl)** | `intl_ch_zefix`, `intl_es_borme`, `intl_gr_gemi`, `intl_ie_cro`, `intl_ec_sercop` |
| **org/person name (weak)** | `fed_fara_bulk`, `fed_revolvingdoor_project`, `fed_doj_fca_settlements`, `fed_naag_multistate_settlements` |
| **DOI** | `xc_biorxiv_medrxiv` |
| **none (time series / docs)** | `fed_treasury_debt_to_penny`, `fed_treasury_avg_interest_rates`, `fed_doj_epstein_library`, `xc_wayback_*` |

**The shape of it:** you already have **three natural clusters** — a **geographic** spine (~12 tables share place), a **healthcare-provider** cluster (~6 tables share NPI/CCN/NDC), and a **judicial** cluster (~7 tables share docket/case). They are **not yet connected to each other.** The highest-value sources are the ones that (a) thicken a cluster, or (b) bridge clusters.

---

## Scoring method

- **Score = number of existing tables a candidate connects to via a usable key.** Solid key = 1.0; fuzzy/name-only = 0.5. This is the primary rank.
- **HUB** = anchors a key that many *future* sources will hang off of (the "wide net / no blinders" dimension). A hub can rank high on strategy even with a low current count — flagged, not auto-promoted.
- **Tiers:**
  - **TIER A — ingest now:** ≥3 solid existing connections, *or* a structural bridge/hub that interjoins ≥4 existing tables, with workable access.
  - **TIER B — ingest soon:** 1–2 solid connections, or a strong hub carrying an access caveat.
  - **TIER 0 — catalog & wait:** 0 solid connections today (pure future hub, or blocked access). Named with what it's waiting on.

---

## TIER A — ingest now (sorted by connection count)

| # | Source | Status | Join keys | Connects to (named existing) | #conn | Hub? | Access / flag |
|---|---|---|---|---|---|---|---|
| 1 | **Census TIGER/Gazetteer + Geocoder** | `[Q]` | FIPS, GEOID, lat/lon, ZCTA | the entire geo spine: `fdic_failed_banks`, `mapping_inequality`, `nara_wra_aad`, `wpa_slave_narratives`, `hhs_taggs`, `cms_nursing_home`, `noaa_ais`, `usgs_earthquakes`, `cfpb_complaints`, `cms_nppes` | **~10** | ★ geo backbone | Use **Gazetteer flat-files + Geocoder API**, NOT the TIGER Shapefiles (no clean pandas path — your `mapping_prejudice` Shapefile fail). |
| 2 | **HUD–USPS ZIP↔county/tract crosswalk** | `[Q]` | zip ↔ FIPS | bridges every zip table (`cfpb_complaints`, `hhs_taggs`, `cms_nppes`, `cms_nursing_home`, `cms_hcris`) to every FIPS table (`fdic_failed_banks`, `mapping_inequality`, `nara_wra_aad`, `wpa_slave_narratives`) | **~9** | ★ the zip/FIPS Rosetta | Tiny quarterly XLSX/CSV. **Cheapest dense win in the whole audit.** |
| 3 | **CMS Open Payments** | `[NEW]` | NPI, NDC, manufacturer name | NPI → `cms_nppes`, `clinicaltrials`, `cms_nursing_home`, `hhs_oig_leie`; NDC → `fda_drug_enforcement` | **5** | ★ provider↔drug↔pharma | Multi-GB general file → **chunk by program year (C3)** or use the Socrata API. Bridges health→corporate via manufacturer name → `sec_edgar`. |
| 4 | **Census ACS 5-year** | `[NEW]`* | FIPS (tract/county) | all FIPS tables (above) + supplies population/income **denominators** to normalize every count | **~6** | ★ demographic denominator | Clean JSON API (`api.census.gov`). *Publisher in queue (TIGER), this product isn't.* |
| 5 | **EPA ECHO / FRS** | `[Q]` | FIPS, lat/lon, FRS_id | geo spine (FIPS + lat/lon) + adds a facility-registry entity | **~7** | ★ facility registry | Web services + bulk. Clean. |
| 6 | **CourtListener bulk (RECAP)** | `[Q]` | docket, court_id, judge/person, citations | `fjc_idb`, `scdb`, `oyez`, `doj_fca_settlements`, `fdic_enforcement`, `doj_crt_cases` | **6** | ★ docket+judge backbone | **Bulk CSV dumps only** — never wire to live PACER (per-doc paywall). Ships the same FJC IDB you have + a judges/People DB that turns your loose `judge` text into entities. |
| 7 | **Medicare Physician & Other Practitioners (by Provider & Service)** | `[NEW]` | NPI, HCPCS, zip/state | NPI → `cms_nppes`, `clinicaltrials`, `cms_nursing_home`, `hhs_oig_leie` (+ `cms_hcris` via CCN) | **4–5** | HCPCS (new) | Bulk CSV + REST, no auth; load by year (~10M rows/yr). |
| 8 | **CMS Open Payments — Part D Prescribers (by Provider & Drug)** | `[NEW]` | NPI, drug name | NPI → `cms_nppes`, `clinicaltrials`, `cms_nursing_home`, `hhs_oig_leie`; drug name → `fda_drug_enforcement` (fuzzy) | **4** | pairs w/ #3 | ~25M rows/yr; load by year. Drug is name-only (no NDC) → join via NDC Directory (#16). |
| 9 | **CMS PECOS Public Provider Enrollment** | `[NEW]` | NPI, PECOS id, group/reassignment | NPI → `cms_nppes`, `clinicaltrials`, `cms_nursing_home`, `hhs_oig_leie` | **4** | ★ provider-ownership edges | Quarterly bulk CSV. The **reassignment edges** (solo→group) are the prize — an ownership graph over providers you already have. |
| 10 | **FEMA Disaster Declarations** | `[NEW]` | FIPS (county) | all FIPS tables | **~6** | — | Clean OpenFEMA API + bulk CSV. Adds a disaster/time dimension over your whole geo spine. |
| 11 | **USASpending — prime award archive** | `[Q]` | UEI, ALN/CFDA, place FIPS/zip, recipient name | `usaspending_subawards` (UEI), `hhs_taggs` (ALN+FIPS), geo (place FIPS/zip), `fara`/`doj_fca` (name) | **3–4** | UEI spine | **Filter by agency+FY — do NOT pull the ~1.5TB full DB.** Prime-award complement to your existing subawards. |
| 12 | **Global Fishing Watch** | `[Q]` | MMSI, IMO, lat/lon | `noaa_ais` (MMSI/IMO — vessel identity over your 7.3M AIS rows) + geo (lat/lon) | **2** (1 deep) | vessel-identity | Free API key. Uniquely lights up the biggest table you have (`fed_noaa_ais`) with vessel ownership/fishing-effort. |

---

## TIER B — ingest soon (real connections, lower payoff or an access caveat)

| Source | Status | Join keys | Connects to (named existing) | #conn | Hub? | Access / flag |
|---|---|---|---|---|---|---|
| **IRS Exempt-Org Business Master File (BMF)** | `[NEW]` | EIN, org name, zip | `hhs_taggs` (EIN); `fara`/`doj_fca`/`naag` (name, fuzzy); geo (zip) | **1 + fuzzy** | ★★ EIN spine | Free bulk CSV, no auth. **Top hub in the whole audit by future value** — every US nonprofit (~1.9M EINs). Only B (not A) because just **one** existing table carries a real EIN today. Ingest right after the geo backbone. |
| **SEC Financial Statement Data Sets** | `[NEW]` | CIK | `sec_edgar_company_tickers` (CIK, 1:1) | **1 deep** | CIK financials | Quarterly bulk ZIP, no auth. Turns your ticker stub into real fundamentals. |
| **SEC Submissions + CompanyFacts bulk** | `[NEW]` | CIK, ticker, SIC, former names | `sec_edgar_company_tickers` | **1** | name-history → entity res | `submissions.zip` is large → stream it. |
| **CMS Provider of Services (POS) file** | `[NEW]` | CCN, address (FIPS/zip), ownership | `cms_hcris`, `cms_nursing_home` (CCN) + geo | **2** | facility ownership | Quarterly bulk CSV. Small (~130k). |
| **FDA NDC Directory (openFDA)** | `[NEW]` | NDC, manufacturer name | `fda_drug_enforcement` (NDC) | **1** | ★ NDC lookup glue | Tiny. **Load early** — it's the dimension that makes every NDC in Open Payments / Part D resolvable. |
| **NUCC Provider Taxonomy** | `[NEW]` | taxonomy code | `cms_nppes` (decodes its taxonomy column) | **1** | NPPES decoder | Tiny CSV. ⚠ commercial-reuse license form. |
| **CDC PLACES / WONDER** | `[NEW]` | county FIPS | all FIPS tables + bridges to health outcomes | **~6** | geo↔health bridge | County health estimates; clean CSV/API. |
| **FEC bulk (candidate/committee/contributions)** | `[Q]` | committee/candidate id, contributor name+**employer**, zip | `fara`/`revolvingdoor`/`sec_edgar` (employer/name, fuzzy); geo (zip/state) | **~3 fuzzy** | ★ money↔person↔org | Bulk ZIP + OpenFEC (free api.data.gov key). Names need normalization. |
| **OpenSanctions (consolidated)** | `[Q]` | entity name, country, LEI, OFAC id | `fara` (foreign principal name+country); intl registries (name) | **2 fuzzy** | ★ PEP/sanctions graph | Free bulk CSV/FtM. ⚠ license: free for journalists/non-commercial — confirm you qualify. |
| **Senate/House Lobbying Disclosure (LD-2)** | `[NEW]` | registrant/client org, lobbyist | `fara` (domestic analog), `revolvingdoor` (person) | **2 fuzzy** | lobbyist↔client | ⚠ **legacy `lda.senate.gov` retires 2026-06-30 — build against the new `LDA.gov` REST API.** |
| **EPA TRI** | `[Q]` | FIPS, lat/lon, TRI_facility_id | geo spine + EPA FRS link | **~6** | — | Bulk CSV. Pairs with ECHO (#5). |
| **BLS QCEW** | `[NEW]` | FIPS, **NAICS** | geo spine + NAICS bridge to industry/corporate | **~6** | NAICS bridge | CSV slices by county. ⚠ `bls.gov` now **403s without a User-Agent header** — set a contact UA. |
| **BLS LAUS / BEA Regional / USDA ERS Atlas** | `[Q]`(BEA) / `[NEW]` | FIPS (county) | geo spine (unemployment / income-GDP / rural typology) | **~6 each** | county-stat layer | All FIPS-keyed county stats. BLS = UA-header gate; BEA = free key; USDA Atlas = **~2023 vintage** (rollup, not timely). Treat as one "county economic layer." |
| **NIH RePORTER** | `[Q]` | EIN, UEI, org, PI | `hhs_taggs` (EIN), `usaspending_subawards` (UEI) | **2** | research-grant↔org | Free REST; 1 req/s, offset cap → paginate by FY/agency. |
| **FDA FAERS (openFDA drug-event)** | `[Q]` | NDC, NPI | `fda_drug_enforcement` (NDC), `cms_nppes` (NPI) | **2** | — | Already queued. Adverse-event reports. |
| **BJS NIBRS** | `[Q]` | FIPS, **ORI** | geo spine + ORI (new crime key) | **~6** | ORI hub | Bulk. Anchors a future law-enforcement (ORI) cluster. |

---

## TIER 0 — catalog & wait (no solid existing connection yet — high future value)

| Source | Status | Why it's a hub | Waiting on |
|---|---|---|---|
| **GLEIF LEI Golden Copy (L1 + L2 ownership)** | `[Q]` | ★★ global legal-entity spine + parent→subsidiary graph | **No existing table carries an LEI.** Lights up the moment you add a CIK↔LEI or LEI-bearing source. Bridges intl registries by name+country (fuzzy) meanwhile. |
| **SAM.gov Entity Extract** | `[Q]` | ★★ the federal **UEI↔DUNS↔CAGE↔name** crosswalk (would push USASpending/grants connectivity way up) | **Access.** Even the "public" monthly extract needs a **system account + federal email/CAC**; API needs an approved FOUO key. Blocked until access is sorted — highest ceiling, worst door. |
| **SEC Form 13F** | `[NEW]` | institutional ownership; **CUSIP** + manager CIK | A CUSIP↔ticker bridge (via SEC FSDS/Submissions) to reach `sec_edgar`. |
| **SEC Form ADV** | `[NEW]` | investment advisers; **CRD** key | A CRD-bearing source; weak CIK/name link to `sec_edgar` today. |
| **GovInfo / Congress.gov** | `[NEW]` | legislative spine; **bioguide_id** (members, bills, votes) | A bioguide-linked source (FEC candidate crosswalk, or `revolvingdoor` name match). ⚠ **use GovInfo/Congress.gov — ProPublica Congress API is dead.** |
| **World Bank / IMF / OECD / WHO** | `[Q]` | country-ISO macro layer | Joins `intl_ember_elec`, `intl_it_istat` (2) — thin until more country-ISO data lands. ⚠ OECD data-explorer is a JS shell (per build-state) — use its SDMX endpoint. |
| **OFAC SDN (standalone)** | `[NEW]` | US sanctions | Redundant — **OpenSanctions already ingests SDN.** Only if you want the primary feed. |
| **DOJ News API** | `[NEW]` | press-release narrative over the legal cluster | Text/NLP join only (no hard key) to `doj_fca`/`doj_crt`/`fjc_idb`. Nice-to-have. |

---

## The web that lights up 🔦

The densest connectivity doesn't come from any single big source — it comes from **one cheap geographic bridge + two cluster-thickeners + two inter-cluster connectors**:

1. **HUD ZIP↔FIPS crosswalk** (tiny) + **Census TIGER/Gazetteer/ACS** → instantly makes your **~12 geographically-keyed tables interjoinable** — bank failures, redlining grades, HHS grants, nursing homes, NPI providers, earthquakes, AIS vessels, CFPB complaints all resolve to a common geography. This is the floor of the whole graph.
2. **CMS Open Payments** → fuses your **healthcare cluster** (NPPES + ClinicalTrials + Nursing Home + LEIE via NPI; FDA via NDC) into one connected provider-payments graph — and via **manufacturer name** is the only clean thread from health into the **corporate** cluster (`sec_edgar`).
3. **CourtListener bulk** → fuses your **judicial cluster** (FJC IDB + SCDB + Oyez + DOJ FCA + FDIC + DOJ CRT) on docket/court and adds a **judges/People DB** that turns six tables' loose name columns into shared entities.
4. **IRS EO BMF (EIN)** + **GLEIF (LEI)** + **SAM.gov (UEI↔DUNS)** → the **entity-resolution backbone** that, over time, lets the spending/corporate/nonprofit/foreign-influence data all resolve to the same organizations. BMF is ingestable today; GLEIF and SAM are the strategic holds.

**If you do nothing else:** ingest **HUD crosswalk + Census (geo backbone)**, **CMS Open Payments**, **CourtListener bulk**, and **IRS EO BMF**. Those five alone connect the three clusters internally and start the bridges between them — roughly **30 of your existing tables** become one navigable graph.

```
        ┌─────────────── GEO SPINE (HUD + Census + ACS + EPA + FEMA) ───────────────┐
        │   fdic_failed_banks · mapping_inequality · nara_wra · wpa · hhs_taggs       │
        │   cms_nursing_home · noaa_ais · usgs_eq · cfpb · cms_nppes · cms_hcris      │
        └───────┬───────────────────────────┬───────────────────────────┬───────────┘
            zip/FIPS                     NPI│lat-lon                  place FIPS
                │                           │                             │
     ┌──────────┴─────────┐   ┌─────────────┴──────────────┐   ┌──────────┴──────────┐
     │  HEALTH (Open Pay,  │   │  (Global Fishing Watch →    │   │ SPENDING (USASpending│
     │  Part D, Physician, │   │   noaa_ais via MMSI/IMO)    │   │ prime; UEI/ALN →     │
     │  PECOS) NPI/NDC/CCN │   │                             │   │ subawards, hhs_taggs)│
     │  nppes·leie·trials· │   └─────────────────────────────┘   └──────────┬──────────┘
     │  nursing·hcris·fda  │                                                 │ EIN / name
     └──────────┬──────────┘                                       ┌─────────┴─────────┐
       manufacturer name → sec_edgar                               │ ENTITY BRIDGE     │
                │                                                   │ IRS BMF (EIN) ·   │
     ┌──────────┴──────────┐   ┌────────────────────────────┐      │ GLEIF (LEI) ·     │
     │ CORPORATE (SEC FSDS,│───│ JUDICIAL (CourtListener) →  │      │ SAM (UEI/DUNS) ·  │
     │ Submissions) CIK →  │   │ fjc_idb·scdb·oyez·doj_fca·  │      │ OpenSanctions ·   │
     │ sec_edgar           │   │ fdic_enf·doj_crt (docket)   │──────│ FEC (employer)    │
     └─────────────────────┘   └────────────────────────────┘      └───────────────────┘
                                          fara · revolvingdoor (names) ──┘
```

---

## Honest flags

**Maintenance traps**
- **CMS Open Payments / Medicare files** — multi-GB; the general file OOM-kills a whole-file load. Use **C3 chunked-by-year** or the Socrata API. All `data.cms.gov` HTML pages are JS-rendered → hit the **REST/CSV endpoint**, never scrape the page.
- **`bls.gov` 403s without a User-Agent header** (confirmed live) — set a contact UA on every BLS request (LAUS, QCEW).
- **Census TIGER is Shapefile** — use Gazetteer flat-files + the Geocoder API instead (you already failed `mapping_prejudice` on a Shapefile).
- **SAM.gov is gated** even for the "public" extract (federal email/CAC). Don't queue it as auto-onboard.
- **USASpending full DB is ~1.5TB** — always filter by agency+FY.
- **Big files needing C3 chunked load:** Open Payments general, Medicare Part D/Physician, SEC `submissions.zip`.

**Dead ends / changed since your queue was written**
- **ProPublica Congress API — dead** (closed to new keys). It's in `sources_queue.py`; swap to **GovInfo / Congress.gov**.
- **Senate LDA legacy site retires 2026-06-30 (9 days)** — lobbying must target the new **`LDA.gov` REST API**.
- **OpenCorporates** open bulk is now heavily gated/commercial — use the free **GLEIF OpenCorp-id↔LEI** slice for the crosswalk instead.
- **AWS IRS-990 e-file bucket** announced it's winding down — mirror soon; ProPublica Nonprofit Explorer is the per-EIN fallback.
- **OECD data-explorer** is a JS shell (per `build-state` batch 5) — use its SDMX endpoint.

**Duplicates / already covered (don't double-onboard)**
- **SEC EDGAR company tickers**, **NPPES** — already landed. SEC FSDS/Submissions *extend* EDGAR; they're not dupes.
- **USASpending subawards** — landed; the prime-award archive (#11) is the complement, not a dupe.
- **OFAC SDN** is a subset of **OpenSanctions** — pick one.
- **~20 of these are already in `sources_queue.py`** (`[Q]`) — they were planned day-one and never run. The value of this audit is telling you **which to run first by join density**, not discovering them.

---

## Corrections to the raw scout output (verified this session)

- **NPPES does NOT carry a usable EIN.** A scout claimed `fed_cms_nppes` carries EIN (→ 9.6M rows on the EIN key). The dbt `schema.yml` lists an `EIN` column, but it's **auto-generated**, the CMS public NPPES file **suppresses EIN**, and `build-state.md` records the dbt build had to **drop a "phantom EIN not_null"** test. → EIN credited to **`hhs_taggs` only**; NPPES connects via **NPI + ZIP**. This deflated IRS-BMF from a claimed 4 connections to its real ~1 + hub value (still a top hub, now correctly in Tier B).
- **`fed_cms_nursing_home` is a stronger bridge than briefed** — verified it carries `npi`, `ccn`, `county_fips`, `zip_code`, **and** `lat/lon` (+ `chain_id` ownership). It sits in both the health and geo clusters; counted accordingly.

## Limits of this audit
- Existing counts are **documented-state** (repo + ledger), **not live-verified** — no Snowflake creds this session. A live pass against `SOURCE_REGISTRY.JOIN_KEYS` + `INFORMATION_SCHEMA` could confirm inferred keys (`usaspending_subawards` UEI/place, `hhs_oig_leie` NPI, `cms_hcris` zip) and the full 901-row catalog.
- Connection counts are **structural** (shared key exists), not **measured** (actual join hit-rate). Name-based (fuzzy) joins especially need real entity resolution to realize.
- If the wishlist Excel resurfaces, cross-check it against this — the scouts found these independently, so overlap = validation, gaps = either a dead source or a real find your list missed.
