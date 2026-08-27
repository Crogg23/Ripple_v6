# RIPPLE STATUS — 2026-08-27 (early) — Audit re-verified adversarially, generator fixed, drop list EXECUTED, depth triaged (60x smaller than labeled); gotcha pass clean; auto-push discovered

*Late additions from the depth pass + final gotcha sweep (all live-verified):*
- **Depth**: the "1,567 shallow sources" = 1,563 portals (scope ruling) + 4 real.
  FEMA housing registrations are 99.996% complete vs the publisher's live count
  (26,250,920 of 26,251,944, zero dupes — publisher API checked directly); UK
  PSC is fully modeled (mart 15,804,611 vs raw 15,804,612) with a 1.8% raw-side
  resume-seam overlap to dedupe. Both stale registry sample notes corrected at
  the base table. Full ranked gap ledger: `reports/depth_triage_2026-08-26.md`.
- **STEEL key families = 13** (recounted from connect/keys.py), not the
  remembered 14. 200 of 645 non-portal landing tables have no registry row
  (mostly multi-table sources) — mapping them is a queued 1-hour chore.
- **"Landed-but-never-modeled" registry list is stale**: every meaningful entry
  spot-checked already HAS a mart with matching counts. Lifecycle labels need
  the same never-re-checked fix as the sample notes.
- **Gotcha pass**: 0 dangling views over the 27 dropped tables in any live DB;
  dbt parses clean (1 pre-existing cosmetic warning: unused config path for a
  nonexistent gleif_rr model); targeted live tests 301/301 green post-drops;
  LDA loader healthy on year 2008.

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
3. **Drop list EXECUTED (Chris said "do it", 08-26 ~20:52).** All 27 drops ran
   clean: the whole `LIBRARY_MARTS.UNCATEGORIZED` bucket (26 tables) plus the
   retired `FINANCE__FED_SEC_13F_POSITIONS` twin. Bucket now holds 0 objects.
   Rollback: `outputs/_rollback_uncategorized_drops_20260826_205217.sql`
   (UNDROP good ~24h from then; permanent copies verified in
   `LIBRARY_MARTS_PREDBT_20260729.UNCATEGORIZED` first — do not drop that DB
   while these matter). The refiled UK sanctions mart was rebuilt as
   `JUSTICE.JUSTICE__INTL_UK_SANCTIONS_LIST` (58,336 rows) BEFORE its old copy
   dropped; the 3 stale seed rows in the time registry were removed + re-seeded.
   The fixed audit re-ran clean CSVs (edge tiers now visible: STEEL 1,386,
   CORROBORATED 2,670, BRIDGE 496, GEO 353, STRONG 5).
   NOT dropped, deliberately: the backups (mostly zero-cost clone shadow AND for many
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

1. **The backup piles**: keep or clear is now an informed call — real cost is
   ~9 GB in one pile; several clone groups are last-copies. Needs your ruling,
   no urgency.
2. **CMS Open Payments re-pull** — the newer (July 23) snapshot sits in
   quarantine while the June 27 one serves. No ready-made loader spec exists;
   it's a new ~7 GB download + ~15M-row load (hours in background, ~$1-2
   compute), built on the bridge-fuel path per the 2022-year precedent. Say go
   and a session builds+runs it.
3. 🚨 **Commits are being auto-pushed to GitHub without approval.** The final
   gotcha pass found local main == origin main — this session never pushed, so
   the editor's git auto-sync is pushing on its own (same mechanism as the
   08-26 surprise merge). Nothing sensitive went up, but "push is Chris's
   explicit call" is currently not true in practice. Fix: turn off VS Code's
   git sync/auto-push, or bless auto-push as policy. Chris's call.
4. Still open from before, untouched tonight: portal-scope contradiction on
   ~79 wired scraped sources; viz options menu pick; 385-bucket reload; GFI
   Tableau scrape; politics timeline view question.

## NEXT

The deferred backlog above. The entity-graph rebuild still waits on the
portal-scope ruling. The Senate LDA loader is still working through its 28-year
backfill in the background (healthy, throttled by the API, checkpointing).

**Cost note:** tonight ≈ pennies of warehouse compute (metadata + counts,
one 8-row UPDATE, 8 DROP VIEWs); the big spend was Claude-side agent tokens
(~0.9M) on the verification pass, on plan.
