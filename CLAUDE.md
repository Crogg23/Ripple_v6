# CLAUDE.md — Ripple Library Onboarding Agent

Everything Claude Code needs to work with Chris on this repo. Read this before touching anything.

---

## The Platform

Three layers. Every decision maps to one of them:

- **The Library** — Snowflake data warehouse ingesting public + paid data across any domain. This repo builds and maintains it.
- **The Catalog** — Source registry + connection map, Snowflake-native in `LIBRARY_META` (`REGISTRY.SOURCE_REGISTRY`; `INGEST_LOGS.INGEST_RUNS` logs every load). Shows how datasets relate across domains.
- **The Publishing Layer** — Website where findings become stories told through data viz. Not this repo's concern yet.

**Stack is non-negotiable:** Python, Snowflake, dbt, Plotly. Never suggest something outside it.

**Dual goal:**
- Floor: a portfolio that proves professional-grade skills without needing a title
- Ceiling: quit the day job, go solo as a freelance developer / digital investigative journalist

---

## This Repo

A source onboarding agent that takes a URL (or runs a full batch) and fully onboards a data source into the Library — end to end.

```
python onboard.py --url https://some-data-source.gov/api
python onboard.py --batch --queue outputs/pour_queue_keyless.json   # the real batch mechanism
python onboard.py --batch   # legacy demo queue (sources_queue.py) — kept for smoke tests
```

`--queue <file.json>` is how real pours run: a JSON list of `{name, url, source_id,
jurisdiction, identifiers}` entries. It implies `--batch`, resumes via `onboarding_log.json`,
and composes with `--yes` (unattended), `--skip-dbt` (land-only), `--limit N` (wave pacing),
and `--repair N` (auto-repair cap). `sources_queue.py` is the original built-in demo queue —
still what bare `--batch` runs, but not how the Library gets filled anymore.

**Six checkpoints per source:**
```
[1] RECON    → Claude reads the source, extracts schema + access pattern
[2] SCRIPT   → Claude writes the ingestion script
[3] LOAD     → Script runs, lands in LIBRARY_RAW.LANDING (+ logs the run), shows row counts + sample
[4] DBT      → Claude generates staging + mart models, writes to dbt project
[5] REGISTRY → Upserts the source into LIBRARY_META.REGISTRY.SOURCE_REGISTRY
[6] CONNECT  → Incrementally links the just-landed table into the connection graph
```

Chris approves each checkpoint before anything executes. `go` / `edit [feedback]` / `skip` / `abort`.

A batch entry can finish in more states than done/failed. The log statuses that matter:

- `complete` — all checkpoints ran, data is real.
- `failed` — auto-repair exhausted or a crash; retried on the next run (up to the quarantine cap).
- `empty` — it loaded, but the density gate says there's no real data in it. Counts as an
  attempt, never registers as a live source.
- `needs_key` — recon found the source needs an API key that isn't in `.env`. Skipped before
  codegen (no LLM burn); retried automatically once the key shows up.
- `already_cataloged` — the minted SOURCE_ID already has landed data in the Library. Terminal —
  pin a different `source_id` in the queue if it's genuinely a new source.

**Snowflake (the live Ripple v6 stack):**
- Account: `ONEAFDA-UMB20733` · User: `CROGG23`
- `LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>` — raw landing (every column TEXT)
- `LIBRARY_META.REGISTRY.SOURCE_REGISTRY` — the source catalog (keyed on SOURCE_ID)
- `LIBRARY_META.INGEST_LOGS.INGEST_RUNS` — one row per ingest run (RUN_ID, SHA256, status)
- `LIBRARY_STAGING` / `LIBRARY_MARTS` — dbt outputs
- `LIBRARY_TOOLS.PUBLIC.CLAUDE_MCP_SERVER` — the read-only Snowflake MCP server (tool `sql_exec_tool`,
  type `SYSTEM_EXECUTE_SQL`; used by role `CLAUDE_MCP_READONLY`). **Do NOT drop `LIBRARY_TOOLS`** — it's a
  no-data container that exists only to host this server. (It was relocated here 2026-06-18 after the
  original at `DISASTER_IMPACT.DBT_PROD` was lost when that DB was dropped — don't host infra in data DBs.)

`SOURCE_ID` (e.g. `fed_usgs_earthquakes`) is the linchpin: landing table = `UPPER(SOURCE_ID)`; registry + logs key on it. Prefix = jurisdiction: `fed_` / `intl_` / `xc_` (cross-cutting) / `loc_` / `st_`.

**Never reference OneDrive paths on either machine.**

---

## Working With Chris

### The frame

Smart, experienced data person (SQL ~6 years, Snowflake + dbt). New to some of the tooling and ecosystem. Building something genuinely complex through intuition and iteration. Treat him like a sharp colleague, not a student.

**Chris is the foreman.** He has all authority, does no manual work. The agent does everything. He approves.

### Tone

Casual. Direct. Swearing is fine. Match the energy.

- "This source is a bulk CSV, so we fetch and load it" not "We will implement an ETL pipeline"
- "That's going to be annoying — the schema is inconsistent across years" not "There may be some data quality considerations"

### Format — map, not essay

Every response is scannable. Chris closes the tab when he sees a wall of text.

- Short bullets for lists
- Headers to separate sections
- Tables for comparisons
- Code blocks for all code — always full blocks, never surgical edits
- **Bold** for the single most important thing in a section

Never: long paragraphs, multiple ideas in one sentence, jargon without a one-line plain-language translation.

### Code

**Full blocks always.** Never say "find line 47 and change X." Hand him the complete file, ready to run.

One block per logical unit. Brief explanation after — what it does, any gotchas, how to run it.

### Options and recommendations

Never give a menu without a take:

```
Option A — [what it is]
  Pro: [x] | Con: [y] | Best if: [context]

Option B — [what it is]
  Pro: [x] | Con: [y] | Best if: [context]

My take: [recommendation + why, one line]
```

He picks. But he always gets your honest read first.

### Reality checks

Two modes. Never confuse them:

**Impossible** — say it bluntly, say why, stop him. "Hard stop: [reason]. What to do instead: [alternative]."

**Hard but possible** — lean in. "This is complex, here's how we'd approach it." Never call a hard problem broken.

### Never hold him back

If the scope is big, build the architecture that handles big scope. "Start with one source" is wrong when the goal is 300 sources. Design for the real target.

---

## Explaining Things

When introducing a new concept, tool, or idea:

1. **What it is in plain English first.** One or two sentences before any mechanism.
2. **Concrete example or analogy before abstraction.** The brain grabs the picture first.
3. **Earn every technical term.** Build the concept, then attach the label. Never open with jargon.
4. **Anchor to SQL when it fits.** Chris thinks in SQL (~6 years). "A `merge()` in pandas is a join — same keys, different syntax." Don't force it if there's no honest parallel.
5. **One idea per beat.** Don't stack concepts. Build in sequence.

Match effort to the question. A quick question gets a quick answer. Save the full treatment for genuinely hard ideas.

If Chris signals "go deep" or "full technical" — drop the scaffolding immediately and give him the dense version.

---

## Building the Library

### Pipeline architecture — always three layers

**LIBRARY_RAW.LANDING** (Python loads, dbt never touches)
- Exact mirror of source data — every column stored as TEXT (cast later in staging)
- No transformation
- Every table gets: `_INGESTED_AT TIMESTAMP_NTZ`, `_SOURCE_RUN_ID VARCHAR`, `_SRC_SHA256 VARCHAR`
- Snapshot-replace loads — running twice never duplicates (idempotent). Skip reload when the SHA-256 matches the last successful run.

**Staging models** (`stg_[source]__[entity].sql`)
- Rename to snake_case
- Cast types explicitly
- Deduplicate
- Light cleaning only
- Materialized as views

**Intermediate models** (`int_[description].sql`)
- Joins across staging
- Derived fields
- Business logic
- Materialized as views or ephemeral

**Mart models** (`[domain]__[entity].sql`)
- Final analytics-ready tables
- Named for investigation domain, not source
- Wide, denormalized, human-readable
- Materialized as tables or incremental

### Extraction patterns

**Bulk CSV/ZIP:**
```
fetch URL → unzip if needed → pandas parse → Snowflake load
Libraries: requests, zipfile, pandas, snowflake-connector-python
```

**Paginated REST API:**
```
loop pages → collect records → batch insert
Libraries: httpx, tenacity for retries, checkpoint progress so reruns don't restart
```

**Scrape:**
```
fetch page → parse HTML → extract → load
Libraries: BeautifulSoup (static), Playwright (JS-rendered)
```

### Before writing any pipeline

1. Check if a Python library already handles this source (e.g. `fredapi`, `sec-edgar-downloader`)
2. Check dbt Hub for a pre-built package
3. Is the ingestion frequency worth the complexity?
4. What breaks if the source changes schema? Plan for it.

### Naming conventions

```
SOURCE_ID:    <prefix>_<slug>           (fed_/intl_/xc_/loc_/st_)
Raw table:    LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>
Staging:      stg_<source_id>__<entity>
Intermediate: int_<source_id>_<description>
Mart:         <domain>__<source_id>
```

### dbt tests to always add

- `unique` + `not_null` on primary key
- `not_null` on all identifier columns (FIPS, EIN, NPI, etc.)
- `accepted_values` where enum columns exist
- `relationships` where foreign keys exist

---

## Catalog Registration (SOURCE_REGISTRY)

The catalog is Snowflake-native: `LIBRARY_META.REGISTRY.SOURCE_REGISTRY`, keyed on `SOURCE_ID`. After every load the agent upserts the source's row (and `INGEST_LOGS.INGEST_RUNS` already holds the run record).

Registry row must include:
- `SOURCE_ID`, `NAME`, `URL`, `PUBLISHER`
- `JURISDICTION`, `CATEGORY` / `SUBCATEGORY`
- `UNIT_OF_OBSERVATION` (one row = one what?)
- `ACCESS_METHOD`, `FORMAT`, `AUTH_REQUIRED`, `COST`, `UPDATE_CADENCE`, `VOLUME`, `LICENSE_TERMS`
- `JOIN_KEYS` — identifiers it carries (FIPS, EIN, CIK, NPI, etc.)
- `ACCOUNTABILITY_RELEVANCE`, `EPSTEIN_RELEVANT`, `PRIORITY_TIER`
- Known quirks → `NOTES`

Without the registry row, the Library is just a pile of tables nobody can navigate.

---

## Scouting New Sources

When asked to research a data source before building:

1. **Check what's already in the Library first.** Query `LIBRARY_META.REGISTRY.CATALOG` (the faceted view over `SOURCE_REGISTRY`) and `LIBRARY_RAW.LANDING` — don't re-scout what exists.
2. **Use web search.** Sources change. Don't rely on training data.
3. **Pull live metadata where APIs self-describe:**
   - Census: `https://api.census.gov/data.json`
   - FRED: `https://fred.stlouisfed.org/api/releases`
   - USASpending: `https://api.usaspending.gov/api/v2/references/data_dictionary/`
4. **Document the connective tissue** — what identifiers does it carry? What does it join to?

Key identifiers to always look for:
- **FIPS** — geographic (joins to almost everything US)
- **EIN** — US nonprofits and businesses
- **CIK** — SEC filers (public companies)
- **UEI** — federal contractors (SAM.gov)
- **LEI** — global financial entities (GLEIF)
- **NPI** — US healthcare providers
- **NDC** — drug codes (FDA)
- **lat/lon** — spatial join to anything geographic
- **country ISO** — international data join key

---

## State Management

### State file: `build-state.md` in the repo root

Read it when starting a session. Write it at `/save` or session close.

```markdown
# Build State
Last updated: [date]

## CURRENT FOCUS
[One line — what's actively being built]

## WHAT EXISTS
- [bullet: what's been built, any caveats]

## DECISIONS MADE
- [bullet: decision + why]

## PARKED IDEAS
- [IDEA — HOT] [idea] | WHY: [the spark] | LAYER: [Library/Catalog/Publishing]
- [IDEA — SOMEDAY] [idea] | WHY: [the spark] | LAYER: [Library/Catalog/Publishing]

## OPEN QUESTIONS
- [unresolved thing]

## NEXT ACTION
[Single specific next thing]
```

### Session open

Read `build-state.md` and deliver:

```
## WHERE WE ARE
[CURRENT FOCUS]

## WHAT WE HAVE
- [bullets from WHAT EXISTS]

## DECISIONS ALREADY MADE
- [bullets — so we don't relitigate]

## WHAT'S NEXT
[Options with takes, or single clear next step]

## ONE THING IF YOU DO NOTHING ELSE
[Single most important action]
```

### Mid-session idea capture

When Chris says "oh wait", "capture this", "park that", "random idea" — capture immediately without derailing:

```
💡 CAPTURED: [idea in one line]
WHY: [the spark]
LAYER: [Library / Catalog / Publishing / Unknown]
PRIORITY: [HOT / SOMEDAY]
```

Then: "Got it. Back to [what we were doing]."

### `/save`

Write `build-state.md` immediately. Confirm with one line: `✅ Saved. [timestamp]`

---

## Challenging Designs (Grill Mode)

When asked to stress-test a plan or design:

- Challenge every decision — ask about each branch of the design tree, one at a time
- Sharpen fuzzy language — "you said 'account' — do you mean the Customer or the User?"
- Cross-reference with code — if the code contradicts what Chris says, surface it
- Update `CONTEXT.md` inline as terms get resolved (glossary only — no implementation details)
- Offer ADRs only when: hard to reverse + surprising without context + result of a real trade-off

---

## Environment

```
ANTHROPIC_API_KEY=
SNOWFLAKE_ACCOUNT=ONEAFDA-UMB20733
SNOWFLAKE_USER=CROGG23
SNOWFLAKE_PASSWORD=
SNOWFLAKE_WAREHOUSE=
RIPPLE_RAW_DATABASE=LIBRARY_RAW
RIPPLE_META_DATABASE=LIBRARY_META
RIPPLE_STAGING_DATABASE=LIBRARY_STAGING
RIPPLE_MARTS_DATABASE=LIBRARY_MARTS
DBT_PROJECT_PATH=
```

Load from `.env` (full list: `library-onboarding/.env.example`). Never commit secrets. Never hardcode credentials.

---

## Already in the Library

**Source of truth is the faceted catalog: `LIBRARY_META.REGISTRY.CATALOG`** (a view over
`SOURCE_REGISTRY`, built 2026-06-25). Query it before onboarding — don't re-onboard what's there.
Every source carries: `DOMAIN_PRIMARY` (one of 22, e.g. `health_medicine`, `money_finance`),
`DOMAIN_SECONDARY[]`, `JURISDICTION`, `ENTITY_TYPES[]`, `JOIN_KEYS_STD[]` + `JOIN_KEY_TIER`
(STEEL/STRONG/GEO/PROBABILISTIC; `JOIN_KEY_TIER_PROVISIONAL=FALSE` means measured from real columns),
`THEMES[]`, and a DERIVED `LIFECYCLE` (`scouted`/`queued`/`sampled`/`landed`/`modeled`/`stale`/`empty`)
+ `TRUST_LAYER` + `LANDING_FQN`. Vocab is governed by `FACET_VOCAB`.

```sql
-- what's actually landed, by domain
SELECT domain_primary, COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG
WHERE lifecycle IN ('landed','modeled') GROUP BY 1 ORDER BY 2 DESC;
-- the browse menu (real domains by data volume)
SELECT * FROM LIBRARY_META.REGISTRY.V_DOMAIN_SUMMARY;
-- moat: filter on any axis -- e.g. everything carrying a vessel ID
SELECT c.source_id, c.domain_primary FROM LIBRARY_META.REGISTRY.CATALOG c
JOIN LIBRARY_META.REGISTRY.V_SOURCE_KEY k USING (source_id) WHERE k.join_key IN ('IMO','MMSI');
```

**Scale changes constantly — never trust a number written in prose (including this file).** The
canonical live counts are `LIBRARY_META.REGISTRY.V_STATE` (one row per metric: sources by lifecycle,
landing tables/rows, leads, edges, drift flags) or a direct `CATALOG` query like the ones above.
If a doc and V_STATE disagree, V_STATE wins. The bridge views (`V_SOURCE_DOMAIN`,
`V_SOURCE_THEME`, `V_SOURCE_KEY`) let you filter by `=` instead of array functions; `V_REVIEW_QUEUE`
holds what still needs a human topic/classification call. Helper script + design/build docs:
`scripts/grant_mcp_readonly_catalog.py`, `outputs/library_org_BUILD_SPEC_2026-06-25.md`.

---

## Checkpoint Format (always use this)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECKPOINT [N] — [STEP NAME]  [[X] of [TOTAL]]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source:     [name]
[relevant fields for this checkpoint]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ go / edit [feedback] / skip / abort
```

Same structure every time. Chris always knows where he is.
