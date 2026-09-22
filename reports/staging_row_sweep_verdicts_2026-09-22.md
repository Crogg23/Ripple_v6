# Staging row sweep, walked — 2026-09-22

Sweep: `scripts/sweep_staging_rows.py`, 1,402 views, landing rows vs view rows.
Raw output: `reports/staging_row_sweep_2026-09-22.tsv`.

| Verdict | Views |
|---|---|
| exact | 1,275 |
| view not built in DBT_CROGERS | 69 |
| ONE LOAD: key hides rows | 42 |
| view larger than landing | 9 |
| many loads: dedupe plausibly right | 4 |
| not comparable | 2 |
| landing table not found | 1 |

The 42 "hiding" views drop 4,651 rows between them. Every one was walked.

## What was checked
1. Per landing table: `count(*) - count(distinct hash(<business columns>))`. If it equals the gap, the dropped rows are byte-identical copies.
2. For the rest: the compiled view SQL with `_row_num = 1` flipped to `> 1`, or the `qualify ... = 1` flipped to `> 1`, so the dropped rows themselves print.
3. Inside each colliding key group: which columns differ.

## Bucket A — exact duplicate rows, 13 views, 1,290 rows. Not hiding.
CMS opt-out 108, NPDES SE violations 33, LEIE 26, TAGGS 9, NARA WRA 23, USASpending contracts orgs 309, GNIS citations 6, BORME 10, GR datagov 12, GR GEMI 33, WB IDS 2, UK sanctions 652, FARA 444 of 445.

## Bucket B — header, trailer and blank-ID rows, 20 views, 27 rows. Not hiding.
EIA860 x4 (`plant_code is not null`), EIA861 x9 (`UNNAMED_0` must be a four-digit year), Purple Book 5, HRSA UDS 1, HUD firm commitments 7 of 8, IHS facilities 4, Retraction Watch 219 of 220 blank RECORD_ID, CFPB 3 null complaint_id, OFAC 1 trailer row, OSHA 300A 3 malformed on purpose.

## Bucket C — FEC PAC summary, 2,686 rows. Not hiding, proven.
Key is (cmte_id, cvg_end_dt). All 2,686 dropped rows have a blank coverage end date. Across the 1,957 groups, the 21 financial columns never differ inside a group and receipts are blank in every group. Only committee name/type/designation vary, in 1,235 groups. Stubs.

## Bucket D — real rows hidden by a key that was too narrow, 4 views, 21 rows. FIXED in code.
| View | Old key | What differed | New key |
|---|---|---|---|
| ICE detention facilities | facility_name | AOR, city, state | + city, state, aor |
| SEC EDGAR filings | accession_number | CIK, entity, EIN | + cik |
| Federal Register documents | document_number | publication_date, citation | + publication_date |
| Revolving Door positions | position_key | industry_sector, sectors | + industry_sector |

Files edited, each with a KEY WIDENED note at the top:
- models/staging/fed_ice_detention_facility_list/stg_fed_ice_detention_facility_list__facility.sql
- models/staging/fed_us_sec_edgar/stg_fed_us_sec_edgar__edgar_filings.sql
- models/staging/fed_federal_register_documents/stg_fed_federal_register_documents__federal_register_documents.sql
- models/staging/fed_revolvingdoor_project/stg_fed_revolvingdoor_project__personnel_positions.sql

Not yet rebuilt in the warehouse: `dbt run` is gated. scripts/price_it.py --like on the EDGAR view's create statement: zero runs in 90 days. No real number for this; a view create is metadata only.

## Left as is
- IE CRO 4: 3 identical, 1 differs only in financial year end; newest kept.
- FARA 1: same full-row hash, different DATE_STAMPED. One row, not chased.
- FCA settlements 7: dropped rows are scraper junk ("Fraud Section Practice Areas", "Error fetching"). The source itself is thin: 19 landed rows.
