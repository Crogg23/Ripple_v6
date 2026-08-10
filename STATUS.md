# RIPPLE STATUS — 2026-08-10 (waves 4+5: 86 sources modeled; NIH full; FEMA reload RUNNING)

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing.** Live/open items:
- FEMA IA full reload RUNNING detached at session close (checkpointed at
  ~3.7M+ of 25,886,797; ~100k rows/2 min ≈ 7-8 h to finish; resumes on rerun
  of scripts/fema_ia_load.py if it dies). When done: rebuild its staging+mart
  and REMOVE the SAMPLE label from its descriptions.
- UK Companies House PSC re-ingest is BLOCKED on a Chris-only wipe: sessions
  can't DELETE/TRUNCATE. One-liner for Chris, then rerun the chunked loader:
  `DELETE FROM LIBRARY_RAW.LANDING.UK_COMPANIES_HOUSE_PSC;` then
  `python scripts/uk_ch_psc_load.py --chunks 32 --run` (~30-60 min).
- Drop list (Chris-only) now ~40 tables in 4 sections:
  reports/duplicate_ingest_drop_list_2026-08-10.md — wave-3 dupes (~30),
  4 EIA vintage twins, 3 junk 1-row loads, 4 snapshot twins
  (screening list / FJC judges / JPML / Prop-65), 2 broken loads to re-ingest
  properly later (USACE dams inventory, DTCC participants), 1 garbage OCC
  by-name table, 1 leftover internal staging table.
- FBI CDE key still semi-exposed in library-onboarding/.env; API signups
  still pending on Chris: DOL WHD, Senate LDA.

**DONE this session (commits 1dae94e2, 5481691d, 173846f3 — all pushed):**
- Wave 4 (46 sources) + wave 5 (40 sources): catalog 452 → 551 modeled.
  Real landed backlog is now ZERO — everything left in 'landed' is either
  on the drop list, a broken load queued for re-ingest, or live-loading.
  Every grain COUNT(DISTINCT)-verified live before modeling.
  - Wave 4: ITIS taxonomy ×19, NYC CFB contributions ×5 cycles,
    EIA-860/861 power-plant+utility family ×28 (vintage decided, 4 corrupt
    twins condemned; 5 tables carry a lost-first-row caveat), GHGRP ×2,
    SBIR, NTSB injuries, FDA UNII hub, DailyMed map, PCAOB Form AP.
  - Wave 5: health ×7 (HPSA, UDS sites, IHS ×2, DMF, Purple Book,
    Health Canada DPD), housing ×8 (FHA snapshot, HUD MF ×2, PHAs, USDA RD,
    NFIP, HMDA LAR SAMPLE + xref), finance ×10 (SEC series/class, FINRA,
    MSRB, OCC ×2, ISO MIC, OSFI, FHLB, NCUA ×2), environment ×5 (TRI, AQS,
    orphaned wells, WQP, HUC8), science/reference/education ×8 (ROR,
    retraction watch, Crossref funders, OSF SAMPLE, TAS tree, College
    Scorecard, CIP codes), Form 5500 Sch SB → labor, ICE facility codes →
    immigration. Four Excel-mangled tables recovered by hunting their
    embedded header rows live.
- NIH RePORTER full history verified complete: 27 years, 2,122,611 rows,
  zero gaps vs publisher counts; mart rebuilt, modeled, not a sample.

**TEST STATUS:** offline 2,698 passed / 2 skipped (run after EACH wave).
dbt: wave-4 430/430; wave-5 339 green after 4 small fixes. All pushed;
CI state not re-checked — verify at next boot.

**YOUR MOVE:**
1. Run the UK PSC wipe one-liner above (then a session reruns the loader).
2. Drop list (~40 tables) whenever you want — all verified, receipts in the
   report.

**NEXT SESSION:**
1. Boot trust check: CI green on the three pushes?
2. Check FEMA IA finished (checkpoint file); rebuild its models, drop the
   SAMPLE label, verify full 25.9M.
3. If Chris ran the wipe: rerun UK PSC loader (32 chunks), rebuild, un-SAMPLE.
4. Re-ingest the two broken loads properly (dams inventory ~93k, DTCC list)
   — small, free APIs.
5. Backlog is drained — next frontier is the 1,569 'sampled' sources and
   the 268 'failed' ones in the catalog, plus Phase 0 leftovers.

**COST:** moderate — ~2-3 Snowflake credits (~$5-8) across both waves:
grain checks over ~110 tables, two multi-model builds (119 + 91 models),
NIH mart rebuild (2.1M), FEMA loader writing steadily. Agent spend:
9 model-writer agents, ~760k tokens total.
