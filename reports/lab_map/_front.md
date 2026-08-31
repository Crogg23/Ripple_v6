# The Laboratory ↔ Warehouse Map

*What every visualization technique in `docs/The_Laboratory.md` would need, what
the warehouse actually holds, and how far each one is from being tryable today.*

**Built 2026-08-22. Metadata only — `INFORMATION_SCHEMA` across all five
databases, plus the wiring tables in LIBRARY_META and the audit reports already
on disk. Zero data SELECTs, zero profiling queries, zero sampling.**

This is a menu, not a plan. It deliberately does **not** say what to build
first.

---

## The one-screen picture

**23 techniques scored. 18 ready to try today, 5 partial, none dead.**

But that headline is misleading on its own, and the three sentences under it are
the actual finding:

1. **The warehouse is 91.6% text strings.** 149,003 of 162,750 columns are TEXT.
   Only 122 tables store map coordinates as real numbers even though 801 have
   columns named for them; 322 of 948 money tables have a real numeric amount;
   1,058 of 3,517 date-ish tables have a real typed date. Every technique that
   needs a number is really a technique that needs a cast first. **The cheapest
   unlock in this warehouse is almost always "add a guarded cast to a dbt model
   that already exists" — the canonical clock did exactly that for time, for 403
   tables, last week.**

2. **Nothing in the warehouse knows the shape of a county.** Exactly 2 of
   162,750 columns are a real geospatial type, and both are the same ship-position
   point column. Zero polygon columns exist anywhere. Five of the geographic
   techniques are scored Ready because the *statistics* work off centroids — but
   their *drawn output* is dots and heat surfaces, never a filled-in map. One
   public boundary-file download fixes all five at once, and it is the only item
   on the whole map that needs something from outside.

3. **The best connection maps in the building are not in the connection layer.**
   The official map holds 4,512 table-to-table links (2026-08-28 rebuild; was 4,910), of which roughly a
   quarter are hard-identifier matches and the rest are name-and-address
   guesses. Meanwhile several source tables carry clean, hard-identifier,
   directed, *dated* edge lists on their own — opioid shipments (178.6M),
   offshore-leaks relationships (3.3M), doctor-to-facility affiliation (2.3M),
   corporate ownership with switch-on and switch-off dates (484k). Three
   separate techniques were scored on the assumption that the graph lives in the
   connection layer; it mostly does not.

> **The single widest constraint:** value is present, type is wrong. The single
> widest *unlock* is one boundary-file ingest. Everything else on this map is a
> cast or a join over tables that already exist.

---

## How to read a technique entry

- **Needs** — the shape of data the technique requires, in plain words.
- **What exists** — what was actually found, with counts and named tables.
- **Readiness** — ✅ Ready · 🟡 Partial · 🔴 Needs new data · 🛠️ Needs cleanup.
- **The gap / Distance to ready** — for anything not Ready, the exact named
  blocker and the single step that would clear it.
- **Candidate tables** — the 1–3 strongest places to prototype against.
- The line in a **blockquote** at the end of each entry is the one thing worth
  remembering about it.

Every table named in this document was checked against the live metadata dump
this session. Backup, restore and retired schemas were excluded by rule.

---

## Method, and what it cannot tell you

Each of the five Laboratory categories was scored by one pass, then handed to a
second pass told to **refute** it — check that every cited table exists with
those exact columns and row counts, hunt for tier inflation, hunt for tier
deflation, and catch anywhere a column *name* had been trusted as proof of a
column's *contents*. Two more passes then swept the finished set for
contradictions, oversold claims and warehouse shapes that no technique had
claimed. Four tier calls changed as a result and every change is shown in place.

**The hard limit of a metadata-only sweep:** a column name and a data type tell
you the shape, never the contents. A numeric latitude column can still be 40%
null. A hard-identifier column can still be sentinel-masked — that exact trap
has bitten this platform twice. Nothing in this document has been value-checked,
and several entries say so explicitly where it matters most.

---

## Corrections this sweep made to things already written down

Four claims that were on the record turned out to be wrong, and they are
corrected here rather than left to be rediscovered.

| what was written | what is actually true |
|---|---|
| The Laboratory: "~12.88M entities across the 31 spine tables" | The resolved-entity tables hold **33,312,349**; the index and node tables hold **84,382,504**. The number is roughly a quarter of current scale. |
| Two scoring passes disagreed on whether a polygon layer exists | It does not. The one column *named* geometry is typed TEXT. A full type census returns 2 geospatial columns warehouse-wide, both the same point column, and zero polygon columns. |
| "Nothing in the warehouse can place a ZIP on a map," used to block flow maps | ZIP → county → population-weighted centroid is a two-hop join over two tables that both exist today. Flows are drawable at county resolution with no new data at all. |
| Two techniques were caveated on county/FIPS columns being broken by a bad numeric cast | That defect was **repaired on 2026-08-10** — the repair note says so in the same words, and the live metadata agrees the columns are TEXT today, leading zeros intact. The warning was stale. |

One more, in the other direction: a mid-sweep claim that the opioid shipment
table's county and date columns were bad casts turned out to have been read off
the **backup copy** of that table, not the live one. The live table's date column
is rated the cleanest big event clock in its batch.

---

## Summary table

Sorted so everything ready to try today is visible at a glance.

| # | Technique | Category | Tier | The one-line reason |
|---|---|---|---|---|
