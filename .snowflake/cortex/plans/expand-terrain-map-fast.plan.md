# Plan: Expand Terrain Map (Fast Path)

## Context

The prior `connect all` attempt burned 45+ minutes fingerprinting 1,805 tables serially — 1,563 of those were PORTAL stubs that add noise but no signal. The fix: pass a source list that EXCLUDES portals, cutting the job from 1,805 tables to ~242.

The connect engine supports `--source-ids-file` (a newline-delimited list). We'll:
1. Generate a file of non-PORTAL source IDs
2. Run `connect all` scoped to just those
3. Then run `build_terrain_map.py` to produce the visualization

Expected time: ~10-15 minutes for fingerprinting 242 tables + discover + spine.

## Implementation Steps

### Step 1: Generate source list file (exclude PORTAL)

Query LANDING tables where name does NOT start with PORTAL_, write to a text file. This gives us the ~242 analytical sources only.

### Step 2: Run connect with scoped source list

The connect engine's fingerprint/discover/spine steps will run on ~242 tables instead of 1,805. Based on the prior run's rate (it processed ~150 FED/INTL tables in ~20 minutes), the full 242 should finish in ~15 minutes.

Command: `python -m connect all --source-ids-file scripts/analytical_sources.txt`

If `--source-ids-file` isn't supported on the `all` subcommand, we'll run the three steps individually:
- `python -m connect fingerprint --source-ids-file ...`
- `python -m connect discover`
- `python -m connect spine`

### Step 3: Build terrain map

Run `python scripts/build_terrain_map.py` which builds:
- SOURCE_OVERLAP_MATRIX (source-to-source shared entities)
- DOMAIN_OVERLAP_MATRIX (domain-to-domain)
- CLUSTER_ASSIGNMENTS (connected components)
- BRIDGE_ENTITIES (entities spanning 3+ domains)
- outputs/terrain_map.html (interactive D3 visualization)

## Verification

- `SELECT COUNT(DISTINCT SOURCE_TABLE) FROM LIBRARY_META."CONNECT".ENTITY_INDEX` should be 50+ (up from 31)
- `terrain_map.html` exists and renders in browser

## Critical Files

- [connect/__main__.py](connect/__main__.py) — CLI entry point, check if source filtering is supported
- [connect/fingerprint.py](connect/fingerprint.py) — where table list is built (may need to filter here)
- [scripts/build_terrain_map.py](scripts/build_terrain_map.py) — already written, ready to run
