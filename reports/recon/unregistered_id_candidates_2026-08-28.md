# Recon: Unregistered ID Columns in COLUMN_CATALOG — 2026-08-28

Mission: find every column in LIBRARY_META.REGISTRY.COLUMN_CATALOG that looks like a
real-world ID but isn't one of the 24 registered STEEL key families. Recon only — nothing
registered, no code, connect layer untouched.

## Scope facts (verified this session)

- COLUMN_CATALOG holds **751 columns total**, covering roughly 15 tables (the pack tables:
  NPPES, Part D prescribers, USAspending contracts, FEC individual contributions, Senate LDA
  filings, LEIE, Senate stock watcher, congress committee membership, and the politics marts).
  It is NOT a warehouse-wide catalog — the "appears in 2+ tables" test could only be run
  inside this slice; warehouse-wide spread estimates below are inferred and marked.
- **Step 1 of the packet came back empty**: there are zero rows with DETECTED_KEY populated
  and KEY_TIER null. Every profiler-detected key already carries a tier
  (STEEL/STRONG/GEO/PROBABILISTIC). All candidates below came from the name-pattern +
  value-shape scan of the 626 undetected columns.
- Scan stats: 626 undetected columns → 291 name/shape hits → 277 grouped candidates →
  judged by hand down to the list below. Rejects were category codes, dates, dollar amounts,
  claim counts, phone numbers, and free text.
- Profiler blind spot confirmed: the catalog's sample of NPPES appears to read early rows
  only, so all 200 "other provider identifier" columns and license slots 4+ show empty
  samples. Full-table checks (below) show they are heavily populated.

## Ranked candidates

Rank is by connective value: how many tables/sources the ID could realistically bridge.

| # | Column(s) | Table(s) in catalog | Sample values | Why it looks like an ID | Likely real-world system | Verified this session |
|---|-----------|--------------------|---------------|------------------------|--------------------------|----------------------|
| 1 | CAGE_CODE | LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS | 0ZPX2, 3M1W9, 61930, 1P3C5 | Fixed 5-char alphanumeric, dense | **CAGE code** (DLA Commercial and Government Entity ID) — the defense-contractor identity axis; also lives in SAM/FPDS/DoD data if/when loaded | 6,324,763 of 6,325,622 rows filled; 92,530 distinct |
| 2 | CONTRACT_AWARD_UNIQUE_KEY | FED_USASPENDING_CONTRACTS | CONT_AWD_47QSSC25P03E4_4732_… | Structured composite (PIID + agency), near-unique | **USAspending award key** — the join between prime contracts and the 227-chunk subawards table currently loading | catalog profile only (9,976/10,000 distinct) |
| 3 | OTHER_PROVIDER_IDENTIFIER_1..50 (+ TYPE/ISSUER/STATE cols, 200 columns) | FED_CMS_NPPES | 110111738 (type 01 = other/Medicare-adjacent, issuer "RAILROAD MEDICARE"), 3054403 (type 05 = **Medicaid**) | Numbered ID slots with type+issuer+state qualifiers | **Legacy provider IDs: state Medicaid IDs, Medicare-era IDs, UPINs** — the bridge from NPI-world to state Medicaid/payer data | Slot 1 alone: 1,559,317 filled, 1,343,026 distinct (catalog showed EMPTY — blind spot) |
| 4 | FEC_ID; CAND_IDS; CMTE_IDS; MEMBER_KEY | POLITICS__MEMBER_FEC_ID; MEMBER_MONEY_RAISED; MEMBER_INDIV_DONATIONS; MEMBER_FEC_ID + MEMBER_SPINE | H0MA04192; ["C00867218"]; A000002 | Exact formats of already-registered families under other names (FEC candidate ID, FEC committee ID, Bioguide) — CAND_IDS/CMTE_IDS are JSON arrays | **Near-misses of FEC_CAND_ID / FEC_CMTE_ID / BIOGUIDE** — cheapest wins on the list, the decoder already exists | catalog samples (formats unambiguous) |
| 5 | TICKER | FED_SENATE_STOCK_WATCHER | PAGS, BBY, UPS, XOM | 1–5 uppercase letters, 1,029 distinct | **Stock ticker** — the only bridge from the name-only senate trades source to CIK-keyed SEC data (ticker→CIK crosswalks are public) | catalog profile |
| 6 | PROVIDER_LICENSE_NUMBER_1..15 + STATE_CODE_1..15 | FED_CMS_NPPES | 07000410A, MA 69133, ME70191 + state cols | ID + issuing-state pairs; formats vary by state board | **State professional license numbers** — joinable to state licensing/discipline boards and exclusion lists, but only as (state, license) composite; formats are messy | Slot 1: 5,777,222 filled, 3,909,402 distinct |
| 7 | UPIN | FED_HHS_OIG_LEIE | T33240, F63970, A64295 | Fixed 6-char letter+5-digit | **Medicare UPIN** (retired 2007) — bridges old exclusion records to NPPES's UPIN slots in the other-identifier block (#3) | catalog samples; 474 distinct in profile |
| 8 | CLIENT_ID; REGISTRANT_ID | FED_SENATE_LDA_FILINGS | 203786; 400275281 | Stable numeric IDs from the Senate lobbying system | **Senate LDA registrant/client IDs** — stable across filings/years within the LDA system; the spine of a lobbying axis (registrant↔client↔filing) | catalog profile (9,245 and 2,057 distinct) |
| 9 | NID | POLITICS__FJC_JUDGE + FJC_APPOINTMENT (2 tables) | 1376976, 1377006 | 7-digit, consistent, 2 tables | **Federal Judicial Center judge ID** — the FJC biographical directory key; bridges judges↔appointments and out to courts | catalog (2-table match inside catalog) |
| 10 | COMMITTEE_CODE | FED_CONGRESS_COMMITTEE_MEMBERSHIP | SSAF14, SSAS20, SSFR07 | Chamber+committee+subcommittee code | **Congressional committee codes** (unitedstates/Stewart convention) — joins membership↔bill referrals | catalog samples |
| 11 | BILL_NUMBER (+ LAW_NUMBER) | POLITICS__BILLS + BILL_COSPONSORS (2 tables) | 1671; 118-219 | Bill number (composite with congress+type); public-law number | **Congress.gov bill / public-law numbering** — internal politics glue, needs congress+bill_type to be unique | catalog (2-table match) |
| 12 | JUSTICE_CODE | POLITICS__JUDGE_IDEOLOGY_SCOTUS | 106, 107, 94 | Small ints but a published external code set | **Supreme Court Database (Spaeth) justice codes** | catalog samples |
| 13 | LINKAGE_ID; SUB_ID; IMAGE_NUM | FEC tables | 247126; 4083020242017155126 | FEC bulk-file record/linkage IDs | **FEC-internal record keys** — join FEC files to each other (linkage id ties candidates↔committees); not identities of real-world entities | catalog profile |

## Rejected (so nobody re-litigates them)

- AUTHORIZED_OFFICIAL_TELEPHONE_NUMBER — phone; probabilistic-match material at best, not a key family.
- HEALTHCARE_PROVIDER_TAXONOMY_CODE_* — classification code (what kind of provider), not an identity.
- TRAN_ID (FEC) — filer-assigned, mixed formats (4187324, IA7971), not stable.
- CAST_CODE, ENTITY_TYPE_CODE, state codes, party codes — category codes.
- All date/amount/count columns the shape-scan caught (DOB, EXCLDATE, coverage dates, drug costs, claim counts).

## Cross-reference against the 24 registered families

No candidate above is an exact duplicate of a registered family. Row 4 is deliberately kept
as the near-miss bucket (same ID systems, unregistered columns). UPIN, CAGE, Medicaid IDs,
tickers, LDA IDs, and FJC NIDs are all ID systems with **no registered family at all**.
