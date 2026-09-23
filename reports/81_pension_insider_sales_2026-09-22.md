# 81 — insider stock moves before a pension collapsed onto PBGC

Run 2026-09-22, rerun the same day after a skeptic pass.
Query in `scripts/probe_81_pension_insider_sales.py`.

## The chain, four hops, every one a hard identifier

| from | key | to |
|---|---|---|
| PBGC trusteed plans | EIN | SEC DERA submissions |
| SEC DERA submissions | CIK | Form 4 submissions |
| Form 4 submissions | ACCESSION_NUMBER | non-derivative transactions |
| Form 4 submissions | ACCESSION_NUMBER | derivative transactions |
| Form 4 submissions | ACCESSION_NUMBER | reporting owners |

## The bottleneck, now proved rather than asserted

The first run claimed 6 bridged companies without checking key width.
A skeptic pass called that unproved. It was checked and it holds.

| side | EIN width | rows |
|---|---|---|
| PBGC | 4 digits | 1 |
| PBGC | 5 digits | 36 |
| PBGC | 6 digits | 6 |
| PBGC | 8 digits | 531 |
| PBGC | 9 digits | 4,602 |
| DERA | 9 digits | 59,147 |
| DERA | placeholder `000000000` | 14,140 |

Both sides are now stripped to digits and left-padded to 9.
DERA placeholder zeros are dropped before the join.

| measure | value |
|---|---|
| PBGC distinct EINs | 4,431 |
| matching a DERA filer EIN after padding | 6 |
| of those, terminated 2016 or later | 2 |

Six, with the width bug fixed. The bottleneck is real, not a bug.
A company whose pension collapses is usually bankrupt or private,
so it files nothing. DERA holds only 2024Q1 through 2026Q1.

## The six that bridged

| sponsor | SEC filer | CIK | terminated | participants |
|---|---|---|---|---|
| RITE AID CORPORATION | RITE AID CORP | 84129 | 2025-07-31 | 6,106 |
| TUPPERWARE BRANDS CORPORATION | TUPPERWARE BRANDS CORP | 1008654 | 2024-09-30 | 584 |
| DELTA AIR LINES INC. | DELTA AIR LINES, INC. | 27904 | 2006-09-02 | 13,237 |
| COPPERWELD CORPORATION | INTERCONTINENTAL HOTELS GROUP PLC | 858446 | 2003-09-30 | 1,680 |
| INFINITE GROUP | INFINITE GROUP INC | 884650 | 2001-11-30 | 77 |
| DUTCH BOY PAINTS | NL INDUSTRIES INC | 72162 | 1980-12-14 | 17 |

COPPERWELD mapping to INTERCONTINENTAL HOTELS is an EIN reuse or a
registry error. It returned no Form 4 rows.

Delta and Dutch Boy terminated in 2006 and 1980, before Form 4 coverage
starts in 2016. Their rows are excluded by the date test, correctly.

## What the query now looks at

The first run read only code S, open-market sales, on common stock.
That was too narrow to carry the sentence it was used for.

| code | meaning |
|---|---|
| S | open-market sale |
| D | disposition back to the issuer |
| F | shares withheld to pay tax |
| M | option exercise |

Both the common-stock and the derivative tables are read.
Form types `4` and `4/A` are both read, so late amendments land.
Reporting owners are collapsed per filing, so a multi-owner filing
cannot double the dollars. Zero multi-owner filings appear here.

## The answer

402 rows, 379 distinct transactions.

### Voluntary cash-out, codes S and D

| sponsor | moves | dollars | closest to termination | people |
|---|---|---|---|---|
| TUPPERWARE BRANDS CORPORATION | 166 | $25,970,299 | 202 days | 18 |
| RITE AID CORPORATION | 7 | $706,782 | 1,463 days | 6 |

### Mechanical, codes F and M

| sponsor | moves | dollars | closest to termination | people |
|---|---|---|---|---|
| TUPPERWARE BRANDS CORPORATION | 103 | $11,384,487 | 129 days | 28 |
| RITE AID CORPORATION | 126 | $4,855,486 | 735 days | 21 |

### The six closest moves of any kind

| sponsor | person | code | date | dollars | days out |
|---|---|---|---|---|---|
| TUPPERWARE | Matute Mariela Irene | F | 2024-05-24 | $6,871 | 129 |
| TUPPERWARE | SHEEHAN KAREN M | D | 2024-03-12 | $596 | 202 |
| TUPPERWARE | SHEEHAN KAREN M | D | 2024-02-25 | $1,114 | 218 |
| TUPPERWARE | LEZAMA HECTOR | D | 2023-11-04 | $51,245 | 331 |
| TUPPERWARE | Van Ingen Jim | F | 2023-07-11 | $1,375 | 447 |
| TUPPERWARE | Matute Mariela Irene | F | 2023-05-24 | $3,029 | 495 |

**No large voluntary cash-out sits near either collapse.**

The nearest voluntary disposals are $596 and $1,114, both 200 days out.
The nearest move of any kind is $6,871 of tax withholding, 129 days out.
The big money is years earlier. Tupperware's chairman took $9.4m in
July 2016, eight years before the plan died.

The plain reason: by PBGC handover the stock is already near worthless
and trading windows are shut. The selling happens while the price holds.

## Limits of this answer, stated

- Rite Aid terminated 2025-07-31. Form 4 data loaded ends 2025-03-31.
  The final four months before that collapse are not held.
- The population is two companies. This is a shape, not a pattern.
- Private sales, buyback tenders, and sales at companies that stopped
  filing are invisible. Bankruptcy is the usual road to a PBGC handover,
  so the method is blind to most of its own subject.

## Data traps found in this run

- `ISSUER_CIK` on the Form 4 tables is zero-padded text. DERA `CIK` is bare.
  Comparing as strings returns zero rows and reads like a real miss.
- PBGC `EIN` drops leading zeros. 531 rows are 8 digits, 43 are shorter.
  DERA pads to 9 and writes `000000000` for 14,140 rows where it has none.
- `TRANSACTION_DATE` on the non-derivative table holds junk. The minimum
  reads year 22, the maximum reads 2047. Bound every window.
- The derivative table renames every column. `TRANS_DATE`, `TRANS_CODE`,
  `TRANS_TOTAL_VALUE`, not the non-derivative spellings.

## Files

- `outputs/81_insider_sales_before_pension_termination.csv` — 402 rows
