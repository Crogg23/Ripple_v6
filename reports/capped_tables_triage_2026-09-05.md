# The 170 capped tables: comb-through and verdict

2026-09-05. Python door. Every table in `LIBRARY_RAW.LANDING` sitting at exactly
10,000 rows. The count is **170**, not 169 as previously recorded.

---

## Why exactly 10,000 is the tell

A real dataset lands at an arbitrary number. 8,432 rows. 11,207 rows. 9,981 rows.

**170 tables landing at exactly 10,000 is a page limit, not a coincidence.** The
CKAN portal loaders stopped at the first page and never paged again.

The proof is in the July purchase-card files. Eleven separate monthly extracts,
different years, different agencies, different merchant counts:

| Table suffix | Month | Distinct merchants | Dollars |
|---|---|---|---|
| 0A2227FC62 | 07 | 5,193 | $3,335,658 |
| 13AC1849E2 | 07 | 4,040 | $3,291,425 |
| 41334802FD | 07 | 4,123 | $3,266,869 |
| 92C8CC9499 | 07 | 4,541 | $3,548,840 |
| B65187987B | 07 | 3,462 | $3,292,953 |
| C877A4F53F | 07 | 5,270 | $3,342,772 |
| CABB75C107 | 07 | 4,086 | $3,173,687 |
| E1AA111C19 | 7 | 5,302 | $3,799,310 |
| F394B50B84 | 07 | 4,079 | $3,952,263 |
| FFF97E32BA | 07 | 4,832 | $3,798,201 |
| 4B6E3CA1AD | 01 | 3,236 | $3,015,836 |

Eleven independent months. Every single one exactly 10,000 rows.

- **What was checked.** Row count, month span, distinct merchant count per file.
- **What a hit means.** The loader truncated; the real month is larger.
- **What a miss means.** Row counts would scatter and no two would match.

**Every dollar figure in that table is a floor.**

---

## What the 170 actually are

| Group | Tables | Content |
|---|---|---|
| **Oklahoma state spending** | **32** | purchase orders, p-cards, payroll, budgets, tax credits |
| Allegheny / Western PA | ~52 | tax parcels, appeals, permits, street trees, TRI sites |
| San Jose, San Antonio, Boston | ~40 | sidewalks, storm drains, channels, city assets |
| Virginia | 13 | address points, parcels, permits |
| Israel national portal | 8 | pension fund deposits and withdrawals |
| Indiana, Houston, California | ~24 | mixed municipal and environmental |
| `FED_SAM_EXCLUSIONS` | 1 | federal debarment list |

Only **50 of 170** carry both a money column and a party column. Of those 50,
**32 are Oklahoma**.

---

## Verdict, table group by table group

### 1. Reload — the 32 Oklahoma tables

| Kind | Tables | What each row is |
|---|---|---|
| Purchase orders | 15 | agency, vendor, description, amount, date |
| Purchase cards | 11 | **named employee**, merchant, item, amount |
| Budget and expenditure | 4 | agency, fund class, statutory reference, total |
| Tax credits and property | 2 | recipient name, credit type, amount |

One purchase-order file alone holds **$2,042,130,161 across 1,303 vendors**, and it
spans only 2025-10-01 to 2026-05-29. Eight months of a fiscal year, cut at 10,000
rows.

**This is the only genuinely investigative content in the whole pond.** Named state
employees, the merchants they charged, and the amounts. Named vendors and what they
were paid. It is the state-level analogue of the federal contract data already
landed.

### 2. Drop — `FED_SAM_EXCLUSIONS`

| Table | Rows |
|---|---|
| `FED_SAM_EXCLUSIONS` | 10,000 |
| `FED_SAM_EXCLUSIONS_FULL_R2` | **168,328** |

The full version is already landed and is 16.8 times larger. **The capped table is
a stale duplicate that can only produce wrong answers.** Anyone querying
`FED_SAM_EXCLUSIONS` by name gets a 6% sample and no warning.

Not dropped. Dropping needs an explicit yes.

### 3. Dedupe — the WPRDC and Western Pennsylvania overlap

Five column signatures appear twice, once under each prefix:

| Content | `WPRDC_ALLEGHENY_` | `WESTERN_PENNSYLV_` |
|---|---|---|
| Tax parcels | 1BA8209338 | 90A0A8B740 |
| Assessment appeals | CDA9E537DC | D7DA51769C |
| Building permits | 5B37A5568E | EF682F7E59 |
| Street trees | 98A0E89FA3 | 1A89F1526C |
| TRI facilities | DE448D04D4 | 0AF7431C6C |

The registry confirms it: "Allegheny County Finished Property Assessment Appeals"
is listed twice with the same URL. **Two loader runs against the same portal under
two names.** The duplication is not limited to the capped set.

### 4. Skip — everything else

Sidewalk width. Storm drain rim-to-invert depth. Street tree growth space length.
Fire call alarm times. Community centre attendance.

**These are municipal asset inventories.** They carry no party, no money, and no
route into any other table in the warehouse. A capped sample of them costs nothing
because a complete copy would also be worth nothing here.

The Israel pension funds are real money with a named controlling corporation, but
nothing in the warehouse joins to an Israeli fund ID. **Out of reach, not out of
interest.**

---

## What is claimed, and what is not

| Claim | Supported |
|---|---|
| 170 tables sit at exactly 10,000 rows | **yes** |
| The 10,000 is a loader page limit | **yes, eleven independent months all match** |
| Every count on a capped table is a floor | **yes** |
| The true upstream row counts | **not known. Needs the portal API** |
| The Oklahoma tables are the only investigative content | **yes, of the 50 with money and party** |
| `FED_SAM_EXCLUSIONS` is superseded | **yes, by a table 16.8x larger** |
| WPRDC and Western PA overlap on five datasets | **yes, matched by column signature** |
| The duplication is confined to capped tables | **no. Not checked outside them** |
| Reloading Oklahoma is cheap | **no real number for this** |

---

## The one thing worth saying out loud

The pond is 5.1 GB of 91 GB and 76% of it is municipal infrastructure geometry.

**One slice matters: 32 Oklahoma tables holding named state employees, named
vendors, and dollars.** The rest is sidewalks.

That is the whole verdict. The cap has been carried as a 169-table problem for
weeks. It is a 32-table problem, and 137 of the tables were never worth loading in
the first place.

---

# Outcome: pager fixed, 32 tables reloaded

Same day. `connect/portal_loader.py`, `fetch_ckan`.

## The bug, exactly

```
CKAN_PAGE = 10_000
while len(out) < max_rows:
    page = min(CKAN_PAGE, max_rows - len(out))
```

Run with `--max-rows 10000`. First iteration takes `page = min(10000, 10000)`,
returns 10,000 records, `len(out)` becomes 10,000, and the `while` guard fails.
**The loop exits after one request and a single page looks like a finished load.**

The cap was never a hard-coded constant. It was the invocation.

## Two changes

**1. The non-advancing-offset guard the docstring already promised.** It said
"bounded by max_rows and a non-advancing-offset stop, so it can never spin." That
guard existed only on the ArcGIS path. Without it, a portal that ignores `offset`
lands page one N times and nothing downstream can tell those from N real pages.

**2. A loud `TRUNCATED at max_rows=` line** whenever a fetch stops because of the
cap rather than because the data ran out, with the portal's own reported total
when it gives one.

## Verified before overwriting anything

Dry run against three datasets, no writes:

| Dataset | Index says | Fetched |
|---|---|---|
| Expenditure Summary | 109,348 | **109,348** |
| Vendor Payments FY2022 | 77,211 | **77,211** |
| Funding Summary FY2022 | 74,236 | **74,236** |

## The reload

32 of 32 loaded. Zero failures. **992,041 rows landed against 320,000 before.**

Warehouse-side check, not the log:

| Measure | Before | After |
|---|---|---|
| Oklahoma tables at exactly 10,000 | 32 | **0** |
| Rows in the 32 reloaded tables | 320,000 | **992,041** |
| Rows across all 65 Oklahoma tables | 423,047 | 1,095,088 |
| Tables at 10,000 warehouse-wide | 170 | **138** |

One table landed 20,957 against an index figure of 21,664. The loader calls
`drop_duplicates()` before landing, so 707 rows were exact duplicates upstream.
Not a short read.

## What the cap was actually hiding

| Table | Measure | Capped | True |
|---|---|---|---|
| Purchase cards FY2016 | rows | 10,000 | 37,338 |
| | distinct merchants | 3,462 | **12,582** |
| | named cardholders | — | 2,763 |
| | dollars | $3,292,953 | **$18,256,692** |
| Direct PO lines 2025-26 | rows | 10,000 | 21,180 |
| | distinct vendors | 1,303 | **1,899** |
| | dollars | $2,042,130,161 | **$9,959,769,883** |

**The purchase-order file was reading 20% of its own money.** The p-card file was
reading 18%.

The capped PO table also appeared to span 2025-10-01 to 2026-05-29. The full table
spans **2025-06-01 to 2026-05-29**. The cap was silently deleting the first four
months of the fiscal year, and the truncated span looked like a plausible one.

## The second cap, found by the skeptic, and it is bigger

**The reload fixed the page cap and left a resource cap standing.**

```python
rid = next((r["id"] for r in resources if r.get("datastore_active")), None)
```

A CKAN package is a folder. `next(...)` takes the first file in it and discards
the rest. Oklahoma publishes one fiscal year of purchase-card data as **twelve
monthly CSVs inside one package**.

Audited all 32 packages live against the portal:

| | Packages | Rows |
|---|---|---|
| Landed by the reload | 32 | 992,041 |
| Actually available | 32 | **7,540,233** |
| **Still missing** | | **6,548,192** |

**27 of the 32 packages hold more than one resource.**

| Package | Resources | Landed | Available |
|---|---|---|---|
| Expenditure Summary | 18 | 109,348 | **1,957,980** |
| Vendor Payments FY2022 | 12 | 77,211 | 789,381 |
| Purchase cards FY2016 | 12 | 37,338 | 442,167 |
| ten more p-card years | 6 to 12 | ~30,000 | ~420,000 each |
| Funding Summary FY2018-22 | 1 | 20,000ish | same |

### The false trap this produced

A first draft of this report filed a data trap: *"Purchase Card FY2016 holds
37,338 rows, all July 2015. The title says fiscal year, the data is one month."*

**That was the loader, not the data.** Fetching every resource returns 442,167
rows across exactly twelve month buckets:

| Year-month | Rows |
|---|---|
| 2015-07 | 37,338 |
| 2015-08 | 39,150 |
| 2015-09 | 39,451 |
| 2015-10 | 40,071 |
| 2015-11 | 33,161 |
| 2015-12 | 32,332 |
| 2016-01 | 34,012 |
| 2016-02 | 38,292 |
| 2016-03 | 37,898 |
| 2016-04 | 36,450 |
| 2016-05 | 36,444 |
| 2016-06 | 37,568 |

July 2015 to June 2016. **The title was honest.** Filing that as a data trap would
have recorded a loader defect as a source defect and misled every future reader.

### Why the verification missed it

The check was "landed rows equals `PORTAL_DATASET_INDEX.ROW_COUNT`", and it
matched exactly on three datasets.

**That check is circular.** The index harvested its row count from the same first
resource the fetcher picks. It cannot detect resource-level loss by construction.

One package proves it: index said 21,664, first resource holds 21,664, the full
package holds 23,414. **The index matched and the load was still short.**

### The first guard was dead code

The offset guard shipped in the first attempt tracked `offset`, a counter this
same loop increments. A number you increment yourself never repeats, so the guard
could never fire. The ArcGIS version works because it hashes the page contents.

Now fixed with `_rows_sig`, and exercised against a stubbed portal that ignores
`offset`: it stops at 10,000 rows instead of landing page one five times.

Also fixed: `max_rows=0` raised `UnboundLocalError` because the TRUNCATED line
referenced a variable bound only inside the loop.

## What is claimed, and what is not

| Claim | Supported |
|---|---|
| The cap came from `--max-rows`, not a constant | **yes, traced in code** |
| The pager now returns full datasets | **yes, three exact index matches** |
| 32 tables reloaded, zero failures | **yes, 992,041 rows** |
| No Oklahoma table sits at 10,000 any more | **yes, checked in the warehouse** |
| The offset guard was missing on CKAN | **yes. It existed only on ArcGIS** |
| The offset guard has now been exercised | **no. No portal in this run ignored offset** |
| The index row counts are themselves correct | **assumed. They matched on 31 of 32** |
| The other 138 capped tables are worth reloading | **no. Triaged above as skip** |
| The reload landed the full packages | **no. 6,548,192 rows sit in unread resources** |
| The FY2016 one-month finding is a data trap | **no. It was the loader. The title was honest** |
| The index row counts prove a complete load | **no. The check is circular** |
| The first offset guard worked | **no. It was dead code. Fixed and now exercised** |

---

# Outcome 2: full reload, every resource in every package

Same day, after the skeptic pass. `--max-rows 2,500,000` per package, which
clears the largest at 1,957,980.

## Result

32 of 32 loaded. Zero failures.

| Measure | June load | Reload 1 | Reload 2 |
|---|---|---|---|
| Rows in the 32 | 320,000 | 992,041 | **7,396,758** |
| Tables at exactly 10,000 | 32 | 0 | 0 |
| Oklahoma family, all 65 tables | — | 1,095,088 | 7,499,805 |
| Oklahoma family on disk | — | — | 169.6 MB |

Warehouse-wide tables sitting at 10,000: **138**, unchanged. Nothing outside the
32 was touched.

## The gap between fetched and landed

7,540,233 rows were available. 7,396,758 landed. **143,475 short.**

That is `drop_duplicates()` in `load_one`, not a short read, and it was checked
rather than assumed. Re-fetched the largest contributor independently:

| Vendor Payments FY2022 | Rows |
|---|---|
| Fetched from the portal | 789,381 |
| After `drop_duplicates()` | **668,789** |
| Landed | **668,789** |

Reproduced to the row. 120,592 of the 143,475 gap is that one table.

**Say it as a loader policy, not a source fact.** The loader drops rows that are
identical across every column. Whether the portal intended them as duplicates is
not established here.

## What twelve resources bought

`Purchase Card (PCard) Fiscal Year-FY 2016`, the table that produced the false
one-month "trap":

| Measure | Capped, June | One resource | All twelve |
|---|---|---|---|
| Rows | 10,000 | 37,338 | **442,167** |
| Months covered | 1 | 1 | **12** |
| Distinct merchants | 3,462 | 12,582 | **90,600** |
| Distinct cardholder surnames | — | 2,763 | **4,087** |
| Dollars | $3,292,953 | $18,256,692 | **$191,313,585** |

**The June table was reading 1.7% of the money.** The first reload got it to 9.5%.

## What is claimed, and what is not

| Claim | Supported |
|---|---|
| 32 of 32 reloaded, zero failures | **yes** |
| 7,396,758 rows landed | **yes, counted in the warehouse** |
| No table in the 32 sits at 10,000 | **yes** |
| Nothing outside the 32 changed | **yes, warehouse count still 138** |
| The 143,475 gap is duplicates | **yes for 120,592 of it, reproduced** |
| The remaining 22,883 of the gap | **assumed duplicates. Not individually checked** |
| The duplicates are meaningless upstream | **not established. This is loader policy** |
| Every Oklahoma package is now complete | **no. Complete against what the portal serves today** |

---

# Outcome 3: the rows landed, the columns are the problem

Skeptic pass on Outcome 2 **agreed on all five claims** — every number reproduced
from the warehouse and from the portal. It then found three problems in what
the rows look like, none of which were in the report.

## The one that will bite: resources do not share a header

A CKAN package is a folder. The loader now reads every file in it, and pandas
unions the keys. **A column present in only some resources is populated on only
some rows.**

Measured across all 32 reloaded tables:

| Table | Columns | Rows | Partially filled |
|---|---|---|---|
| Vendor Payments FY2022 | 105 | 668,789 | **71** |
| Expenditure Summary | 38 | 1,957,980 | **35** |
| nine PO tables | 29 to 31 | ~22,000 | 15 to 19 |
| p-card FY2021 | 19 | 335,640 | 6 |
| eleven p-card years | 16 | ~400,000 | 0 to 1 |
| five funding summaries | 14 to 15 | ~20,000 | 0 to 2 |

**19 of 32 tables carry partially-filled columns.**

The money case, on the largest by dollars:

| Column | Rows populated | Sum |
|---|---|---|
| `PYMNT_AMT` | 589,381 of 668,789 | $7,871,848,150 |
| `PAYMENT_AMOUNT` | 79,407 of 668,789 | $1,282,618,447 |

**Sum `PYMNT_AMT` alone and 14% of the money silently disappears**, along with a
whole month of payments. `AGENCY_NUMBER` on Expenditure Summary sits at 50%.

- **What was checked.** Fill rate of every non-lineage column against `count(*)`.
- **What a hit means.** The package's files disagree on their header.
- **What a miss means.** Every column populated on every row, one schema.

## Two more, smaller

**`ROWID` is not an ID.** 442,167 rows and 163,508 distinct on p-card FY2016. It
restarts inside each monthly file, so it collides across a package. It also props
up `drop_duplicates()` — some rows survive dedupe only because `ROWID` differs.
Ignore it and FY2016 still holds 8,651 genuine duplicate groups.

**`MERCHANT` is a terminal string, not a merchant.** 90,600 distinct strings
collapse to 34,742 on letters alone. `WAL-MART #0151` and `WAL-MART #3340` are
two. Amazon appears under four spellings. **The "90,600 merchants" figure in
Outcome 2 is a string count and should be read as one.**

All three are recorded in `.claude/traps.md`.

## Loader hole the skeptic named, now closed

`fetch_ckan` read `result.records` and never read `result.total`, which sits in
the same JSON. A server that clamps `limit` returns a short page, the normal
`len(recs) < page` door closes the loop, and **nothing anywhere says the fetch was
short.**

Now it captures the portal's own total per resource and warns when it comes up
short. Tested against a stub that clamps `limit` to 100:

```
[warn] .../r1: got 100 of 50000 rows the portal reports
```

The real package stays silent and returns all 442,167 rows.

Also renamed: the cap message now reads `HIT max_rows=... -- may be short` rather
than `TRUNCATED`, because it fires whenever data exactly fills the cap and that
is not always a truncation.

## What is claimed, and what is not

| Claim | Supported |
|---|---|
| 19 of 32 tables have partially-filled columns | **yes, fill rate measured per column** |
| Summing `PYMNT_AMT` alone loses 14% | **yes** |
| `ROWID` is not unique | **yes, 163,508 distinct over 442,167 rows** |
| The 90,600 merchants figure is a string count | **yes. 34,742 on letters only** |
| 34,742 is the true merchant count | **no. It is a second string count, less wrong** |
| The loader now catches short fetches | **yes, tested against a clamping stub** |
| The 32 tables are usable as landed | **only with a fill check per column first** |

