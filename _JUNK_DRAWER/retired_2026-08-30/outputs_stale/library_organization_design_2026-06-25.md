All references confirmed. Writing the final recommendation.

# Ripple Library — The Organizing Scheme

**The decision:** A **faceted catalog**. Stop filing 1,503 sources into one folder tree. Tag every source along **7 independent axes** stored as controlled-vocabulary columns on `SOURCE_REGISTRY`, then turn *"what do I have about X"* into a single `WHERE` clause the agent can write blind. Four of the seven facets fill themselves in from the warehouse — so maintenance rides on top of onboarding instead of being a separate chore. The two things that make this win for *you* specifically: **JOIN-KEY is a first-class facet** (your actual moat — UEI/EIN/CIK/NPI/IMO/FIPS become a filter), and **THEME is the investigative-lens axis** (follow_the_money / harm_to_people / etc. — the north star as a queryable column). Default browse view pivots on DOMAIN so you still get a "walk the shape of the Library" menu.

---

## 1. The Scheme — 7 facets

Every source carries a tag set, not a folder location. Each facet answers a *different question*, so they never collide.

| # | Facet | Question | Values | Multi? | Source |
|---|-------|----------|--------|--------|--------|
| F1 | **DOMAIN** | What's it about? | 22 fixed | Yes (1 primary + array) | human/agent |
| F2 | **JURISDICTION** | What gov/geo level? | 5 fixed | No | **auto** (SOURCE_ID prefix) |
| F3 | **ENTITY_TYPE** | What is one row? | 12 fixed | Yes | human/agent (from UNIT_OF_OBS) |
| F4 | **JOIN_KEYS_STD** | What IDs does it carry? | ~24 fixed | Yes | **auto** (fingerprint) |
| F5 | **THEME** | What accountability angle? | 10 fixed | Yes | human/agent |
| F6 | **LIFECYCLE** | How far along? | 6 ordered | No | **auto** (INGEST_RUNS) |
| F7 | **TRUST_LAYER** | How cooked? | 3 (raw/staging/mart) | No | **auto** (warehouse) |

**The split that makes it reliable:** F2/F4/F6/F7 derive themselves from ground truth and can never go stale. Only F1/F3/F5 are human-assigned — and those happen at the REGISTRY checkpoint you already approve.

### F1 — DOMAIN (22 values)

Reuses your **20 dbt mart-folder names** as the vocab so the catalog and the marts speak one language. Near-dupes collapsed (`history`+`historical_records`, `regulation`+`regulatory`, `justice`+`judiciary`+`legal_enforcement`).

```
money_finance          spending_budget        government_power
money_in_politics      justice_courts         health_medicine
sanctions_enforcement  corporate_entities     energy_environment
geo_demographics       crime_security         economy_labor_trade
history_culture        transport_movement     housing_social
science_research       procurement_intl       disasters_hazards
conflict_aid_global    consumer_protection
```
Plus 2 pseudo-domains for things that aren't *about* a subject:
- `open_data_portal` — the ~593 PORTAL_ harvests + meta-discovery. **Biggest single cleanup.**
- `targeted_investigation` — the Epstein cluster + future purpose-built threads.

### F2 — JURISDICTION (free — it's the prefix)
`fed` · `intl` · `xc` · `loc` · `st`. Already enforced by `naming.JURISDICTION_PREFIX`. Just fix the 10 stray `US` rows → `fed`/`st`.

### F3 — ENTITY_TYPE (FtM-aligned, 12 values)
`person · company · organization · vessel · aircraft · facility · place · payment · filing · case · asset · event`. Derived from `UNIT_OF_OBSERVATION` (already populated on all 1,503 rows). Adopting OCCRP FollowTheMoney types buys interop with Aleph/OpenSanctions later.

### F4 — JOIN_KEYS_STD (the moat — straight from `tag_portal_index.KEY_TOKENS`)

| Tier | Keys | Join trust |
|------|------|------------|
| **STEEL** | EIN NPI CIK UEI DUNS LEI IMO MMSI CCN PATENT | Fact-grade, auto-mergeable |
| **STRONG** | DOCKET NAICS NCES SIC | High |
| **GEO** | FIPS ZIP LATLON COUNTRY GEOM | Map-join only |
| **PROBABILISTIC** | NAME ADDRESS | Lead-grade only — never auto-merge |

Auto-populated from `outputs/connect_fingerprints.json` for landed tables (measured from real columns). You inherit the hard-won exclusions for free (DOI is deliberately out — it false-matched "Date Of Injury").

### F5 — THEME (the investigative lens — the north star, queryable)
The reporter's own verbs:
```
follow_the_money    power_who_holds_it    harm_to_people
sanctions_illicit   revolving_door        corporate_ownership
enforcement_actions public_health_safety  civil_rights_history   epstein
```
"every source tagged `follow_the_money` that also carries a STEEL key" = *follow money into harm*, as a `WHERE`.

### F6 — LIFECYCLE (6 ordered, derived — the honest "what did I actually land")
Fixes the worst gap (1,503 registered / ~55 truly landed). `INCLUDE='Y'` is a lie — it's `Y` on all 593 sample-only portals — so this is **computed, not typed**.

| State | Meaning | Derived from |
|-------|---------|--------------|
| `scouted` | in registry, never loaded | no INGEST_RUNS row |
| `queued` | approved to onboard | INCLUDE='Y', no run |
| `sampled` | proof-slice only (the 593 portals, capped tables) | run exists, row_count below cap |
| `landed` | full data in LANDING | INGEST_RUNS.STATUS='success' |
| `modeled` | has a dbt mart | mart exists in LIBRARY_MARTS |
| `stale` | SHA drifted / load failed | last run failed |

### F7 — TRUST_LAYER (medallion — free)
`raw · staging · mart`. The spine you already run. Keeps "how cooked" separate from "what about."

---

## 2. How Every Source Gets Classified

### The synonym merges (166 categories → 22 domains)

A crosswalk table maps every messy old value to a canonical DOMAIN. The 16 Phase-1 clusters cover the bulk:

| Today's mess (casing/punct/snake_case variants) | → DOMAIN |
|---|---|
| Health / health / Healthcare / healthcare / global health | `health_medicine` |
| Legal/Court/Justice/Courts/law enforcement/criminal justice (8+ labels) | `justice_courts` |
| Corporate Registry / company registry / beneficial-ownership / entity backbone | `corporate_entities` |
| lobbying / Money-in-Politics / campaign finance / political influence / FARA | `money_in_politics` |
| Open Data / national-portal / meta-discovery / aggregators / data preservation | `open_data_portal` |
| transit / Transportation / maritime / flight tracking | `transport_movement` |
| scholarly_literature / academic archive / astronomy / genomics / chemistry | `science_research` |
| Spending & Budget / State Spending / Contracts & Grants | `spending_budget` |
| Energy & Environment / energy grid / climate / air quality / soil | `energy_environment` |
| History & Culture / newspapers / digital heritage / slavery records | `history_culture` |

Source-TYPE labels (`Open Data`, `national-portal`, `aggregators`) leave the topical axis entirely — they describe *shape*, so the portals become `DOMAIN=open_data_portal` and the rest map to `ACCESS_METHOD`/`FORMAT`.

### The cross-domain fix (no forced lies)
`DOMAIN_SECONDARY` is an **array**. SAM exclusions = `sanctions_enforcement` (primary) + `[money_finance, health_medicine]` (secondary). OFAC SDN = `sanctions_enforcement` + `[transport_movement]` (sanctioned vessels). All true at once. A single tree would force a lie here; the array kills it.

### Lifecycle (scouted → in-flight → landed)
Not a column you maintain — a **derived state in the CATALOG view** (§3c). Land a table → it flips to `landed` on the next query. Zero human touch.

---

## 3. The Backend Tool — Snowflake implementation

### 3a. New columns on SOURCE_REGISTRY

```sql
ALTER TABLE LIBRARY_META.REGISTRY.SOURCE_REGISTRY ADD COLUMN
    DOMAIN_PRIMARY    VARCHAR,   -- F1, one of 22
    DOMAIN_SECONDARY  ARRAY,     -- F1, the "SAM is Money AND Health" fix (cap at 3)
    ENTITY_TYPES      ARRAY,     -- F3, FtM types
    JOIN_KEYS_STD     ARRAY,     -- F4, from KEY_TOKENS (auto from fingerprint)
    JOIN_KEY_TIER     VARCHAR,   -- F4, top tier present: STEEL/STRONG/GEO/PROBABILISTIC/NONE
    JOIN_KEY_TIER_PROVISIONAL BOOLEAN,  -- TRUE until fingerprinted from real columns
    THEMES            ARRAY,     -- F5
    HAS_EVENTS        BOOLEAN;   -- "When" axis as a flag, not a bucket
```

Add these 8 to `register._COLUMNS` (line 17 of `library-onboarding/register.py`) or the MERGE won't write them. Keep `JURISDICTION` (clean it, don't re-add). Keep old `CATEGORY`/`SUBCATEGORY` as legacy/audit — demoted, not dropped. **`LIFECYCLE`, `TRUST_LAYER`, `LANDED_ROW_COUNT` are NOT columns** — they're derived in the view (§3c), so they can't go stale.

### 3b. The guard table (so it can never drift back to 166)

```sql
CREATE TABLE LIBRARY_META.REGISTRY.FACET_VOCAB (
    FACET     VARCHAR,   -- 'DOMAIN' | 'ENTITY_TYPE' | 'JOIN_KEY' | 'THEME' | 'JURISDICTION'
    VALUE     VARCHAR,   -- the allowed token
    TIER      VARCHAR,   -- for JOIN_KEY: STEEL/STRONG/GEO/PROBABILISTIC
    LABEL     VARCHAR,
    SORT_ORD  NUMBER
);
```

`FACET_VOCAB` is the **single source of truth** — the mart folders conform to it, not the other way round (so renaming a folder can't silently desync the vocab). A dbt `accepted_values` test validates `DOMAIN_PRIMARY` against it on every run.

### 3c. The CATALOG view — the "what do I have about X" engine

```sql
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.CATALOG AS
WITH landed AS (
    SELECT TABLE_NAME, ROW_COUNT
    FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'LANDING'
),
runs AS (
    SELECT SOURCE_ID, MAX(IFF(STATUS='success', RUN_TS, NULL)) AS last_success,
           MAX(RUN_TS) AS last_run
    FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS GROUP BY 1
),
marts AS (   -- guard: only count names that round-trip to a real SOURCE_ID
    SELECT DISTINCT SPLIT_PART(TABLE_NAME,'__',2) AS sid
    FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
    WHERE SPLIT_PART(TABLE_NAME,'__',2) IN
          (SELECT SOURCE_ID FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY)
)
SELECT
    r.SOURCE_ID, r.NAME,
    r.DOMAIN_PRIMARY, r.DOMAIN_SECONDARY, r.JURISDICTION,
    r.ENTITY_TYPES, r.JOIN_KEYS_STD, r.JOIN_KEY_TIER, r.JOIN_KEY_TIER_PROVISIONAL,
    r.THEMES, r.HAS_EVENTS, r.PRIORITY_TIER,
    CASE
        WHEN m.sid IS NOT NULL                                   THEN 'modeled'
        WHEN runs.last_success IS NULL AND runs.last_run IS NOT NULL THEN 'stale'
        WHEN runs.last_success IS NOT NULL AND l.ROW_COUNT >= 5000   THEN 'landed'
        WHEN runs.last_success IS NOT NULL                       THEN 'sampled'
        WHEN r.INCLUDE = 'Y'                                     THEN 'queued'
        ELSE 'scouted'
    END                                          AS LIFECYCLE,
    l.ROW_COUNT                                  AS LANDED_ROW_COUNT,
    CASE WHEN m.sid IS NOT NULL THEN 'mart'
         WHEN l.ROW_COUNT IS NOT NULL THEN 'raw' ELSE 'none' END AS TRUST_LAYER,
    'LIBRARY_RAW.LANDING.' || UPPER(r.SOURCE_ID) AS LANDING_FQN,  -- HARD invariant: table = UPPER(SOURCE_ID)
    r.URL, r.PUBLISHER, r.DESCRIPTION
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r
LEFT JOIN landed l ON l.TABLE_NAME = UPPER(r.SOURCE_ID)
LEFT JOIN runs     ON runs.SOURCE_ID = r.SOURCE_ID
LEFT JOIN marts m  ON m.sid = r.SOURCE_ID;
```

`LANDING_FQN` is reconstructed from `UPPER(SOURCE_ID)` — the catalog row always points at the right landing table, and `LIFECYCLE='modeled'` learns about marts automatically.

### 3d. Bridge views — so you write `=` not `ARRAY_CONTAINS`

ARRAY columns are powerful but clumsy day-to-day. Wrap them in FLATTEN bridges (build these in v1, not later):

```sql
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_DOMAIN AS
SELECT r.SOURCE_ID, r.DOMAIN_PRIMARY AS DOMAIN, 'PRIMARY' AS ROLE
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r
UNION ALL
SELECT r.SOURCE_ID, d.value::VARCHAR, 'SECONDARY'
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r,
     LATERAL FLATTEN(input => r.DOMAIN_SECONDARY) d;

CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_THEME AS
SELECT r.SOURCE_ID, t.value::VARCHAR AS THEME
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r,
     LATERAL FLATTEN(input => r.THEMES) t;

CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_KEY AS
SELECT r.SOURCE_ID, k.value::VARCHAR AS JOIN_KEY
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r,
     LATERAL FLATTEN(input => r.JOIN_KEYS_STD) k;
```

Now `WHERE DOMAIN='health_medicine'` is a clean predicate. Use the bridges for filtering; use CATALOG for the full row.

### 3e. The DOMAIN summary — the top "menu" screen (browse mode)

```sql
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_DOMAIN_SUMMARY AS
SELECT DOMAIN_PRIMARY AS DOMAIN,
       COUNT(*)                              AS sources,
       COUNT_IF(LIFECYCLE IN ('landed','modeled')) AS landed,
       SUM(LANDED_ROW_COUNT)                 AS total_rows,
       COUNT_IF(LIFECYCLE IN ('scouted','queued'))  AS backlog
FROM LIBRARY_META.REGISTRY.CATALOG
WHERE DOMAIN_PRIMARY <> 'open_data_portal'   -- portals don't drown the real domains
GROUP BY 1
ORDER BY total_rows DESC NULLS LAST;
```

### 3f. Snowsight object tags (the warehouse browser becomes investigation-organized for free)

```sql
CREATE TAG IF NOT EXISTS LIBRARY_META.REGISTRY.THEME_TAG;
-- apply to each landing table from its primary THEME so the move shows up
-- in Snowsight's native browser, not just in the CATALOG view.
```

---

## 4. Navigation — what it feels like

```
RIPPLE LIBRARY — FACETED CATALOG
────────────────────────────────────────────
Slice by any facet (combine freely):
  [1] DOMAIN       money_finance · health_medicine · justice_courts …(22)
  [2] JURISDICTION fed · intl · xc · loc · st
  [3] ENTITY       person · company · vessel · facility …(12)
  [4] JOIN-KEY     STEEL(EIN NPI CIK UEI…) · STRONG · GEO · NAME
  [5] THEME        follow_the_money · revolving_door · epstein …(10)
  [6] LIFECYCLE    scouted · queued · sampled · landed · modeled · stale
────────────────────────────────────────────
> filter domain=health_medicine lifecycle=landed
  16 sources · 12.1M rows  →  [list]
```

**Default browse — the shape of the Library:**
```sql
SELECT * FROM LIBRARY_META.REGISTRY.V_DOMAIN_SUMMARY;
```

**"What do I have on healthcare, with real data?"**
```sql
SELECT SOURCE_ID, NAME, LANDED_ROW_COUNT
FROM LIBRARY_META.REGISTRY.CATALOG
WHERE DOMAIN_PRIMARY = 'health_medicine'
  AND LIFECYCLE IN ('landed','modeled')
ORDER BY LANDED_ROW_COUNT DESC;
-- FED_CMS_NPPES (9.6M), facility affiliation (2.2M), LEIE …
```

**"Everything carrying a vessel ID" — the moat query, impossible today:**
```sql
SELECT c.SOURCE_ID, c.NAME, c.DOMAIN_PRIMARY
FROM LIBRARY_META.REGISTRY.CATALOG c
JOIN LIBRARY_META.REGISTRY.V_SOURCE_KEY k USING (SOURCE_ID)
WHERE k.JOIN_KEY IN ('IMO','MMSI');
-- NOAA AIS, Global Fishing Watch, MarineTraffic, OFAC SDN → sanctioned-vessel investigation, pre-assembled
```

**The north-star query — follow money into harm, fact-grade only:**
```sql
SELECT c.SOURCE_ID, c.NAME, c.DOMAIN_PRIMARY, c.JOIN_KEY_TIER
FROM LIBRARY_META.REGISTRY.CATALOG c
JOIN LIBRARY_META.REGISTRY.V_SOURCE_THEME t USING (SOURCE_ID)
WHERE t.THEME = 'follow_the_money'
  AND c.JOIN_KEY_TIER = 'STEEL'          -- auto-mergeable, not name-matching
  AND c.JOIN_KEY_TIER_PROVISIONAL = FALSE -- fingerprinted, not guessed
  AND c.LIFECYCLE = 'landed';
```

**The backlog — what's worth landing next:**
```sql
SELECT DOMAIN_PRIMARY, COUNT(*) AS scouted_not_landed
FROM LIBRARY_META.REGISTRY.CATALOG
WHERE LIFECYCLE IN ('scouted','queued')
GROUP BY 1 ORDER BY 2 DESC;
-- surfaces crime_security (0 landed!), housing_social (0!), conflict_aid_global (0!)
```

The agent path: reporter says *"follow the money into a hospital chain"* → agent maps to `THEME=follow_the_money` + `DOMAIN IN (health_medicine, spending_budget)` + key in `(CCN,NPI,EIN)` → one WHERE → ranked landed sources → hands SOURCE_IDs to `connect/dossier.py`.

---

## 5. Migration Path — incremental, non-destructive

Stand it up in passes. Each pass is independently useful — you can stop after any one and still have gained something. Old columns are kept the whole way, so it's reversible.

**Pass 0 — Schema (10 min).** Snapshot the registry. Run the `ALTER TABLE` (§3a). Create `FACET_VOCAB` + seed it. Create the `CATALOG` view + the 3 bridge views + summary. Add the 8 columns to `register._COLUMNS`. **At this point the CATALOG view already works** — lifecycle/trust/row-counts are live with zero tagging.

**Pass 1 — Free facets (instant, deterministic, agent).**
- `JURISDICTION` ← SOURCE_ID prefix; fix 10 `US` rows.
- `LIFECYCLE`, `TRUST_LAYER`, `LANDED_ROW_COUNT` ← already derived. Done.

**Pass 2 — JOIN_KEYS_STD from fingerprint (agent).** Read `outputs/connect_fingerprints.json` for the ~55 landed tables → write `JOIN_KEYS_STD` + `JOIN_KEY_TIER`, set `JOIN_KEY_TIER_PROVISIONAL=FALSE`. For unlanded sources, run `tag_portal_index.tag()` over free-text `JOIN_KEYS`+`DESCRIPTION` and set **`PROVISIONAL=TRUE`** (it's a guess until real columns confirm it).

**Pass 3 — DOMAIN crosswalk (agent).** Build `old_category → DOMAIN_PRIMARY` from the 16 clusters; single `UPDATE` keyed on SOURCE_ID. Resolves the ~910 classified rows instantly.

**Pass 4 — Triage the 593 blanks (agent, with a trust flag).** Auto-classify by slug/NAME:
- `portal_*` / `loc_*_open` → `open_data_portal` (clears the bulk)
- `*_lobby*`→`money_in_politics`, `*_court*`→`justice_courts`, `*_census*`→`geo_demographics`, etc.
- **Anything the heuristic isn't confident on → `DOMAIN_PRIMARY='UNCLASSIFIED'`**, not a silent confident-wrong fill. Lifts coverage 61%→~100% but routes the ambiguous tail to a review queue instead of polluting the catalog.

**Pass 5 — Human facets, landed-first (agent proposes → you approve).** ENTITY_TYPES from `UNIT_OF_OBSERVATION`; THEMES + `DOMAIN_SECONDARY` from `ACCOUNTABILITY_RELEVANCE`+`EPSTEIN_RELEVANT`. **Do the ~55 landed sources first** — they're what gets queried. The 1,448 scouted-only get tagged lazily as they onboard.

**Pass 6 — Lock it.** Turn on the dbt `accepted_values` tests against `FACET_VOCAB`. Now the registry *can't* drift.

**Auto vs your eye:** Passes 1–4 are fully agent-automated (deterministic rules + crosswalk). Pass 5's primary-DOMAIN/THEME calls and the `UNCLASSIFIED` residue from Pass 4 are the only places you actually look — and only for landed sources up front.

---

## 6. Maintenance — staying clean to 300+

- **Auto-facets (F2/F4/F6/F7): zero human cost.** They recompute on every load. Land a table → lifecycle flips, trust updates, row-count refreshes. No touch.
- **Human facets (F1/F3/F5): ~30 sec/source**, done by the agent at the REGISTRY checkpoint, you approve with `go`. That's the *normal* onboarding flow — no separate curation job.
- **Vocab changes: rare, centralized.** Adding a 23rd domain is one `INSERT` into `FACET_VOCAB`. Solo-builder advantage — no governance fight.

**Two guards that keep tag discipline from rotting** (this is the design's one real risk — 3 facets are hand-assigned):

```sql
-- Audit 1: carries a cross-domain STEEL key but DOMAIN_SECONDARY is empty
-- (the silent cross-domain collapse the design must catch)
SELECT c.SOURCE_ID, c.DOMAIN_PRIMARY, c.JOIN_KEYS_STD
FROM LIBRARY_META.REGISTRY.CATALOG c
WHERE c.JOIN_KEY_TIER = 'STEEL'
  AND ARRAY_SIZE(c.DOMAIN_SECONDARY) = 0
  AND c.LIFECYCLE IN ('landed','modeled');

-- Audit 2: landed but no THEME, or still UNCLASSIFIED
SELECT SOURCE_ID, NAME FROM LIBRARY_META.REGISTRY.CATALOG
WHERE LIFECYCLE IN ('landed','modeled')
  AND (ARRAY_SIZE(THEMES) = 0 OR DOMAIN_PRIMARY = 'UNCLASSIFIED');
```

Run those monthly (or wire as dbt tests). The `accepted_values` gate stops casing/vocab drift nightly; the two audits catch *under*-tagging the gate can't see. That combo is what makes the catalog survive past 300 landed instead of quietly rotting back toward a single tree.

---

**One-line take:** Faceted catalog on the registry you already have — 8 new columns + a `FACET_VOCAB` guard + one `CATALOG` view + 3 FLATTEN bridges. Four facets fill themselves from the warehouse, JOIN-KEY and THEME make the moat and the north star into `WHERE` clauses, and it stands up incrementally — the CATALOG view works the moment Pass 0 lands, before you've tagged a single thing.

**Files it hooks into:**
- `/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding/register.py` — add 8 cols to `_COLUMNS` (line 17)
- `/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding/naming.py` — JURISDICTION prefix invariant
- `/Users/chrisr./Documents/GitHub/Ripple_v6/portal_recon/tag_portal_index.py` — `KEY_TOKENS` = the JOIN_KEYS_STD vocab (line 86)
- `/Users/chrisr./Documents/GitHub/Ripple_v6/connect/fingerprint.py` + `/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/connect_fingerprints.json` — auto-populate F4
- `/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding/build_library_map.py` — repoint renderer at `CATALOG` for the faceted browse map
- `/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding/ripple_dbt/models/marts/` — 20 folder names = DOMAIN vocab seed (conform folders to `FACET_VOCAB`, not vice versa)