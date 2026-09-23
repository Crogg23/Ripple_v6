# Catalog audit verdict — 2026-09-23

Chris: "I am currently under the impression my data warehouse is 95/100 grade. Im skeptical."

**Verdict: the data grade holds at 100. The map grade is 65.**
The data grade counts problems fixed inside the tables. The map grade asks whether the
catalog tells the truth about those tables. Nobody had graded the map before today.

Full machine output: `audit/catalog_audit_2026-09-23.md`, plus three TSVs beside it.
Script: `scripts/audit_catalog.py` fetch / links / analyze. Read-only.
Cost: 996 queries, 1,532 seconds on an X-Small warehouse, about 0.43 credits.

## The map grade, five parts

```
part                     passed      of     score   what was checked
key labels true             534     627     85.2    2,000 sampled values per column vs the key's shape
hard ID links work          226     244     92.6    full distinct ID lists, table A vs table B
tables with a summary       319     659     48.4    table comment, dbt description, or registry one-liner
columns described           361  20,868      1.7    dbt column description or registry gloss
inventory clean             651     659     98.8    backups, duplicates, objects that will not open
MAP, plain average                           65.3

83 labeled key columns were empty in the sample and are not graded either way.
```

The average is a proposal. Chris picks the weights.

## What each part found, walked

### 1. Key labels: the tagger reads one word and ignores the rest
- Checked: every column the platform tagger labels, 2,000 sampled values each, against the
  key's real shape. NPI 10 digits with a check digit, DEA two letters and a check digit,
  FIPS by width, and so on.
- Hit means the label is true. Miss means a join on it matches nothing or matches wrong.
- Found: `MULTIPLE_NPI_FLAG` holds Y/N and is labeled NPI. `NPI_DEACTIVATION_DATE` holds dates.
  `EIN_ZIP5` holds zips, labeled EIN. `CCN_FACILITY_TYPE`, `ISSUER_CIK_NONE`, `NPI_IS_REAL`,
  `PRIOR_DEA_REPORTS` the same. One word fires the label; FLAG, DATE, TYPE, NAME beside it are ignored.
- FIPS lumps three sizes: 55 state columns, 43 county, 1 tract, 1 block group. 10 more hold
  bare 3-digit county parts like "075", which repeat in every state and join to nothing alone.
- ZIP is applied to Canadian, Chinese and EU postcodes: GLEIF, OSFI, Elections Canada, FDA
  establishments, EU sanctions.
- NAME: of 1,450 name-labeled columns, 170 hold places, 138 numbers, 115 one-word codes,
  75 things like drug names and race categories. 445 hold organizations, 47 people,
  124 parts of people's names, and 223 are names where org vs person can't be told.
  All four of those count as a usable name link, graded PROBABILISTIC.

### 2. Links: the hard IDs mostly work
- Checked: for 319 hard-ID columns, every distinct cleaned value, pulled in full.
  A link works when 5% of A's IDs also appear in B, and at least 50 IDs or all of A if smaller.
  Backups are left out, so a table matching its own copy does not count.
- 226 of 244 tables with a hard ID have at least one working partner.
- Generous measure: one working partner is enough.
- Dead ends: DEA numbers live only in ARCOS, so no partner. 13 other tables likewise.
- 4 tables have partners that match nothing: BJS data, SEC insider owners, PBGC plans at 3.1%,
  NOAA ship tracks.

### 3 and 4. Words: most of the map is blank
- Checked: Snowflake table comments, dbt YAML descriptions, the registry one-liners and glosses.
- 48% of tables have any summary. 1.7% of columns have any description.
- Why it bites, one example: the capped contracts table, 20,000,000 rows, still sits in
  ECONOMICS beside the full 93M reload. dbt's description says in capitals "CAPPED, use r2."
  Snowflake shows no comment. Anyone browsing sees a normal contracts table.

### 5. Inventory: small, but the catalog lied about it
- The 22 "empty tables" are views holding 473,954,380 rows, including 128M grant records
  and 101M 13F holdings. The catalog showed them as zero.
- 7 `__PREV_` backups in the catalog, one of them 84,172,112 FEC contribution rows.
- One exact duplicate: PECOS provider enrollment appears in HEALTH and again in IMMIGRATION.

## Data problems surfaced on the way, outside the map

- **FDIC bank data LEI:** all 2,252 filled values are 16 characters. A real LEI is 20.
  FDIC publishes it cut short; the model's code already said so and says LEFT(gleif.lei, 16)
  matches 2,224 of 2,252. Not our bug: a missing-words problem, now a column comment.
- **ATF gun dealer zips:** at least 3,329 are 3, 4 or 8 digits, from the top five lengths.
  The leading zeros are gone, so Puerto Rico's 00602 is stored as "602".
- **SAM exclusions NPI:** 40.7% of sampled values fit. The rest include "0000000000" placeholders.

## Untagged keys found by value

- SEC accession numbers in 25 columns. The platform tagger has no accession key.
- FEC committee IDs in `CAND_PCC`, `SPE_ID`, and `OTHER_ID` on individual contributions.
- GLEIF relationship node IDs are LEIs, 3 columns.
- NDC drug codes, 7 columns.

## Skeptic pass, fresh context

AGREE on the grade. DISAGREE on three examples, all fixed above:
- "SEC EDGAR matches nothing" was the 50-ID floor failing tables with under 50 IDs that match 100%.
- Three tables re-sampled after the ID pull had never been pulled. Re-pulled.
- FIPS county parts are 10, not 13; the name breakdown was folded into one number.
Also from the skeptic: 554 of the 751 registry glosses point at tables no longer in the catalog.
Samples are the first 2,000 stored rows, not random.

## Proposed fixes, numbered, for Chris to approve or reject

1. Retire the regex catalog. Build the catalog from the platform tagger only.
2. Tagger rule: a key word next to FLAG, DATE, TYPE, NAME, IS, NONE, EXT, REPORTS,
   TICKER or LAST gets no key. One exclude list, re-run, re-audit.
3. Split FIPS into state, county and tract by value width. Bare 3-digit county parts get no key.
4. ZIP only on US tables. International postcodes get a POSTCODE label, no join.
5. NAME only where values are organizations or people. Places move to Where, drugs to What.
6. Add keys: SEC ACCESSION, the three FEC committee columns, the GLEIF node LEIs, NDC.
7. Catalog reads table type and counts views. Backups leave the catalog.
8. Drop the 7 backups and one PECOS copy: needs `greenlight destroy` per list, reader check first.
9. Push existing descriptions into Snowflake comments. Chris picks the route: persist_docs
   on the next full mart build, or COMMENT statements from the registry, no rebuild.
10. Data fixes, separate from the map: FDIC LEI truncation, ATF zip padding.
11. Add a MAP section to `score_warehouse.py`, one query per part, so the grade is a command.

Writes needing a go: the audit table `LIBRARY_META.AUDIT.CATALOG_AUDIT`, and fixes 8, 9, 10.

## Status after "Fix all", 2026-09-23

| # | Fix | State | Proof |
|---|---|---|---|
| 1 | Catalog from the platform tagger | done | `python scripts/audit_catalog.py catalog` writes outputs/catalog/catalog.json + er.json; Patch Panel renders headless, 0 errors |
| 2 | Describing words kill a hard key | done | connect/keys.py DESCRIPTOR_TOKENS; tests/test_catalog_keys.py; 48 false key columns off, LAST_RPT_SPONS_EIN kept after skeptic |
| 3 | FIPS split by width | done | STATE_FIPS / COUNTY_FIPS / TRACT_FIPS; bare county parts, incl. zero-stripped 1-2 digit ones, get no key |
| 4 | ZIP only where values are US zips | done | failing columns lose the key; empty-in-sample place labels dropped |
| 5 | NAME only on orgs and people | done | places and codes off; drug and product names go to What |
| 6 | New keys | done, catalog only | CATALOG_KEYS: SEC accession 22 cols, FEC committee 3, GLEIF LEI 3, Bioguide member keys 3, FDA 510k/PMA 4; THING_TOKENS: NDC, HCPCS, CFDA, CAS, ICD, NAICS, SIC. Engine untouched: promoting them into TABLE_COLUMN_KEYS forces `connect apply-config` |
| 7 | Catalog reads table type, counts views, drops backups | done | 652 tables, 7 backups out, 22 views with COUNT(*) |
| 8 | Remove 7 backups + PECOS copy | done, greenlight destroy | 8 of 8 removed; 0 readers and PECOS twin re-proved at run time; DDL in outputs/catalog_dropped_ddl_2026-09-23.sql; UNDROP works until 24h after |
| 9 | Descriptions into Snowflake | done | 502 of 502; persist_docs on; ATF comment written by its rebuild |
| 10 | ATF zips, FDIC LEI | done, greenlight rebuild | ATF rebuilt, 4 of 4 pass incl. assert_atf_zip_width; live: 70,114 five-digit + 7,400 nine-digit, PR reads 00602. FDIC is source-side, now a column comment |
| 11 | MAP in the ruler | done | score_warehouse.py prints MAP after DATA, never added |

MAP after the fixes: 66.9, inventory 100% clean. Audit findings loaded to LIBRARY_META.AUDIT.CATALOG_AUDIT, 1,144 rows.
Not touched: 4 TIMELINE __PREV_ backup tables, outside the catalog and never on the list.
Earlier note, 66.5: Unchanged on purpose: comments made existing words visible,
they did not add words. The gap is 20,506 columns with no description anywhere.

Skeptic, second pass: AGREE on 4, 5, 6. DISAGREE on three, all fixed: a real EIN column
killed by 'last', zero-stripped county parts read as states, empty columns keeping place
and name labels. Open, reported not fixed: the engine's config pin does not hash
detect_key, so the next discover reslice drops the 48 false key columns from KEYSET_LIVE
without a drift warning.
