# Dead ends, scope C build: FDIC enforcement orders (2026-09-07)

Docket 118 died on a 14-row table that was the fdic.gov navigation menu. The real thing is
10,838 orders back to 1975. It is landed, marted, tested, and counted.
Python door only; the chat plug-in was not used. The old 14-row table was not touched.

## Where the data came from

orders.fdic.gov is a Salesforce site. What was tried, in order:

| path | result |
|---|---|
| plain GET on `orders.fdic.gov/s/` | JS shell, "CSS Error", no data |
| FDIC monthly press releases (`fdic.gov/news/press-releases/2026/fdic-publishes-july-enforcement-actions`) | one sentence and a link back to orders.fdic.gov, no table |
| BankFind API (`api.fdic.gov`) | no enforcement endpoint |
| data.gov | nothing |
| the site's Aura endpoint, found by watching the search form in Playwright | **works with a plain POST, no browser, no cookie, no token** |

The endpoint is `POST https://orders.fdic.gov/s/sfsites/aura`. Two Apex actions do the job:
`EDOSSearchFormController.countResults` (an integer) and `EDOSSearchFormController.buildWrapperList`
(a page of orders as JSON, with the banks and respondents nested). The site's own "Download All"
button is a third action (`convertCSV`) that returns the same 10,838 rows as a CSV with the child
lists squashed into semicolon strings; the JSON is cleaner, so that is what lands.

Salesforce SOQL OFFSET stops at 2,000. The loader pulls one year at a time (busiest year is 2010 at
902) and would split a year into months if it ever passed the cap.

## What was built

| piece | path |
|---|---|
| loader | `scripts/fdic_enforcement_load.py` (dry run by default, `--run` lands, resumes by year from `logs/fdic_enforcement_orders_checkpoint.json` and from what the table already holds) |
| landing | `LIBRARY_RAW.LANDING.FED_FDIC_ENFORCEMENT_ORDERS`, 23 columns as text + `INGESTED_AT` + `_SOURCE_RUN_ID` |
| staging | `ripple_dbt/models/staging/fed_fdic_enforcement_orders/stg_fed_fdic_enforcement_orders__orders.sql` + `schema.yml` (source declared there) |
| mart | `LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS` from `models/marts/justice/justice__fed_fdic_enforcement_orders.sql` |
| tests | `models/marts/justice/schema_fed_fdic_enforcement_orders.yml` |

## Commands run, in order

```
python scripts/fdic_enforcement_load.py            # dry run: counts by year, 10,838 total, first 20 rows
python scripts/fdic_enforcement_load.py --run      # landed 10,838; quality gate DQ OK, density 0.2083
cd library-onboarding/ripple_dbt
dbt run  -s stg_fed_fdic_enforcement_orders__orders justice__fed_fdic_enforcement_orders   # 2 success
dbt test -s stg_fed_fdic_enforcement_orders__orders justice__fed_fdic_enforcement_orders   # 11 tests: 6 pass, 5 warn, 0 fail
```

No hook refused anything.

The first `dbt test` failed 4 tests: `order_type` null on 23 rows, `document_url` null on 24. Checked:
the 23 are the undated orders (Salesforce records with only a docket, a bank and respondents, no
title, no type, no PDF), the 24th is one 2012 CMP order, `FDIC-12-0147k`, with no document. Source
gaps, so both tests were set to warn with the reason written in the yml.

## The numbers (Python door, `connect/db.py`)

**Landing**

| check | result |
|---|---|
| rows | 10,838 (= `countResults` with no date filter on the site) |
| distinct ORDER_ID | 10,838, so that is the grain |
| distinct DOCKET_NUMBER | 8,302: one docket carries the order, the modification and the termination as separate rows; 17 rows have no docket |
| ORDER_ISSUED_DATE | 1975-06-11 to 2026-07-31, all 10 chars; 23 null |
| CERT_NUMBER | 10,789 non-blank; 183 read `N/A`; 10,606 numeric; 4,243 distinct |
| BANK_COUNT | 1 bank on 10,600; 0 on 43; 2 to 23 on 195 (first bank fills the main columns, all of them sit in BANKS_ALL) |
| one run | `_SOURCE_RUN_ID` one value, `INGESTED_AT` 2026-09-07 |

**Years**

1975 (1), 1979 (1), 1980 (1), then every year through 2026. The 1980s are thin: 14 in 1985, 129 in 1989.
1990 is the first full year at 293. Peak is 2010 at 902, the crisis years 2009-2012 hold 2,943 of the
10,838. 2026 has 86 through July.

**Orders by type, top 10**

| order type | orders |
|---|---|
| Cease and Desist / Consent Orders | 4,833 |
| Assessment of Civil Money Penalty | 2,228 |
| Removal/Prohibition Order | 1,958 |
| Voluntary Termination of Deposit Insurance | 443 |
| Involuntary Termination of Deposit Insurance | 294 |
| Prompt Corrective Action | 284 |
| Assessment of Civil Money Penalty;Removal/Prohibition Order | 202 |
| Section 19 Application | 106 |
| Cross Guaranty | 72 |
| Temporary Order to Cease and Desist | 61 |

`ORDER_TYPE` is a semicolon list on the combined rows. Equality on the whole string undercounts each
type; use LIKE or split.

**Cert attach to FINANCE__FED_FDIC_BANK_DATA** (27,836 institutions, CERT unique, joined on
`try_to_number` both sides)

| measure | result |
|---|---|
| orders attached | 10,565 of 10,838, **97.5%** |
| among orders with a numeric cert | 10,565 of 10,606, 99.6% |
| misses | 183 `N/A` (bank redacted on adjudicated decisions), 49 blank (Section 19 letters about a person), 41 numeric certs the directory does not carry |
| by decade | 1980s 118 of 217; 1990s 3,117 of 3,144; 2000s 2,428 of 2,450; 2010s 4,167 of 4,236; 2020s 712 of 766 |

Most-ordered banks: Truist Bank cert 9846 (68 orders, mostly prohibition orders against individual
employees), Citizens Bank of Pennsylvania 57282 (26), Independence Bank 57379 (24), Bank of Louisiana
17878 (22), United Commercial Bank 32469 (21).

CMP dollars: `CMP_AMOUNT_TOTAL` sums to $284.1M on plain CMP orders and $196.3M on the
CMP + C&D + restitution combined rows. It is the sum over respondents on the order, landed as text.

## What this does and does not fix for docket 118

The enforcement leg is fixed: one row per order, cert on 97.5%, back to 1975.

The SBA leg is still name-only. `ECONOMICS__FED_SBA_LOANS` carries `LENDER_NAME` and `LENDER_STATE`
and no cert or RSSD. The path to the question is SBA lender name -> FDIC bank directory (name + state)
-> cert -> this table. That name match has not been built or measured; the trap file already says
generic bank names collide and "National Association" names do not. So the question moves from
"a piece is missing" to "part done."

## Traps found today

- 23 orders on orders.fdic.gov have no issued date, no title, no type and no PDF link; they are real
  records (docket, bank, respondents, CMP) that the site's date search never returns. The loader
  fetches them with `Order_Issued_Date__c = null` as its own bucket.
- `DOCKET_NUMBER` is not a key: 8,302 distinct on 10,838 rows, and some hold two dockets in one
  string. The key is the Salesforce `ORDER_ID`.
- `CERT_NUMBER` reads `N/A` as a string on 183 rows; `is not null` overcounts. Use `try_to_number`.
- `ORDER_TYPE` is a semicolon list on the combined rows (202 on the CMP + prohibition combination alone).

## Skeptic pass

Fresh-context reviewer re-hit the live endpoint (countResults 10,838, undated 23, 2010 = 902) and
re-ran the join and `dbt test`. Every number reproduced. Four notes, three fixed the same hour:

| note | what was done |
|---|---|
| `fetch_undated` never compared fetched to counted | warning added |
| a year of exactly 2,000 orders would raise instead of splitting (`<=` vs `>=`) | split now fires at `>= 2000` |
| `File_URL__c` read off the response but not in the requested field list | tried adding it to `FIELDS`: the endpoint then returns zero rows, no error. Reverted. The loader now raises if a year lands with no URL on any row, so the failure is loud instead of a warn-severity test. |
| **195 orders name 2 to 23 banks; 376 second-and-later bank links live only in `BANKS_ALL`** and the cert join sees the first bank only (the 1988 MBANK collapse is 23 banks under one cert) | not fixed here. A bank-level question needs a bridge model that splits `BANKS_ALL` into one row per order-bank. Parked. |
