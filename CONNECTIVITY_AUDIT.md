# The Library — Full Connectivity Audit
**Date:** 2026-06-21 · **Scope:** recon + ranking only (no ingest, no models, no warehouse writes)
**Author:** onboarding agent · **Input:** `public_data_sources_1.csv` (the catalog/wishlist, 891 sources) + the in-repo dbt project + `build-state.md`

---

## ⚠️ PROVENANCE & CONFIDENCE BASIS — read this first
This audit was built **without live Snowflake access this session.** The injected `SNOWFLAKE_PAT` is dead (`394400`), the read-only MCP server is down with it (same token), and the working PAT lives only in a gitignored `.env` absent from this container. So every number below rests on one of three evidence levels — and they are **not** equal:

| Evidence level | What it is | Covers | Trust |
|---|---|---|---|
| **Column-verified** | Real renamed/cast columns read from the dbt **staging SQL** in this repo | 36 modeled sources | High — but from repo code, not live `SHOW COLUMNS`, and **can't see population** |
| **Catalog-declared** | The `join_keys` field each source declares in the catalog CSV | all 891 | Medium — a *claim*, not a verified column (this is where phantoms hide) |
| **Last-known live** | Warehouse counts from your `build-state.md` (2026-06-20) | table inventory | Stale by 1 day; **not re-confirmed this session** |

**Consequence:** the only connections I can call **STEEL** are those where the key is column-verified on *both* sides (just **4 pairs**). Everything else is **declared** and must be validated against live data before you trust it. **Phantom-key detection genuinely requires the live warehouse** — I caught the one corroborated phantom (NPPES-EIN) from known fact + the dbt scan, but a full phantom sweep needs the PAT restored.

---

## 1 · TOP-LINE

**Table universe**
- **891** catalog sources (the wishlist) · **44** landed tables (build-state 2026-06-20: "45 landing tables", one is the dropped demo) · **36** of those modeled in dbt
- The catalog is **not** a superset of what's landed: **11 landed sources aren't in this catalog snapshot** (SEC EDGAR tickers, FDIC failed banks, Federal Register, Treasury ×2, FDA recalls, the Wayback/Epstein proofs).

**Connections in the *existing* landed graph (44 tables, 156 strands):**

| Tier | Pairs | Meaning |
|---|---|---|
| 🔵 **STEEL** | **4** | key column-verified on both sides |
| 🟢 **STRONG** | **92** | joinable key, ≥1 side declared-only (mostly FIPS/ZIP/company_id) |
| 🟡 **GEO** | **50** | connected only via geographic rollup (lat/lon, state, country) |
| 🔴 **PROBABILISTIC** | **10** | court-scoped docket / name-only |

**The headline number:**
> Today, **25 of 44 landed tables (57%)** carry at least one **trustworthy (STEEL/STRONG)** strand; 5 more connect only through geography; **12 sit isolated.**
> Run the **full ladder** (surrogate keys + ZIP↔FIPS bridge + county rollup) on *what's already landed* and that rises to **~30 of 44**.
> Apply **Tier-A ingest** (the 30 highest-payoff wishlist sources — **24 of which are already in `sources_queue.py` and never ran**) and the warehouse collapses into **one dominant connected component of ~60 tables** anchored on the FIPS/ZIP geographic spine and the USASpending–SAM–Census contractor hub. **Every Tier-A source links to 15–29 landed tables.**

**Of the 858 wishlist sources:** 661 (77%) connect to ≥1 landed table at *some* tier; **433 (50%) carry a STEEL/STRONG-grade key** into the existing graph; **166 connect to nothing** (date/name/custom only).

---

## 2 · THE KEY MAP (Phase 1)
Confirmed = column-verified in dbt staging. Inferred = catalog-declared, **not** column-checked. Phantom/dead = declared but doesn't actually join.

### Landed + modeled sources (the current graph)

| source_id | 🔵 CONFIRMED (dbt-verified) | 🟢 INFERRED (catalog-declared) | ⚫ PHANTOM / DEAD |
|---|---|---|---|
| fed_cms_nppes | NPI | EIN, ZIP | **EIN — declared but suppressed from public NPPES (real cols = NPI only). Confirmed phantom.** |
| fed_cms_hcris | CCN, ZIP, county, state | NPI | NPI — not in real cols (HCRIS keys on CCN). *Verify live.* |
| fed_cms_nursing_home | NPI, ZIP, address, lat_lon | CCN, FIPS | CCN suspected-missing in scan — *likely my scan gap, verify live.* |
| fed_sec_edgar_company_tickers | CIK, ticker | — | — |
| fed_fdic_failed_banks | FIPS, state | — | — |
| fed_mapping_inequality | FIPS, lat_lon | — | — |
| fed_nara_wra_aad | FIPS | lat_lon | — |
| fed_noaa_ais | IMO, MMSI, lat_lon | — | — |
| fed_fjc_idb | docket | state | docket = district-court-scoped |
| fed_scdb / fed_oyez | docket | (oyez: case_id) | docket = SCOTUS-scoped (joins to each other, **not** to fjc) |
| fed_fdic_enforcement | docket | company_id | — |
| fed_cfpb_complaints | ZIP | state | — |
| fed_fda_drug_enforcement | ZIP | — | — |
| fed_hhs_taggs | — | EIN, FIPS, ZIP, lat_lon | (none verified — staging didn't cast them; verify live) |
| fed_fara_bulk | address | company_id, state | — |
| fed_nara_aad / fed_wpa_slave_narratives | — | FIPS, lat_lon | — |
| fed_slavevoyages_intraamerican | — | FIPS, country, lat_lon | — |
| fed_doj_crt_cases / fed_doj_fca_settlements / fed_naag_multistate_settlements | — | company_id, state | — |
| intl_ch_zefix | address | company_id, country | — |
| intl_gr_gemi | ZIP | company_id | — |
| intl_es_borme / intl_ie_cro | — | company_id, country | — |
| intl_ec_sercop | — | company_id | — |
| intl_ember_elec / intl_it_istat | — | country | — |
| intl_hudoc | — | country, docket (ECHR) | — |
| xc_biorxiv_medrxiv | DOI | — | — |
| fed_clinicaltrials / fed_treasury_* / fed_federal_register_documents / fed_revolvingdoor_project | — | — (custom/date/name only) | **time-series & registry tables — no entity/geo key; near-isolated** |

### Catalog-wide key carriers (all 891, declared)

| Key | # sources | Role in the graph |
|---|---|---|
| `date` | 690 | **surrogate-key component** (never a join alone) |
| `lat_lon` | 274 | geographic rollup → county FIPS |
| **`FIPS`** | **245** | **the US geographic backbone** |
| `country` | 202 | the international backbone |
| `state` | 191 | coarse US geo |
| `person_name` | 186 | entity-resolution axis (probabilistic) |
| `ZIP` | 164 | rolls to FIPS via HUD crosswalk |
| **`company_id`** | **130** | corporate-registry backbone (jurisdiction-scoped) |
| `EIN` | 62 | US nonprofit/business |
| `docket` | 48 | court-scoped (not one space) |
| `parcel` | 33 | local property |
| `DOI`/ORCID | 20 · `NPI` 17 · `MMSI` 8 · `CIK` 7 · `UEI`/`DUNS` 6–7 · `LEI` 6 · `IMO` 6 | sparse high-value entity hubs |

---

## 3 · THE CONNECTION GRAPH

### 🔵 STEEL — the only column-verified strands (trust these)
| A ↔ B | technique | key | why STEEL |
|---|---|---|---|
| `fed_cms_nppes` ↔ `fed_cms_nursing_home` | direct | **NPI** | NPI cast in both staging models |
| `fed_mapping_inequality` ↔ `fed_fdic_failed_banks` | direct | **FIPS** | FIPS cast in both |
| `fed_mapping_inequality` ↔ `fed_nara_wra_aad` | direct | **FIPS** | FIPS cast in both |
| `fed_fdic_failed_banks` ↔ `fed_nara_wra_aad` | direct | **FIPS** | FIPS cast in both |

That's it. The entire trustworthy-verified core today is **one healthcare pair (NPI) and one redlining/bank-failure/internment triangle (FIPS)** — three datasets that join on county and let you ask *"what happened in the same places."*

### 🟢 STRONG — declared joinable keys (mechanical once validated)
Grouped by cluster (representative strands; full pairwise list is mechanical from the key map):

- **US geographic spine (FIPS/ZIP/county):** `fed_fdic_failed_banks` · `fed_mapping_inequality` · `fed_nara_wra_aad` · `fed_nara_aad` · `fed_wpa_slave_narratives` · `fed_slavevoyages_intraamerican` · `fed_hhs_taggs` · `fed_cms_hcris` · `fed_cms_nursing_home` · `fed_cfpb_complaints` · `fed_fda_drug_enforcement` — all mutually joinable on FIPS or ZIP→FIPS.
- **Corporate registry (company_id, jurisdiction-gated):** `intl_ch_zefix` · `intl_es_borme` · `intl_ie_cro` · `intl_gr_gemi` · `intl_ec_sercop` · `fed_fara_bulk` · `fed_fdic_enforcement` · the DOJ/NAAG settlement tables — each joins **within its jurisdiction** only.
- **Maritime (MMSI/IMO):** `fed_noaa_ais` is the landed anchor; the whole wishlist maritime cluster (GFW, MarineTraffic, VesselFinder, Equasis, IMO GISIS, AISHub) hangs off it.

### 🟡 GEO — connected only through place (coarser grain)
Any lat/lon, state, or country source rolled to a common grain. Pulls in the international set (`intl_ember_elec`, `intl_it_istat`, `intl_hudoc`) on **country**, and the `_subawards`/scrape tables on **state**.

### 🔴 PROBABILISTIC — candidates, must validate before use
- **`fed_scdb` ↔ `fed_oyez`** on docket — *plausible* (both SCOTUS) but docket formats differ; validate.
- **`fed_fjc_idb` docket** does **NOT** join to SCDB/Oyez (district vs Supreme Court — different number spaces). **Do not draw this strand.**
- Person-name links across `fed_revolvingdoor_project` / `fed_fara_bulk` / the DOJ tables / Congress sources — real investigative value, but name-only = fuzzy.

---

## 4 · THE WEB THAT LIGHTS UP (the money shot)
**The densest, highest-trust cluster is the US-geography spine.** 387 of 891 catalog sources carry a US-geographic key (FIPS 245 / ZIP 164 / lat-lon 274). Rolled to **county FIPS**, they become one joinable surface — *"show me everything that happened in this county."*

It already has a verified seed in the warehouse (the FIPS triangle above). The moment the federal geographic heavyweights land, it becomes the backbone of the entire Library:

```
                      ┌─────────── fed_census_acs (FIPS/ZIP/tract) ───────────┐
                      │                                                        │
   fed_usaspending ───┼─ FIPS+EIN+UEI ─ fed_sam_entity ─ UEI/DUNS ─ fed_fpds  │
   (award $ by place) │                  (who got paid)                       │
                      │                                                        │
  [LANDED FIPS seed]  │   EPA ECHO/TRI ── FIPS+lat/lon ── HUD ── ZIP↔FIPS ──── │
  fdic_failed_banks ──┤   (pollution by place)         (the crosswalk bridge) │
  mapping_inequality ─┤                                                        │
  nara_wra_aad ───────┴─ FIPS ─ CMS (NPPES/nursing_home/hcris) ─ NPI/CCN ──────┘
                                 (healthcare by place + provider)
```

**Why it's the money shot:** it fuses *money* (USASpending/FPDS/SAM), *place* (Census/FIPS), *harm* (EPA/CMS/CFPB), and *history* (redlining/internment) on a single key you can trust. And it's **cheap to light up** — almost every node is already queued.

Second-densest: the **corporate/ownership web** — `company_id` (130) bridged by **GLEIF LEI** + **OpenCorporates** + **OpenSanctions** + **ICIJ Offshore Leaks**, anchored to US filers via **SEC EDGAR CIK**. Higher investigative payoff (Epstein-relevant), but needs the bridges built first (see §5).

---

## 5 · SURROGATE & BRIDGE OPPORTUNITIES (the net-new value)
These are connections **direct key-matching misses** — the manufactured strands.

### Surrogate keys (ID + timestamp) — 126 candidate sources
Event-level tables that share *who + when* but no native shared key. Manufacture `entity_id ‖ event_date`:
- **Lobbying ↔ revolving-door ↔ FARA:** `person_name ‖ date` joins `fed_revolvingdoor_project` (landed, currently isolated) to lobbying/FARA registrations → *"who moved from government to lobbying, and when."*
- **Settlements ↔ enforcement:** `company_id ‖ date` across `fed_doj_fca_settlements` · `fed_fdic_enforcement` · `fed_naag_multistate_settlements` → one enforcement timeline per company.
- **Congress:** `bioguide ‖ date` across the (wishlist) Congress/GovInfo/PACER/CourtListener cluster.
> Specify columns: surrogate = `LOWER(normalized_name) || '|' || TO_DATE(event_ts)`.

### Bridge / crosswalk tables — each links whole clusters
| Bridge | Connects | Have it? |
|---|---|---|
| **HUD USPS ZIP ↔ FIPS** | the **38 ZIP-only** sources → the **245-source FIPS cluster** | ❌ need to ingest (`fed_hud_data`, already queued) |
| **Census TIGER / county centroids** | the **12 lat-lon-only** sources → county FIPS (point-in-polygon) | ❌ queued (Census TIGER) |
| **GLEIF LEI golden-copy** | the **91 international `company_id` registries** → each other + US | ❌ queued (`intl_gleif`) |
| **OpenCorporates** | `company_id` ↔ `LEI` ↔ jurisdiction | ❌ queued (`intl_opencorporates`) |
| **SEC EDGAR CIK↔ticker** (landed!) | public filers ↔ market data | ✅ landed but **isolated** — lands its cluster when `fed_sec_edgar` (filings) arrives |

**The single highest-leverage bridge to build: HUD ZIP↔FIPS.** It's one small table that promotes 38 ZIP-only sources into the 245-source geographic backbone.

---

## 6 · RANKED INGESTION PLAN (Phase 4)

### TIER A — ingest now (max STEEL/STRONG added to the existing graph)
Sorted by tier-weighted distinct landed tables connected (score = 3·steel + 2·strong + 1·geo). **`Q` = already in `sources_queue.py`.**

| # | source_id | tier | links to landed (STR/GEO) | keys | Q? |
|---|---|---|---|---|---|
| 1 | **fed_usaspending** | 1 | 22 / 7 | FIPS, EIN, UEI, DUNS, CIK, company_id, ZIP, country | **Q** |
| 2 | fed_sam_entity | 1 | 21 / 1 | UEI, DUNS, EIN, company_id, FIPS, ZIP | **Q** |
| 3 | fed_usaspending_bulk | 1 | 21 / 1 | (same as USASpending, bulk) | **Q** |
| 4 | fed_census_acs | 1 | 15 / 12 | FIPS, ZIP, state, country | **Q** (TIGER) |
| 5 | fed_fpds | 1 | 20 / 1 | UEI, DUNS, company_id, FIPS, ZIP | **Q** (SAM) |
| 6 | fed_sam_opportunities | 1 | 20 / 1 | UEI, DUNS, company_id, FIPS | **Q** |
| 7 | fed_epa_echo | 1 | 16 / 5 | FIPS, lat/lon, EIN, ZIP, state | **Q** |
| 8 | fed_epa_tri | 1 | 16 / 5 | FIPS, lat/lon, EIN, ZIP | **Q** |
| 9 | fed_cms_main | 1 | 16 / 5 | NPI, FIPS, ZIP, state | **Q** (NPPES family) |
| 10 | fed_hud_data | 2 | 16 / 5 | FIPS, ZIP, EIN — **+the ZIP↔FIPS bridge** | **Q** |
| 11–15 | fed_census_business_patterns · fed_census_economic · fed_cfpb_hmda · fed_dol_osha_inspections · fed_dol_wage_hour | 1 | 16 / 5 | FIPS, EIN, ZIP, state | — |
| 16 | fed_cms_open_payments | 1 | NPI hub | NPI — Sunshine Act payments to providers | — |
| 17–22 | fed_fcc_broadband · fed_fema_openfema · fed_epa_sdwa/envirofacts · fed_fdic_bank_data · fed_cdc_data_portal | 1–2 | 15 / 6 | FIPS, lat/lon, ZIP, state | — |
| 23–26 | **st_ny_open · st_nj_open · st_pa_open · st_ca_open** | 1 | 15 / 6 | FIPS, ZIP, lat/lon | — |
| 27 | xc_wikidata | 1 | company_id, CIK, LEI, FIPS, country | the cross-domain ID bridge | — |
| 28–30 | fed_sba_ppp · fed_sba_loans · fed_cms_medicare_provider | 1 | EIN / NPI hubs | — |

### TIER B — ingest soon (real connections, coarser or narrower)
- **The bridge/anchor set:** `intl_gleif` (LEI), `intl_opencorporates`, `intl_opensanctions`, `intl_icij_offshore`, `fed_sec_edgar` (CIK filings — **de-isolates the landed EDGAR table**). High investigative value, but they unlock the *corporate* cluster which has thinner landed anchors today.
- **Maritime cluster:** GFW, MarineTraffic, Equasis, IMO GISIS — all hang off landed `fed_noaa_ais` (MMSI/IMO), but only connect to that one anchor for now.
- **International country-grain:** World Bank, IMF, OECD, WHO — GEO-tier only (country), join `intl_ember_elec`/`intl_it_istat`.
- **Congress/courts surrogate cluster:** CourtListener, PACER, Congress/GovInfo — need the surrogate `bioguide‖date` / `docket‖court` build-out.

### TIER 0 — catalog only (no current connection; named blocker)
**166 sources** carry only date/name/custom. Waiting on:
- **transit (17):** GTFS feeds — need lat/lon extraction → then GEO-tier.
- **data preservation / web archives (17):** no entity grain — link only by URL/time.
- **astronomy (7), chemistry (5), academic archives (7):** genuinely outside the accountability graph — catalog them, don't prioritize.
- **financial time-series (8) + landed `fed_treasury_*`, `fed_federal_register_documents`, `fed_clinicaltrials`:** time-series/registry shape, no entity/geo key — isolated until a dimension table gives them one.

### ‼️ Re-prioritization, not net-new work
**24 of the top-30 Tier-A sources are already in `sources_queue.py` and never ran.** The single highest-connectivity ingest in the entire wishlist — **`fed_usaspending`** — is queue entry #2. SAM.gov, EPA ECHO/TRI, HUD, Census, FEC, SEC EDGAR are all queued-but-unrun. **Landing the existing queue, in payoff order, is most of this plan.** Only landed from the queue so far: `usaspending_subawards` (proof slice), `cms_nppes`, `intl_hudoc`, `usgs_earthquakes`.

---

## 7 · HONEST FLAGS

**Phantom / dead keys**
- ⚫ **NPPES-EIN — confirmed phantom.** Catalog declares `fed_cms_nppes` join_keys = "NPI, **EIN**, zip"; the real staging columns expose **NPI only**. CMS suppressed EIN from the public NPPES file. **Anyone joining providers→nonprofits on NPPES-EIN gets nothing.** Use NPI; reach EIN via a different bridge.
- ⚠️ **hcris-NPI, nursing_home-CCN** declared but not seen in my dbt column scan — **likely my scan's incompleteness, not true phantoms.** Verify against live columns before trusting *or* discarding.
- 🔴 **docket is not one key.** SCOTUS (SCDB/Oyez), district court (FJC IDB), and FDIC admin dockets are **separate number spaces.** Don't draw a docket strand across court systems.
- 🟡 **company_id is jurisdiction-scoped.** Spain's BORME number ≠ Ireland's CRO number. Cross-jurisdiction corporate joins **require** the GLEIF/OpenCorporates bridge — they are not direct.

**Maintenance traps / dead sources (from `build-state.md`)**
- `fed_cms_tic_mrf` (ghost — false-success, no table), `fed_doj_crt_cases` (1 row — resistant JS scrape), `intl_demo_quotes_toscrape_js` (dropped demo). Thin landings flagged for review: `intl_ie_cro` (3), `fed_nara_wra_aad`, `fed_fdic_enforcement`.

**Duplicates / overlaps in the catalog**
- `fed_usaspending` vs `fed_usaspending_bulk` vs landed `fed_usaspending_subawards` — same data family, three rows. `fed_sec_edgar` / `_insiders` / `_efts` — pick the filings core first. Don't triple-ingest.

**INFERRED keys I'm leaning on that MUST be verified live before you trust them**
- Every 🟢 STRONG strand where the key is **declared-only** (the majority): all FIPS/ZIP/EIN connections on `fed_hhs_taggs`, `fed_nara_aad`, `fed_slavevoyages_intraamerican`, the DOJ/NAAG settlement tables, and **all 858 wishlist key declarations.** They are claims from the catalog's `join_keys` field, not column-checked. The Tier-A ranking is robust to individual errors (it's driven by the dense geo backbone), but **no single STRONG strand should be shipped to a mart without confirming the column exists and is populated.**

---

## 8 · WHAT UNBLOCKS THE FULL LIVE AUDIT
This brief is the best honest read from the repo + catalog. To upgrade it to a **column-verified, population-checked** audit (and run a real phantom sweep across all 891), I need:
1. **A fresh `SNOWFLAKE_PAT`** in `library-onboarding/.env` (revives the connector *and* the MCP server) — same fix as 2026-06-20.
2. Then I re-run Phase 1 against live `SHOW COLUMNS` + population checks, promote declared→verified where they hold, and demote the phantoms.

**One thing if you do nothing else:** land **`fed_usaspending`** (already queue #2) and build the **HUD ZIP↔FIPS** bridge. That one source + one crosswalk lights up more of the graph than anything else on the board.
