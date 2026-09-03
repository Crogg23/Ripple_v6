# What's actually in the warehouse — the dossier

Gen 1-3 content recon. 2026-09-02 to 2026-09-03. Glanceable version.

## The numbers

```
tables scanned         2,208
rows                    1.34B
size                    96 GB
columns                 79,007 — 78,074 of them plain text, even the dates
cost                    ~$11, 2.85 hrs
gen 3 cost              $0 — reused gen 1's files, no new queries
```

## Gen 1 — opened every table, checked the actual values

**Why values, not names:** 78,074 of 79,007 columns are text.
A date might read `09302024`. A timestamp might read `1788291300090871`.
The column name tells you nothing. The values do.

**Dead data, still huge:**
- DEA drug-transaction table — 178M rows, dead since 2012
- FDA adverse-event table — looks dead 2014, but only one date field is
- Any chart on these needs the vintage in the title, or it lies

**Biggest dollar totals — mostly not real:**
- $382T in wages — a rollup, county+state+national all summed together
- $659T in SEC stock holdings — same position counted every quarter
- $11.4T in contract obligations — this one's real, one row = one event
- Rule of thumb: before trusting a sum, check if one row = one event

**Weird single numbers — typos, not data:**
- $400B insider-trading price, everything else in that column tops $340
- Bankruptcy debt fields cap at $999,999,999,999.99 — a form ceiling, not a number
- One drug-dose value is 2,800x the normal range — a unit mixup

**Cross-agency names — this part is real and useful:**
- Walmart — gun licenses, Medicare billing, injury reports, 10 different agencies
- Tennessee Valley Authority — every power-grid filing there is

**Four gotchas, now written down for good:**
- Portal-scraped tables cap at exactly 10,000 rows — that's a sample, not the dataset
- Some load-timestamps are stored in the wrong time unit — reads as year 56 million
- Some geo dates are milliseconds with a stray `.0` — sums as trillions
- One CMS "payment" column is actually just an ID number

**A second reader caught 4 mistakes before this shipped:**
- "table ends 2014" — true for one date field, not the other
- "exactly $1,000B" — actually $999,999,999,999.99
- 850 "over time" charts were quietly using load-date, not event-date
- A third of the "biggest sums" list wasn't dollars at all

## Gen 2 — folded into gen 1, no separate step

Matching each big name to its own year-by-year curve turned out
cheap enough to do inside gen 1's pass. It shipped there.

The load-date bug above — that's this piece. Now labeled everywhere it happens.

## Gen 3 — connect the dots across agencies, watch it break, fix it, verify it

**The idea:** fold "WALMART INC" and "WAL-MART STORES EAST LP" into one entity,
across all 2,208 tables, using only files already on disk. Zero new cost.

**It broke immediately.** Top hits weren't companies —
JOHNSON, SMITH, BROWN. 664,000 rows for "Johnson" in one CMS table alone.
Not one entity — thousands of unrelated physicians who share a surname.

**Traced and fixed, twice:**
- Bug 1 — surnames leaking through columns literally named "last name"
- Bug 2 — country names (Australia, Brazil) leaking through filing-origin fields
- Fixed both, re-ran

**Split the results by risk, then verified with 37 independent readers:**

```
                verified   real entity   hit rate
single word         25          2          8%
multi-word           12         11         92%
```

- Single-word real hits: **TESLA** and **PACIFICORP** — PacifiCorp is a genuinely new find
- Single-word noise: JOHNSON, SMITH, THOMAS, DAVIS, JONES... 23 of 25, all common names
- Multi-word real hits: Walmart entities, Exxon Mobil, Bank of America, UPS, Microsoft, Duke Energy
- Multi-word miss: **ST LUKES HOSPITAL**

**The St. Luke's catch is the big one.** It looked like one hospital chain
across 8 CMS datasets — the Walmart pattern. It isn't.
Dozens of unrelated hospitals share that name — Kansas City, Boise, Houston, more —
each with its own facility ID, sitting next to equally generic names:
"Memorial Hospital," "Holy Cross Hospital," "Community Hospital."

Gen 1's own report still lists all six of those as confirmed hits.
None of the other five have been checked yet.

## Bottom line

- Warehouse content is known now, not assumed — gen 1's job, done
- Cross-agency name matching works, but only past a check
- One word: verify it one at a time. Two-plus words: trust it ~9 times out of 10
- Even then, a generic name still needs an eyeball

**→ Full receipts, every table name, every agent's reasoning: the two technical reports in reports/recon/.**
