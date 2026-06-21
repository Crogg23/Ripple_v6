# Wave 3 — Portal Dataset Index → Snowflake + Confidence-Tiered Join Keys

**Goal:** get the 338k-dataset Wave-2 index out of git and into a queryable
Snowflake table, and tier every join-key match by confidence so you can search
338k datasets by *what they actually connect to*.

---

## Status

| Step | What | State |
|---|---|---|
| 1 | Load index → `LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX` | ⛔ **BLOCKED — the PAT is dead** |
| 2 | Confidence-tier every dataset (STEEL/STRONG/GEO/PROB) | ✅ **Done + verified over all 338,520** |
| 3 | Example queries (step 3 of the peel, as SQL) | ✅ Written; counts computed locally |
| 4 | This brief + PR | ✅ |

**The tagging is the hard part and it's done and proven.** The only thing standing
between this and a loaded, queryable table is a working Snowflake token — the one in
the container is revoked (details at the bottom). **Drop a fresh PAT in
`library-onboarding/.env` and run one command** (also at the bottom) and it loads +
verifies itself.

> I have **not** asserted the table loaded — I couldn't reach Snowflake this session,
> so every count below is computed locally from the source index. They're the values
> the Snowflake queries will return once it's loaded.

---

## Row count

- **Source index: 338,520 datasets** — independently re-counted by streaming the gz
  this session (matches Wave-2's `totals.datasets_indexed` exactly).
- Snowflake `COUNT(*)`: **pending the load.** The loader refuses to tag the table
  unless its count equals 338,520 first (hard gate).

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

Four queries, with the counts they return (computed locally; Snowflake will match):

| # | Query | Returns |
|---|---|---:|
| 1 | Every dataset carrying **EIN** (org backbone) | **30** |
| 2 | Every **STEEL-tier** dataset (precise connectable set) | **185** |
| 3 | Datasets **by portal, ranked** (richest boxes) | **96** portals |
| 4 | Datasets with **a GEO key AND a STEEL key** (cross-joinable gold) | **145** |

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
- **The 57MB gz no longer needs to live in git.** Once this loads, the queryable
  truth is in Snowflake; the gz stays as a local/Wave-2-branch backup and is now
  `.gitignore`d here so it won't bloat this branch.

---

## ⛔ The blocker — and the one thing to fix it

The container's `SNOWFLAKE_PAT` is **revoked**: every call returns
`401 — "Programmatic access token is invalid."` (Its JWT `exp` is 2027, so it's not
a clock-expiry — it was rotated server-side.) There's **no `library-onboarding/.env`**
to override it with, and no password fallback. So I can't create the table, load it,
or verify the count this session — and I won't claim otherwise.

**To finish (≈10–15 min of Snowflake time):**

```bash
# 1. put a fresh PAT in library-onboarding/.env  (SNOWFLAKE_PAT=...)
cd portal_recon
set -a; source ../library-onboarding/.env; set +a   # override=True wins over stale env

# 2. restore the input gz if this is a fresh container (it's gitignored now):
#    git cat-file blob 058bed7 > portal_datasets_index.json.gz   # from the Wave-2 branch

# 3. eyeball the SQL it will run, then load for real:
python tag_portal_index.py --load --dry-run
python tag_portal_index.py --load        # creates table, loads, VERIFIES count, tags
```

The loader self-gates: it **refuses to tag** unless Snowflake `COUNT(*)` equals
338,520 first. When it finishes it prints the tier distribution — which should match
the table above.

> Heads-up: the `--load` path is built to the proven Wave-1 REST-API pattern but
> **hasn't been run against Snowflake this session** (no live PAT). `--dry-run` prints
> the exact DDL + a real batch so you can sanity-check before it writes. The
> `--local`/`--selftest` paths are fully verified.

---

## Files

- `tag_portal_index.py` — loader + tagger (`--local` / `--selftest` / `--load`)
- `portal_index_queries.sql` — the four peel queries
- `portal_index_tier_summary.json` — machine-readable breakdown
- `PORTAL_INDEX_WAVE3_BRIEF.md` — this brief
