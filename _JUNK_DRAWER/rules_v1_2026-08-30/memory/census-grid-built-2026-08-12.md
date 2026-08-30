---
name: census-grid-built-2026-08-12
description: "the measurement-grammar grid shipped — 1,765 models classified into noun/event/link/code from metadata only; parking tally is the roadmap; source bookkeeping doesn't reconcile"
metadata: 
  node_type: memory
  type: project
  originSessionId: 65369c52-a5cc-445f-987b-8b58cc3ba44c
  modified: 2026-08-18T01:35:19.747Z
---

The census grid ([[warehouse-measurement-grammar-2026-08-12]]) was built 2026-08-12,
entirely from repo metadata (dbt manifest + model SQL + source yml descriptions),
**zero warehouse queries**. Outputs in `reports/census_grid_2026-08-12/`
(SUMMARY.md + 8 CSVs), builders in `scripts/census/` (extract_models.py →
build_grid.py, deterministic, no LLM at runtime).

**Numbers:** 1,765 models → 38 families / 278 things / 52,235 grid cells
(30,509 ready-to-fill, 21,726 structural holes, all visible). 4,357 parked
branches; tally ranks the roadmap: per-person-served (1,426) > lineage (658) =
harm-join (658) > no-date-column (616) > spine-join (615) > assessed-vs-collected
(160). Classification evidence recorded per model; residue kept visible: 9
unmapped, 235 shape-guessed ("unresolved" family), 12 with unrecoverable column
lists (NPPES etc. — columns live only in the warehouse).

**Census finding:** the platform has no authoritative source list — onboarding
log says 774 attempted (88 complete, 684 "failed"), yet 1,141 source dirs are
staged and 1,329 raw landing tables exist; no shared key joins these. Parked as
needs-crosswalk.

**Design calls made (Chris said "go" to the widened design):** dual-listing
instead of event→noun promotion (class is a role); slots derived from column
semantic types so unfillable slots show as holes; fallback classifications land
in "unresolved", never in real families; container words (document/report/list)
lose to specific words in the token scan.

**Traps hit building it:** Snowflake `select * exclude(...)` / `* replace(...)`
defeat naive SQL parsing; `{# #}` jinja comments corrupt paren tracking;
subject-dir names leak into name-token scans (justice__ → "justice person" bug).

**FILLED 2026-08-17** (Chris: "full send"; actual cost ~$2 vs $6–21 quote —
the 2026-08-11 verification scan was reusable for 562/589 marts, only 27 fresh
scans needed). All 589 mart models measured: 1.23B rows, 306 fresh into 2026,
12 stale (990 index stops Jan 2020). Outputs in
`reports/census_grid_2026-08-12/fill/` (FILL_SUMMARY.md + fill_tables.csv);
builders in `scripts/census/`. **Pension EIN check PASSED** — 100% filled,
4,431 distinct, no masking, but leading zeros stripped (join zero-padded).
Staging→raw crosswalk parsed from model SQL (1,170/1,172; 2 broken staging
views: college-scorecard, OSHA inspections). Ranked trap census: FAERS
reactions 76% dup rows, contracts epoch-1970 on all 20M rows, NEISS 9.8M
far-future dates, SEC fund tables year-0095 dates, foreign-assistance EIN a
single repeated value. Court internal IDs are real keys, still zero edges —
registration is the next unlock.
