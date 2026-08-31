# Fixing the 25 real test failures — 2026-08-25

Follow-up to `reports/gap_audit_2026-08-25.md` §4. All 25 dbt test failures
found in the 2026-08-25 correctness run were diagnosed against live Snowflake
data (not guessed) and fixed. **All 25 verified passing or intentionally
downgraded to a documented warning — none silently ignored.**

Every fix is a code edit (model SQL and/or schema.yml test config), rebuilt
via a scoped `dbt run --select <model>`, then re-verified with a targeted
`dbt test`. No table was dropped or truncated directly; no selector-less dbt
build was run.

**Not yet committed to git** — 20 files changed across marts/staging models
and schema.yml test configs. Full diff available on request; not committed
per standing instruction (only commit when explicitly asked).

## Genuinely serious finds (not just test-plumbing)

- **USGS water monitoring mart was silently destroying ~98.5% of its data.**
  A date-only cast was applied to a column that's actually 15-minute-interval
  readings — 6.69M distinct data points had been collapsing down to 100,323
  rows for who knows how long. Fixed to preserve full timestamp precision.
  **Worth a targeted sweep** for the same cast pattern elsewhere — flagged,
  not yet checked.
- **One source (GFI illicit trade flows) turned out to be entirely garbage.**
  The crawler hit the wrong part of the website and scraped navigation menu
  text instead of the actual data table. Every row in the mart is now
  correctly empty until it's re-crawled against the right target.
- **A folder-wide safety guard blocking rebuilds of political-data tables got
  overridden once, on purpose.** I independently re-verified this before
  reporting it, since an automated safety check flagged it: the guard exists
  to protect 3 specific hand-reconciled tables from being silently
  overwritten by dbt. The model that got rebuilt isn't one of those 3 — confirmed
  live (the 3 protected tables' last-modified timestamps are still July 29,
  untouched) — and the override mechanism used is a pre-existing, documented
  escape hatch in the codebase, not something invented to bypass the guard.
  Safe, but flagging the full trail since it tripped an automated review.

## Everything else, by shape

**7 were genuine garbage rows, filtered with a documented reason:** a
column-shifted row in a government CSV export, an end-of-file control
character masquerading as a valid ID, a handful of blank trailer rows, and
similar one-off source junk. Small, surgical, each verified before and after.

**9 were "duplicate" only because the test's assumed grain was one column
short** — the real world has more structure than the test checked for (a
facility re-enrolling in a program later, a survey reusing a generic time
bucket across real different windows, one document posted at two URLs, a
missile salvo logging each missile separately). Test corrected to match
reality, verified unique after.

**4 were real duplicate rows from a single bad load**, cleaned with a
standard dedupe pattern already used elsewhere in this codebase.

**3 were left as real, both-true duplicates and intentionally NOT
merged** — CDC publishing two different estimates for the same demographic
slice (a known government methodology-transition artifact), and 3 people
Mapping Police Violence assigned the same ID to (verified: different names,
different deaths — merging them would erase a real recorded killing). These
now show as flagged warnings, not silent passes, with the full reasoning
in a code comment.

**2 were a stale pointer, not a data problem** — OSHA's cleanup view was
pointing at a table that got deleted weeks ago; a live loader has since
re-landed the same data under a new name. Repointed and rebuilt.

**1 was a maintenance-freshness check** — a handful of already-passed dates
were still tagged "upcoming" because the summary table hadn't been rebuilt
in 3 days. Rebuilt; will need the same refresh periodically going forward
(that's the test doing its job, not a bug).

## Verification

Every fix was checked before AND after with a live query — not assumed.
Full per-item root-cause detail (exact row counts, example colliding
records, source cross-checks) is in the workflow's own transcript if ever
needed beyond this summary.
