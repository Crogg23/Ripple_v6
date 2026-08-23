# The Fix List

*Every known-broken thing in the warehouse, one place, ranked by how badly it lies to
you if you trust it. Compiled 2026-08-22 from three sources: the 2026-08-11 full
warehouse verification sweep, the 2026-07-27 mart defect sweep, and this session's
freshness/re-pull investigation. Nothing here is new detective work — it's a merge.*

**Read this before trusting any number out of the warehouse.** If a table you're using
isn't on this list, it hasn't been *cleared* — it just hasn't been *caught* yet.

---

## 🔴 TIER 1 — corrupts the number itself (wrong answer, high confidence)

These don't look broken. They look like normal data. That's what makes them dangerous.

1. **Federal contracts table is a 1M-row-per-year cap, not the full year.** Each FY
   covers only ~2–3 months of real activity; the rest is silently missing. Any trend
   line is showing you the cap, not reality. — *needs a priced re-pull, your call*
2. **FHFA mortgage database: 19M rows, only 7,204 are real** (~2,600x duplication —
   a paginated loader re-fetched the same content in a loop).
3. **ForeignAssistance.gov: 97.6% exact duplicates** (95,658 real rows out of 3.97M) —
   same runaway-loader bug as #2.
4. **EPA penalty dollars: one settlement's total gets stamped onto every facility it
   covered.** A $10M case touching 200 facilities sums to $2B, not $10M.
5. **Drug side-effect reports (FAERS): ~75% of 62M rows have columns shifted sideways**
   — drug name, dosage, and outcome no longer line up correctly on those rows.
6. **NCUA credit-union call reports: the table isn't call-report data at all** — it's
   the column-description dictionary sheet, loaded as if it were real rows.
7. **Mine death counts report zero.** Unverified root cause; treat any injury-severity
   field on this source as untrustworthy until checked.
8. **SEC 13F filings: dollar amounts mix two units** (whole dollars vs. thousands)
   with no per-row flag saying which — sums are meaningless until tagged.
9. **Vehicle recall counts: suspected duplication** — amended recalls may republish as
   new rows instead of updating the original.
10. **Federal debarment list: under 9% loaded, and the status flags that did load were
    fabricated by the loader**, not sourced from the real file.
11. **FAA aircraft registry: the tail-number key is 100% blank, and all four date
    columns read 1970** (epoch-parse bug) — the table's own join key doesn't work.
12. **CFTC futures/financial positions: the "as-of" date column is 100% corrupted to
    1970-01-03** — a second, correct date column exists, so this is fixable, not fatal.
13. **openFDA: 8 raw source tables are wiped down to 1–2,542 rows** while their built
    marts stayed full — meaning the marts can't be rebuilt or audited against source
    anymore. Two of those marts are themselves short of the real total (device-event
    reports 2.7M of 25.7M; establishment registrations 263k of 333k).

## 🟠 TIER 2 — undercounts or overcounts, moderate confidence problem

14. **30 sources measured short of what the publisher actually has** — biggest gaps:
    Senate lobbying filings (9% loaded), Federal Register (9%), GLEIF ownership
    relationships (73%), FEMA flood-community status (77%), ransomware victim tracker
    (63%). Full list in `outputs/_completeness_vs_publisher_2026-08-11.csv`.
15. **8 sources show MORE rows than the publisher advertises** — could be legitimate
    growth since the publisher's own count was taken, or a duplication bug; not yet
    told apart. Includes GLEIF exceptions (9.5x), EPA ECHO (2.1x).
16. **A further ~10 tables are 20–80% exact duplicates** without being full loops —
    EPA Title V certificates (81%), Google political-ad creative mapping (80%), FAERS
    outcomes (78%), DHS immigration stats (77%), UK sanctions list (42%), and others.
17. **104 ID-named columns across 43 tables are ≥99% blank or sentinel-masked** —
    columns that look like real join keys (docket numbers, funder IDs, EINs) but
    almost never have a value. The exact trap that already burned NPPES EIN and NOAA
    AIS `imo_number` — never trust an ID column without `COUNT(DISTINCT)` first.
18. **Corporate facility→parent bridge covers 5.3% of EPA facilities** (grown from
    1.4% this session via a hand-verified 68-company dictionary). Real and clean where
    it hits, but "no match" mostly means "small business with no public LEI," not "no
    corporate parent."

## 🟡 TIER 3 — monitoring/measurement layer is the thing that's wrong

19. **The freshness dashboard itself produces false "stale" alarms.** Confirmed this
    session on five sources (California lobbying, ICIJ, Texas lobbying, Retraction
    Watch, PBGC) — the monitor was reading the wrong date column, not measuring real
    staleness. Trust a "fresh" reading; double-check a "stale" one before acting.
20. **275 of 342 sources have an auto-guessed update cadence**, not a verified one —
    the freshness state for those is a best-effort inference, not a confirmed fact.
21. **Uniqueness tests may not actually be running.** 505 of 607 marts declare a
    uniqueness test, but no dbt test-run artifacts exist in the repo newer than the
    last two weeks of mart rebuilds — an undemonstrated guard isn't a guard.
22. **A duplicate table landed today** (`FED_NCHS_DRUG_POISONING_MORTALITY_COUNTY`) —
    exact duplicate of an existing source. Needs a manual drop (DDL is blocked for
    sessions): `DROP TABLE LIBRARY_RAW.LANDING.FED_NCHS_DRUG_POISONING_MORTALITY_COUNTY;`

## ⚪ TIER 4 — cosmetic, low risk, fix when convenient

23. Mojibake (broken character encoding) in 9 tables, worst is NOAA storm events, all
    under 1.25% of rows.
24. Treasury daily cash data has a literal string `"null"` as a category value instead
    of a real null.
25. Senate stock-trade disclosures have raw HTML markup embedded in asset descriptions.
26. A prior sweep found pandas writing the literal text `'nan'` instead of a true null
    in ~4.2M cells warehouse-wide, including at least one branch ID and some
    coordinates — repair script exists (`scripts/repair_nan_text.py`) but full
    warehouse coverage of the fix is unconfirmed.
27. Far-future sentinel dates (2068–2069) show up in ~56 date columns from a
    century-pivot bug in one parsing path; most of the far-future dates elsewhere are
    legitimate (expiration dates), so this needs a column-by-column pass, not a
    blanket rule.

## ⚫ UNSCANNED — not yet checked either way

28. **16 tables errored out of the last full scan** and have never been re-verified:
    all 6 ICIJ Offshore Leaks node/edge tables, OpenSanctions default list, ICE
    detainer records, two SEC fund tables, EIA balancing authority, and 5 others.
    *(Note: this session separately confirmed ICIJ's file itself is current — that's
    about freshness, not about whether the load completed cleanly.)*
29. **~160 sources have no loader script in the repo at all.** Not necessarily broken
    — just never automated. Treat gaps found in these domains as "maybe just not
    built yet," not "doesn't exist publicly."

---

## Cost and effort per item

Effort = analyst/session time to actually fix it (not counting review). Cost = real
warehouse compute only; effort time itself isn't billed per-item. **S** = under an hour,
pennies. **M** = a few hours, ~$1–5 compute. **L** = a half-day+, ~$5–20 compute,
usually a full re-pull of a large file. **XL** = its own priced session.

| # | Item | Effort | Compute cost | Why |
|---|---|---|---|---|
| 1 | Contracts truncation | **XL** | $10–30 | full multi-year API re-pull past whatever caused the cap; rate-limited, many pages |
| 2 | FHFA mortgage dupes | **S** | pennies | dedupe query, data's already here |
| 3 | ForeignAssistance dupes | **S** | pennies | same — dedupe, not re-pull |
| 4 | EPA penalty stamping | **M** | ~$1 | redesign the case→facility join logic to allocate, not copy |
| 5 | FAERS column-shift | **L** | $5–10 | find the parsing bug, reload 62M rows |
| 6 | NCUA wrong file loaded | **M** | ~$1 | identify + load the correct source file |
| 7 | Mine deaths = zero | **M** | ~$1 | root-cause the code mapping first, then fix |
| 8 | SEC 13F mixed units | **M** | ~$1 | build a per-filer unit-detection rule |
| 9 | NHTSA recall dupes | **S** | pennies | dedupe by recall ID + latest revision |
| 10 | Debarment list | **M** | ~$1–3 | new loader against the real source |
| 11 | FAA registry epoch+blank key | **S** | pennies | epoch fix uses an existing macro; key issue needs one look |
| 12 | CFTC epoch dates | **S** | pennies | same existing epoch macro, second date column is fine |
| 13 | openFDA wiped raw tables | **M** | $2–5 | re-download several files fresh, raw copies are gone |
| 14 | 30 sources short of publisher | **L** (whole batch) | $5–15 | mixed bag — some are one-line re-pulls, some need investigation |
| 15 | 8 sources over-published count | **M** | ~$1 | investigate each; likely legit growth on most |
| 16 | ~10 tables 20–80% duplicate | **M** (whole batch) | ~$2 | dedupe queries, same shape as #2/#3 |
| 17 | 104 dead ID columns | **S** | free | documentation/metadata fix — mark untrustworthy, no rebuild needed |
| 18 | Corporate bridge growth | **M** more brand work / **XL** spine rebuild | $0 more curation / $10–15 rebuild | already grown once this session; further growth is manual curation |
| 19 | Freshness false alarms | **M** (ongoing) | free | one source at a time, as each gets used for real |
| 20 | 275 auto-guessed cadences | **L** | free | clerical cataloging pass, ~340 sources, tedious not hard |
| 21 | Uniqueness tests unverified | **S** | free | just run the dbt test suite and check |
| 22 | Duplicate table today | **S** | free | one DROP command — blocked on your permissions, not effort |
| 23–27 | Cosmetic (5 items) | **S** each | free–pennies | find/replace or a single cast fix |
| 28 | 16 unscanned errored tables | **M** | ~$1–2 | debug why the scan choked, then re-run it |
| 29 | ~160 no-loader sources | **XL** | varies wildly | this is the big one — see below |

### The one honest outlier: item 29

**160 sources, no loader, no shortcut.** A simple flat-file source might be 30–60 minutes
to write and verify; an API needing pagination or auth can run several hours. At even a
conservative average, this is **well over 100 hours of build work** if pursued in full —
by far the largest number on this entire list. It should never be tackled as "the whole
pile" — it's a target list to pull from a handful at a time, prioritized by what a domain
actually needs, not worked top-to-bottom.

### Rough total, everything else (items 1–28)

**Time:** low tens of hours across ~28 items, most of them S/M.
**Compute:** roughly **$40–70** if every item above got done — nothing here is a big
spend individually; it adds up because there are a lot of small jobs.

## The honest confidence statement

Tiers 1–2 come from a **dedicated full-warehouse sweep** (2026-08-11) plus a **mart-level
sweep** (2026-07-27) — real audits, not guesses. Tier 3 is what this session (2026-08-22)
found by accident while investigating freshness. **Nothing here should be read as "the
full list forever."** Both prior sweeps found what they were looking for; a fresh sweep
run today, against the warehouse's current state, would almost certainly surface things
neither one caught — the same way today's freshness work caught five false alarms nobody
had specifically checked before.

**If you want a harder floor:** re-running a full defect sweep against today's warehouse
state is a priced session, same shape as the 2026-08-11 one. Everything above is free —
it's already been paid for and just needed compiling.
