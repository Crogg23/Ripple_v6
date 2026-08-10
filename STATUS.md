# RIPPLE STATUS — 2026-08-10 (backlog wave 3: 22 sources modeled; truncated-load hunt)

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE (still open):**
- Three loads confirmed TRUNCATED, all now loudly labeled, none yet re-loaded:
  - UK Companies House PSC: exactly 7,000,000 of ~10M records (round-count
    trap again). Modeled as loud SAMPLE. Loader supports chunked resume but
    the landed 7M is one unchunked stream from the 2026-08-05 snapshot —
    clean fix is a full re-ingest from a current snapshot (~30-60 min).
  - FEMA IA housing registrations: 3.08M of 25,886,797 (true count confirmed
    vs OpenFEMA metadata). Modeled as loud SAMPLE; full reload queued.
  - NIH RePORTER: full-history reload RUNNING in background at session close
    (detached, checkpointed; 2000–2012 of ~26 years done, ~6.5 min/year).
    If it dies, rerun scripts/nih_reporter_load.py — it resumes at the next
    undone year automatically.
- Trust-check finding at boot: the previous session ran waves 2a–2d (~30
  sources) but never rewrote STATUS.md — the boot brief was a session stale.
- 11 orphan twin tables (unchanged) PLUS a new duplicate-ingest drop list:
  ~25 landed twins of already-modeled sources + 5 RCRA dupe twins, all
  verified by row-count/column match — reports/duplicate_ingest_drop_list_2026-08-10.md
  (DROPs are Chris-only). Old junk marts (faa portal / va appendix) unchanged.
- FBI CDE key still semi-exposed in library-onboarding/.env; API signups
  still pending on Chris: DOL WHD, Senate LDA.

**DONE this session (one commit 028d9b13, pushed, CI green both workflows):**
Backlog wave 3 — 22 sources flipped landed→modeled (catalog 430→452), every
grain COUNT(DISTINCT)-verified live before modeling:
- FJC federal court cases, 4 tables → JUSTICE: civil 10.86M, criminal 6.30M
  defendant-records, bankruptcy 6.97M (casekey+snapshot), appellate 988k.
  The pre-existing court mart was a PHANTOM (staging read a nonexistent
  landing table, mart never built) — deleted, zero references.
- HMDA historic mortgages 19.14M → HOUSING (2015–2017 only, stated loudly).
- Elections Canada contributions 12.65M → POLITICS (placed in the lobbying
  folder because the politics folder's mirror-guard blocks dbt builds).
- FracFocus fracking chemicals ×3 → ENVIRONMENT (registry 7.20M ingredient
  lines exactly unique on disclosure+purpose+ingredient).
- EPA RCRAInfo hazardous-waste family ×6 → ENVIRONMENT (handlers 1.61M,
  monthly vio/SNC 2.68M, evaluations, violations, enforcements, NAICS).
- EPA FRS facilities 3.28M → ENVIRONMENT (84,926 registry ids NOT in the
  bigger already-modeled FRS extract — different cuts, both kept).
- FEMA IA registrations (SAMPLE) → HOUSING; UK PSC (SAMPLE) → CORPORATE_REGISTRY;
  Open Payments profile supplement 1.70M → HEALTH (NPI join key);
  USGS GNIS place names 1.25M → REFERENCE; USCG/NRC incident tables ×2 → ENVIRONMENT.
- Connection engine: persisted keyset carried 6.27M stale keys from the
  pre-dedup IRS EO BMF table — reseeded via its own repair path; its
  validate now fully PASSes (was the one failing check in the suite).
- Sorted all 170 "landed" catalog rows: ~30 are duplicate registrations
  (drop list above), ~129 real backlog remain (biggest: ITIS taxonomy family,
  NYC campaign finance ×5, EIA-860/861 family ×~30, GHGRP, SBIR, PCAOB).

**TEST STATUS:** offline 2,698 passed / 2 skipped / 0 failed (full clean run
post-fix). dbt wave-3 build: 44 models + 104 tests green against production.
CI green on the push (both workflows).

**YOUR MOVE:**
1. Nothing blocking. The duplicate-ingest drop list is ready when you want
   to clear the ~30 dupe tables (Chris-only DROPs).

**NEXT SESSION:**
1. Verify the NIH reload finished (checkpoint file), rebuild its mart, and
   confirm it flips modeled.
2. Full re-ingests for the two truncated SAMPLEs: UK PSC (~10M, fresh
   snapshot) and FEMA IA (25.9M via OpenFEMA API — sizeable, price it first).
3. Keep draining the ~129-source real backlog (ITIS family, NYC campaign
   finance, EIA-860/861 — the EIA family needs a vintage decision first:
   two near-identical copies landed, see drop list).
4. Phase 0 leftovers: orphan + dupe drops, API signups (DOL WHD, Senate LDA).

**COST:** moderate — ~2-3 Snowflake credits (~$5-8): wave-3 grain checks over
25M+19M+12M-row tables, 44 model builds + 104 tests (8m42s build), connection
keyset reseed (157M-row state rebuild), two full offline-suite runs, NIH
reload still ticking (small writes). Agent spend: 4 parallel model-writers,
~290k tokens total.
