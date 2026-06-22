# Wave 3 — Portal Dataset Index → Snowflake + Confidence-Tiered Join Keys

**Goal:** get the 338k-dataset Wave-2 index out of git and into a queryable
Snowflake table, and tier every join-key match by confidence so you can search
338k datasets by *what they actually connect to*.

---

## Status

| Step | What | State |
|---|---|---|
| 1 | Load index → `LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX` | ✅ **Loaded + count-verified in Snowflake (338,520)** |
| 2 | Confidence-tier every dataset (STEEL/STRONG/GEO/PROB) | ✅ **Tagged; distribution matches the local run exactly** |
| 3 | Example queries (step 3 of the peel, as SQL) | ✅ Run against the live table — counts below |
| 4 | This brief + PR | ✅ |

**It's done, end to end.** Fresh PAT came in, the loader ran, and Snowflake
independently confirms **338,520 rows** with a tag distribution that matches the
offline computation to the dataset. The master index is live and queryable at
`LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX`.

> Every count below was **confirmed in Snowflake this session** — not just computed
> locally. (Role: `CLAUDE_MCP_READONLY`, which holds `CREATE TABLE` on the REGISTRY
> schema; warehouse `DBT_WH`.)

---

## Row count — verified

- **Source index: 338,520 datasets** — independently re-counted by streaming the gz
  (matches Wave-2's `totals.datasets_indexed` exactly).
- **Snowflake `COUNT(*)` = 338,520** — confirmed this session. The loader gates on
  this (it refuses to tag unless the count matches) and it passed. No delta.

---

## The big caveat: only 78,651 datasets expose their columns

You can't tag a join key you can't see. Of 338,520 datasets:

- **78,651 (23%) expose column names** → these are the only ones that can be tagged.
- **259,869 (77%) don't** → mostly ArcGIS feature listings + CKAN packages whose
  resources weren't column-enriched. They load fine (`top_tier = NULL` =
  "untaggable"), they're just not join-searchable until columns are harvested.

So the tier breakdown below is **out of the 78,651 taggable set**, not 338k.

---

## Step 2 — Tier breakdown (the payoff)

Of the **78,651** column-known datasets:

| Top tier | Datasets | What it means |
|---|---:|---|
| 🔩 **STEEL** | **185** | hard entity ID — CCN, NPI, EIN, PATENT, DUNS, UEI |
| **STRONG** | **563** | domain-native ID — NAICS, SIC, DOCKET, NCES |
| **GEO** | **47,438** | FIPS / ZIP / lat-lon / country / geometry |
| **PROBABILISTIC** | **9,834** | only a name/address column — fuzzy, never clean |
| NONE | **20,631** | columns known, but carry no join key |
| *(untaggable)* | *259,869* | columns not exposed by the source |
| **Carries ≥1 key** | **58,020** | of the taggable set |

**By join key** (a dataset can carry several):

| Key | Tier | Datasets |
|---|---|---:|
| GEOM (geometry) | GEO | 36,242 |
| NAME | PROB | 32,507 |
| ADDRESS | PROB | 16,981 |
| ZIP | GEO | 11,913 |
| LATLON | GEO | 7,796 |
| FIPS | GEO | 4,435 |
| COUNTRY | GEO | 1,676 |
| NAICS | STRONG | 364 |
| SIC | STRONG | 153 |
| DOCKET | STRONG | 145 |
| **CCN** | STEEL | 92 |
| **NPI** | STEEL | 44 |
| NCES | STRONG | 31 |
| **EIN** | STEEL | 30 |
| **PATENT** | STEEL | 15 |
| **DUNS** | STEEL | 6 |
| **UEI** | STEEL | 2 |

---

## Honest tiering — what I did to *not* inflate steel

The task was blunt: *a false steel tag is worse than no tag.* So:

- **I audited every ambiguous steel key against its real columns.** CCN, NPI, EIN,
  PATENT all checked out — CCN is `CCN`/`CCN_` on hospital/renal/surgical datasets
  (CMS Certification Number ✓); EIN is `EIN`/`OrgEIN` on nonprofit datasets ✓;
  PATENT is `patent_no`/`patent_number` ✓.
- **I dropped DOI entirely.** A `doi` column *sounds* like a digital object
  identifier (steel), but all 8 hits were noise: `median_days_doi_to_order...`
  (**Date Of Injury**) and `DOI_Aggregate`/`DOI_Concentration` (an env-justice
  **Demographic Index**). Zero real DOIs → not tagged. That's the discipline working.
- **Whole-token matching**, camelCase-aware: `ein` matches `EIN`/`ein_number` but
  never `protein`. Generic columns (`id`, `name`-alone-as-noise, `date`, `value`)
  are **not** key matches.
- **Tiered down where ambiguous:** bare `iso` is *not* tagged COUNTRY (could be an
  ISO date/currency) — COUNTRY needs `country`/`iso2`/`iso3`/`iso3166`.
- **Not auto-tagged steel:** NDC and CUSIP are real hard IDs but weren't in the
  steel set for this pass — easy to add later if you want them.
- **Cross-checked vs Wave-2's boolean flag:** LATLON (7,796), NAICS (364), SIC (153),
  NPI (44), EIN (30), DUNS (6), UEI (2) match to the dataset. My deltas are
  explained — I added token variants (`statefp`, `zcta5`, `postal_code` pair) and
  net-new keys (GEOM, NAME, ADDRESS, DOCKET, NCES, CCN, PATENT).

---

## Step 3 — The peel, as SQL (`portal_index_queries.sql`)

Four queries, **run against the live Snowflake table** — these are the counts they
returned:

| # | Query | Returns |
|---|---|---:|
| 1 | Every dataset carrying **EIN** (org backbone) | **30** |
| 2 | Every **STEEL-tier** dataset (precise connectable set) | **185** |
| 3 | Datasets **by portal, ranked** (richest boxes) | **96** portals |
| 4 | Datasets with **a GEO key AND a STEEL key** (cross-joinable gold) | **145** |

Spot-check of a real row (proves the array + URL landed): NY State's *Database of
Economic Incentives* → `join_keys = ["EIN","ZIP","ADDRESS","NAME"]`, `top_tier =
STEEL`, `source_url = https://data.ny.gov/d/26ei-n4eb`.

**Richest portals (query 3, top of the list):**

| Datasets | Portal |
|---:|---|
| 25,000\* | Open Government Portal Canada (open.canada.ca) |
| 25,000\* | data.gov.au |
| 25,000\* | UK National Data Library (data.gov.uk) |
| 25,000\* | Humanitarian Data Exchange (HDX) |
| 25,000\* | Virginia Open Data Portal |
| 22,328 | Ireland (data.gov.ie) |
| 20,900 | Greece (data.gov.gr) |
| 20,739 | Netherlands (data.overheid.nl) |

\* capped at the Wave-2 per-portal harvest limit (25k) — these are **floors**, not
true portal totals.

---

## Where the master index lives now

- **Target table:** `LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX` (one new table, as
  scoped — no dbt models, no landing tables, no portal data ingested).
- **Columns:** `dataset_uid` (PK), `portal_source_id`, `portal_name`, `platform`,
  `dataset_title`, `dataset_id`, `column_names` (ARRAY), `row_count`, `last_updated`,
  `source_url`, **`join_keys`** (ARRAY), **`top_tier`**.
  - `dataset_uid` + `portal_source_id` are additive: a PK for the index, and the
    SOURCE_ID hook back into `SOURCE_REGISTRY`.
  - `source_url` is best-effort: the explicit dataset URL where the API gave one
    (Socrata `permalink`, ArcGIS service URL), else the platform-standard dataset
    page (`/d/{id}`, `/datasets/{id}`, `/dataset/{id}`).
- **The 57MB gz no longer needs to live in git.** The queryable truth is now in
  Snowflake; the gz stays as a local/Wave-2-branch backup and is `.gitignore`d here
  so it won't bloat this branch.

---

## ✅ Loaded & verified (Snowflake-confirmed)

The fresh PAT landed, the loader ran, and Snowflake confirms it. The distribution it
printed back matches the offline run to the dataset:

| Snowflake `GROUP BY top_tier` | Datasets |
|---|---:|
| UNKNOWN_COLUMNS (NULL) | 259,869 |
| GEO | 47,438 |
| NONE | 20,631 |
| PROBABILISTIC | 9,834 |
| STRONG | 563 |
| STEEL | 185 |
| **total** | **338,520** |

**To refresh it later** (it's idempotent — `CREATE OR REPLACE`, count-gated):

```bash
# fresh PAT in library-onboarding/.env  (SNOWFLAKE_PAT=...)
cd portal_recon
set -a; source ../library-onboarding/.env; set +a
# restore the input gz on a fresh container (it's gitignored):
#   git cat-file blob 058bed7 > portal_datasets_index.json.gz   # from the Wave-2 branch
python tag_portal_index.py --load        # reloads, re-verifies count==338,520, re-tags
```

The loader self-gates: it **refuses to tag** unless Snowflake `COUNT(*)` equals
338,520 first. This run passed the gate.

---

## Files

- `tag_portal_index.py` — loader + tagger (`--local` / `--selftest` / `--load`)
- `portal_index_queries.sql` — the four peel queries
- `portal_index_tier_summary.json` — machine-readable breakdown
- `PORTAL_INDEX_WAVE3_BRIEF.md` — this brief
