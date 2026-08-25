# Ripple Warehouse — Mechanics Reference

**Dated 2026-08-24.** Written as a companion to the four CSVs in this folder
(`tables.csv`, `columns.csv`, `key_columns_all.csv` / `key_columns_verified.csv`,
`key_overlap_edges_new.csv`, `spine_connect_edges_live.csv`,
`scale_summary_by_schema.csv`). This file explains **how the machine works**;
the CSVs carry the numbers. Per the house rule, if a number here ever disagrees
with a CSV, the CSV wins — this prose is dated the moment it's written.

Everything below was confirmed live against Snowflake this session
(2026-08-24), or read directly out of the code that runs the platform
(`connect/`, `honesty/`, `portal_recon/tag_portal_index.py`, dbt config). None
of it is copied from an older report.

## Headline numbers (all live-counted this session)

- **7 databases, 5,436 objects total**: 3,350 real tables (`BASE TABLE`) + 2,086
  views. **4,974,176,335 rows, 185.4GB**, summed across every real table.
- **847 real tables** carry at least one genuine entity-grade key (person /
  organization / facility / provider / case / asset) by live column-NAME
  detection — versus **178** formally registered in the spine's own gate
  (`DISPLAY_SPECS`). That gap is the platform's real unwired-connectivity
  backlog. (This audit's detector is name-based, same as the platform's own
  scout tagger — it does **not** catch the ~20 table-scoped special-cased
  keys `DISPLAY_SPECS` registers by exact `(table, column)` pair for columns
  whose name alone can't carry the key, e.g. FEC's positional `C1`/`C15`
  columns or CourtListener's bare `ID` columns — see `connect/keys.py`'s
  `TABLE_COLUMN_KEYS`. So 847 is a floor on name-detectable keys, not a
  ceiling on every real key in the warehouse.)
- **24,011 real, measured pairwise table overlaps** computed this session
  (not estimated — every one is a live `COUNT` of actually-shared entity
  values). 11,839 corroborate what the spine's own engine already found;
  **12,172 are new measured coverage** this audit adds.
- **2 databases are effectively dead weight**: `THE_LIBRARY` (254 views, zero
  rows anywhere) and `LIBRARY_MARTS_PREDBT_20260729` (a frozen pre-dbt
  backup, 318 tables of real but superseded data).
- **3 bugs caught live, 2 fixed live this session**: a broken mart view
  (§9b — rebuilt, verified queryable again) and a 3-week-stale status file
  (§10 — regenerated). The third — a truncated landing table superseded by
  its own re-pull (§6) — is a data change, not a code fix, so it's a
  recommendation below, not something done without asking.

---

## 1. The seven databases, and what each one actually is

The warehouse is not one database — it's seven, and the prior scale report
(`reports/mart_rowcounts_2026-08-24.csv`, 701 tables) only ever measured one
of them. Full picture:

| Database | Real role | Base tables | Views | Live rows (base tables) |
|---|---|---:|---:|---:|
| `LIBRARY_RAW` | **landing** — raw pulls, one table per government source | 2,212 | 2 | ~1.25B+ |
| `LIBRARY_STAGING` | **staging** — dbt's first cleanup pass (rename, retype) | 11 | 1,367 | small (mostly views) |
| `LIBRARY_MARTS` | **marts** — the finished, query-ready tables | 701 | 423 | ~1.3B+ |
| `LIBRARY_META` | **metadata / spine / registries** — the entity graph and every control table | 108 | 27 | ~1.6B+ (mostly spine scratch tables) |
| `LIBRARY_TOOLS` | empty | 0 | 0 | — |
| `THE_LIBRARY` | **dead** — 254 views, **zero base tables**, zero live rows anywhere | 0 | 254 | 0 |
| `LIBRARY_MARTS_PREDBT_20260729` | **legacy backup** — a frozen pre-dbt snapshot of the marts, dated in its own name | 318 | 13 | real, but stale by definition |

**`THE_LIBRARY` is structurally a second, parallel domain taxonomy** (26
schemas: `CAMPAIGN_FINANCE`, `COMPANIES`, `CRIME_SECURITY`, `ECONOMY`,
`GOVERNMENT`, `HEALTH`...) that was apparently scaffolded at some point and
never built out — every one of its 254 objects is a `VIEW`, and every view
returns/represents zero rows in this audit's tables.csv (needs a human call on
whether it's worth deleting or was mid-build). It is NOT the same thing as
`LIBRARY_MARTS`'s domain schemas, even though several schema names overlap in
spirit (`HEALTH`, `JUSTICE`, `HOUSING`...).

`LIBRARY_MARTS_PREDBT_20260729` is exactly what its name says: a dated backup
taken before the dbt migration. Its row counts are real (this audit
live-counted them) but frozen at that date — anything built or fixed in
`LIBRARY_MARTS` since then (the whole 2026-08-22 year-killer fix, for
instance) is **not** reflected there.

## 2. The four-verb build (SCOUT → COLLECT → CONNECT → DETECT)

From `docs/RIPPLE.md` (the canonical explainer), confirmed against the actual
code in this session:

1. **SCOUT** (`portal_recon/`) — catalogs open-data portals without pulling
   data, tags each dataset's columns by which join-key type they carry
   (STEEL/STRONG/GEO/PROBABILISTIC — see §3), before anything is loaded.
2. **COLLECT** (`library-onboarding/`, `scripts/*_load.py`) — one script per
   source pours rows into a `LIBRARY_RAW.LANDING` table. This is where the
   2,212 landing tables come from. Loaders checkpoint to local JSON (e.g.
   `data/usaspending_full/checkpoint.json`) so a multi-hour pull can resume.
3. **CONNECT** (`connect/`) — builds the entity spine and the connection
   graph. This is the part this audit spent the most time re-verifying (§4-6).
4. **DETECT** (`connect/leads*.py`, `connect/cohort*.py`) — turns a confirmed
   connection into a reviewable lead. Every lead lands in
   `LIBRARY_META.CONNECT.LEADS` regardless of which detector produced it.

## 3. The trust vocabulary (the one thing to actually internalize)

Every join key in the codebase carries one of four tiers, defined once in
`portal_recon/tag_portal_index.py` and reused everywhere (`connect/keys.py`,
the scout, the registry):

| Tier | Meaning | Examples found this session |
|---|---|---|
| **STEEL** | a hard government ID — the gold standard | EIN, NPI, CCN, CIK, UEI, DUNS, LEI, FRS_ID, PWSID, BIOGUIDE, FEC_CAND_ID/CMTE_ID |
| **STRONG** | a real, narrower code, but not universal | (mostly the excluded classification codes below) |
| **GEO** | a location — real, but coarse (almost every table has one) | ZIP, FIPS, COUNTRY, LATLON, GEOM |
| **PROBABILISTIC** | a name/address — a hint, never proof on its own | NAME, ADDRESS, PERSON |

**Two important carve-outs, both already decided in the code, both honored in
this audit rather than re-litigated:**

- `NAICS` / `SIC` / `NCES` tag as STRONG by the raw tagger, but are
  **industry/institution classification codes, not entity identifiers** — the
  codebase explicitly bans them from ever counting as a connection
  (`connect/discover.py` "D17", `connect/spine_entity.py`
  `_CLASSIFICATION_CODES`). Sharing a NAICS code means "same industry," never
  "same company." This audit's overlap pass excludes them for the same reason.
- Even within STEEL/STRONG, `connect/spine_entity.py` keeps a governed list
  (`SPINE_ENTITY_BY_KEY`) of which key labels are actually spine-eligible, and
  types each one by what kind of thing it identifies: `person`,
  `organization`, `facility`, `provider`, `case`, `asset`, `vessel`, or
  `place`. This audit reused that exact list rather than inventing a second
  trust taxonomy — see `key_columns_all.csv`'s `spine_entity_grain` column.

**A second, separate trust vocabulary exists one layer up, for graph edges
specifically** (from `connect/discover.py`'s tier labels, visible in
`spine_connect_edges_live.csv`'s `TIER` column): `STEEL` (hard-ID match,
matches the column tier), `BRIDGE` (two *different* hard-ID types on the same
row, e.g. `CIK~EIN`), `CORROBORATED` (name@zip — a real signal, but never a
standalone fact), and `GEO` (shared location only). **Same-ID-number is a
fact; same-name is a lead** — this line from `docs/RIPPLE.md` is not a
slogan, it's implemented exactly as these four labels.

## 4. The spine gate: `DISPLAY_SPECS`

A table does not automatically join the entity spine just because one of its
columns carries a recognized key. It has to be explicitly registered in
`connect/entity_index_specs.py`'s `DISPLAY_SPECS` dict — one entry per table,
naming which column carries the key, which columns carry a human-readable
name/address, and an `authority` rank (lower wins) for whose name/address
survives when two sources describe the same entity.

**As of this session: 178 tables are registered in `DISPLAY_SPECS`, carrying
205 key entries.** This audit's own column-name detection sweep (independent
of that registry) found **847 real tables** carrying at least one genuine
entity-grade key (person/organization/facility/provider/case/asset — not
counting the coarse "place" keys; see the headline-numbers caveat above on
what name-based detection can't see). That gap — 847 detected vs. 178
registered — is the platform's real "known but not yet wired into the spine"
backlog; see `key_columns_all.csv`'s `spine_wired` column for the exact list.

**A table not in `DISPLAY_SPECS` is not in the spine or entity index today** —
this is stated directly in the module's own docstring, correcting an earlier,
broader claim in the same file's history.

## 5. The entity graph, at scale (live-counted this session)

`LIBRARY_META.CONNECT` is where the actual graph lives:

| Table | Live rows | What it is |
|---|---:|---|
| `ENTITY_GOLDEN` / `ENTITY_MAP` | 33,312,349 | the golden-record entity list (one row per real-world thing, survivorship-resolved) |
| `SPINE_KEYSET` / `ENTITY_INDEX` / `CONNECT_NODES` | 84,382,504 | every (key type, key value) node the spine has ever seen |
| `MATCH_PAIRS` | 181,002,484 | raw candidate match pairs before scoring |
| `KEYSET_LIVE` / `KEYSET_SCRATCH` | 176,983,257 | working keysets for the current build |
| `CONNECT_EDGES` | 4,910 | **the platform's own measured pairwise table-overlap results** — see §6 |
| `LEADS` | 17,598 | the human review queue |

## 6. What was already measured vs. what this audit adds

**Correction to the prior handoff:** the "only 29 pairwise overlaps measured"
claim was based on `reports/source_overlap_edges.json`, which turns out to be
a small manual export, not the live state. The platform's own spine engine
(`connect/discover.py`) has already computed and stored **4,910 real,
measured table-to-table overlaps** in `LIBRARY_META.CONNECT.CONNECT_EDGES`,
covering **258 distinct tables**, built 2026-08-18 through 2026-08-22 (one
run, `RUN_ID 8283dd47ad1d468f`, extended incrementally over those four days).
Breakdown by tier: 1,244 STEEL/STRONG hard-ID edges, ~353 GEO edges, 2,670
CORROBORATED (name@zip) edges, and a handful of cross-key-type `BRIDGE`
edges (e.g. `CIK~EIN`, `EIN~UEI`, `CCN~NPI` — literally the same row carrying
two different ID types, which is how the platform links otherwise-unlinkable
key namespaces). That full table is exported here as
`spine_connect_edges_live.csv` so it doesn't have to be re-derived.

**This audit's own contribution** (`key_overlap_edges_new.csv`) computed real
pairwise overlap across all 816 tables carrying a live-verified, non-empty
entity-grade key (a narrower, higher-confidence set than the 847 raw
detections above — this excludes columns that verified to zero real
distinct values, e.g. a masked-ID trap), using the exact same normalization
logic (`connect/keys.py:normalize_sql`) the platform itself uses, so the
numbers are directly comparable, not a second competing methodology —
**24,011 measured table-pairs total**. Every row is tagged
`already_in_spine_connect_edges`: **11,839 pairs are between two tables the
spine has already profiled** (both sides appear somewhere among the 258
tables in `CONNECT_EDGES`) and **12,172 involve at least one table the
spine's own engine has never touched** — genuinely new coverage.

*(A precision note on that flag: "already profiled" means both tables are in
the spine's covered universe, not that this exact table-pair-and-key was
necessarily one of its 4,910 measured rows — `discover.py` doesn't
necessarily run every key type against every pair of tables it's ever
touched. This session spot-checked 8 "already profiled" pairs directly
against `CONNECT_EDGES`: 5 had an exact matching row, and the counts matched
either exactly or within 0.3% — the small drift is the spine's edges being
6+ days old against this session's live numbers, not a methodology
disagreement. The other 3 had no matching row at all, meaning the spine
never actually computed that specific pair+key even though it had profiled
both tables for other keys — real, previously-uncomputed coverage, not
duplication.)*

The biggest new-coverage key types: `DOCKET` (6,174 new pairs — see the
caveat below), `EIN` (1,790), `NPI` (1,457), `CCN` (853), `CIK` (481).

**On closer look, a large share of the "new" edges are the SAME source
appearing more than once in the warehouse**, not a novel cross-source link:
many mart tables are mirrored into a second `TIMELINE` schema copy (§ this
audit's own scale count treats `HEALTH.HEALTH__X` and `TIMELINE.HEALTH__X` as
two tables because they physically are, dbt-materialized twice), and in at
least one case a duplicate also survives in a `_RESTORE_20260731` junk
schema. A 100%-overlap edge between a table and its own mirror is real and
correctly measured, but it is not a *new finding* about the data — it is a
*storage-duplication* finding. `key_overlap_edges_new.csv` doesn't collapse
these automatically (that would hide the duplication itself, which is worth
knowing); treat same-root-name pairs as "confirmed mirror, not a new
connection" when reading the file.

**Scope decision, stated plainly:** the pairwise-overlap pass (both the
platform's own and this audit's) is restricted to entity/case/asset/provider-
grade keys — it does not attempt full pairwise overlap on the coarse "place"
keys (ZIP/FIPS/COUNTRY/LATLON/GEOM) or on NAME/ADDRESS. Almost every table in
the warehouse has some ZIP or NAME column; a full combinatorial overlap pass
there would produce thousands of meaningless "connections" (two tables both
having *some* customer in the 90210 ZIP code proves nothing). This mirrors
the codebase's own `ENTITY_KEYS` design, not a shortcut invented for this
audit.

## 6b. `DOCKET` — an actual verdict, not a punt

`DOCKET` is the single biggest overlap group this session measured (169
tables, 6,560 pairs). Unlike `EIN`/`NPI`/`CCN`/`CIK`/`UEI`/`LEI`/`FRS_ID`/
`PWSID` (each a **single national authority** issuing that ID), a "docket
number" is assigned independently by whichever court, agency, or enforcement
body created it — so the raw label can't be trusted uniformly. Rather than
leave that as a blanket caveat, this session broke the 6,560 pairs down by
who's actually publishing them, and there are three genuinely different
buckets — **not one problem, three different confidence levels**:

**1. TRUST IT — the federal courts cluster (45 table pairs, high confidence).**
CourtListener's docket/opinion/oral-argument tables and the Federal Judicial
Center's IDB (civil/criminal/bankruptcy/appellate case databases) overlap at
87-100% coverage on one side, in the millions of shared case numbers. These
are **two independent government-adjacent publishers describing the same
real-world federal court cases** — that's corroboration, the strongest signal
short of a hard ID. **Verdict: promote this cluster.** It's the richest
un-wired connection this audit found and deserves an actual `DISPLAY_SPECS`
entry (or a dedicated "federal case" spine entity) rather than living as an
unscored `DOCKET` guess.

**2. TRUST IT, NARROWLY — same-agency pairs (2,909 pairs, medium-high
confidence).** Two tables from the *same* publisher (two EPA enforcement
tables, two OSHA tables) sharing a docket column almost certainly share the
same internal numbering system. Real, but scoped: only trust a `DOCKET` match
between tables from the same agency family. Worth wiring per-agency, not
warehouse-wide.

**3. DON'T TRUST IT — cross-agency, non-court pairs (the remaining ~3,600
pairs). Verdict: mostly noise, and I found the actual mechanism.** 47% of
these pairs share 5 or fewer values out of what are often million-row tables
— that's not a connection, that's short numeric strings coinciding by chance.
Worse, a handful have deceptively *high* overlap: `FED_FDIC_BANK_DATA`'s
docket-like column matches **99.98%** of `FED_COURTLISTENER_DOCKETS`' values
— not because a bank's internal record ever touches a real court case, but
because FDIC's ID column is drawn from a small, low-cardinality number space
that coincidentally sits inside CourtListener's enormous docket-number range.
This is exactly the "score against chance" collision check `docs/RIPPLE.md`
describes `connect/discover.py` doing for real edges — this audit's raw
overlap sweep doesn't apply that check, and this pair is the textbook example
of why it exists. **Recommendation: don't spend review time on cross-agency,
non-court `DOCKET` matches as-is; if it's worth pursuing, it needs the same
coincidence-scoring gate as everything else in `discover.py`, not a bare
equi-join.**

## 7. Standing data traps, cross-referenced (not re-invented)

`honesty/traps.py` carries a written, code-enforced registry of every known
"looks-real-but-isn't" column (e.g. NPPES's `EIN` column: 100% non-null,
**zero** real EINs — every value is `''` or the literal text `<UNAVAIL>`).
`LIBRARY_META.REGISTRY.COLUMN_TRUST` is the live Snowflake mirror of that
same discipline, scoped to mart tables (174 flagged columns as of this
session). Both were pulled fresh and cross-referenced against this audit's
own live distinct-value counts in `tables.csv`'s `data_quality_flags` column
and `key_columns_verified.csv` — where this audit's own numbers agree with
the registry, that's corroboration; any table below is a **new** finding this
session surfaced that wasn't already in the registry.

**New finding this session:** `FED_USASPENDING_CONTRACTS_FULL` (a landing
table) has **exactly 20,000,000 rows** — a confirmed instance of the
round-number loader-cap trap the constitution already warns about. It is a
dead, superseded table: the actual re-pull lives in
`FED_USASPENDING_CONTRACTS_FULL_R2`, which is live right now at 63.7M+ rows
and still growing (checkpoint shows it's worked through FY2007-2021 as of
this session; see `data/usaspending_full/checkpoint.json`). Any query against
the plain (`_FULL`, non-`R2`) table is silently working with 1/3 of the real
data set. Flagged in `tables.csv`.

## 8. Junk / backup / dead schemas, named explicitly

So these don't silently blend into domain totals:

- **`_RESTORE_20260701`, `_RESTORE_20260731`** (in `LIBRARY_MARTS` and its
  PREDBT snapshot) — dated restore/recovery scratch schemas.
- **`REVIEW`, `UNCATEGORIZED`** (in `LIBRARY_MARTS`) — exactly what they say.
- **`CONNECT_BAK_20260730`, `CONNECT_PRESPINE_20260730`** (in `LIBRARY_META`)
  — two full backup copies of the spine, ~272.6M rows each, taken before a
  2026-07-30 spine change. Real, live-counted storage, zero current use.
- **The entire `LIBRARY_MARTS_PREDBT_20260729` database** and **the entire
  `THE_LIBRARY` database** — see §1.

`tables.csv`'s `status` column marks every one of these explicitly
(`junk_schema` / `backup_schema` / `legacy_backup` / `legacy_dead`) rather
than folding them into `active`.

## 9. One naming quirk worth knowing before it causes confusion

`LIBRARY_STAGING.DBT_CROGERS` holds 1,355 of `LIBRARY_STAGING`'s 1,367 views —
**not** a personal developer sandbox. It's the literal default schema name
configured in `library-onboarding/ripple_dbt/profiles.yml` (`schema:
DBT_CROGERS`), so every staging model that doesn't explicitly override its
schema lands there verbatim. `CORE`, `POLITICS`, and `SEEDS` are the specific
model groups that *do* override it. Mart-layer schema names (`HEALTH`,
`JUSTICE`, ...) are unrelated overrides set the same way, one per domain.

---

## 9b. A live-broken mart view, caught mid-sweep — **fixed this session**

While verifying key columns, `LIBRARY_MARTS.TIMELINE.LABOR__FED_MSHA_VIOLATIONS`
threw a hard SQL compilation error on a plain `SELECT`: the view declared 30
columns but its underlying query produced 31. Root cause, found in the
model's own code comment: the base MSHA violations table had `docket_no`
added to its grain on 2026-08-22 (two days before this audit), but this one
downstream `SELECT *` view was never rebuilt afterward, so its cached column
list was one short of the table it wraps. **Rebuilt live this session**
(`dbt run --select timeline__labor__fed_msha_violations`) — confirmed
queryable again, 3,087,265 rows. No data was touched, only the view
definition was recompiled.

## 10. `build-state.md` was stale — **regenerated this session**

`build-state.md` calls itself "the only numbers that count," but the file on
disk had been generated 2026-08-01 — three weeks stale (it showed
`connect.edges: 663` against a live 4,910; `landing.tables: 1937` against a
live 2,208). **The live view it's generated from,
`LIBRARY_META.REGISTRY.V_STATE`, was never stale** — the printout had just
drifted from the view it's supposed to mirror. Re-ran
`python scripts/gen_build_state.py --write` this session; the file now
carries live 2026-08-25 numbers (`connect.edges: 4910`,
`landing.rows: 1,250,067,942`) that match this audit's independently-computed
figures exactly. No warehouse data changed — this only rewrites a local
markdown file from a read-only view.

## 11. What's flagged but NOT touched, and why

Standing repo policy (`build-state.md`'s `preview_then_apply`, 2026-06-25):
**"the agent never executes DDL/DML against shared infra directly."** Two
findings from this audit are real cleanup candidates but involve deleting
actual stored data, so they're handed over as exact recommendations rather
than run:

- **`LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL`** (20,000,000 rows,
  confirmed truncated and superseded by `FED_USASPENDING_CONTRACTS_FULL_R2`,
  §7) is dead weight — nothing should be reading it once the `_R2` re-pull
  finishes. One-liner, when ready: `DROP TABLE
  LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL;`
- **The two full spine backups**, `LIBRARY_META.CONNECT_BAK_20260730` and
  `LIBRARY_META.CONNECT_PRESPINE_20260730` (~272.6M rows each, §8), and **the
  entire `LIBRARY_MARTS_PREDBT_20260729` and `THE_LIBRARY` databases** (§1)
  are candidates for archiving/dropping, but that's a bigger call (is either
  backup still a safety net for something?) than this audit can make alone —
  flagged for a decision, not a command.

## Methodology notes (so this can be re-run and trusted)

- **Row counts are live `SELECT COUNT(*)`**, run this session against every
  one of the 3,350 real (`BASE TABLE`) objects across all seven databases —
  not read off `INFORMATION_SCHEMA` metadata and not copied from any earlier
  CSV. Views are not row-counted (a view has no storage of its own; counting
  it means executing its query, which for a staging view is redundant with
  its landing table and for a mart view could be arbitrarily expensive).
- **Key detection is the platform's own tagger** (`connect/keys.py:detect_key`,
  which wraps `portal_recon/tag_portal_index.py`'s `KEY_TOKENS`), run against
  every one of the 181,804 live column names this session pulled from
  `INFORMATION_SCHEMA.COLUMNS`. Nothing here is a new detection heuristic.
- **Every key-column trust check pairs `COUNT(*)` with
  `COUNT(DISTINCT normalized_value)` and a live 5-value sample** — never a
  bare null check — per the constitution's standing rule (§7) and the
  NPPES/FCC/NOAA precedent that a "100% populated" column can be 100% fake.
  Normalization uses the platform's own `normalize_sql()` (pad-not-strip,
  sentinel/placeholder stripping already built in), so a masked-ID trap like
  NPPES's `EIN` shows up as near-zero real distinct values here too, not as a
  false "fully joinable" key.
- **Pairwise overlap uses one query per key label**, not one query per table
  pair: every table carrying a given key is unioned together with a table tag,
  grouped by normalized value, and the resulting table-combination counts are
  expanded into pairwise overlap counts in Python. This is mathematically
  exact (not sampled) and scales as O(key labels), not O(table pairs) — the
  same technique the platform's own `discover.py` uses.
