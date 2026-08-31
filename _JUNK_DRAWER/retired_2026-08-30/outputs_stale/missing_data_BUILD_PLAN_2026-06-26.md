# Missing-Data Build Plan — 2026-06-26

Turns the "what data are we missing" map into an ordered, gated execution program. Source of the
map: the 12-cluster research workflow (`wf_2484c50a-6b4`) + live catalog grounding (1,506 scouted /
54 landed). **Core finding: this is a LOADING plan, not a scouting plan** — ~90% of the high-value
genres are already `scouted` catalog rows that were never poured in.

Ranking lens (Chris, 2026-06-26): **maximize connections onto a spine we already have landed.**

Legend — **Gate**: `AUTO` = agent runs it (safe/offline/no budget) · `GO` = needs Chris's go (spends
Snowflake compute or mutates the catalog) · `DECIDE` = needs a design call before code.

---

## KEY REALIZATION THAT ORDERS EVERYTHING

The raw LOAD never needs join-key infrastructure (landing is an all-TEXT mirror). Join keys only
matter at the CONNECT step. So:

- **Loads on keys the tagger already knows** (NPI, CCN, UEI, DUNS, CIK, EIN, IMO, MMSI, NAICS, LEI) —
  connect the day they land. **No new code.** → Phase 1.
- **Loads that introduce a NEW key** (TAIL_NUMBER, ICAO24, FRS_ID, ORI, FEC_CMTE_ID/CAND_ID, CUSIP,
  BIOGUIDE) — land fine, but stay disconnected until the tagger learns the token. → Phase 2, gated on
  the key-infra step (#K below).

The whole high-ROI front (health-money, contracting, securities, nonprofit, sanctions) is Phase 1 —
**zero new key infra.** Aviation/crime/elections is Phase 2.

---

## PHASE 0 — FOUNDATION (this session, mostly AUTO)

| # | Step | Gate | Notes |
|---|---|---|---|
| 0.1 | This build plan | AUTO | done |
| 0.2 | build-state.md next-build queue | AUTO | done |
| 0.3 | Open Payments loader spec (deterministic, `bridge_fuel_specs.py`) | AUTO | done — preview before run |
| 0.4 | Catalog domaining-cleanup preview (`scripts/propose_catalog_domaining_fixes.py`) | AUTO→GO | preview AUTO; `--apply` is GO |
| K | Join-key infrastructure design (new tokens + NORM_RULES) | DECIDE | spec below; edit gated |

### Step K — join-key infrastructure (the Phase-2 prerequisite)

`connect/keys.py.detect_key` reuses the **global tagger** `portal_recon/tag_portal_index.KEY_TOKENS`,
which also tags the 338k portal index + 638-table graph. The project convention (see
`bridge_fuel_specs.py`) is **never broaden the global tagger casually** — a loose token false-positives
everywhere. New keys must be added with *precise* tokens (or `PAIR_RULES`), then verified by re-running
`connect fingerprint` and checking for spurious new edges.

Proposed additions (gated — do NOT ship until verified against the live graph):

```
# portal_recon/tag_portal_index.py  KEY_TOKENS  (tier, {tokens})
TAIL_NUMBER : STEEL  {"n_number","tail_number","registration_n"}   # NOT bare "tail"/"reg" (false +)
ICAO24      : STEEL  {"icao24","mode_s","transponder_hex"}
FRS_ID      : STRONG {"registry_id","frs_id"}                       # EPA Facility Registry
ORI         : STRONG {"ori9","originating_agency_identifier"}       # NOT bare "ori" (origin/category)
FEC_CMTE_ID : STRONG {"cmte_id","committee_id"}
FEC_CAND_ID : STRONG {"cand_id","candidate_id"}
CUSIP       : STRONG {"cusip"}
BIOGUIDE    : STRONG {"bioguide_id","bioguide"}

# connect/keys.py  NORM_RULES  (mode, width)
TAIL_NUMBER : ("alnum_upper", 0)   ICAO24 : ("fixed", 6)   FRS_ID : ("code", 0)
ORI : ("code", 0)   FEC_CMTE_ID : ("fixed", 9)   FEC_CAND_ID : ("fixed", 9)
CUSIP : ("fixed", 9)   BIOGUIDE : ("alnum_upper", 0)
```
Risk note: `ORI` and `TAIL_NUMBER` are the dangerous ones (origin/retail/territory collisions). Gate
on a fingerprint dry-run that shows zero new false edges on the existing 638 tables before merging.

---

## PHASE 1 — LOAD-NOW (existing keys, ranked by spine lit). Each = one `GO` checkpoint.

| Rank | source_id (catalog state) | Key → landed spine it lights | Loader | New detector |
|---|---|---|---|---|
| 1 | `fed_cms_open_payments` (scouted) | **NPI → NPPES 9.6M + LEIE** | bridge_fuel (spec'd) | **banned-but-PAID** (LEIE × Open Payments) |
| 2 | `fed_cms_part_d_prescribers` (scouted) | NPI → NPPES + LEIE | bridge_fuel | excluded-but-prescribing |
| 2b | `fed_cms_medicare_provider` Part B (scouted) | NPI → NPPES + LEIE | bridge_fuel | excluded-but-billing-Medicare |
| 3 | USASpending **File D1 DoD** (absent) | UEI → USASpending 6.3M + SAM | LLM agent / new script | debarred-but-funded (defense) |
| 3b | `fed_usaspending_subawards` (sampled) | UEI → USASpending + SAM | LLM agent | debarred-at-subaward-tier |
| 3c | SAM.gov **Entity Mgmt** (scouted) | UEI → USASpending + SAM | LLM agent (api key) | gives every UEI a name+address |
| 4 | `fed_sec_edgar_insiders` (scouted) | **CIK → ticker map** (dead today) | LLM agent | insider-trade-on-events |
| 4b | SEC **Financial Statement sets** (absent) | CIK + EIN → ticker map + EIN spine | LLM agent | leverage/going-concern flags |
| 5 | `fed_irs_990` + `fed_irs_eo_bmf` (scouted) | **EIN** (activates dormant key) | bridge_fuel | revoked-but-funded |
| 6 | `intl_opensanctions` (scouted) | IMO/LEI/NAME → OFAC + AIS | LLM agent (FtM JSON) | broadens the sanctioned-vessel FLAG side |
| 6b | `fed_gfw_api`/`_bulk` (scouted) | MMSI/IMO → NOAA AIS | LLM agent (api key) | sanctioned-vessel-at-transshipment |
| 7 | `fed_fac_single_audit` (scouted) | **EIN + UEI** (dual-key bridge) | LLM agent (data.gov key) | adverse-audit-but-funded |
| 8 | EPA **ECHO Exporter** (scouted) | EIN/NAICS → corporate (FRS = Phase 2) | bridge_fuel | penalized-polluter-but-funded |
| 9 | DOL **OSHA** + **WHD** (scouted) | EIN → EIN spine | bridge_fuel | wage-theft/safety-debarred-but-funded |

Detector each unlocks is config-only on `connect/leads_specs.py` once both legs are landed.

---

## PHASE 2 — NEW-VERTICAL (needs Step K first). Gated.

| source_id (state) | New key | Why | Detector |
|---|---|---|---|
| `fed_faa_registry` (scouted) | TAIL_NUMBER, ICAO24 | the aviation spine root; Epstein-planes | (registry leg) |
| `xc_opensky_network` (scouted) / ADS-B | ICAO24 | live-tracking leg | **hidden-but-flying** (LADD × ADS-B → owner) |
| FAA **LADD** block list (absent) | TAIL_NUMBER | the FLAG list | hidden-but-flying |
| `fed_fbi_cde` NIBRS (scouted) | ORI | fills crime_security from 0 | policing-accountability anchor |
| `fed_fec_bulk` (scouted) | FEC_CMTE_ID/CAND_ID | money-in-politics federal layer | (+ congress crosswalk) |
| `xc_unitedstates_congress` (scouted) | BIOGUIDE/FEC_CAND_ID | **load FIRST** — turns 3 name-piles into hard links | congress-traded-what-it-regulates |
| `fed_house/senate_financialdisclosure` (scouted) | BIOGUIDE | STOCK Act trades | congress-stock-trades |

---

## PHASE 3 — EMPTY-DOMAIN FILLS (one source each; mix of Phase 1/2)

| Domain (0 landed) | Pour | Phase |
|---|---|---|
| geo_demographics | Census ACS + TIGER (`api.census.gov`) — FIPS backbone the whole library leans on | 1 (FIPS exists) |
| crime_security | FBI NIBRS (`fed_fbi_cde`) | 2 (ORI) |
| education | NCES CCD + IPEDS | 2 (NCES exists actually → 1) |
| elections_voting | MIT Election Lab county returns + FEC candidate master | 2 (FIPS exists → returns are Phase 1) |
| money_finance | SEC Form 4 insiders (Phase 1 #4) | 1 |
| money_in_politics | FollowTheMoney + FEC (Phase 1/2) | 1/2 |
| immigration_migration | EOIR immigration-court case data | 1 (court records, no new key) |
| procurement_intl | USASpending File D1 (Phase 1 #3) | 1 |

---

## PHASE 4 — TRULY ABSENT (not even scouted — these need a scout pass first)

SEC Financial Statement Data Sets · SEC 13F holdings · SEC Form D · USASpending File D1 · NYC ACRIS /
county deeds at scale · Port State Control (Paris/Tokyo MoU, scrape) · FAA LADD · vessel ownership
(Equasis/IHS). Scout → then they enter Phase 1/2.

---

## COURTS GAP (flagged — the courts-legal cluster agent died mid-run)

`justice_courts` is landed-but-shallow (SCDB/Oyez/FCA/FJC-stats); the **DOCKET** key is in the
normalizer with almost no data behind it — same "key with no territory" pattern as CIK/EIN. Scouted &
unloaded: `fed_pacer`, CourtListener/RECAP. Add as a Phase-1 LLM-agent load (DOCKET exists). Re-run the
failed cluster agent if a fuller courts map is wanted.

---

## BACKFILL ENGINE — loader performance (Chris asked "can we go faster?")

The honest finding: **warehouse size is NOT the main lever** on the current loader. Every load is
(1) a client-side download, then (2) serial `write_pandas` — PUT+COPY per 200k-row chunk. The cost is
client round-trips + download bandwidth, not warehouse horsepower. Doubling the warehouse = 2-4× credits
for ~1.2× speed. Three levers, in ROI order:

1. **Parallelism — DONE (2026-06-26).** `bridge_fuel_load.py --workers N` runs N specs concurrently,
   each its own connection. A warehouse bills *uptime, not queries*, so concurrent COPYs are ~free
   speedup. Keep N modest (4-8) — local download/disk is the cap, not the warehouse. Also added
   comma-list `--spec a,b,c`.
2. **PUT-many → single `COPY INTO` — NEXT (designed, not built).** Replace serial per-chunk
   `write_pandas` with: stream the file → write chunks to local gzipped CSVs → `PUT` all to an internal
   stage (PUT parallelizes upload threads) → **one** `COPY INTO tbl FROM @stage` (Snowflake parallelizes
   across files + within each, using ALL warehouse threads). Keep the all-TEXT mirror + provenance
   stamps (add `_INGESTED_AT/_SOURCE_RUN_ID/_SRC_SHA256` as columns before PUT, or via COPY transform).
   Idempotency unchanged (SHA skip; overwrite stage per run). **This is the change that makes warehouse
   size finally pay off** — COPY is thread-bound, so S/M/L give near-linear wall-clock at ~flat credits.
3. **Warehouse sizing — only after #2, and only for a backfill sprint.** Per-second billing × size
   (XS=1, S=2, M=4 credits/hr): a 2× warehouse finishing in half the time ≈ same credits, so size is
   cost-neutral *when the work is warehouse-bound* (true only after #2). ⚠️ **The `RIPPLE_BUDGET` monitor
   (15 credits, suspend @90%) WILL halt a real backfill** — raise it for the sprint, drop it back after.

**Backfill cost reality:** most of the ~850 scouted sources are SMALL (portal/registry) → fast at any
size. Cost is the few giants. A full backfill is ~$50-150 compute one-time; storage ~$1/mo. Money isn't
the constraint — the budget *monitor* is. NB: the LLM-agent path (`registry_batch.py`) needs
`ANTHROPIC_API_KEY` (currently absent from `.env`); the deterministic paths (`bridge_fuel_load`,
`connect harvest`/`portal_loader`) are what parallelize cleanly today.

## RECOMMENDED OPENING RUN (3 loads, in order)

1. **`fed_cms_open_payments`** — one bulk load, NPI into 9.6M providers, ships banned-but-PAID day one.
2. **`fed_irs_990` + `fed_irs_eo_bmf`** — makes the EIN key real (follow-the-money backbone).
3. **`fed_faa_registry` + `xc_opensky_network`** — needs Step K first; breaks single-vertical risk +
   gives the Epstein theme a spine.

Budget note: loads run on `RIPPLE_WH` under the 15-credit/mo `RIPPLE_BUDGET` monitor. Big files
(Open Payments ~15M rows/yr) are chunked; storage is trivial, compute is the only cost and it's capped.
