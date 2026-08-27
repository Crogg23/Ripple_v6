# RIPPLE STATUS — 2026-08-27 (early) — Warehouse audit re-verified adversarially; generator's mis-filing bug fixed; cleanup reduced to a short drop list awaiting Chris

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

## 🚨 Read this first

1. **Do NOT trust "dead / junk / 0 rows" labels in any audit CSV.** Two audits
   in a row (08-24 and 08-26) hardcoded those verdicts by schema NAME and
   summed uncounted views as zero. That chain nearly produced
   `DROP DATABASE THE_LIBRARY` (live: 254 views serving 100M+ rows, and the
   default DB of `viz/sqlrun.py`) and labeled the REVIEW sign-off machinery
   "junk". `scripts/warehouse_audit_2026-08-26.py` is now fixed (name labels
   renamed to non-verdicts, views marked NOT_MEASURED, DB list from
   SHOW DATABASES) — but the CSVs in `reports/the_audit_2026-08-26/` were
   written by the OLD code. Re-run the script before citing them.
2. **The mart-generator's OTHER bug is fixed: it was mis-filing marts into
   UNCATEGORIZED.** On 08-26 it built 24 thinner duplicates of existing
   categorized marts in one run (missing ID_HINTS + a dedupe guard that can't
   see raw-layer duplicate landings). Fixed in `scripts/gen_mart_models.py`:
   10 new hints, fail-closed on uncategorized (`--allow-uncategorized` to
   override), and an unparsed-header guard (UNNAMED_* columns → "reload the
   source", not "build a mart"). 26 uncategorized dbt models disabled with
   dated comments; 1 (UK sanctions, 58k rows — MORE than its justice twin)
   refiled to `models/marts/justice/`. `scripts/fix_errored_models.py` is
   retired with a hard sys.exit (rerunning it would regenerate duplicates).
3. **Drop list for Chris (classifier blocks these for sessions — by design).**
   All verified safe by live dependency sweep (0 views / deps / procs / tasks
   across all DBs, only audit-script reads in 120 days of query history), and
   all fully backed up in `LIBRARY_MARTS_PREDBT_20260729.UNCATEGORIZED`:
   - `DROP TABLE LIBRARY_MARTS.UNCATEGORIZED.UNCATEGORIZED__FED_SEC_13F_POSITIONS;` (101.3M rows, hash-identical to the FINANCE copy)
   - `DROP TABLE LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_POSITIONS;` (its twin — model retired 08-23, `finance__fed_sec_13f_holdings` is the authoritative successor with the value_usd unit fix; dropping only one leaves false closure)
   - `DROP TABLE LIBRARY_MARTS.UNCATEGORIZED.UNCATEGORIZED__FED_FEC_LEADERSHIP_PAC;` (degraded copy — its FEC_CANDIDATE_ID was date-cast to 100% NULL; FINANCE copy dominates)
   - The 24 duplicate tables built 08-26 into `LIBRARY_MARTS.UNCATEGORIZED` (their models are now disabled; each table's keeper is named in its model file's comment).
   NOT on the list: the backups (mostly zero-cost clone shadow AND for many
   clone groups the LAST copy of pre-dbt data — see below), THE_LIBRARY,
   REVIEW anything, `LIBRARY_RAW.RETIRED` (deliberate quarantine with a live
   rollback script; 2 of its tables are the ONLY copies of round-capped
   990-efiler indexes).

## What this session did (Fable, overnight)

- **Adversarially re-verified the whole cleanup plan live** (9-agent pass, all
  read-only): full verdicts in the session transcript; headline corrections —
  the "51 GB reclaimable" was ~82% zero-copy clone shadow (bills ≈ $0; only
  `_RESTORE_20260731`'s 9.18 GB is real storage), the two 07-30 spine backups
  are content-identical clones of each other AND the only copy of 9 pre-spine
  tables, and `LIBRARY_MARTS.FINDINGS` ("0 rows" in the audit) is actually the
  investigative output layer: 37,105 rows across 13 live views, read 08-24.
- **Fixed the false dead-key verdict** in `LIBRARY_META.REGISTRY.COLUMN_TRUST`:
  FEC_CANDIDATE_ID on the leadership-PAC family was marked dead_id/1.0 from
  measuring the cast-destroyed mart copy; raw source is 8,619/8,619 populated,
  8,076 distinct — a live STEEL spine key. Row corrected (UPDATE, logged in WHY).
- **Hardened the Senate LDA loader** (`scripts/senate_lda_load.py`): connection
  now health-checked/reconnected per upload with one retry on auth expiry —
  the 390114 token-expiry that killed it twice on 08-26 can't kill a finished
  multi-hour download any more. NOTE: the running loader then recovered on its
  own (2005 uploaded + checkpointed, now fetching 2008) — it was slow under
  API throttling, never hung. Leave it running; the fix applies from the next
  restart.
- **Dropped 8 broken views** in `LIBRARY_STAGING.CORE` — pre-rename relics
  referencing databases (`RIPPLE_RAW/STAGING/META`) that no longer exist;
  each one's DDL was individually verified before dropping. Zero readers.
- **Added `tests/test_review_gate_live.py`** — canary on the publish gate,
  which has never recorded a real decision (2 smoke rows only) so its broken
  and healthy outputs were indistinguishable. 3 tests, green.
- **Solved the "superseded copies have MORE rows" mystery, both cases:**
  CFPB backup's +11,501 rows are duplicate COMPLAINT_IDs the dbt rebuild
  correctly deduped (live mart is exactly distinct — good news). CMS Open
  Payments: the RETIRED copy is a NEWER snapshot (July 23) than the surviving
  LANDING table (June 27) — wrong-direction retirement; the right fix is a
  fresh re-pull of Open Payments, not un-retiring.

## BROKE

Nothing this session. Full test suite was started at close — result in the
final chat message (this file written while it ran; if it failed, the chat
says so first).

## YOUR MOVE (Chris)

1. **Run the drop list above** (or say "no" — each line is independent).
2. **The backup piles**: keep or clear is now an informed call — real cost is
   ~9 GB in one pile; several clone groups are last-copies. Needs your ruling,
   no urgency.
3. **CMS Open Payments re-pull** (newer data currently sits in quarantine).
4. Still open from before, untouched tonight: portal-scope contradiction on
   ~79 wired scraped sources; viz options menu pick; 385-bucket reload; GFI
   Tableau scrape; politics timeline view question; push to origin.

## NEXT

Re-run the (fixed) warehouse audit for clean CSVs, then the deferred backlog
above. The entity-graph rebuild still waits on the portal-scope ruling.

**Cost note:** tonight ≈ pennies of warehouse compute (metadata + counts,
one 8-row UPDATE, 8 DROP VIEWs); the big spend was Claude-side agent tokens
(~0.9M) on the verification pass, on plan.
