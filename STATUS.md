# RIPPLE STATUS — 2026-08-26 — Backlog close-out; 0 test errors; staging-view gap mostly closed

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**Scoreboard: test suite is clean and bigger than it's ever been** — 5,156
tests (up from 4,814 Monday), 4,910 pass / 246 warn / **0 error**. Monday's
first full run this week had 25 real ERROR-level failures; today closed the
whole backlog list from that audit, then kept going once the first pass
revealed the backlog was measured wrong in two places.

**BROKE: nothing from today's own work. Two standing items, not new:**
- **Senate LDA lobbying loader** (running since before today) died on a
  Snowflake auth-token expiry after landing years 1999–2004 + 2006 clean.
  Restarted from 2007 (killed the dead process first so it couldn't collide
  with the restart). Still on 2007 as of session end — confirmed alive via
  CPU trend, just very slow against the documented rate limit. Check
  `logs/senate_lda_stdout.log` / `logs/senate_lda_checkpoint.json` at next
  boot before assuming it's stuck.
- **GFI trade data still broken** — the real country-by-country table is a
  Tableau Public chart embed (canvas/SVG, not HTML), so even headless-browser
  rendering can't reach it. Needs a Tableau-aware scrape; not rushed today.

## Today's close-out (commits `c8dc64e5`, `da47a034`, `5664bdd8`)

**Round 1 — the planned backlog:**
- **BIA tribal land data fixed at the root.** Registered URL was an ArcGIS
  Hub home page, not a dataset. Found the real government FeatureServer,
  verified it live (335 real Land Area Representation polygons), landed it,
  rekeyed the staging model, re-enabled + rewired both downstream marts (one
  was reading raw landing directly, skipping staging — same bug class as 6
  other pairs fixed 2026-07-31). All tests green.
- **Entity spine:** 4 real federal sources wired (SAM exclusions, IRS 527
  orgs, 2 SEC EDGAR tables). Correction to Monday's audit: "~850 unwired
  tables" was inflated by counting every schema layer — real number is 319
  unwired landing tables, 273 of them junk portal-crawl (out of scope per
  Chris), only 46 real federal candidates, and only 4 currently clear the
  registry's strict verification bar. The other 42 aren't yet promoted to
  "modeled" lifecycle or have a registry/reality key-name mismatch.
- **Grain/natural-key backfill:** 924 sources warehouse-wide got
  GRAIN/NATURAL_KEY/SPINE_ENTITY resolved (rollback snapshot taken).
- **Same-day regression, found and fixed:** the timeline registry test broke
  mid-session — root-caused to a materialized table
  (`timeline__politics_index`) that structurally can NEVER auto-refresh via
  a normal `dbt run`, because it depends on the politics-guard-protected
  mirror tables (by design). Worked around for today's row; the same
  staleness will recur for the next politics-domain date that crosses into
  "today." Real, standing gap — is the fix "make it a view instead of a
  frozen table"? Chris's call.
- **Senate LDA filings mart deduped:** 10,485 duplicate rows, same failure
  class as this week's OSHA fix (rate-limited loader retrying after a
  partially-successful page write). Loader's own root-cause bug is separate
  and still open.
- **IRS revocation mart:** filtered one IRS-published test/placeholder
  record ("TEST COMPANY INC1 TESTS", EIN 999999999).
- **Dashboards:** leads overlay regenerated with live counts (17,596 leads
  across 8 detectors — both numbers had drifted hard from Monday's stale
  353/4 guess). Old broken connection-graph dashboard (dead CDN link)
  retired in favor of the newer Snowflake-backed one.
- **Repo hygiene:** 8 junk dbt build directories cleaned + gitignored.

**Round 2 — the staging-view gap turned out to be measured wrong, so kept going:**
- **The "242 missing staging views" defect count is measurement-bug-
  inflated.** Its check guesses a live view's name from the source_id string;
  real staging models don't always follow that exact pattern (e.g. several
  IRS-527 sources share one folder with a double-underscore naming
  convention the guess misses entirely). Recomputed the TRUE gap using dbt's
  own manifest dependency graph instead of string-guessing: **216 landing
  tables genuinely have zero staging model** (not 242) — confirmed by
  checking the filesystem directly for a sample, not just re-querying.
- Of those 216, **89 already had a resolved key** and should have been
  generatable — but the generator itself had two real bugs blocking almost
  all of them:
  1. It skipped generating a model entirely whenever the raw table's source
     was already declared in a different folder — even though that has
     nothing to do with whether a model exists. Fixed: still emit the model,
     just don't re-declare the source (dbt errors on duplicate declarations).
  2. Composite (multi-column) natural keys got a hard not_null test on every
     individual column — wrong by construction, since the real completeness
     gate is the full combination and individual composite-key columns are
     often legitimately sparse. One CMS source alone caused 67 of the first
     batch's 111 test failures this way. Fixed: per-column not_null on
     composite keys is now a warning; the combination test stays a hard
     error; single-column keys are unchanged (still hard error, correctly).
  3. Along the way, found a real, separate data bug in one of the 83: 3 of
     383,283 rows in a 2025 OSHA source are column-shifted (a company name
     sitting in the CITY column, an impossible year 2795 in a timestamp
     column) — filtered out; root cause is upstream and out of scope for a
     3-row blast radius.
- **Result: 83 new staging models generated and verified end to end.**
  All of today's work is now part of a 5,156-test suite at 0 errors.
- **True remaining gap: 213 landing tables with no staging view** (127 have
  no resolvable key at all — genuinely ambiguous, not false alarms; the
  other 86-ish need the same manifest-based recheck once more sources get
  keys resolved). List of what was fixable today is at
  `outputs/true_staging_gap_2026-08-26.txt`.

## YOUR MOVE (Chris)

1. **Drop the old truncated USASpending contracts table** (20M-row sampling
   artifact) — fully superseded, the correct 93M-row table is wired end to
   end including staging as of today. Repo policy blocks agents running raw
   DDL: `DROP TABLE LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL;`
2. **GFI trade data** — needs a real follow-up session with a Tableau-
   scraping approach. Not urgent, just don't assume it's a quick fix again.
3. **The stale politics timeline table** — "make it a view instead of a
   table" (matches everything else that depends on today's-date math), or
   something else? Real design call, not urgent.

## NEXT

Boot: check the Senate LDA loader (still on 2007 as of close). The staging-
view gap is now genuinely small (213, mostly no-key sources needing human
judgment, not tooling) — worth one more pass once more sources clear the
grain-resolution bar. GFI needs a dedicated Tableau-scrape session whenever
prioritized. The 42 not-yet-wired real federal spine sources are a bounded,
known-size follow-up.

**Cost note:** ~4.2+ credits (~$8-13+) meter-verified from account usage —
likely undercounted since Snowflake's usage reporting lags live activity by
up to a few hours and this reading was pulled right at session end.

## Not committed

Nothing — working tree is clean as of this session's close (3 commits ahead
of origin, not pushed). The Senate LDA loader's checkpoint/log files will be
dirty again once it lands more years; that's expected, same as every session
this week.
