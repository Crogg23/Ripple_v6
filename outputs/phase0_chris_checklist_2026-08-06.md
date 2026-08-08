# Phase 0 — Chris's Snowsight sitting (~1 hour, one pass)

The only items on the whole roadmap an agent can't do. Everything else is
sequenced behind these. Source plan: the 5-phase "maintenance-only database"
roadmap (approved 2026-08-06).

## 1. Credential prep (NOT the full cutover — that's deliberate)

The scoped role can't write to landing yet, so cutting over now would break
every loader. This sitting only *prepares*:

- [ ] In Snowsight as ACCOUNTADMIN: `SHOW GRANTS TO ROLE RIPPLE_TRANSFORM_RW;`
- [ ] Grant what's missing for loader work:
      `GRANT INSERT, CREATE TABLE ON SCHEMA LIBRARY_RAW.LANDING TO ROLE RIPPLE_TRANSFORM_RW;`
      (adjust to actual gaps the SHOW GRANTS reveals; also needs write on
      `LIBRARY_META.REGISTRY` and `LIBRARY_META.INGEST_LOGS`)
- [ ] Generate/locate the `RIPPLE_TRANSFORM_RW` PAT token, keep it handy
- [ ] **Do NOT remove `LIBRARY_PAT` yet** — that happens at the end of Phase 2,
      after the last heavy loader run (NIH resume, DDP stays, HMDA mart)

## 2. DROP the 11 orphan twin tables (you, one at a time — per post-incident policy)

List in `outputs/connect_wiring_report_2026-08-05.md` (search "Orphan
quarantine"): FED_FHFA_SUSPENDED_COUNTERPARTY, FED_JPML_PENDING_MDL,
INTL_UK_SANCTIONS_LIST, INTL_UN_CONSOLIDATED_SANCTIONS,
STATE_OEHHA_PROP65_CHEMICALS, 5 ICIJ_OFFSHORE_LEAKS copies, FED_IRS_527_ORGS.
They're already masked out of the map (`connect/fingerprint.py` SKIP_TABLES),
so dropping changes nothing downstream.

- [ ] Verify each has a surviving twin before dropping (names differ only by suffix)
- [ ] `DROP TABLE LIBRARY_RAW.LANDING.<name>;` one at a time

## 3. HMDA honesty call (audit critical #2)

UPDATE 2026-08-08: rename is DONE (mart now `HOUSING__FED_CFPB_HMDA_DC_ONLY`,
verified identical 28,301 rows). Only the old-copy drop remains — agent is
permission-blocked from running DROP, so it's yours:

- [ ] `DROP TABLE LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA;`
      The real 19.1M-row nationwide file is already landed
      (`FED_CFPB_HMDA_HISTORIC`); Phase 2 builds the honest mart on it.

## 4. Three standing decisions — one line each is enough

- [ ] **CI write access** (CHRIS_DECISIONS item 3): keep CI parse-only, builds
      manual? (recommended) — or let CI build marts on merge?
- [ ] **Backup posture** (audit #6): approve weekly zero-copy
      `CREATE TABLE ... CLONE` of LIBRARY_RAW.LANDING, 4 weeks retention?
      (recommended; near-zero storage cost until tables change)
- [ ] **ZIP country-gating** (CHRIS_DECISIONS item 2b): should the ZIP
      normalizer stop minting fake US ZIPs from foreign postal codes
      (`KY1-1106` → 11106)? Yes = included in Phase 3's single spine rebuild.

## 5. Optional, same sitting if energy allows

- [ ] **A15** (Pattern Desk): run `scripts/provision_pattern_desk.sql` as
      ACCOUNTADMIN — the follow-on mart rebuild is already done (2026-08-06,
      41/41 tests pass)
- [ ] **A16** (Playground): run `infra/ddl/06_column_catalog.sql` — needs no
      credential work at all
- [ ] **TxDPS account** (~2 min, free) if Texas sex-offender coverage wanted;
      yes/no on Hawaii's $100 download

## What already happened without you (2026-08-06, FYI)

- LEAD_QUEUE rebuilt — the 4 missing leads are back, reconcile test passes.
  The human-sign-off rule is true again.
- The dbt engine is pinned (the two-binaries-one-name trap is closed).
- All 6 gate-bypass/discarded-verdict loaders now run the quality gate and
  fail loudly.
- New `key_is_real` dbt test class catches the masked-blank bug 0/3,801 old
  tests could see. First run immediately found a new dead column:
  Form 5500 `sponsor_dfe_ein` is 100% blank (use `spons_dfe_ein` instead).
- 3 permanently-broken staging models fixed.
