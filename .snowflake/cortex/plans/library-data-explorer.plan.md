---
name: "library data explorer"
created: "2026-07-28T14:07:58.652Z"
status: pending
---

# Plan: THE\_LIBRARY Interactive Data Explorer

## Context

**What we explored:**

- THE\_LIBRARY has 404 objects but 153 are FT\_SNAPSHOT duplicates -> showing 251 curated tables
- FRIENDLY\_LAYER provides plain-English descriptions for all 251 (avg 330 chars, max 618)
- CONNECT\_EDGES provides join relationships but needs UPPER() case fix on SOURCE\_ID
- 14,486 total columns across those tables
- Entity edges (NPI, EIN, BIOGUIDE, etc.): \~234 connections — bold, default visible
- Geographic edges (ZIP, FIPS, COUNTRY): \~656 connections — ghost lines, 20% opacity
- Most-connected node: 22 edges (no supernova hub problem)
- Cross-schema entity links are sparse (\~15) — geo ghosts provide the "web" feeling
- Estimated file size: \~2.5MB — fast to load, works offline

**Key design decisions (confirmed):**

- Exclude FT\_SNAPSHOT tables (duplicates)
- Force-directed organic layout (cose-bilkent for compound nodes)
- Geographic edges as ghost lines (20% opacity), entity edges bold
- Search by table name, description, or column name
- Single standalone HTML file, no CDN, no AI, no server

## Implementation Steps

### Step 1: Extract Metadata JSON

Three Snowflake queries:

```sql
-- Nodes: tables with descriptions
SELECT FRIENDLY_SCHEMA, FRIENDLY_NAME, ONE_LINER, COMMENT, ROW_COUNT, 
       UPPER(SOURCE_ID) as SOURCE_ID, THE_LIBRARY_FQN
FROM LIBRARY_META.REGISTRY.FRIENDLY_LAYER;

-- Edges: table relationships  
WITH ls AS (
  SELECT DISTINCT UPPER(SOURCE_ID) as SRC, FRIENDLY_SCHEMA, FRIENDLY_NAME
  FROM LIBRARY_META.REGISTRY.FRIENDLY_LAYER
  WHERE SOURCE_ID IS NOT NULL AND SOURCE_ID != ''
)
SELECT a.FRIENDLY_SCHEMA as schema_a, a.FRIENDLY_NAME as table_a,
       b.FRIENDLY_SCHEMA as schema_b, b.FRIENDLY_NAME as table_b,
       e.KEY, e.TIER, e.MATCHED, e.CONFIDENCE
FROM LIBRARY_META."CONNECT".CONNECT_EDGES e
JOIN ls a ON e.A = a.SRC
JOIN ls b ON e.B = b.SRC;

-- Columns: schema for each table
SELECT table_schema, table_name, column_name, data_type
FROM THE_LIBRARY.INFORMATION_SCHEMA.COLUMNS
WHERE table_schema NOT IN ('INFORMATION_SCHEMA', 'PUBLIC')
  AND table_name NOT LIKE 'FT_SNAPSHOT%'
ORDER BY table_schema, table_name, ordinal_position;
```

Output: JSON blob embedded in the HTML as `const DATA = {...}`.

### Step 2: Vendor Graph Library

- Download cytoscape.js v3.x UMD bundle (minified, \~800KB)
- Download cytoscape-cose-bilkent layout extension (\~60KB)
- Inline both in `<script>` tags at top of HTML
- No external requests at runtime

### Step 3: Graph Structure

```
Compound node hierarchy:
  Schema (parent) -> contains Table (child) nodes

Node styling:
  - Schema nodes: large rounded rectangles, labeled, colored by domain
  - Table nodes: small circles inside schema, labeled on hover/click

Edge styling:
  - Entity keys (NPI, EIN, BIOGUIDE, CIK, CCN, DOCKET, LEI, ICPSR): 
    bold, colored by key type, visible by default
  - Geographic keys (ZIP, FIPS, NAME@ZIP, COUNTRY, GEO_IN, NAME@FIPS):
    thin, 20% opacity gray, visible as ghost layer

Layout: cose-bilkent
  - nodeRepulsion: high enough to spread schemas apart
  - idealEdgeLength: tuned for readability
  - Compound gravity keeps tables clustered within their schema
```

### Step 4: Detail Sidebar

When a table node is clicked, right sidebar (300px wide) shows:

- Table name (large heading)
- One-liner (subtitle)
- Full description (paragraph)
- Row count badge
- Columns table (name | type), scrollable
- "Connected via" section: grouped by key type, each entry clickable to navigate

### Step 5: Search and Filter

- Search input: debounced, fuzzy-matches against table names, one-liners, and column names
- Schema toggles: checkboxes or pill buttons to show/hide entire schemas
- Edge toggle: "Show geographic connections" checkbox (default OFF for bold view, but ghosts still visible)
- Reset button: returns to default view

### Step 6: Visual Polish

- Dark graph background (#1a1a2e or similar) — nodes and edges pop
- Stats banner at top: "251 datasets / 24 domains / 14,486 columns / 234 entity connections"
- System font stack (Inter → Segoe UI → sans-serif)
- Smooth 300ms transitions on expand/collapse
- Initial auto-fit to viewport
- Zoom controls (+ / - buttons) in corner

### Step 7: Rebuild Script

`rebuild_explorer.py`:

- Connects via snowflake-connector-python (using stored connection)
- Runs the three queries
- Writes JSON blob
- Reads HTML template, injects JSON, writes final `the_library_explorer.html`
- One command: `python reports/rebuild_explorer.py`

## Verification

1. Open `the_library_explorer.html` as `file://` in Chrome — graph renders, no console errors
2. Click a schema — tables visible, sidebar works
3. Click a table — sidebar shows columns, description, connections
4. Search "hospital" — HEALTH tables highlight
5. Toggle geo edges — ghost lines appear/strengthen
6. Verify no external network requests (DevTools Network tab empty)
7. Test on a second machine (no install required, just open the file)

## Critical Files

- `c:\Code\Ripple_v6\reports\the_library_explorer.html` — the deliverable
- `c:\Code\Ripple_v6\reports\rebuild_explorer.py` — regeneration script
- `c:\Code\Ripple_v6\reports\vendor\cytoscape.min.js` — vendored lib (inlined during build)

## Risk Register

| Risk                                     | Likelihood | Mitigation                                                                                |
| ---------------------------------------- | ---------- | ----------------------------------------------------------------------------------------- |
| Force-directed layout looks random/messy | Medium     | Use cose-bilkent (designed for clusters), add "re-layout" button, pin after stabilization |
| 251 labels overlap and become unreadable | Medium     | Only show labels on hover or when zoomed in. Schema labels always visible.                |
| Cytoscape.js file too large to inline    | Low        | 800KB is fine. Could gzip but unnecessary.                                                |
| FRIENDLY\_LAYER descriptions go stale    | Low        | Rebuild script re-extracts. Run after each pour.                                          |
| Color palette looks unprofessional       | Low        | Use a pre-selected 24-color palette (categorical, accessible). Not random.                |
