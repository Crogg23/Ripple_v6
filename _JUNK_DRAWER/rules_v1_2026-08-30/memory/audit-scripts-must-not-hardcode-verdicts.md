---
name: audit-scripts-must-not-hardcode-verdicts
description: "A measuring script must never hardcode the verdict it is supposed to discover, and 'no row count' must never be rendered as '0 rows' — both produced near-miss DROP recommendations on the Ripple warehouse."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d4ca535e-d165-4201-a5ea-9f1e61f1ccda
  modified: 2026-08-27T02:09:10.040Z
---

Two defect patterns turned the 2026-08-26 Ripple warehouse audit
(`scripts/warehouse_audit_2026-08-26.py`) into a source of confidently wrong
drop recommendations. Both are easy to repeat and hard to spot, because the
output *looks* like measurement.

**1. The script hardcoded the verdicts it was supposed to discover.**
Its `schema_status()` function name-matched and returned fixed labels:
`THE_LIBRARY` → `legacy_dead`, any schema named `UNCATEGORIZED` or `REVIEW`
→ `junk_schema`, `*_PREDBT_*` → `legacy_backup`. The cleanup plan then cited
the audit's own `status` column as evidence those things were dead. That is
circular: the audit did not find them dead, it asserted it in code, and a
later reader mistook the assertion for a finding. Both labels were wrong —
`THE_LIBRARY` is the default database for the repo's own SQL runner
(`viz/sqlrun.py` executes `USE DATABASE THE_LIBRARY`) and 24 of the 26
"junk" `UNCATEGORIZED` tables had been built that same day by 29 live dbt
models.

**2. "Not measured" was rendered as "0 rows."** Row counting ran only on
`table_type = 'BASE TABLE'`, so all 2,175 views (39% of the 5,571 objects)
got a blank live count — and the per-schema summary summed blanks as zero.
Whole view-only areas therefore printed as `0 rows`, which reads as *empty*
rather than *unmeasured*. `THE_LIBRARY` is 100% views (254/254);
`LIBRARY_STAGING.DBT_CROGERS` is 1,438 views; `LIBRARY_MARTS.TIMELINE` is
402. A live spot-check of 8 `THE_LIBRARY` views found 58.1M / 17.2M / 1.3M
rows and more. Snowflake also leaves `INFORMATION_SCHEMA.TABLES.ROW_COUNT`
null for views, so the metadata column repeats the same lie.

**Why:** Chris, 2026-08-26 — a cleanup plan built on these outputs nearly
recommended `DROP DATABASE THE_LIBRARY`, and the same claim had already
survived a *previous* audit and several STATUS.md rewrites unchallenged.
His reaction was sharp distrust and a demand to hand the work to another
session. Repetition across sessions had been standing in for verification.
Same root cause as [[feedback-verify-inventory-before-computing]], one level
deeper: there, a hardcoded *input* list; here, hardcoded *conclusions* and a
silent measurement gap. Related: [[completeness-check-traps]] (SHORT/OVER is
a hypothesis, not a verdict) and [[warehouse-data-traps]].

**How to apply:**
- In any inventory/audit script, keep *observed facts* and *judgments* in
  separate columns, and make every judgment carry the evidence that produced
  it. Never let a name-pattern write a status field that downstream readers
  will treat as measured.
- Emit an explicit `not_measured` / `skipped_view` marker; never let a null
  count aggregate into a zero total. If a whole class of objects is skipped
  for cost reasons, say so in the summary file itself, next to the number.
- Before acting on any "dead / empty / safe to drop" claim: run a live
  `SELECT COUNT(*)` on a sample, and grep the repo for references to the
  name (`.mcp.json`, `viz/`, dbt models, tests). On this warehouse that grep
  has caught a live dependency every single time it was run.
- Re-verify a drop candidate by an *independent method*, not by re-reading
  the same report. The one recommendation that survived here
  (2 orphan `UNCATEGORIZED` marts) was confirmed by set-differencing built
  tables against dbt model files — a different signal than the audit used.

**Addendum (same session, after the fix run):** three more instances of the
same "verified claim, wrong anyway" family surfaced while fixing:
- The adversarial verifier that cleared the two-table drop `ls`'d the wrong
  directory depth (`models/` not `models/marts/`) and reported the uncategorized
  model folder as nonexistent while 29 models sat in it. Conclusion survived on
  other evidence; reasoning was invalid. Even verification passes need their
  load-bearing claims spot-checked at the source.
- The loader-frozen verifier declared the Senate LDA loader's Snowflake socket
  dead (CLOSE_WAIT) and a third crash "certain." The loader then uploaded year
  2005 successfully and kept going. The auto-mode classifier blocking the
  taskkill saved a healthy multi-hour loader — treat blocked destructive calls
  as a second opinion, not an obstacle.
- The "51 GB reclaimable backups" framing inverted reality: ~82% was zero-copy
  clone shadow (bills ~0), and for many clone groups the backup is the LAST
  copy because the original was dropped in the dbt migration. Logical bytes ≠
  billed bytes; check TABLE_STORAGE_METRICS clone groups before valuing a drop.
