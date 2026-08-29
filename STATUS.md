# RIPPLE STATUS — 2026-08-28 — Fable recon done: 13 unregistered ID candidates ranked (CAGE code is the headline); mega-loads still running; spine rebuild landed clean earlier tonight

*One screen. Rewritten (never appended) at the end of every session.*

## 🚨 Read this first

1. **Fable recon mission (unregistered ID columns) is DONE.** Full ranked
   deliverable: `reports/recon/unregistered_id_candidates_2026-08-28.md`.
   Headline results, all verified against the live warehouse this session:
   - The packet's step 1 came back **empty**: zero rows in COLUMN_CATALOG with
     DETECTED_KEY set but KEY_TIER blank — every detected key is already
     tiered. All candidates came from name/shape scanning the 626 undetected
     columns (751 total → 277 grouped candidates → 13 keepers).
   - **CAGE code** (defense-contractor ID) in the contracts table: 6.32M of
     6.33M rows filled, 92,530 distinct — a whole registered-family-grade axis
     sitting unregistered.
   - **Profiler blind spot found:** COLUMN_CATALOG's samples for NPPES read
     early rows only — all 200 "other provider identifier" columns showed
     empty, but slot 1 alone has 1.56M filled / 1.34M distinct (state Medicaid
     IDs, Railroad Medicare, UPINs). License slot 1: 5.78M filled / 3.91M
     distinct. The catalog under-reports sparse-at-top columns.
   - Easy wins: 4 politics-mart columns are exact formats of already-registered
     families (FEC candidate/committee IDs, Bioguide) under other names — two
     are JSON arrays.
   - Scope honesty: COLUMN_CATALOG only covers ~15 pack tables, so the
     "appears in 2+ tables" test was mostly untestable inside it; warehouse-wide
     spread in the report is marked inferred. The 2026-08-18 value-shape
     sniffer covered warehouse-wide and found different things — the two lists
     complement, not duplicate.
   - Nothing was registered, no code written, connect layer untouched (per
     packet).
2. **Still open from earlier tonight (unchanged by this recon):**
   - 8 spatial join errors — malformed lat/lng in EPA Toxic Release Inventory
     and NTSB aviation events broke point-in-polygon for those pairs. Skipped
     safely, not yet fixed.
   - 5 new loader scripts + connect-layer edits **still uncommitted** in the
     working tree.
3. **Loads running overnight, checkpointed + resumable:**
   - MAUDE device injuries → `FED_FDA_MAUDE_FULL`: 25,711,469 records, ~6–8h.
     Resume: `python scripts/fda_bulk_split_load.py --spec FED_FDA_MAUDE_FULL
     --run`. Verify with SUM(ARRAY_SIZE) not row count.
   - USAspending subawards → `FED_USASPENDING_SUBAWARDS_FULL`: 227 monthly
     chunks, ~20–30h. Resume: `python -u
     scripts/usaspending_subawards_full_load.py --run`.
   - Senate LDA backfill also still running (healthy, throttled).
4. **Spine rebuild from earlier tonight landed clean** (context for the recon):
   entities 35.95M → 37.25M, index rows 90.0M → 92.6M, STRONG families 5 → 2
   (docket collision dead), incremental catch-up unfrozen (2,122 watermarks
   re-pinned).

## BROKE

Nothing new broke. Two pre-existing open bugs restated above (spatial lat/lng,
uncommitted work). The direct Snowflake MCP connector rejected its token this
session — worked around via the repo's own key-pair connection
(`scripts/_snowflake_conn.py`); Chris may want to refresh that token.

## YOUR MOVE (Chris)

Read the ranked candidate table (it's short — 13 rows) and pick which ID
families are worth wiring. The recon deliberately registered nothing. Top 3 by
connective value: CAGE code, the contracts↔subawards award key (pairs with the
subawards load finishing overnight), and the NPPES legacy-ID block (the bridge
toward state Medicaid data).

## NEXT

1. The major sweep/refinement conversation (keyless giants FEMA 26M / HMDA 19M
   / CFPB 17M; dead domains; broken axes) — now with the recon list as input.
2. Commit the 5 loader scripts + connect-layer edits.
3. Re-run the DUNS orphan check (query still needs schema-name quoting fix).
4. Fix the 2 spatial source tables (EPA TRI, NTSB) malformed coordinates.
5. Wire the 5 verified-but-unregistered keys from prior sessions (MSHA
   controller, OFLC case, EIN+PN plan, NDC, CUSIP) — now joined by this
   session's 13 candidates for triage.
6. Point name+zip machinery at the keyless giants; repoint contracts staging
   to the R2 full table; known-truth tracer capstone.

**Cost note:** this recon was cheap — one catalog dump (751 rows) plus three
full-table verify scans (~16M rows total), well under $1 of warehouse compute.
Earlier tonight's rebuild ran on the quoted ~$12–18; exact credits still not
pulled from the meter. Overnight loads carry forward from the 08-27 log.
