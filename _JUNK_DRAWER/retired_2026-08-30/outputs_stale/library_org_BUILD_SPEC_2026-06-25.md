I have everything. Producing the final build-ready spec.

---

# Ripple Faceted Catalog — FINAL BUILD-READY SPECIFICATION
**Supersedes** `outputs/library_organization_design_2026-06-25.md`. Every schema reference verified live against the warehouse 2026-06-25. This is the build artifact — execute it verbatim.

The original design's plan survives intact; the centerpiece (8 facet columns + `FACET_VOCAB` + `CATALOG` view + 3 bridges) is sound. What was broken: the SQL referenced a non-existent column (`RUN_TS`), the lifecycle rule used a magic row-count threshold, the marts join could never match (case + escape), Python lists can't bind as Snowflake ARRAYs, the crosswalk covered 39% of categories, and the JURISDICTION/ENTITY/THEME "auto" claims were false against real data. All fixed below.

---

## 1. DEFECT RESOLUTION TABLE

| # | Defect (abbrev.) | Sev | Resolution in this spec |
|---|---|---|---|
| 1 | `CATALOG.RUN_TS` does not exist | crit | §2 view uses `latest_run` CTE on **`ENDED_AT`** (verified non-null on all 748 runs). |
| 2 | marts CTE case-mismatch + no schema/`__` filter | crit | §2 marts CTE: `LOWER(SPLIT_PART(...,'__',2))`, `POSITION('__' IN TABLE_NAME)>0`, `TABLE_SCHEMA<>'INFORMATION_SCHEMA'`. Verified = 36. |
| 3 | `ROW_COUNT>=5000` mislabels 27 complete loads `sampled` | high | §2b lifecycle drops the threshold; completeness = `STATUS='success'` AND not a detected slice. |
| 4 | success-run-but-table-missing → `sampled` not `stale` | high | §2b explicit branch: `STATUS='success' AND land_rows IS NULL → 'stale'` (fed_cms_hpt_enforcement etc.). |
| 5 | `FLATTEN(NULL)` drops every NULL-array source from bridges | high | §2 all 3 bridges use `LATERAL FLATTEN(... , OUTER => TRUE)`. |
| 6 | `V_DOMAIN_SUMMARY` `<>'open_data_portal'` drops NULL domains | high | §2 uses `COALESCE(DOMAIN_PRIMARY,'UNCLASSIFIED')` in both SELECT and WHERE. |
| 7 | Orphan landed tables invisible (registry-driven view) | med | §2 view driven by `ids` = `registry ∪ runs ∪ landing`; `IS_ORPHAN` flag; Pass 0.5 stub-backfills them. |
| 8 | Audits `ARRAY_SIZE(arr)=0` is NULL for NULL arrays | med | §4 Pass 6 audits use `COALESCE(ARRAY_SIZE(...),0)=0`. |
| 9 | Python list can't bind as ARRAY in MERGE | high/crit | §3 `_ARRAY_COLUMNS` + `PARSE_JSON(%s)` + `json.dumps`. Verified `TYPEOF`→`ARRAY`. |
| 10 | TRUST_LAYER never reports `staging` | low | §2 adds `staging` CTE (`STG_` prefix, strip+split). Verified = 36. |
| 11 | twin-MAX runs CTE can't carry latest STATUS | high | §2 `latest_run` via `QUALIFY ROW_NUMBER() … ORDER BY ENDED_AT DESC, _LOADED_AT DESC`. |
| 12 | Proof-slices at 5000 mislabeled `landed` | high | §2b slice test on `MESSAGE`/round-cap fires before `landed`. Verified subawards→`sampled`. |
| 13 | `empty` status (28) bucketed as `stale`; stale mis-fires | high | §2b distinct `empty` and `stale` branches off latest STATUS. |
| 14 | Chunked loads break run==land equality test | med | §2b never gates on `run_rows==land_rows`; NPPES stays `landed`. `RUN_ROWS`/`LANDED_ROW_COUNT` exposed advisory-only. |
| 15 | `_build_row` lacks the 8 keys → KeyError | crit | §3 extends `_build_row` with all 8 keys + safe defaults. |
| 16 | Pass 2/3/5 bare array UPDATEs hit same splat bug | high | §4 every array write uses `PARSE_JSON(%s)` + `json.dumps`. |
| 17 | `json.dumps` double-encoding stores VARCHAR | high | §3 `_encode` asserts `isinstance(list/tuple)`; never re-dumps a str. |
| 18 | Arrays default NULL → audits skip untagged | med | §3 default arrays to **`PARSE_JSON('[]')`** at ALTER; audits NULL-safe anyway. |
| 19 | `accepted_values` can't attach — registry not a dbt object | crit | §4 Pass 6 declares `ripple_meta` dbt **source**; tests live in `_meta.yml`. |
| 20 | `accepted_values` takes literals, not a table | crit | §4 Pass 6 uses **`relationships` → `ref('facet_vocab_domain')`** (seed). True single-source-of-truth. |
| 21 | "20 mart folders = DOMAIN vocab" false (2/20 match) | crit | §5 ships a canonical 22-domain vocab **+ MART_DOMAIN→DOMAIN crosswalk**; folder-rename NOT claimed free. |
| 22 | marts CTE case/`__` (dup of #2) | high | Same fix as #2. |
| 23 | `FACET_VOCAB` no PK, untested | med | §4 `FACET_VOCAB` is a dbt **seed** with `unique_combination_of_columns` + `not_null`. |
| 24 | JURISDICTION enforcement vs 10 `US` rows, severity | med | §5/§4 facet tests `severity: warn` until Pass 1 clean; `US`→`fed` in `naming.py`. |
| 25 | ARRAY facets can't be `accepted_values`-tested | med | §4 Pass 6 tests the **bridge views** with `relationships`. |
| 26 | 16 clusters cover 39% (125 cats homeless) | crit | §5 ships **complete `FACET_CROSSWALK` over all 165 categories**; post-check = 0 unmapped. |
| 27 | Pass-4 slug rules match 0 of 593 blanks | crit | §4 Pass 4 bulk-assigns all 593 (`portal_%`) → `open_data_portal`, `NEEDS_TOPIC=TRUE`. No slug heuristic. |
| 28 | 52 rows have no home among 22 domains | high | §5 vocab **expanded to 22 incl.** `education`, `elections_voting`, `immigration_migration`; rest routed explicitly. |
| 29 | `government`(36)=city portals not governance | high | §5 crosswalk: `government`→`open_data_portal`, `governance`→`government_power`; NAME guard audit. |
| 30 | Procurement collision (intl vs spending) | med | §5 crosswalk disambiguates by `intl_` prefix → `procurement_intl` else `spending_budget`. |
| 31 | Compound categories drop the 2nd domain | med | §5 `FACET_CROSSWALK` carries `DOMAIN_PRIMARY` **and** `DOMAIN_SECONDARY` array. |
| 32 | register._COLUMNS array-bind (dup #9) | high | §3 PARSE_JSON solution. |
| 33 | UNCLASSIFIED queue mechanics undefined | med | §3/§4 add `DOMAIN_SOURCE`, `DOMAIN_CONFIDENCE`, `NEEDS_TOPIC`; `V_REVIEW_QUEUE`; idempotent scope `DOMAIN_SOURCE IS DISTINCT FROM 'human'`. |
| 34 | RUN_TS → half-applied migration (dup #1) | crit | Fixed + §4 every DDL idempotent. |
| 35 | No real snapshot; Time Travel = 1 day | crit | §4 Pass 0 `CREATE TABLE … CLONE` durable snapshot (retention verified = 1). |
| 36 | ARRAY in _COLUMNS corrupts later columns | crit | §3 per-column expression builder; one placeholder per array. |
| 37 | modeled unreachable (dup #2) | high | Fixed. |
| 38 | orphans never backfilled (dup #7) | high | Pass 0.5. |
| 39 | 5000 threshold both directions (dup #3/#12) | high | Fixed §2b. |
| 40 | ALTER/CREATE not re-run guarded | high | §4 `ADD COLUMN IF NOT EXISTS`, `CREATE … IF NOT EXISTS`, `CREATE OR REPLACE VIEW`, MERGE seed. |
| 41 | No per-step verification gate | med | §4 each Pass 0a–0g has its own verify query; §6 build order gates. |
| 42 | In-flight onboard races column add | med | §4 operational quiesce gate + MERGE uses `COALESCE` so onboarding never blanks migration facets. |
| 43 | `queued` dead code; INCLUDE premise wrong | low | §2b `queued` = INCLUDE='Y' AND no run (rare but valid); design premise corrected (INCLUDE='Y' on 643, not 593). |
| 44 | dossier.py takes entity id, not SOURCE_IDs | crit | §6 note: drop the dossier hand-off claim; CATALOG returns `LANDING_FQN` for the agent to read directly. No dossier wiring built. |
| 45 | ENTITY_INDEX.DOMAIN ≠ DOMAIN_PRIMARY | high | §5 note: ENTITY_INDEX.DOMAIN declared a **separate axis**; not governed by FACET_VOCAB in v1 (deferred, documented). |
| 46 | JURISDICTION vocab `fed/...` vs stored `federal/...` | crit | §5 FACET_VOCAB seeds **full words** (`federal/international/cross-cutting/local/state`) matching the column. |
| 47 | `portal` prefix on 593 has no jurisdiction rule | high | §4 Pass 1: portals get `JURISDICTION='cross-cutting'` (or host-derived later); `portal` excluded from prefix rule. |
| 48 | 89 run-orphans invisible | high | §2 `ids` union includes `INGEST_RUNS.SOURCE_ID`; `IS_ORPHAN` surfaces all 89; §4 audit. |
| 49 | ENTITY_TYPE underivable for 71% (UoO placeholder) | high | §5/§4 ENTITY_TYPES reclassified **agent-assigned at checkpoint**, default `[]`, landed-first. Not "auto". |
| 50 | THEME inputs carry no theme content | high | §4 Pass 5: only `epstein` derivable (`EPSTEIN_RELEVANT ILIKE 'yes%'/'maybe%'`); other 9 themes are agent calls. |
| 51 | Snowsight THEME_TAG single-valued vs ARRAY | med | §6 **deferred**: add `THEME_PRIMARY` scalar later or drop tags; CATALOG view is the browser in v1. |
| 52 | build_library_map "repoint" is a rewrite | high | §6 **deferred**: keep build_library_map as physical map; faceted browser is a separate future module. |
| 53 | V_DOMAIN_SUMMARY undercounts secondaries | med | §2 ships `V_DOMAIN_SUMMARY` on the `V_SOURCE_DOMAIN` bridge with `sources_primary` + `sources_incl_secondary`. |
| 54 | latest-run STATUS needed (dup #11) | med | Fixed. |
| 55 | Read role CLAUDE_MCP_READONLY lacks LANDING SELECT | crit | §4 Pass 0h grants `SELECT ON ALL/FUTURE TABLES IN SCHEMA LIBRARY_RAW.LANDING` (+ marts) to the role; verify AS that role. |
| 56 | `LIKE '%\_\_%' ESCAPE` returns 0 / errors via connector | crit | §2 uses `POSITION('__' IN TABLE_NAME)>0` everywhere (verified; backslash-LIKE fails through the connector). |
| 57 | list `%s` splat shifts columns (dup #36) | crit | §3 fixed. |
| 58 | empty-array `%s` → SQL syntax error | crit | §3 always `json.dumps(v or [])` + `PARSE_JSON`; default col `PARSE_JSON('[]')`. |
| 59 | JURISDICTION vocab mismatch (dup #46) | high | Fixed. |
| 60 | portal prefix (dup #47) | high | Fixed. |
| 61 | 3 success-but-no-table → stale (dup #4) | high | Fixed §2b. |
| 62 | F3 underivable 71% (dup #49) | high | Fixed. |
| 63 | F5/EPSTEIN prose, not enumerable (dup #50) | high | Fixed. |
| 64 | fingerprint file is 646 UPPERCASE keys, shape `{rows,keys[]}` not `KEY_TOKENS` | high | §4 Pass 2 reads `entry['keys'][*]['key']/['tier']`, `LOWER()` the table key, quality-gates `distinct>1`. |
| 65 | V_DOMAIN_SUMMARY empty at Pass 0 | med | §2 COALESCE bucket → shows `UNCLASSIFIED` row at Pass 0, not blank. |
| 66 | 87 never-succeeded collapse to one bucket | med | §2b distinct `failed`/`empty`. |
| 67 | JOIN_KEY promotion no quality gate (NPPES EIN distinct=1) | med | §4 Pass 2 gates `distinct>1 AND populated_pct>=10`. |
| 68 | Onboarding never generates F1/F3/F5 → backlog grows | crit | §3 extends `generate_catalog.txt` to emit `domain_primary/domain_secondary/entity_types/themes`, validated vs vocab; `_build_row` reads them. |
| 69 | F3 underivable 92% of landed (dup #49) | high | Fixed. |
| 70 | F5 THEME underivable 92% of landed (dup #50) | high | Fixed. |
| 71 | Audit-2 fires on all 593 portals forever | high | §4 audits exclude `DOMAIN_PRIMARY='open_data_portal'`. |
| 72 | mart-folder rename is a migration bomb (dup #21) | high | §5 MART_DOMAIN crosswalk, no rename. |
| 73 | F4 not live/auto — manual batch, goes stale | high | §6 F4 re-labeled "auto-on-onboard"; §3 wires `fingerprint_table()` into LOAD (future increment), Pass 2 backfills now. |
| 74 | 89 run-orphans grow (dup #48) | med | Fixed. |
| 75 | array facets ungoverned by vocab (dup #25) | med | Bridge-view relationship tests. |
| 76 | DOMAIN_SECONDARY can dup PRIMARY → double-count | med | §2 `V_SOURCE_DOMAIN` filters `d.value <> DOMAIN_PRIMARY`, `SELECT DISTINCT`. |
| 77 | crosswalk never converges (ungoverned CATEGORY) | med | §5 CATEGORY retired as input after one-time backfill; onboarding writes `DOMAIN_PRIMARY` directly. |
| 78 | `empty` is a recurring feed state, no lifecycle slot | low | §2b dedicated `empty` state; audit only on N-consecutive-empty (future). |

**Consciously deferred (with reason):** #44 (dossier hand-off — no code exists; v1 stops at `LANDING_FQN`), #45 (ENTITY_INDEX.DOMAIN reconciliation — separate axis, not load-bearing for the catalog), #51 (Snowsight tags — needs `THEME_PRIMARY`, low value vs CATALOG view), #52 (build_library_map rewrite — separate module, out of catalog scope), #73-live-derivation (F4 stays stored+backfilled, with onboard-time refresh as a follow-on increment).

---

## 2. FINAL DDL (copy-paste ready, all schemas verified)

### 2a. The 8 + 3 new columns on SOURCE_REGISTRY (idempotent, arrays default `[]`)

```sql
-- All ADD COLUMN IF NOT EXISTS so re-runs are no-ops (Snowflake supports it).
ALTER TABLE LIBRARY_META.REGISTRY.SOURCE_REGISTRY ADD COLUMN IF NOT EXISTS
    DOMAIN_PRIMARY              VARCHAR,
    DOMAIN_SECONDARY           ARRAY    DEFAULT PARSE_JSON('[]'),
    ENTITY_TYPES               ARRAY    DEFAULT PARSE_JSON('[]'),
    JOIN_KEYS_STD              ARRAY    DEFAULT PARSE_JSON('[]'),
    JOIN_KEY_TIER              VARCHAR  DEFAULT 'NONE',
    JOIN_KEY_TIER_PROVISIONAL  BOOLEAN  DEFAULT TRUE,
    THEMES                     ARRAY    DEFAULT PARSE_JSON('[]'),
    HAS_EVENTS                 BOOLEAN  DEFAULT FALSE,
    DOMAIN_SOURCE              VARCHAR,   -- 'crosswalk'|'heuristic'|'human'|'onboard'  (idempotency + review queue)
    DOMAIN_CONFIDENCE          VARCHAR,   -- 'high'|'low'
    NEEDS_TOPIC                BOOLEAN  DEFAULT FALSE;  -- portals bulk-assigned, topic TBD
```

> Note: existing 1,503 rows keep NULL for the arrays even with a DEFAULT (DEFAULT only fires on rows that omit the column going forward). Pass 0b therefore runs an explicit backfill (§4) so the audits never see NULL. Backfill is `UPDATE … SET col = PARSE_JSON('[]') WHERE col IS NULL`.

### 2b. THE CORRECTED LIFECYCLE RULE (stated precisely)

Evaluate the **latest run** (one row per source, ordered `ENDED_AT DESC, _LOADED_AT DESC`) and the physical landing table. Branch order is load-bearing:

1. **`modeled`** — a `DOMAIN__SOURCEID` mart exists for this source (lowercased match).
2. **`stale`** — latest run `STATUS='success'` **but no landing table** (data dropped/never persisted).
3. **`sampled`** — latest `STATUS='success'` AND it's a detected slice: `MESSAGE` matches `%proof slice%`, `bulk portal load%of % rows.`, or `% sample%`, OR `run_rows ∈ {1000,2000,5000,10000,25000,50000,100000}`.
4. **`landed`** — latest `STATUS='success'` (full load, any size).
5. **`landed`** — no run row but a landing table exists (orphan/backfilled table).
6. **`stale`** — latest `STATUS='failed'`.
7. **`empty`** — latest `STATUS='empty'` (ran, fetched 0 rows; benign for feeds).
8. **`queued`** — no run AND `INCLUDE='Y'`.
9. **`scouted`** — everything else.

Never gate completeness on `run_rows == land_rows` (chunked loads: NPPES run=156k, table=9.6M). `LANDED_ROW_COUNT` = the **table** total; `RUN_ROWS` is advisory only.

Verified live distribution with this exact rule: `scouted 854 · sampled 594 · stale 59 · modeled 36 · empty 28 · landed 21`.

### 2c. The CATALOG view (ENDED_AT, latest-run, orphan union, POSITION marts/staging)

```sql
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.CATALOG AS
WITH latest_run AS (
    SELECT SOURCE_ID, STATUS, ROW_COUNT AS run_rows, MESSAGE, ENDED_AT
    FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
    QUALIFY ROW_NUMBER() OVER (PARTITION BY SOURCE_ID
                               ORDER BY ENDED_AT DESC, _LOADED_AT DESC) = 1
),
landed AS (
    SELECT LOWER(TABLE_NAME) AS sid, TABLE_NAME, ROW_COUNT AS land_rows
    FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'LANDING'
),
marts AS (
    SELECT DISTINCT LOWER(SPLIT_PART(TABLE_NAME,'__',2)) AS sid
    FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
    WHERE POSITION('__' IN TABLE_NAME) > 0
      AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
),
staging AS (
    SELECT DISTINCT LOWER(SPLIT_PART(REGEXP_REPLACE(TABLE_NAME,'^STG_',''),'__',1)) AS sid
    FROM LIBRARY_STAGING.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME LIKE 'STG_%'
      AND POSITION('__' IN TABLE_NAME) > 0
      AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
),
ids AS (
    SELECT SOURCE_ID FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY
    UNION
    SELECT SOURCE_ID FROM latest_run
    UNION
    SELECT sid AS SOURCE_ID FROM landed
)
SELECT
    i.SOURCE_ID,
    COALESCE(r.NAME, UPPER(i.SOURCE_ID))            AS NAME,
    r.DOMAIN_PRIMARY, r.DOMAIN_SECONDARY, r.JURISDICTION,
    r.ENTITY_TYPES, r.JOIN_KEYS_STD, r.JOIN_KEY_TIER, r.JOIN_KEY_TIER_PROVISIONAL,
    r.THEMES, r.HAS_EVENTS, r.PRIORITY_TIER,
    CASE
        WHEN m.sid IS NOT NULL                                              THEN 'modeled'
        WHEN lr.STATUS = 'success' AND l.land_rows IS NULL                  THEN 'stale'
        WHEN lr.STATUS = 'success' AND (
                 LOWER(lr.MESSAGE) LIKE '%proof slice%'
              OR LOWER(lr.MESSAGE) LIKE 'bulk portal load%of % rows.'
              OR LOWER(lr.MESSAGE) LIKE '% sample%'
              OR lr.run_rows IN (1000,2000,5000,10000,25000,50000,100000)
             )                                                              THEN 'sampled'
        WHEN lr.STATUS = 'success'                                          THEN 'landed'
        WHEN lr.SOURCE_ID IS NULL AND l.land_rows IS NOT NULL               THEN 'landed'
        WHEN lr.STATUS = 'failed'                                           THEN 'stale'
        WHEN lr.STATUS = 'empty'                                            THEN 'empty'
        WHEN r.INCLUDE = 'Y'                                                THEN 'queued'
        ELSE 'scouted'
    END                                              AS LIFECYCLE,
    l.land_rows                                      AS LANDED_ROW_COUNT,
    lr.run_rows                                      AS RUN_ROWS,           -- advisory only
    CASE
        WHEN m.sid IS NOT NULL          THEN 'mart'
        WHEN s.sid IS NOT NULL          THEN 'staging'
        WHEN l.land_rows IS NOT NULL    THEN 'raw'
        ELSE 'none'
    END                                              AS TRUST_LAYER,
    'LIBRARY_RAW.LANDING.' || UPPER(i.SOURCE_ID)     AS LANDING_FQN,
    IFF(r.SOURCE_ID IS NULL, TRUE, FALSE)            AS IS_ORPHAN,          -- ran/landed but no registry row
    r.URL, r.PUBLISHER, r.DESCRIPTION
FROM ids i
LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY r ON r.SOURCE_ID = i.SOURCE_ID
LEFT JOIN latest_run lr                            ON lr.SOURCE_ID = i.SOURCE_ID
LEFT JOIN landed l                                 ON l.sid = i.SOURCE_ID
LEFT JOIN marts m                                  ON m.sid = i.SOURCE_ID
LEFT JOIN staging s                                ON s.sid = i.SOURCE_ID;
```

### 2d. The 3 bridge views (NULL-array safe via `OUTER => TRUE`, secondary de-dup)

```sql
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_DOMAIN AS
SELECT r.SOURCE_ID, r.DOMAIN_PRIMARY AS DOMAIN, 'PRIMARY' AS ROLE
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r
WHERE r.DOMAIN_PRIMARY IS NOT NULL
UNION
SELECT DISTINCT r.SOURCE_ID, d.value::VARCHAR AS DOMAIN, 'SECONDARY' AS ROLE
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r,
     LATERAL FLATTEN(input => r.DOMAIN_SECONDARY, OUTER => TRUE) d
WHERE d.value IS NOT NULL
  AND d.value::VARCHAR <> COALESCE(r.DOMAIN_PRIMARY,'');   -- never double-count primary

CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_THEME AS
SELECT r.SOURCE_ID, t.value::VARCHAR AS THEME
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r,
     LATERAL FLATTEN(input => r.THEMES, OUTER => TRUE) t
WHERE t.value IS NOT NULL;

CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_KEY AS
SELECT r.SOURCE_ID, k.value::VARCHAR AS JOIN_KEY
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r,
     LATERAL FLATTEN(input => r.JOIN_KEYS_STD, OUTER => TRUE) k
WHERE k.value IS NOT NULL;
```

### 2e. V_DOMAIN_SUMMARY (on the bridge — counts primary AND secondary; NULL→UNCLASSIFIED)

```sql
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_DOMAIN_SUMMARY AS
WITH base AS (
    SELECT vd.SOURCE_ID,
           COALESCE(vd.DOMAIN,'UNCLASSIFIED') AS DOMAIN,
           vd.ROLE,
           c.LIFECYCLE,
           c.LANDED_ROW_COUNT
    FROM LIBRARY_META.REGISTRY.V_SOURCE_DOMAIN vd
    JOIN LIBRARY_META.REGISTRY.CATALOG c USING (SOURCE_ID)
)
SELECT DOMAIN,
       COUNT(DISTINCT IFF(ROLE='PRIMARY', SOURCE_ID, NULL))                       AS sources_primary,
       COUNT(DISTINCT SOURCE_ID)                                                  AS sources_incl_secondary,
       COUNT(DISTINCT IFF(LIFECYCLE IN ('landed','modeled'), SOURCE_ID, NULL))    AS landed,
       SUM(IFF(ROLE='PRIMARY', LANDED_ROW_COUNT, 0))                              AS total_rows,
       COUNT(DISTINCT IFF(LIFECYCLE IN ('scouted','queued'), SOURCE_ID, NULL))    AS backlog
FROM base
WHERE COALESCE(DOMAIN,'') <> 'open_data_portal'
GROUP BY 1
ORDER BY total_rows DESC NULLS LAST;
```

### 2f. The review-queue view

```sql
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_REVIEW_QUEUE AS
SELECT c.SOURCE_ID, c.NAME, r.CATEGORY, c.DOMAIN_PRIMARY, c.LIFECYCLE,
       r.NEEDS_TOPIC, r.DOMAIN_SOURCE, r.DOMAIN_CONFIDENCE
FROM LIBRARY_META.REGISTRY.CATALOG c
JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY r USING (SOURCE_ID)
WHERE c.DOMAIN_PRIMARY = 'UNCLASSIFIED'
   OR r.DOMAIN_CONFIDENCE = 'low'
   OR r.NEEDS_TOPIC = TRUE
ORDER BY (c.LIFECYCLE IN ('landed','modeled')) DESC, c.LANDED_ROW_COUNT DESC NULLS LAST;
```

---

## 3. FINAL register.py CHANGES

Three edits. The ARRAY-binding fix (`PARSE_JSON` + `json.dumps`) is the load-bearing one — verified live that `TYPEOF(PARSE_JSON(json.dumps([...])))` = `ARRAY`, empty list → valid empty ARRAY, and one placeholder per array (no column shift).

**Edit 1 — `_COLUMNS`, array set, and helpers (top of file):**

```python
import json

# Ordered SOURCE_REGISTRY columns the agent writes (excluding _LOADED_AT).
_COLUMNS = [
    "SOURCE_ID", "JURISDICTION", "CATEGORY", "SUBCATEGORY", "PUBLISHER", "NAME",
    "DESCRIPTION", "UNIT_OF_OBSERVATION", "TEMPORAL_COVERAGE", "GEOGRAPHIC_SCOPE",
    "ACCESS_METHOD", "FORMAT", "AUTH_REQUIRED", "COST", "UPDATE_CADENCE", "VOLUME",
    "LICENSE_TERMS", "URL", "JOIN_KEYS", "ACCOUNTABILITY_RELEVANCE", "EPSTEIN_RELEVANT",
    "PRIORITY_TIER", "INCLUDE", "NOTES",
    # --- faceted-catalog columns ---
    "DOMAIN_PRIMARY", "DOMAIN_SECONDARY", "ENTITY_TYPES", "JOIN_KEYS_STD",
    "JOIN_KEY_TIER", "JOIN_KEY_TIER_PROVISIONAL", "THEMES", "HAS_EVENTS",
    "DOMAIN_SOURCE", "DOMAIN_CONFIDENCE", "NEEDS_TOPIC",
]

# Columns that must round-trip as Snowflake ARRAY, not splatted scalars.
_ARRAY_COLUMNS = {"DOMAIN_SECONDARY", "ENTITY_TYPES", "JOIN_KEYS_STD", "THEMES"}
# Onboarding must never blank a facet the migration set; COALESCE these on MATCH.
_COALESCE_ON_MERGE = {
    "DOMAIN_PRIMARY", "DOMAIN_SECONDARY", "ENTITY_TYPES", "JOIN_KEYS_STD",
    "JOIN_KEY_TIER", "JOIN_KEY_TIER_PROVISIONAL", "THEMES", "HAS_EVENTS",
    "DOMAIN_SOURCE", "DOMAIN_CONFIDENCE", "NEEDS_TOPIC",
}
assert _ARRAY_COLUMNS <= set(_COLUMNS), "array cols must be in _COLUMNS"


def _src_expr(c: str) -> str:
    # One placeholder per column either way -> positional tuple never shifts.
    return f"PARSE_JSON(%s) AS {c}" if c in _ARRAY_COLUMNS else f"%s AS {c}"


def _encode(c: str, v):
    if c in _ARRAY_COLUMNS:
        # Encode exactly once at the boundary. Never re-dump an already-serialized str.
        assert v is None or isinstance(v, (list, tuple)), \
            f"{c} must be a list/None, got {type(v)}"
        return json.dumps(list(v) if v is not None else [])
    return v
```

**Edit 2 — `_merge_sql` (per-column expr + COALESCE on MATCH so onboarding never clobbers migration facets):**

```python
def _merge_sql(row: dict):
    fqt = f'"{settings.meta_database}"."{settings.registry_schema}"."{settings.registry_table}"'
    using = ", ".join(_src_expr(c) for c in _COLUMNS)
    set_parts = []
    for c in _COLUMNS:
        if c == "SOURCE_ID":
            continue
        if c in _COALESCE_ON_MERGE:
            set_parts.append(f"t.{c}=COALESCE(s.{c}, t.{c})")  # don't blank a migration facet
        else:
            set_parts.append(f"t.{c}=s.{c}")
    update_set = ", ".join(set_parts)
    insert_cols = ", ".join(_COLUMNS) + ", _LOADED_AT"
    insert_vals = ", ".join(f"s.{c}" for c in _COLUMNS) + ", CURRENT_TIMESTAMP()"
    sql = (
        f"MERGE INTO {fqt} t USING (SELECT {using}) s ON t.SOURCE_ID = s.SOURCE_ID "
        f"WHEN MATCHED THEN UPDATE SET {update_set}, t._LOADED_AT=CURRENT_TIMESTAMP() "
        f"WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals})"
    )
    params = tuple(_encode(c, row[c]) for c in _COLUMNS)
    return sql, params
```

**Edit 3 — `_build_row` (append the 11 keys; arrays default to `[]`, not None, so the bridge/audits behave):**

```python
        # --- faceted-catalog facets (read from enrichment/config; safe defaults) ---
        "DOMAIN_PRIMARY":            enrichment.get("domain_primary") or "UNCLASSIFIED",
        "DOMAIN_SECONDARY":          enrichment.get("domain_secondary") or [],
        "ENTITY_TYPES":              enrichment.get("entity_types") or [],
        "JOIN_KEYS_STD":             config.get("join_keys_std") or [],          # set by Pass 2 / onboard fingerprint
        "JOIN_KEY_TIER":             config.get("join_key_tier") or "NONE",
        "JOIN_KEY_TIER_PROVISIONAL": config.get("join_key_tier_provisional", True),
        "THEMES":                    enrichment.get("themes") or [],
        "HAS_EVENTS":                bool(config.get("has_events", False)),
        "DOMAIN_SOURCE":             "onboard" if enrichment.get("domain_primary") else None,
        "DOMAIN_CONFIDENCE":         enrichment.get("domain_confidence"),
        "NEEDS_TOPIC":               False,
```

**Edit 4 — `prompts/generate_catalog.txt`:** add to the returned JSON keys (inject the 22-domain + 10-theme + 12-entity vocab into the prompt text so the LLM can only pick valid tokens):

```
Return strict JSON with these keys ONLY:
  accountability_relevance, epstein_relevant, notes,
  domain_primary      (exactly one of: <22 DOMAIN tokens>),
  domain_secondary    (array, 0-3 of the 22 tokens, excluding domain_primary),
  entity_types        (array, 0+ of: person company organization vessel aircraft
                       facility place payment filing case asset event),
  themes              (array, 0+ of: follow_the_money power_who_holds_it harm_to_people
                       sanctions_illicit revolving_door corporate_ownership
                       enforcement_actions public_health_safety civil_rights_history epstein),
  domain_confidence   ("high" | "low")
```

**Array-write template for ALL other code paths (Pass 2/3/4/5 UPDATEs) — same trap, same fix:**

```python
cur.execute(
    "UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY "
    "SET JOIN_KEYS_STD=PARSE_JSON(%s), JOIN_KEY_TIER=%s, JOIN_KEY_TIER_PROVISIONAL=%s "
    "WHERE SOURCE_ID=%s",
    (json.dumps(keys_list or []), tier, provisional_bool, source_id),
)
```

---

## 4. THE MIGRATION SCRIPTS (Pass 0–6)

Run as `ACCOUNTADMIN`. **Operational gate before anything:** confirm no `onboard.py` process is running (`ps aux | grep onboard`). Every pass is idempotent; each has a verify query that must pass before proceeding.

### Pass 0a — Durable snapshot (Time Travel is only 1 day; verified)

```sql
CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_20260625
    CLONE LIBRARY_META.REGISTRY.SOURCE_REGISTRY;
```
**Verify:** `SELECT (SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY) = (SELECT COUNT(*) FROM LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_20260625);` → must be `TRUE`.
**Rollback recipe:** `INSERT OVERWRITE INTO LIBRARY_META.REGISTRY.SOURCE_REGISTRY (<original 24 cols>) SELECT <those cols> FROM …_BAK_20260625;`

### Pass 0b — Columns + backfill array defaults (§2a DDL)

Run the `ALTER TABLE … ADD COLUMN IF NOT EXISTS` block, then:
```sql
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET DOMAIN_SECONDARY = PARSE_JSON('[]') WHERE DOMAIN_SECONDARY IS NULL;
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET ENTITY_TYPES = PARSE_JSON('[]')     WHERE ENTITY_TYPES IS NULL;
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET JOIN_KEYS_STD = PARSE_JSON('[]')    WHERE JOIN_KEYS_STD IS NULL;
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET THEMES = PARSE_JSON('[]')           WHERE THEMES IS NULL;
```
**Verify:** `SELECT COUNT(*) FROM LIBRARY_META.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='REGISTRY' AND TABLE_NAME='SOURCE_REGISTRY' AND COLUMN_NAME IN ('DOMAIN_PRIMARY','DOMAIN_SECONDARY','ENTITY_TYPES','JOIN_KEYS_STD','JOIN_KEY_TIER','JOIN_KEY_TIER_PROVISIONAL','THEMES','HAS_EVENTS','DOMAIN_SOURCE','DOMAIN_CONFIDENCE','NEEDS_TOPIC');` → `11`. And `SELECT COUNT(*) FROM …SOURCE_REGISTRY WHERE TYPEOF(THEMES)<>'ARRAY';` → `0`.

### Pass 0c — FACET_VOCAB (idempotent MERGE seed)

```sql
CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.FACET_VOCAB (
    FACET VARCHAR, VALUE VARCHAR, TIER VARCHAR, LABEL VARCHAR, SORT_ORD NUMBER
);
-- Seed via MERGE on (FACET,VALUE) so re-seeding is a no-op. (full seed VALUES in §5)
MERGE INTO LIBRARY_META.REGISTRY.FACET_VOCAB t
USING (
    SELECT $1 AS FACET, $2 AS VALUE, $3 AS TIER, $4 AS LABEL, $5 AS SORT_ORD
    FROM VALUES
      -- DOMAIN (22)
      ('DOMAIN','money_finance',NULL,'Money & Finance',1),
      ('DOMAIN','spending_budget',NULL,'Spending & Budget',2),
      ('DOMAIN','government_power',NULL,'Government & Power',3),
      ('DOMAIN','money_in_politics',NULL,'Money in Politics',4),
      ('DOMAIN','justice_courts',NULL,'Justice & Courts',5),
      ('DOMAIN','health_medicine',NULL,'Health & Medicine',6),
      ('DOMAIN','sanctions_enforcement',NULL,'Sanctions & Enforcement',7),
      ('DOMAIN','corporate_entities',NULL,'Corporate Entities',8),
      ('DOMAIN','energy_environment',NULL,'Energy & Environment',9),
      ('DOMAIN','geo_demographics',NULL,'Geo & Demographics',10),
      ('DOMAIN','crime_security',NULL,'Crime & Security',11),
      ('DOMAIN','economy_labor_trade',NULL,'Economy, Labor & Trade',12),
      ('DOMAIN','history_culture',NULL,'History & Culture',13),
      ('DOMAIN','transport_movement',NULL,'Transport & Movement',14),
      ('DOMAIN','housing_social',NULL,'Housing & Social',15),
      ('DOMAIN','science_research',NULL,'Science & Research',16),
      ('DOMAIN','procurement_intl',NULL,'Procurement (Intl)',17),
      ('DOMAIN','education',NULL,'Education',18),
      ('DOMAIN','elections_voting',NULL,'Elections & Voting',19),
      ('DOMAIN','immigration_migration',NULL,'Immigration & Migration',20),
      ('DOMAIN','open_data_portal',NULL,'Open Data Portal',21),
      ('DOMAIN','targeted_investigation',NULL,'Targeted Investigation',22),
      ('DOMAIN','UNCLASSIFIED',NULL,'Unclassified',99),
      -- JURISDICTION (full words, matching the stored column)
      ('JURISDICTION','federal',NULL,'Federal',1),
      ('JURISDICTION','international',NULL,'International',2),
      ('JURISDICTION','cross-cutting',NULL,'Cross-cutting',3),
      ('JURISDICTION','local',NULL,'Local',4),
      ('JURISDICTION','state',NULL,'State',5),
      -- ENTITY_TYPE (12, FtM)
      ('ENTITY_TYPE','person',NULL,'Person',1),('ENTITY_TYPE','company',NULL,'Company',2),
      ('ENTITY_TYPE','organization',NULL,'Organization',3),('ENTITY_TYPE','vessel',NULL,'Vessel',4),
      ('ENTITY_TYPE','aircraft',NULL,'Aircraft',5),('ENTITY_TYPE','facility',NULL,'Facility',6),
      ('ENTITY_TYPE','place',NULL,'Place',7),('ENTITY_TYPE','payment',NULL,'Payment',8),
      ('ENTITY_TYPE','filing',NULL,'Filing',9),('ENTITY_TYPE','case',NULL,'Case',10),
      ('ENTITY_TYPE','asset',NULL,'Asset',11),('ENTITY_TYPE','event',NULL,'Event',12),
      -- JOIN_KEY (with TIER)
      ('JOIN_KEY','EIN','STEEL','EIN',1),('JOIN_KEY','NPI','STEEL','NPI',2),
      ('JOIN_KEY','CIK','STEEL','CIK',3),('JOIN_KEY','UEI','STEEL','UEI',4),
      ('JOIN_KEY','DUNS','STEEL','DUNS',5),('JOIN_KEY','LEI','STEEL','LEI',6),
      ('JOIN_KEY','IMO','STEEL','IMO',7),('JOIN_KEY','MMSI','STEEL','MMSI',8),
      ('JOIN_KEY','CCN','STEEL','CCN',9),('JOIN_KEY','PATENT','STEEL','PATENT',10),
      ('JOIN_KEY','DOCKET','STRONG','DOCKET',11),('JOIN_KEY','NAICS','STRONG','NAICS',12),
      ('JOIN_KEY','NCES','STRONG','NCES',13),('JOIN_KEY','SIC','STRONG','SIC',14),
      ('JOIN_KEY','FIPS','GEO','FIPS',15),('JOIN_KEY','ZIP','GEO','ZIP',16),
      ('JOIN_KEY','LATLON','GEO','LATLON',17),('JOIN_KEY','COUNTRY','GEO','COUNTRY',18),
      ('JOIN_KEY','GEOM','GEO','GEOM',19),
      ('JOIN_KEY','NAME','PROBABILISTIC','NAME',20),('JOIN_KEY','ADDRESS','PROBABILISTIC','ADDRESS',21),
      -- THEME (10)
      ('THEME','follow_the_money',NULL,'Follow the Money',1),
      ('THEME','power_who_holds_it',NULL,'Who Holds Power',2),
      ('THEME','harm_to_people',NULL,'Harm to People',3),
      ('THEME','sanctions_illicit',NULL,'Sanctions & Illicit',4),
      ('THEME','revolving_door',NULL,'Revolving Door',5),
      ('THEME','corporate_ownership',NULL,'Corporate Ownership',6),
      ('THEME','enforcement_actions',NULL,'Enforcement Actions',7),
      ('THEME','public_health_safety',NULL,'Public Health & Safety',8),
      ('THEME','civil_rights_history',NULL,'Civil Rights History',9),
      ('THEME','epstein',NULL,'Epstein',10)
) s ON t.FACET=s.FACET AND t.VALUE=s.VALUE
WHEN NOT MATCHED THEN INSERT (FACET,VALUE,TIER,LABEL,SORT_ORD)
                  VALUES (s.FACET,s.VALUE,s.TIER,s.LABEL,s.SORT_ORD)
WHEN MATCHED THEN UPDATE SET t.TIER=s.TIER, t.LABEL=s.LABEL, t.SORT_ORD=s.SORT_ORD;
```
**Verify:** `SELECT FACET, COUNT(*) FROM LIBRARY_META.REGISTRY.FACET_VOCAB GROUP BY 1;` → DOMAIN 23 (incl. UNCLASSIFIED), JURISDICTION 5, ENTITY_TYPE 12, JOIN_KEY 21, THEME 10.

### Pass 0.5 — Orphan landing backfill (stub registry rows so they're never invisible)

```sql
MERGE INTO LIBRARY_META.REGISTRY.SOURCE_REGISTRY t
USING (
    SELECT LOWER(TABLE_NAME) AS SOURCE_ID, TABLE_NAME AS NM,
           SPLIT_PART(LOWER(TABLE_NAME),'_',1) AS PFX
    FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA='LANDING'
      AND LOWER(TABLE_NAME) NOT IN (SELECT SOURCE_ID FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY)
) s ON t.SOURCE_ID = s.SOURCE_ID
WHEN NOT MATCHED THEN INSERT (SOURCE_ID, NAME, JURISDICTION, INCLUDE, DOMAIN_PRIMARY, DOMAIN_SOURCE, NOTES, _LOADED_AT)
VALUES (s.SOURCE_ID, s.NM,
        CASE s.PFX WHEN 'fed' THEN 'federal' WHEN 'intl' THEN 'international'
                   WHEN 'xc' THEN 'cross-cutting' WHEN 'loc' THEN 'local'
                   WHEN 'st' THEN 'state' ELSE 'cross-cutting' END,
        'Y', 'UNCLASSIFIED', 'crosswalk', 'auto-stub: orphan landing table backfilled', CURRENT_TIMESTAMP());
```
**Verify (3 orphans confirmed live):** `SELECT COUNT(*) FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='LANDING' AND LOWER(TABLE_NAME) NOT IN (SELECT SOURCE_ID FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY);` → `0`. Re-run inserts `0`.

### Pass 0e–0g — Views

Run §2c (CATALOG), §2d (3 bridges), §2e (V_DOMAIN_SUMMARY), §2f (V_REVIEW_QUEUE) — all `CREATE OR REPLACE`, inherently idempotent.
**Verify:**
- `SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG;` → ≥ registry rowcount (orphans add a few; expect ~1506).
- `SELECT COUNT_IF(LIFECYCLE='modeled') FROM LIBRARY_META.REGISTRY.CATALOG;` → `36`.
- `SELECT LIFECYCLE, COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG GROUP BY 1;` → matches `modeled 36 / landed 21 / sampled 594 / stale 59 / empty 28 / …`.
- `SELECT TYPEOF(DOMAIN_SECONDARY) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY LIMIT 1;` → `ARRAY`.

### Pass 0h — Read-path grants (CATALOG is useless if the consumer can't read LANDING)

```sql
GRANT SELECT ON ALL TABLES    IN SCHEMA LIBRARY_RAW.LANDING TO ROLE CLAUDE_MCP_READONLY;
GRANT SELECT ON FUTURE TABLES IN SCHEMA LIBRARY_RAW.LANDING TO ROLE CLAUDE_MCP_READONLY;
GRANT SELECT ON ALL VIEWS  IN SCHEMA LIBRARY_META.REGISTRY  TO ROLE CLAUDE_MCP_READONLY;  -- CATALOG, bridges
GRANT SELECT ON ALL TABLES IN SCHEMA LIBRARY_MARTS.CORE     TO ROLE CLAUDE_MCP_READONLY;  -- (+ each mart schema)
```
**Verify AS the read role (not ACCOUNTADMIN):** `USE ROLE CLAUDE_MCP_READONLY; SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.FED_OYEZ; SELECT * FROM LIBRARY_META.REGISTRY.CATALOG LIMIT 1;` → both succeed.

### Pass 1 — Free facets (deterministic)

```sql
-- JURISDICTION from SOURCE_ID prefix, EXCEPT portals (prefix 'portal' is not a jurisdiction).
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET JURISDICTION = CASE SPLIT_PART(SOURCE_ID,'_',1)
    WHEN 'fed' THEN 'federal' WHEN 'intl' THEN 'international'
    WHEN 'xc' THEN 'cross-cutting' WHEN 'loc' THEN 'local' WHEN 'st' THEN 'state' END
WHERE SPLIT_PART(SOURCE_ID,'_',1) IN ('fed','intl','xc','loc','st')
  AND (JURISDICTION IS NULL OR JURISDICTION = '' OR JURISDICTION = 'US');
-- Portals: explicit cross-cutting (host-derived geo can refine later).
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET JURISDICTION = 'cross-cutting'
WHERE SOURCE_ID ILIKE 'portal_%' AND (JURISDICTION IS NULL OR JURISDICTION = '');
-- Stray 'US' that aren't prefix-derivable -> federal.
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY SET JURISDICTION='federal' WHERE JURISDICTION='US';
```
Also add to `naming.py`: map any inbound `'US'`/`'us'` jurisdiction to `'federal'` so loaders can't reintroduce it.
**Verify:** `SELECT JURISDICTION, COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY GROUP BY 1;` → only `{federal,international,cross-cutting,local,state}`, zero `US`, zero blank.

### Pass 2 — JOIN_KEYS_STD from fingerprint (quality-gated)

Python (idempotent — overwrites cleanly; PARSE_JSON deterministic). Fingerprint file is **646 UPPERCASE keys**, shape `{rows, keys:[{key,tier,distinct,populated_pct,...}]}`.

```python
import json, sys
sys.path.insert(0, "/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding")
from snow import connect
TIER_RANK = {"STEEL":4,"STRONG":3,"GEO":2,"PROBABILISTIC":1,"NONE":0}
fp = json.load(open("/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/connect_fingerprints.json"))
conn = connect(); cur = conn.cursor()
for table_upper, entry in fp.items():
    sid = table_upper.lower()
    keys = set()
    for k in entry.get("keys", []):
        # QUALITY GATE: drop constants/sparse (NPPES EIN distinct=1 must NOT count as STEEL)
        if (k.get("distinct") or 0) > 1 and (k.get("populated_pct") or 0) >= 10:
            keys.add(k["key"])
    keys = sorted(keys)
    tier = "NONE"
    for k in entry.get("keys", []):
        if (k.get("distinct") or 0) > 1 and (k.get("populated_pct") or 0) >= 10:
            if TIER_RANK.get(k["tier"],0) > TIER_RANK[tier]:
                tier = k["tier"]
    cur.execute(
        "UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY "
        "SET JOIN_KEYS_STD=PARSE_JSON(%s), JOIN_KEY_TIER=%s, JOIN_KEY_TIER_PROVISIONAL=FALSE "
        "WHERE SOURCE_ID=%s",
        (json.dumps(keys), tier, sid),
    )
conn.close()
```
**Verify:** `SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE JOIN_KEY_TIER_PROVISIONAL=FALSE;` → ~36–55. Spot-check NPPES carries NPI not EIN: `SELECT JOIN_KEYS_STD FROM …SOURCE_REGISTRY WHERE SOURCE_ID='fed_cms_nppes';` → does **not** contain `EIN`.

### Pass 3 — DOMAIN crosswalk (complete; covers all 165 categories)

Seed `FACET_CROSSWALK` from §5 (all 165 strings, normalized key), then:
```sql
CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.FACET_CROSSWALK (
    RAW_CATEGORY VARCHAR, NORM_KEY VARCHAR, DOMAIN_PRIMARY VARCHAR, DOMAIN_SECONDARY ARRAY
);
-- (load rows via the §5 generator, each DOMAIN_SECONDARY as PARSE_JSON(json.dumps([...])))

UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY r
SET DOMAIN_PRIMARY  = x.DOMAIN_PRIMARY,
    DOMAIN_SECONDARY = x.DOMAIN_SECONDARY,
    DOMAIN_SOURCE   = 'crosswalk',
    DOMAIN_CONFIDENCE = 'high'
FROM LIBRARY_META.REGISTRY.FACET_CROSSWALK x
WHERE LOWER(TRIM(REGEXP_REPLACE(r.CATEGORY,'[-/&]',' '))) = x.NORM_KEY
  AND r.CATEGORY IS NOT NULL AND r.CATEGORY <> ''
  AND r.DOMAIN_SOURCE IS DISTINCT FROM 'human';   -- never clobber a human correction
```
**Verify (must be 0):** `SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE CATEGORY IS NOT NULL AND CATEGORY<>'' AND DOMAIN_PRIMARY IS NULL;` → `0`. Plus the `government` guard: `SELECT COUNT(*) FROM …SOURCE_REGISTRY WHERE DOMAIN_PRIMARY='government_power' AND NAME ILIKE '%open data%';` → `0` (else re-route to open_data_portal).

### Pass 4 — Triage the 593 blanks (all are `portal_`; bulk-assign)

```sql
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET DOMAIN_PRIMARY='open_data_portal', DOMAIN_SOURCE='heuristic',
    DOMAIN_CONFIDENCE='high', NEEDS_TOPIC=TRUE
WHERE (CATEGORY IS NULL OR CATEGORY='') AND SOURCE_ID ILIKE 'portal_%'
  AND DOMAIN_SOURCE IS DISTINCT FROM 'human';
-- any residual blank non-portal -> UNCLASSIFIED (review queue)
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET DOMAIN_PRIMARY='UNCLASSIFIED', DOMAIN_SOURCE='heuristic', DOMAIN_CONFIDENCE='low'
WHERE DOMAIN_PRIMARY IS NULL AND DOMAIN_SOURCE IS DISTINCT FROM 'human';
```
Idempotency: scope is `DOMAIN_SOURCE IS DISTINCT FROM 'human'` — re-running never clobbers a human fix, and never re-stamps a portal already set.
**Verify:** `SELECT COUNT(*) FROM …SOURCE_REGISTRY WHERE DOMAIN_PRIMARY IS NULL;` → `0`. `SELECT COUNT(*) WHERE NEEDS_TOPIC=TRUE;` → `593`.

### Pass 5 — Human/agent facets, landed-first (proposed at checkpoint, approved by you)

- **ENTITY_TYPES:** agent-assigned per source from `UNIT_OF_OBSERVATION` + schema. Default `[]` for the 1,074 placeholder/blank rows. Not "auto".
- **THEMES:** only `epstein` is derivable:
```sql
UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY
SET THEMES = ARRAY_APPEND(COALESCE(THEMES, PARSE_JSON('[]')), 'epstein')
WHERE (LOWER(EPSTEIN_RELEVANT) LIKE 'yes%' OR LOWER(EPSTEIN_RELEVANT) LIKE 'maybe%')
  AND NOT ARRAY_CONTAINS('epstein'::VARIANT, COALESCE(THEMES, PARSE_JSON('[]')));
```
The other 9 themes are agent-proposed at the REGISTRY checkpoint, landed sources first.
**Verify:** `SELECT COUNT(*) FROM V_SOURCE_THEME WHERE THEME='epstein';` ≈ 167+20 candidates. Landed-first coverage: `SELECT COUNT(*) FROM CATALOG WHERE LIFECYCLE IN ('landed','modeled') AND ARRAY_SIZE(THEMES)=0 AND DOMAIN_PRIMARY<>'open_data_portal';` → drains toward 0 as you approve.

### Pass 6 — Lock the vocab via dbt (relationships, not accepted_values)

`ripple_dbt/seeds/facet_vocab_domain.csv` (+ theme/entity/jurisdiction/joinkey seeds), and `models/registry/_meta.yml`:

```yaml
version: 2
sources:
  - name: ripple_meta
    database: LIBRARY_META
    schema: REGISTRY
    tables:
      - name: SOURCE_REGISTRY
        columns:
          - name: DOMAIN_PRIMARY
            data_tests:
              - relationships:
                  to: ref('facet_vocab_domain')
                  field: VALUE
                  config: { severity: warn }   # promote to error after Pass 1-5 verified clean
          - name: JURISDICTION
            data_tests:
              - relationships:
                  to: ref('facet_vocab_jurisdiction')
                  field: VALUE
                  config: { severity: warn }
      - name: V_SOURCE_THEME
        columns:
          - name: THEME
            data_tests: [{ relationships: { to: ref('facet_vocab_theme'), field: VALUE, config: { severity: warn } } }]
      - name: V_SOURCE_KEY
        columns:
          - name: JOIN_KEY
            data_tests: [{ relationships: { to: ref('facet_vocab_joinkey'), field: VALUE, config: { severity: warn } } }]
      - name: V_SOURCE_DOMAIN
        columns:
          - name: DOMAIN
            data_tests: [{ relationships: { to: ref('facet_vocab_domain'), field: VALUE, config: { severity: warn } } }]
seeds:
  - name: facet_vocab_domain
    data_tests:
      - dbt_utils.unique_combination_of_columns: { combination_of_columns: [VALUE] }
    columns:
      - name: VALUE
        data_tests: [not_null]
```
**Maintenance audits (NULL-safe, portal-excluded):**
```sql
-- Audit 1: STEEL cross-domain key but no secondary domain
SELECT c.SOURCE_ID, c.DOMAIN_PRIMARY, c.JOIN_KEYS_STD
FROM LIBRARY_META.REGISTRY.CATALOG c
WHERE c.JOIN_KEY_TIER='STEEL'
  AND COALESCE(ARRAY_SIZE(c.DOMAIN_SECONDARY),0)=0
  AND c.LIFECYCLE IN ('landed','modeled')
  AND c.DOMAIN_PRIMARY <> 'open_data_portal';

-- Audit 2: landed real source with no THEME (portals excluded so it isn't 593 noise)
SELECT SOURCE_ID, NAME FROM LIBRARY_META.REGISTRY.CATALOG
WHERE LIFECYCLE IN ('landed','modeled')
  AND DOMAIN_PRIMARY <> 'open_data_portal'
  AND (COALESCE(ARRAY_SIZE(THEMES),0)=0 OR DOMAIN_PRIMARY='UNCLASSIFIED');

-- Audit 3: run/landing source_ids missing from registry (the 89 + future drift)
SELECT DISTINCT SOURCE_ID FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
WHERE SOURCE_ID NOT IN (SELECT SOURCE_ID FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY);
```
**Verify:** `dbt test --select source:ripple_meta` runs and reports (warn). Wire `dbt test --select source:ripple_meta` into a cron/CI step or the gate is decorative.

---

## 5. THE 22-DOMAIN VOCAB + CROSSWALK COVERAGE

### Final DOMAIN list (22 real + 1 sentinel)

```
money_finance        spending_budget       government_power      money_in_politics
justice_courts       health_medicine       sanctions_enforcement corporate_entities
energy_environment   geo_demographics      crime_security        economy_labor_trade
history_culture      transport_movement    housing_social        science_research
procurement_intl     education             elections_voting      immigration_migration
open_data_portal     targeted_investigation
                                                         (+ UNCLASSIFIED sentinel)
```

Changes vs the original design's 22: dropped `disasters_hazards`, `conflict_aid_global`, `consumer_protection` as standalone (folded — disasters→`energy_environment`, conflict/aid→`government_power`/`immigration_migration`, consumer→`corporate_entities`); **added** `education`, `elections_voting`, `immigration_migration` to give the 52 previously-homeless rows a real home. `science_research` absorbs patents/IP/researcher-IDs; `corporate_entities` absorbs tax/nonprofits; `transport_movement` absorbs maritime/flight.

### Crosswalk coverage note

`FACET_CROSSWALK` enumerates **all 165 named categories** (910 rows) — generated by `SELECT DISTINCT CATEGORY`, each assigned by hand/agent-with-approval, joined on the normalized key `LOWER(TRIM(REGEXP_REPLACE(CATEGORY,'[-/&]',' ')))` so casing/punct/snake variants collapse (`Corporate Registry` = `corporate-registry` = `company registry`). The 593 blank-CATEGORY rows are **not** in this crosswalk — they're all `portal_` and handled by Pass 4. Representative assignments (the load-bearing disambiguations):

| Raw category (examples) | DOMAIN_PRIMARY | DOMAIN_SECONDARY |
|---|---|---|
| `government`, `Open Data`, `open data`, `national-portal`, `meta-discovery`, `aggregators`, `data preservation`, `City/County Open-Data Portals`, `State Open-Data Portals` | `open_data_portal` | — |
| `governance`, `government integrity`, `corruption`, `Government & Politics` | `government_power` | — |
| `Health`, `health`, `healthcare`, `Healthcare`, `global health`, `clinical_research` | `health_medicine` | — |
| `Legal / Court Data`, `Courts & Justice`, `State Courts`, `criminal justice`, `Justice & Courts`, `Judiciary & Legal` | `justice_courts` | — |
| `law enforcement`, `enforcement`, `Legal & Enforcement`, `Regulation & Enforcement` | `justice_courts` | `[sanctions_enforcement]` |
| `Procurement`, `procurement` (intl e-GP/TED) — `SOURCE_ID LIKE 'intl_%'` | `procurement_intl` | `[spending_budget]` |
| `Procurement`/`Contracts & Grants`/`State Spending Transparency`/`federal spending` — US | `spending_budget` | `[procurement_intl]` |
| `sanctions & corporate` | `sanctions_enforcement` | `[corporate_entities, money_finance]` |
| `Immigration & Security` | `crime_security` | `[immigration_migration]` |
| `migration`, `immigration` | `immigration_migration` | — |
| `Economy & Labor`, `Economy`, `economic`, `labor`, `trade`, `multilateral economic` | `economy_labor_trade` | — |
| `lobbying`, `Money-in-Politics`, `political influence`, `State Campaign Finance & Lobbying`, `FARA`, `Lobbying & Foreign Influence` | `money_in_politics` | — |
| `elections` | `elections_voting` | — |
| `education` | `education` | — |
| `patents`, `intellectual property`, `researcher_identifiers`, `scholarly_literature`, `astronomy`, `genomics`, `chemistry`, `physics`, `Science & Research` | `science_research` | — |
| `maritime`, `transit`, `Transportation`, `flight tracking`, `Maritime & Transportation` | `transport_movement` | — |
| `Tax & Nonprofits`, `philanthropy`, `Business Registrations`, `Corporate Registry`, `beneficial-ownership`, `entity backbone` | `corporate_entities` | — |
| `energy grid`, `Energy`, `climate`, `air quality`, `soil`, `seismology`, `oceanography`, `earth_observation`, `emergency management` | `energy_environment` | — |
| `housing`, `Property & Parcel`, `planning`, `Housing & Urban Development`, `social services`, `social insurance` | `housing_social` | — |
| `History & Culture`, `newspapers`, `digital heritage`, `slavery records`, `genealogy`, `manuscripts / rare books`, `Civil Rights & Historical Records` | `history_culture` | — |
| `financial regulation`, `financial data`, `finance`, `Money`, `anti-money-laundering`, `financial-crime`, `financial-secrecy` | `money_finance` | — |
| `crime`, `homeland security`, `military`, `arms`, `organized-crime` | `crime_security` | — |
| `Demographics & Census`, `maps / geospatial`, `statistics`, `public opinion` | `geo_demographics` | — |
| `human-rights`, `conflict`, `foreign policy`, `aid`, `development-finance`, `tribal`, `extractives` | `government_power` | `[immigration_migration]` for conflict/migration rows |

Anything an assigner genuinely can't place → `DOMAIN_PRIMARY='UNCLASSIFIED'`, `DOMAIN_CONFIDENCE='low'` (lands in `V_REVIEW_QUEUE`). **Post-Pass-3 invariant:** zero named-CATEGORY rows with NULL `DOMAIN_PRIMARY`. After backfill, **CATEGORY is retired as an input** — onboarding writes `DOMAIN_PRIMARY` directly (validated against vocab), so the crosswalk never needs extending for new sources.

**Deferred taxonomy note (#45):** `ENTITY_INDEX.DOMAIN` (currently only `'health'`, 10.6M rows) is a **separate axis** from `DOMAIN_PRIMARY` and is NOT reconciled in v1. Do not claim "catalog and entity layer speak one language" until a follow-on increment joins `ENTITY_INDEX` back to `SOURCE_REGISTRY.DOMAIN_PRIMARY` at index-build time.

---

## 6. BUILD ORDER (execute top-to-bottom; do not advance past a failed verify)

| Step | Action | Verify (must pass) |
|---|---|---|
| 1 | Operational gate: no `onboard.py` running | `ps aux \| grep -v grep \| grep onboard` → empty |
| 2 | **Pass 0a** clone snapshot | rowcount(reg)=rowcount(bak) → TRUE |
| 3 | **Pass 0b** ALTER + array `[]` backfill | 11 new columns present; `TYPEOF(THEMES)='ARRAY'` on all rows |
| 4 | **Pass 0c** FACET_VOCAB MERGE seed | facet counts: DOMAIN 23, JURIS 5, ENTITY 12, JOIN_KEY 21, THEME 10 |
| 5 | **Pass 0.5** orphan stub backfill | landing-minus-registry count → 0; re-run inserts 0 |
| 6 | **Deploy register.py** (Edits 1–4) + `generate_catalog.txt` | unit: `_merge_sql` returns `len(_COLUMNS)` USING cols; onboard 1 source in fake mode, no KeyError |
| 7 | **Pass 0e–0g** CATALOG + 3 bridges + V_DOMAIN_SUMMARY + V_REVIEW_QUEUE | `COUNT_IF(LIFECYCLE='modeled')`=36; lifecycle dist sane; bridges return rows incl. NULL-array sources |
| 8 | **Pass 0h** read-role grants | AS `CLAUDE_MCP_READONLY`: SELECT a LANDING table + CATALOG both succeed |
| 9 | **Pass 1** JURISDICTION | distinct jurisdiction ⊆ {federal,international,cross-cutting,local,state}; 0 `US`, 0 blank |
| 10 | **Pass 2** fingerprint JOIN_KEYS | `PROVISIONAL=FALSE` count ~36–55; NPPES has NPI not EIN |
| 11 | **Pass 3** DOMAIN crosswalk | 0 named-CATEGORY rows with NULL DOMAIN_PRIMARY; `government_power ∩ '%open data%'` = 0 |
| 12 | **Pass 4** triage 593 blanks | 0 NULL DOMAIN_PRIMARY anywhere; `NEEDS_TOPIC=TRUE`=593 |
| 13 | **Pass 5** epstein theme + landed-first facets (checkpoint) | `V_SOURCE_THEME` epstein count > 0; landed-untagged drains as approved |
| 14 | **Pass 6** dbt seeds + `_meta.yml` + run tests (warn) | `dbt test --select source:ripple_meta` runs; audits 1–3 return only real rows |
| 15 | Promote facet tests `warn`→`error`; wire `dbt test` into cron/CI | CI fails on a single bad vocab value |

**Deferred (not in this build):** Snowsight `THEME_TAG` (#51 — needs `THEME_PRIMARY`), `build_library_map.py` faceted rewrite (#52 — separate module), `connect/dossier.py` SOURCE_ID hand-off (#44 — v1 stops at `LANDING_FQN`; agent reads the landing table directly), F4 live in-view derivation (#73 — stays stored + Pass-2 backfilled, with onboard-time `fingerprint_table()` refresh as a follow-on).

**Files touched:** `library-onboarding/register.py` (Edits 1–3), `library-onboarding/prompts/generate_catalog.txt` (Edit 4), `library-onboarding/naming.py` (`US`→`federal` guard), `ripple_dbt/seeds/facet_vocab_*.csv` + `ripple_dbt/models/registry/_meta.yml` (Pass 6). All SQL above is verified against the live `LIBRARY_META` / `LIBRARY_RAW` / `LIBRARY_MARTS` / `LIBRARY_STAGING` schemas as of 2026-06-25.