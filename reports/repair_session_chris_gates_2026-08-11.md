# Repair session 2026-08-11 — the things only Chris can run/decide

Everything below is blocked to sessions by design (destructive ops / money /
keys). Each is one action. Nothing else in the repair arc waits on these —
marts are already corrected at the model layer; these clean up the raw layer
and unlock the remaining ingests.

## 1. Landing dedupe swap (removes 22.9M junk rows from the raw layer)

The two runaway-pager landing tables are still physically inflated (marts are
already deduped). The reviewed tool refuses healthy tables, previews first,
and preserves the inflated originals under a side table until you drop them:

    python scripts/dedupe_landing_exact.py --run

## 2. Drop the wrong-file credit-union table (replaced by verified reload)

    DROP TABLE LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS;

## 3. Additions to the existing drop list (orphaned by this session's model retirements)

    DROP TABLE LIBRARY_MARTS.UNCATEGORIZED.UNCATEGORIZED__INT_GLEIF_RR;
    DROP TABLE LIBRARY_MARTS.ECONOMICS.ECONOMICS__INT_GLEIF_RR;
    DROP TABLE LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RR;
    DROP TABLE LIBRARY_MARTS.JUSTICE.JUSTICE__FED_MSHA_ACCIDENTS;
    DROP TABLE LIBRARY_MARTS.JUSTICE.JUSTICE__FED_MSHA_MINES;
    DROP TABLE LIBRARY_MARTS.JUSTICE.JUSTICE__FED_MSHA_VIOLATIONS;
    DROP TABLE LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_STOCK_WATCHER;
    DROP TABLE LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NHTSA_INVESTIGATIONS;  -- no repo model, routing residue
    DROP TABLE LIBRARY_RAW.LANDING.INT_GLEIF_RR;  -- duplicate GLEIF landing, kept twin is INTL_GLEIF_RELATIONSHIPS
    DROP TABLE LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS_FULL;  -- aborted first attempt, garbage inferred schema (kept copy is _FULL_R2)
    DROP TABLE LIBRARY_RAW.LANDING.FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK_FULL;  -- superseded by _FULL_R2
    DROP TABLE LIBRARY_RAW.LANDING.XC_RANSOMWARELIVE_VICTIMS_FULL;  -- superseded by _FULL_R2
    -- and once you're satisfied with the repointed marts, the six OLD short
    -- landing tables (SAM 9k, NFIP 25k, ransomware 29k, voteview 3k, FR 2.7k,
    -- CDC 15k) can retire the same way.

(The ~50-table list from 2026-08-10 in reports/duplicate_ingest_drop_list_2026-08-10.md
still stands separately; the aircraft-registry July twin is on it.)

## 4. Priced go/no-go: the two genuinely-short FDA pulls

- Device adverse events: we hold 2.7M of 25.7M (one quarter, deliberately cut
  short). Full pull = ~23M more records of chunked JSON, est. 3-6 hours of
  paginated download + ~$5-10 warehouse credit to land and rebuild. Say go and
  a session runs it checkpointed.
- Establishment registrations: 330k of 333k (~99% — barely short). Cheap
  (~minutes, <$1); same go applies.

## 5. Still key-gated on you (2-minute signups, unchanged from before)

- Broadband map, wage-and-hour, Senate lobbying (the lobbying reload is the
  biggest single completeness gap left: we hold 9% of ~2M filings).

## 6. Unchanged from previous sessions

- UK company-ownership wipe one-liner (still queued).
- Scheduled cadence for the uniqueness test suite: sessions can now run it via
  the sanctioned wrapper (library-onboarding/ripple_dbt/run_tests.bat); wiring
  it into the scheduled-refresh DDL (infra/ddl/09) is warehouse DDL = yours.
