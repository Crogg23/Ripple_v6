# Audit closeout: the five open items from 2026-09-06

Run 2026-09-07 through the Python door as ACCOUNTADMIN. Read-only.
Nothing was written, dropped, renamed or rebuilt.

Connection used:

```python
import sys; sys.path.insert(0, "library-onboarding")
from dotenv import load_dotenv; load_dotenv("library-onboarding/.env", override=True)
import snow; conn = snow.connect()
```

---

## 1. Claims that did NOT reproduce

| # | claim | claimed | actual |
|---|---|---|---|
| 1 | LDA crawl "still growing, mid-2011" | in progress | stopped; positions table holds 2011 only |
| 2 | door built "two" non-transient marts | 2 | 14 live marts + 1 rollback copy |
| 3 | "648 of 678 sibling marts transient" | 678 total | 691 total; 648/43 split is right |
| 4 | roster avg congresses per member | 3.49 | 3.619 |
| 5 | House rows with an exact dollar figure | 68 | 98, and all 98 lost their cents |
| 6 | traps appended 2026-09-06 | 22 | 38 entries carry that date |

Everything else in section 4 reproduced.

### And this report's own misses, caught by the skeptic pass

| claim | first written | corrected to |
|---|---|---|
| House rows with chopped asset and wrong owner | 54 | **107** |
| trap entries that held | 24 of 26 | **21 of 24 assessed. 3 never checked** |
| non-transient marts framed as a door novelty | 14 of 691 | **43 non-transient. 28 predate the door** |
| dangling upper-bound amounts | not reported | **72** |
| the dead-column cast | one model file | **a generator defect. 2 more enabled models** |
| 20-filing count check | stated as settled | **0.8% of corpus. Widened to 20.8%** |
| IRS 527 sample | first 6M lines | **all 18,300,801 lines** |

---

## 2. Parser defects found

### BLOCKER — `OWNER_TOKEN` has no word boundary

`scripts/house_ptr_load.py`

```python
OWNER_TOKEN = re.compile(r"SP|DC|JT")
```

`TRADE` uses `\b(?:SP|DC|JT)\b`. This one does not. So a brand name that
starts with SP is split into an owner code and a chopped asset.

Verified against three live PDFs. Filing 20019942 line 1, filing 20018692
lines 12 and 13. The PDF reads:

```
...Date notificationDateamount cap. gains >$200?SPDR S&P 500 (SPY) [ST] P 12/02/2021 ...
```

There is no owner code in that filing. The row landed as:

```
OWNER              = SP
ASSET_DESCRIPTION  = DR S&P 500 (SPY) [ST]
```

Two errors in one row: the asset is chopped, and a self-owned trade is
recorded as a spouse trade.

**107 rows in the confirmed class**, in six shapes. The first four were found
on the first pass. The last two were found by the skeptic pass and reproduced
here.

```
SPDR   -> SP + "DR ..."      39
SPY    -> SP + "Y ..."        9
SPX    -> SP + "X ..."        4
CRISPR -> SP + "R ..."        2
UNSP   -> SP + "/ADR ..."    47   <- whole issuer name deleted
BDC    -> DC + ", Inc. ..."   6   <- whole issuer name deleted
                            ---
                            107
```

The two late classes are worse than SPDR. SPDR at least leaves a readable
`DR S&P 500`. These leave nothing of the company at all.

Filing 20023404, PDF text:

```
VOLVO AB UNSP/ADR (VLVLY) [ST]S 07/10/202308/04/2023$50,001 -
```

`OWNER_TOKEN` finds the `SP` inside **UNSP**. Landed asset: `/ADR (VLVLY) [ST]`.

Golub Capital, straight off `RAW_LINE`, no PDF needed:

```
Golub Capital BDC, Inc. (GBDC) [ST] S 01/20/202102/06/2021$15,001 -
```

`DC` found inside **BDC**. Landed asset: `, Inc. (GBDC) [ST]`.

Why the first pass stopped at 54: the 221-row field sweep reported "0 assets
starting mid-word" and that result was carried as if it generalised. It was
true of that sample only.

**The fix is NOT `\b`.** The House PDF glues a real owner code straight onto
the asset name with no space -- `SPAbbVie Inc. (AbbV)`, `JTBerkshire Hathaway`,
`SPCentinela VY uHS`. 3,073 of 6,242 locatable rows are that shape, so a
boundary breaks thousands. The next obvious candidate,
`(?:SP|DC|JT)(?=[A-Z][a-z]|[a-z]|\s|$)`, rejects 49 of 52 known-bad rows and
wrongly breaks 430 good ones -- "3M Company", "JP Morgan", "O'Reilly", "SS&C".

Smallest safe move: land `OWNER_RAW` beside `OWNER` so all 107 are recoverable
without reparsing every PDF.

### REAL -- 72 amounts kept a dangling upper bound

```
$15,001 -    41
$100,001 -   12
$50,001 -     9
$250,001 -    7
$1,001 -      2
$500,001 -    1
```

The House form offers only fixed ranges, so an open upper bound is a lost
value, never a filer's choice. The next-line rescue at
`scripts/house_ptr_load.py:258` fires only for the last trade on a line, and
only when the next line starts with a dollar sign.

### REAL — cents are truncated on every exact-dollar amount

`TRADE`'s amount group is `\$[\d,]+`, which stops at the decimal point.

98 rows carry a genuine single dollar figure rather than a range. All 98
lost their cents.

```
DOC 20033370  PDF: $224.00   landed: $224
DOC 20018000  PDF: $669.27   landed: $669
DOC 20018081  PDF: $474.06   landed: $474
```

### MINOR — TICKER picks the first parenthetical, not the ticker

```python
TICKER = re.compile(r"\((?:Ticker:?\s*)?([A-Za-z][A-Za-z0-9.\-]{0,6})\)", re.I)
```

Seven characters is wide enough to swallow a country or an asset name.

Filing 20019458 line 6, PDF text:

```
SPAnheuser-busch Inbev SASponsored AdR (belgium) (bud)[CS]P 08/09/2021 ...
```

`TICKER` landed `BELGIUM`. The real ticker `BUD` is in the second
parenthetical. Same class, warehouse-wide: `RIPPLE` 2, `BITCOIN` 2,
`SOLANA` 2, `CARDONA` 1.

### The count check PASSED, on 20.8% of the corpus

Independent marker: a PTR trade row is the only thing in the form carrying a
transaction date immediately followed by a notification date. Counted with
`\d{2}/\d{2}/\d{4}\s*\d{2}/\d{2}/\d{4}` -- not the loader's own regex.

The loader's `TRADE` needs `[PSE]` plus both dates plus an amount. This marker
needs only the two dates, so it is a strict superset: it can see a trade the
loader dropped for a missing type letter or a mangled amount.

**Round one, 20 random filings**, drawn with `order by hash(DOC_ID) limit 20`:

```
20020080 Welch      1    20033694 Biggs        5
20027916 Goldman    1    20018605 Brooks       1
20033756 Gottheimer 9    20023204 Larsen       1
20018690 Sessions   2    20029034 Bresnahan  114
20033661 Hill       4    20026736 Joyce        1
20033370 Evans      2    20021932 Burgess      1
20018001 Lowenthal  6    20019450 Peters       2
20018672 Sessions  15    20020892 Lowenthal    1
20034177 Keating    3    20018933 Green       11
                         20034416 Dingell      2
                         20019458 Lofgren     39
```

20 of 20 match. 221 trades.

**That sample could not carry the conclusion.** 221 trades is 0.8% of 26,737.
Fourteen of the 20 filings hold five trades or fewer. Bresnahan alone is 52%
of the sample. Zero mismatches in 20 filings puts the 95% upper bound on the
per-filing error rate near 14%.

**Round two, the 20 largest filings**, re-fetched live, with a second
newline-tolerant marker as a third count:

```
20030891 McClain    722    20022948 Goldman   195
20023404 Goldman    541    20032149 Biggs     189
20033446 McClain    473    20023892 Stanton   188
20019379 Suozzi     453    20033619 Cisneros  178
20030387 Shreve     296    20023082 Allen     176
20022653 Goldman    268    20021165 Suozzi    164
20032070 Hoyle      230    20032211 Hoyle     162
20030977 Letlow     224    20019530 Axne      159
20018311 Meijer     202    20030930 Torres    156
20021470 Manning    199    20011417 Malinowski 153

db = 5,328   strict marker = 5,328   newline-tolerant = 5,328   mismatches = 0
```

**5,549 trades checked across 40 filings, 20.8% of the corpus. None dropped.**

Two blind spots remain, and neither round could see them:

Both counts read the **same pypdf extraction**. A page pypdf renders empty is
invisible to both, identically. Not tested here.

Both require the two dates **adjacent**. A blank notification date is missed
by both. The newline-tolerant re-run closes the whitespace half of this; a
genuinely absent date is still unmeasured.

The marker counts rows only. It cannot see a wrong owner, a chopped asset, a
stolen ticker or a truncated amount -- which is where every defect above lives.

Field sweep over the 221 rows of round one: 0 assets carrying a form label,
1 single-bound amount, 1 bad ticker. It reported 0 assets starting mid-word,
and that clean result did **not** generalise -- see the 107 rows above.

Seven rows flagged as "owner code not found in the PDF" were checked by hand
and are all correct. That check was wrong, not the loader -- the PDF glues the
code onto the asset, so a standalone-token search cannot see it.

---

## 3. The Python-door marts

### BLOCKER — two models with `+enabled: false` were built anyway

`dbt_project.yml` marks both disabled as redundant raw twins:

```yaml
politics__fed_govinfo_billstatus:
  +enabled: false
politics__fed_govinfo_bill_cosponsors:
  +enabled: false
```

Both are live in LIBRARY_MARTS, created 2026-09-06 22:06.

| table | rows | canonical twin | twin rows |
|---|---|---|---|
| POLITICS__FED_GOVINFO_BILLSTATUS | 107,150 | POLITICS__BILLS | 36,465 |
| POLITICS__FED_GOVINFO_BILL_COSPONSORS | 1,268,519 | POLITICS__BILL_COSPONSORS | 367,735 |

Worth saying in the same breath: the "redundant, agrees" note that justified
the disable is now stale. The backfill made the raw twins 3x bigger than the
canonical ones. There is a real argument for enabling them. It has not been
made in `dbt_project.yml`, so the door did something dbt would refuse.

### BLOCKER — `guard_politics_mirror()` bypassed on five POLITICS marts

The folder carries `+pre-hook: "{{ guard_politics_mirror() }}"`. dbt hard-fails
at compile time without `--vars '{"allow_politics_rebuild": true}'`.

Built through the door with no gate at all:

```
POLITICS__FED_GOVINFO_BILLSTATUS
POLITICS__FED_GOVINFO_BILL_COSPONSORS
POLITICS__FED_SENATE_EFD_FILINGS
POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS
POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
```

### REAL — LATEST_ACTION_TEXT is dead in the mart

`models/marts/politics/politics__fed_govinfo_billstatus.sql:23`

```sql
try_to_double(LATEST_ACTION_TEXT) as latest_action_text,
```

A numeric cast on free text returns NULL on every row.

```
landing FED_GOVINFO_BILLSTATUS   107,150 rows, 0 NULL, 5 empty strings
mart    POLITICS__FED_GOVINFO..  107,150 rows, 0 non-null, 0 distinct
```

The defect is in the model file, so dbt would have produced the same column.
The door is what published it.

**It is a generator defect, not one file.** The model header says
"Generated by gen_mart_models.py". The same generator shipped the same cast
onto two models that are **enabled**, and so reachable by a real dbt run:

```
health__fed_hrsa_shortage_areas.sql:52  try_to_double(HPSA_DESIGNATION_POPULATION_TYPE_DESCRIPTION)
science__intl_embl_ensembl.sql:27       try_to_double(POPULATION_NAME)
```

Four model files carry a numeric cast on an obviously textual column.

### REAL — 15 non-transient tables, but the pattern predates the door

LIBRARY_MARTS holds 691 base tables: 648 transient, 43 not. Of those 43,
**28 predate the door** -- POLITICS__FEC_COMMITTEE from 06-29, fourteen
PUBLIC `__AGG` tables from 07-12, POLITICS__SENATE_TRADES from 08-01,
DIM_ZIP_POINT from 08-22. Non-transient is an established habit in this
warehouse, not a novelty the door invented.

The 15 it did create on 2026-09-06, all owned by ACCOUNTADMIN -- 14 live
marts and one rollback copy:

```
TIMELINE__FINANCE_INDEX                       46,326
FINANCE__FED_FEC_INDIV_CONTRIBUTIONS     283,771,819   10.58 GB active
POLITICS__FED_GOVINFO_BILL_COSPONSORS      1,268,519
POLITICS__FED_GOVINFO_BILLSTATUS             107,150
POLITICS__FED_SENATE_EFD_FILINGS                 799
FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES 8,191,177
FINANCE__FED_SENATE_EFD_PTR                    6,855
POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS  140,463
FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS 9,701,952
TIMELINE__HEALTH_INDEX                       133,690
HEALTH__FED_CMS_HCRIS                         80,077
TIMELINE__POLITICS_INDEX                     106,452
FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES    276,183
POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP   26,970
```

Fail-safe and time-travel bytes read 0 today, so nothing is being paid yet.
The exposure is the next rebuild: a non-transient 10.58 GB table drops seven
days of unrecoverable fail-safe storage that a transient one never would.

### PASSED — grants and ownership match their siblings

```
POLITICS__FED_GOVINFO_BILLSTATUS   OWNERSHIP ACCOUNTADMIN   SELECT RIPPLE_READER
POLITICS__BILLS  (dbt-era, 07-29)  OWNERSHIP ACCOUNTADMIN   SELECT RIPPLE_READER
FINANCE__FED_SENATE_EFD_PTR        OWNERSHIP ACCOUNTADMIN   SELECT RIPPLE_READER
```

Future grants on the schema cover the door's tables. No drift.

### PASSED — the renderer expands only what it says it expands

Rendered `politics__fed_govinfo_billstatus` and `finance__fed_senate_efd_ptr`
through the script's own `render()`. Both produced plain SQL, no unexpanded
Jinja, sources resolved to `LIBRARY_RAW.LANDING.*`, schema read out of config.

---

## 4. Trap entries checked

38 entries carry the date 2026-09-06, not 22. Twelve already carried a
`CORRECTED 2026-09-07` annotation from an earlier pass, leaving 26 open.

**24 of those 26 were assessed. 21 held, 2 falsified, 1 unverified.**

Three of the 26 were never attacked at all, and are still open:

```
traps.md:124  RIPPLE_REFRESH_SOURCE fetches the file BEFORE the ETag compare
traps.md:131  committees-historical.yaml holds no membership; last commit is emptied
traps.md:152  a House PTR trade is three lines; anchored matched 20 of 35
```

| trap | verdict | evidence |
|---|---|---|
| EPA_ECHO 3,157,891 rows, 82.1% no inspection date | HOLDS | 3,157,891 and 82.1% exact |
| FDA one row; CMS_DIALYSIS date is one range string | HOLDS | 1 row; 7,557 rows, 1 distinct value |
| freshness ledger clears before insert | HOLDS | build_freshness_ledger.py:313 |
| three USASPENDING contracts tables | HOLDS | 6.3M / 20.0M / 93.2M |
| FEC BULK_REFRESH holds single-cycle URLs | HOLDS | 5 entries; candidates 27,095 live |
| assess_density returns "empty", never "ok" | HOLDS | ingest.py:253; test_land_frame.py:112 guards it |
| FEC csv field limit raised | HOLDS | loadkit/fec_parse.py:27 |
| PARTY is majority/minority | HOLDS | 15,074 / 11,897, summing to landing's 26,971 |
| roster 26,970 rows, congresses 113-119 | HOLDS | mart 26,970. Landing is 26,971 |
| roster avg 3.49 congresses per member | FALSIFIED | 3.619 |
| CAND_ID blank on 33,937 IE rows, 12.3% | HOLDS | 33,937, 12.29% |
| SOURCE_COVERAGE_YEARS appends | HOLDS | 22,430 rows over 8,480 keys |
| HCRIS column renamed to FTE_EMPLOYEES_ON_PAYROLL | HOLDS | only that spelling exists |
| HCRIS grain RPT_REC_NUM unique on 80,077 | HOLDS | 80,077 distinct; 1,186 hospital-years >1 |
| HCRIS SOURCE_FILE_YEAR is the file label | HOLDS | Irwin County 2023 = 12/01/2022-01/31/2023 |
| IRS 527 A and B diverge at position 15 | HOLDS | see section 5 |
| two meta-column conventions live | HOLDS | in LANDING: 1,789 vs 433. All of LIBRARY_RAW: 1,789 vs 439 |
| 13 bills with no number, 11 "Reserved for" | HOLDS | exact, all 11 in the 117th |
| LAW_NUMBER empty string on 104,998 | HOLDS | 104,998 empty, 0 NULL, 2,152 laws |
| DocID prefix 2 / 8 / 9 = 2,633 / 421 / 51 | HOLDS | exact; 421+51 = the 472 scans |
| pypdf NUL bytes | HOLDS | house_ptr_load.py:244 replaces them |
| guard_politics_mirror bypassed by the door | HOLDS | see section 3 |
| "648 of 678 sibling marts", "these two" | FALSIFIED | 691 total; 14 tables, not 2 |
| roster misses 14-35 members per congress | UNVERIFIED | 523-533 distinct per congress; no Voteview join run |

### Not in the traps file and should be

`FED_USASPENDING_CONTRACTS_FULL` holds **exactly** 20,000,000 rows. A round
number that exact is a cap hit, not a count. Its sibling `_FULL_R2` holds
93,153,424 over the same span.

---

## 5. IRS 527 field layout — independently confirmed

The claim: A and B are both 18 fields; A holds the year-to-date aggregate at
15 and the date at 16; B holds the date at 15 and the purpose at 16.

**Every position below is a 0-based index.** Read 1-based, field 15 is the
occupation on both schedules and the whole table reads as nonsense.

Verified **from the raw zip**, not the warehouse, so the loader's own
assumption could not confirm itself. Scanned **all 18,300,801 lines** of
`var/IRS/data/scripts/pofd/download/FullDataFile.txt`, end to end.

```
                        SCHEDULE A            SCHEDULE B
rows                     9,701,952             8,191,177
ragged rows dropped              8                    17
field 15 numeric         9,701,952  (100.000%)  8,174,252  (99.793%)
field 15 date-shaped            32  (  0.000%)  8,174,252  (99.793%)
field 16 date-shaped     9,684,012  ( 99.815%)          0  ( 0.000%)
field 16 free text               0  (  0.000%)  8,173,267  (99.781%)
```

Two things fall out of the full pass that a sample could not give:

The A and B row counts land **exactly** on the warehouse: 9,701,952 and
8,191,177. The ragged drops land exactly on the loader's claim: 8 and 17,
25 together out of 17,893,129.

The aggregate test, which no position count can fake:

```
A field 15 >= field 13 (the amount)   9,701,890 of 9,701,952   99.9994%
A field 15 == field 13                1,101,804              first gift of the year
A field 15 <  field 13                       62
```

A date column cannot be greater than or equal to a dollar amount 99.9994% of
the time by accident. Shape alone would not prove this; the ordering against
a second column is what makes it a meaning test rather than a format test.

Real rows:

```
A: LOCAL 208 PAC PER CAPI  amt=878  f15=3806        f16=20030402
B: Doug Linkhart           amt=1000 f15=20030521    f16=City Council Race for Denver C
```

**The layout is right. 17.9M rows have their dates in the right column.**

**One clause is still assumed: the word "year".** The `>=` test proves
field 15 is a running total in the same units as the amount, never below
it, equal to it 1,101,804 times. That kills "date", "id", "occupation".
It does not pin the reset period -- cycle-to-date, election-to-date and
since-inception all satisfy it too. The test that would settle it, and was
not run: find a repeat contributor to one EIN spanning 1 January and see
whether the aggregate resets.

44 A rows carry an aggregate below their own amount, 0.0014%. Not material.

---

## 6. LDA lobbyist crawl

**Stopped at 08:03 today.** No LDA process on the box now. That is the last
write, not a proof it finished cleanly -- it could equally have died there.

```
logs/senate_lda_checkpoint.json
  filings_*      1999-2011, 2020, 2021       15 years
  positions_*    2011 only                    1 year
  contributions_ 2011 only                    1 year
```

```
FED_SENATE_LDA_FILINGS             915,725   last altered 09-07 00:22
FED_SENATE_LDA_LOBBYIST_POSITIONS  376,948   last altered 09-07 00:22   FILING_YEAR = 2011 only
FED_SENATE_LDA_CONTRIBUTIONS       187,067   last altered 09-07 08:03
```

The mart `POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS` holds 140,463 against
376,948 in landing. Behind, as the handoff said.

The handoff called this "mid-2011 of 14 years". It is worse than that. The
positions table holds **one year of the loader's 1999-2026 range**, and the
run is over, not paused. `main()` will re-stream 1999-2010 for positions on
the next run because `positions_<year>` is absent for those years while
`filings_<year>` is present — that path works, it just never got there.

---

## 7. Verdict

**Trustworthy where it was checked. Two places it is not. This report needed
correcting twice before that sentence was safe to write.**

The loaders land what they say. Forty House filings against their PDFs came
back clean on trade count across 5,549 trades, 20.8% of the corpus. That is
the check the handoff most wanted, and it holds. The IRS 527 layout -- the one
that would have silently ruined 17.9M rows -- is right, confirmed off the raw
file end to end.

Where it is not trustworthy:

**The Python door is not a dbt substitute and the marts prove it.** It built
two models the project has explicitly disabled, and walked past the one guard
written to stop exactly that. Nothing here is wrong data. All of it is a
safety rail that is no longer there. The transience gap is real but it is not
the door's invention -- 28 non-transient marts predate it.

**The House PTR parser still eats company names.** 107 rows carry a chopped
asset and a wrong owner, and on 53 of those the issuer name is gone entirely.
72 more rows lost the top of their amount range. The obvious regex fix breaks
430 good rows, so this needs a different signal, not a quick patch.

**The trap file is better than its reputation.** 21 of 24 assessed entries
held exactly, several to the row. Two were wrong on a number, neither on the
mechanism. Three were never checked and should not be trusted yet.

**On this report itself.** The first draft got six things wrong and a skeptic
pass found all six. The two that mattered were both undercounts reached the
same way: a clean result on a small sample was carried as if it generalised.
The 221-row field sweep said "0 assets starting mid-word" and that became "54
rows"; the real number is 107. Twenty small filings said "no trades dropped"
and that was true, but not yet earned. Both are fixed above with the wider
run behind them.


---

# Part two: the fixes, 2026-09-07

Everything above is the audit. This is what was done about it, under a recorded
`greenlight rebuild`. Three reloads of FED_HOUSE_PTR, three mart rebuilds, and
two skeptic passes that between them corrected ten of my own numbers.

## Final state of FED_HOUSE_PTR

Snapshot taken before anything ran: `FED_HOUSE_PTR__PREV_20260907`.

```
                              BEFORE     AFTER
rows                          27,209    27,286
filings                        3,105     3,109
chopped company names            104         0
form furniture inside assets   2,843         0
dangling amount ranges            72         0
amounts carrying cents             0        98
OWNER_RAW column                   -    27,286
```

The row count moved and that is not the parser. Four filings landed on
House.gov between runs -- Wied 9/2, Cisneros 9/4, Khanna 9/4, Taylor 9/5,
carrying 77 rows between them. Checked three ways:

```
filings only in the new table       4
filings only in the old table       0
shared filings whose count moved    0
```

Every filing that existed before parses to exactly the same number of rows.

## What was fixed in the parser

| defect | rows | fix |
|---|---|---|
| owner code eaten from inside a brand | 104 | follow-set guard plus a named list |
| a real code killed by that named list | 2 | capital-then-lowercase beats the list |
| form footer glued onto the asset | 2,843 | FURNITURE strip, no leading-F anchor |
| amount top dropped by pypdf | 72 | filled from the form's own bracket ladder |
| cents cut off an exact figure | 98 | optional decimals in the amount capture |
| ticker taken from the wrong bracket | 5 | last parenthetical, capped at six |

`OWNER_RAW` now lands beside `OWNER` on every row. It carries the untouched
head of the block, so a bad split is a query away from being found rather than
a refetch of 2,633 PDFs. It is what proved the Xylem miss below.

### Three fixes tried and thrown away

Written down because each one looks right and is not.

```
(?<![A-Za-z0-9]) before the code     false-rejects 179 real codes, 12.4%
(?<![A-Z0-9]) before the code        false-rejects  66 real codes,  4.6%
(?=[A-Z][a-z]) after the code        false-rejects 2,080 -- assets are often ALL CAPS
lowercase-to-uppercase account cut   cuts PayPal to Pal, AdaptHealth to Health
```

The last one is the trap. It cut 34 real company names on a 96-filing sample.
Roughly six rows keep an account-name prefix instead. Visibly ugly beats
silently wrong.

## The Xylem miss, and why the named list is dangerous

A skeptic pass found two rows where the fix itself broke something.

Doc 20019340, lines 40 and 41. The text reads:

```
Ameriprise SEP IRA  +  SP  +  Xylem Inc. Common Stock New(XYl) [ST]
```

Glued together that is `...IRASPXylem`, which contains `SPX`. The deny list
matched and dropped a real owner code.

**The brand was spelled by the seam, not by either side.** `SP` + anything
starting `X`, `Y`, `DR`, `GI` or `AC` is exposed the same way.

The fix: a capital-then-lowercase word after the code beats the list, because
every brand on it carries on in capitals. Checked against all 59 rows the list
touches -- it flips the 2 Xylem rows and leaves the other 57 alone.

## The mart casts

7 casts removed, 9 kept, decided by measuring landing rather than reading names.

```
COLUMN                                        NON-NULL    REAL TEXT
POLITICS__..._BILLSTATUS.LATEST_ACTION_TEXT    107,150      107,145
HEALTH__..._SHORTAGE_AREAS.HPSA_FORMAL_RATIO   165,531      117,202
SCIENCE__INTL_EMBL_ENSEMBL.POPULATION_NAME         643            0
```

**Read the right column of that table, not the left.** These marts write empty
strings, never NULL, so a `count(col)` returns every row and reads as fully
populated. POPULATION_NAME recovers nothing at all -- its landing column is
empty end to end, and dropping the cast only changed NULL into `''`.

## The Python door

Four gates now, all checked before the connection opens.

```
+enabled: false in dbt_project.yml     hard stop, no override
enabled=false in the model's config    hard stop, no override
a model under marts/politics/          needs --allow-politics-rebuild
a config that will not parse or read   refuses, exit 2
tables created                          TRANSIENT, matching dbt-snowflake
```

The second gate is the one the first skeptic pass found. Reading only
`dbt_project.yml` closed one door and left another open: 35 model files carry
`enabled=false` inside their own `{{ config(...) }}` block, and 32 of them
reached `build()`. `uncategorized__fed_eia_860_plant` proved it live.

The fourth gate is the other hole. An empty or moved `models.ripple` used to
return `{}`, which answered "enabled, unguarded" for every model in the
project -- the politics guard included.

Exhaustive re-test after the fixes:

```
models with enabled=false in their own config   35, all blocked
models under marts/politics/                    39, all blocked
empty config file                               refused, exit 2
valid yaml with no models.ripple                refused, exit 2
malformed yaml                                  refused, exit 2
```

## What is still open

`POLITICS__FED_GOVINFO_BILL_COSPONSORS` is the twin of the mart re-enabled
today and carries the same stale "redundant" note, at 1,268,519 rows against
the canonical 367,735. It is still `+enabled: false` and still non-transient.
The same decision applies to it and has not been made.

Roughly six House rows keep a brokerage account name on the front of the asset.
See the thrown-away fixes above for why that is left alone.

Four crypto names still land in TICKER where a symbol belongs -- SOLANA,
RIPPLE. Four rows.

## Verdict on part two

**The parser rewrite holds.** Every pre-existing filing parses to the same row
count, and all six defect classes are at zero. The one thing the fix itself
broke was caught and fixed.

**The door is a real gate now, not a comment.** It refuses on four counts and
fails closed on a config it cannot read.

**Two of my own headline numbers were inflated and are corrected above.** The
furniture count was checked with a case-sensitive pattern against text that is
case-mangled, so "0 remaining" was really 14. "Zero false rejects" was really
two. Both are now measured the right way and both really are zero.
