# Plan: Fix Connect Engine and Terrain Map

## Context

The connect engine pipeline (`python -m connect all`) runs four steps: **fingerprint -> discover -> spine -> explore**. The discover step completed successfully and found 1,085 edges across 176 sources. However, the **spine step fails** because `entity_index_specs.py` references a non-existent column `ENTITY_LEGAL_NAME` for the GLEIF table — the actual column is `"Entity.LegalName"` (XML-derived dot notation in the raw landing table).

Additionally, the terrain map visualization has two issues:
1. `build_terrain_map.py` depends on ENTITY_INDEX (which requires a working spine), so it falls back to stale/empty data
2. The hand-built `terrain_map.html` has a rendering bug where `light-dark()` is used as a D3 attribute string (lines 231/311) instead of CSS

The domain edge data is already corrected in Snowflake (IRS 990 reclassified to corporate_entities, USASPENDING_CONTRACTS_FULL to spending_budget).

## Current State

```
Pipeline step        Status
fingerprint          OK - 242 tables profiled
discover             OK - 1,085 edges found across 176 sources  
spine                BROKEN - ENTITY_LEGAL_NAME column doesn't exist
explore              SKIPPED (depends on spine)
terrain_map.html     PARTIALLY WORKING - data correct, SVG strokes broken
build_terrain_map.py STALE - pulls from empty ENTITY_INDEX
```

---

## Implementation Steps

### Step 1: Fix GLEIF Column in entity_index_specs.py

**File:** [connect/entity_index_specs.py](connect/entity_index_specs.py) (line 158-159)

**Current:**
```python
"INTL_GLEIF": {
    "key": "LEI", "key_col": "LEI", "org": "ENTITY_LEGAL_NAME", "authority": 1,
},
```

**Fix:**
```python
"INTL_GLEIF": {
    "key": "LEI", "key_col": "LEI", "org": "Entity.LegalName",
    "city": "Entity.LegalAddress.City",
    "state": "Entity.LegalAddress.Region",
    "zip": "Entity.LegalAddress.PostalCode",
    "authority": 1,
},
```

The dot-notation columns need to be quoted in SQL. Check that `spine.py`'s `_name_expr()` and `_addr_cols()` helpers wrap column names in double quotes (they likely do via `f'"{col}"'`). If not, the quoting needs to be added for dot-containing column names.

---

### Step 2: Fix terrain_map.html SVG Stroke Bug

**File:** [outputs/terrain_map.html](outputs/terrain_map.html) (lines 231, 311)

**Problem:** D3's `.attr('stroke', 'light-dark(#9ca3af, #444)')` sets an inline SVG attribute, not CSS. The `light-dark()` function only works in CSS stylesheets, not as an attribute value.

**Fix options (prefer option A):**

**A) Use CSS classes:**
```css
.link { stroke: light-dark(#9ca3af, #444); }
```
Then remove the `.attr('stroke', ...)` calls entirely — the CSS rule handles it.

**B) Use `currentColor` with CSS:**
```css
.link { color: light-dark(#9ca3af, #444); }
```
Then `.attr('stroke', 'currentColor')`.

Also fix the inline `style="color:light-dark(...)"` on line 56-57 — that should work in CSS stylesheets but verify browser support for inline styles.

---

### Step 3: Upgrade build_terrain_map.py to Use CONNECT_EDGES

**File:** [scripts/build_terrain_map.py](scripts/build_terrain_map.py)

The script currently queries `ENTITY_INDEX` (which is empty when spine fails). Rewrite `build_source_overlap_matrix()` and `build_domain_overlap()` to use `CONNECT_EDGES` directly:

```python
def build_domain_edges(cur):
    """Pull cross-domain edges from CONNECT_EDGES with corrected filters."""
    cur.execute("""
        SELECT 
            ra.DOMAIN_PRIMARY AS domain_a,
            rb.DOMAIN_PRIMARY AS domain_b,
            COUNT(*) AS edge_count,
            SUM(e.MATCHED) AS total_shared
        FROM LIBRARY_META."CONNECT".CONNECT_EDGES e
        LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY ra ON UPPER(ra.SOURCE_ID) = e.A
        LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY rb ON UPPER(rb.SOURCE_ID) = e.B
        WHERE e.A NOT LIKE 'PORTAL_%' AND e.B NOT LIKE 'PORTAL_%'
          AND COALESCE(ra.DOMAIN_PRIMARY, 'x') != COALESCE(rb.DOMAIN_PRIMARY, 'y')
          AND NOT (e.KEY = 'ZIP' AND e.TIER = 'GEO')
          AND e.CONFIDENCE >= 0.3
        GROUP BY 1, 2
        HAVING SUM(e.MATCHED) >= 50
        ORDER BY total_shared DESC
    """)
    return cur.fetchall()
```

Add a `build_top_source_edges()` function that fetches the top 15 cross-domain edges and generates explain text based on templates keyed by `(TIER, KEY)` combinations:

| Tier + Key | Template |
|---|---|
| STEEL + CIK/NPI/EIN/etc | "{matched} entities linked by exact {key} identifier..." |
| CORROBORATED + NAME@ZIP | "{matched} entities share name+ZIP across both datasets..." |
| GEO + FIPS | "{matched} counties appear in both datasets..." |

The node weights should be computed as cross-domain-only (sum of MATCHED where source domain differs from partner domain).

Keep the ENTITY_INDEX path as a fallback for bridge-entity detection (only works post-spine), with a graceful skip if the table is empty.

---

### Step 4: Run Spine Rebuild

After the GLEIF fix, execute:
```
python -m connect spine
```

Expected result: The spine builds ENTITY_GOLDEN and ENTITY_INDEX tables across all spec'd tables (NPI, EIN, CIK, LEI, UEI, IMO, BIOGUIDE, ICPSR). This unlocks bridge-entity detection (entities spanning 3+ domains).

If it fails on other specs, each failure is a column name mismatch — fix iteratively by checking INFORMATION_SCHEMA.COLUMNS for each table.

---

### Step 5: Fix Remaining Domain Misclassifications

Run a sweep query to find suspicious classifications:

```sql
-- Same-source splits (same base name, different domains)
SELECT a.SOURCE_ID, a.DOMAIN_PRIMARY, b.SOURCE_ID, b.DOMAIN_PRIMARY
FROM SOURCE_REGISTRY a JOIN SOURCE_REGISTRY b
  ON REPLACE(a.SOURCE_ID, '_FULL', '') = REPLACE(b.SOURCE_ID, '_FULL', '')
  AND a.SOURCE_ID != b.SOURCE_ID
  AND a.DOMAIN_PRIMARY != b.DOMAIN_PRIMARY;
```

Known remaining candidates:
- `FED_USASPENDING_ASSISTANCE_FULL` — already fixed to spending_budget
- Check if any PORTAL sources with STEEL keys are misclassified (23 of them have hard keys)

---

### Step 6: Full Pipeline Re-run and Final Map

Execute sequentially:
```bash
python -m connect all       # ~15-20 min for 242 tables
python scripts/build_terrain_map.py
```

Then open `outputs/terrain_map.html` and verify:
- Domain graph shows 14+ connected domains
- Node sizes are proportional (no single domain 37x bigger)
- Sidebar has honest explain text
- Bridge entities panel is populated (entities in 3+ domains)
- SVG renders correctly in both light and dark mode

---

## Verification

1. **Spine builds without error:** `python -m connect spine` exits 0, ENTITY_INDEX has > 0 rows
2. **Terrain map renders:** Open in browser, force graph animates, sidebar shows cards
3. **No overclaimed data:** Spot-check 3 explain sentences against the actual TIER/KEY/MATCHED
4. **Light/dark mode:** Toggle browser color scheme, verify SVG strokes adapt
5. **Cross-domain only:** Run `SELECT * FROM domainEdges WHERE s = t` on the inline data — should return 0

## Critical Files

- `connect/entity_index_specs.py` — The GLEIF column fix (root cause of spine failure)
- `connect/spine.py` — Builds ENTITY_GOLDEN/ENTITY_INDEX; must handle dot-notation columns in SQL
- `scripts/build_terrain_map.py` — Needs rewrite to use CONNECT_EDGES instead of ENTITY_INDEX
- `outputs/terrain_map.html` — SVG stroke bug fix and final output verification
- `connect/discover.py` — Reference for how edges are created (no changes needed, but explains the data flow)
