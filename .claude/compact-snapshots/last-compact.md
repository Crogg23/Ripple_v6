# Snapshot taken right before context compaction

## STATUS.md at compaction time
# RIPPLE STATUS — 2026-08-29 — Full-rebuild ritual retired: `apply-config` applies key/spec changes as bounded reslices; 08-29 ID batch flipped ON in code, waiting for Chris to run the one command

*One screen. Rewritten (never appended) at the end of every session.*

## 🚨 Read this first

1. **The "every new key needs a 4.5h rebuild" rule is dead — and the 4.5h was never
   true.** Query history: the 08-28 rebuild was ~50 busy-minutes on X-Small (~$2–3);
   the 08-11 one took 25 min. The stale "$10–15 / 4.5h" quote had been repeated since
   08-08. Logged as feedback memory.
2. **New system (shipped, tested offline, not yet run live):** config is pinned per
   unit (per key family / per spine spec / per table's graph keys). On drift,
   `python -m connect apply-config` classifies the change and reslices ONLY the tables
   it touches (new family → its tables; changed normalizer → tables carrying it; new
   extra key → that table; removed spec → retract). The heartbeat auto-applies drift
   instead of refusing. A full rebuild re-pins and stays the equivalence backstop.
   Design + measured numbers: `reports/recon/apply_config_design_2026-08-29.md`.
3. **The 08-29 ID batch is now ON in code** (CAGE, award key, PECOS PAC/enrollment ids,
   FDIC cert, Fed RSSD, EIA plant + utility ids; verified live earlier today —
   `reports/recon/bucket_b_wiring_2026-08-29.md`). Offline plan: 19 spine reslices +
   11 graph reslices, 0 retractions; the 93M-row contracts table is the long pole.
   First run auto-pins the flags-off baseline (proven: it reproduces the live sentinel).
4. **🚨 Pre-existing bug found and fixed in the incremental engine:** the "what changed"
   set was written as `NEW MINUS OLD UNION OLD MINUS NEW` without parentheses;
   Snowflake reads that left-to-right, so it collapsed to `OLD MINUS NEW` — every
   incremental run since the engine shipped has silently skipped ADDED keys in the
   entity map / nodes / pairs (index + golden were unaffected). Live-proven: a new
   table previewed affected=0 with 54,406 keys; after the fix 54,406. No live damage
   today (no incremental run since the 08-28 full rebuild), but any earlier
   incremental-only period may have under-merged — the 08-28 rebuild reset it.
   Pinned by a test.
5. **Chris's move (the classifier blocks the spine write from this session; the
   dry-run ran and pinned the baseline):** `python -m connect apply-config`.
   Expect minutes, not hours. Then `python -m connect validate-incremental` for the
   equivalence proof.
6. **Pre-existing, unchanged:** incremental-vs-backstop drift test red (9 keyset tables
   from the 08-28 rebuild; apply-config's re-pin + a later re-seed clears it); 8 spatial
   join errors (EPA TRI + NTSB coordinates); overnight loads (MAUDE, subawards 4.74M so
   far, LDA) not checked; Snowflake MCP token rejected.
7. **Working tree uncommitted:** keys.py, entity_index_specs.py, discover.py,
   incremental.py, __main__.py, 2 new test files, 6 report files, STATUS.md.

## BROKE

Nothing new broke. Offline suites 143 passed (apply-config classifier, batch pins,
incremental, keys, visibility, honesty, leads).

## YOUR MOVE (Chris)

Run `python -m connect apply-config` (item 5). Then say whether to commit.

## NEXT

1. After apply-config lands: measure edges for the 8 new families; refresh the graph
   map snapshot (`connect fingerprint`) so the map sees them (08-18 lesson).
2. Retire the staged-batch flags entirely (apply-config makes them unnecessary).
3. Repair float-text CERT/RSSD in failed-banks + OCC tables → add 3 scoped keys.
4. NDC segment-aware normalizer.
5. Verify overnight loads; re-run subawards↔contracts award-key overlap once both
   finish.
6. EPA TRI + NTSB coordinates; DOCKET issuer namespace; optional bucket-C census via
   the 338k-dataset portal index.

**Cost note:** ~$2–3 warehouse compute this session (verify passes over ~100M rows,
normalizer dry-runs, two runs of the live incremental test). apply-config itself:
expected minutes on X-Small.

## Working tree at compaction time
## main...origin/main
 M .claude/compact-snapshots/last-compact.md
 M reports/viz/_build/join_handbook_template.html
 M reports/viz/join_handbook.html
?? reports/viz/_build/build_join_handbook.py

## Recent commits
3f2839a4 Add tests for apply-config changes and introduce join_handbook.html
38843a2c Update checkpoint data and add report on unregistered ID candidates
83c2e991 Refactor code structure for improved readability and maintainability
08b3376d Add spine wiring preparation script and update test acknowledgments
3f4fc4bd STATUS: depth triage results, gotcha-pass results, auto-push discovery
