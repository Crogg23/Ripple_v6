# Ingestion Master Plan — bring in everything — 2026-08-05

**Hand this file to a fresh Claude Code session and say "execute Phase N of
outputs/ingestion_master_plan_2026-08-05.md".** One phase per session. Do not run two
phases in one session — context gets long, loaders get sloppy.

**Session setup:** Sonnet in Claude Code (the constitution's Building lane), default
effort. This is loader construction — mechanical, pattern-reuse work. Do NOT burn Opus
or max effort on it. If a phase turns into a debugging swamp, that session can escalate
effort itself; don't pre-pay for it.

**Where this work happens:** Claude Code, not Snowflake Cortex Code. Reasons, short:
ingestion is 90% *outside* the warehouse — fetching files, fighting 403s and TLS
quirks, checkpointed downloads, API pagination. Cortex Code lives inside Snowsight and
can't reach out to fetch anything; it's good at SQL over data that's already landed.
It also has none of this repo's memory: the constitution, the loader traps, the
verification rules, the build_review wrapper. Use Cortex later for in-warehouse
analysis if you like it; the bringing-in stays here.

**Source of truth for what to build:** `outputs/source_rankings_2026-08-05.md` (the
ranked list) and `outputs/ready_to_build_sources.csv` (URLs). This file is the order
and the rules.

---

## Standing rules for every phase (non-negotiable, from the constitution + memory)

1. **Landing pattern:** raw file → stage → `RAW_<SOURCE>` table → dbt staging model.
   Never transform during load. Keep the raw file on disk until verification passes.
2. **Verification before "done" — every table, no exceptions:**
   - Row count vs. source's own claimed count (when the site states one).
   - For every intended join key: `COUNT(*)`, `COUNT(DISTINCT key)`, and a 20-row
     value sample. A bare null-check has produced false "100% populated" reads twice
     (NPPES EIN, NOAA AIS imo_number). Masked/sentinel values are the #1 trap.
   - One `TRY_TO_DATE` check per date column — the 'YYYYMMDD' epoch trap is real.
   - Log the result in the load-log control table (create it in Phase 0).
3. **Long downloads:** the 10-minute background-Bash cap kills loaders. Anything that
   might run long uses detached `Start-Process` with checkpoint files, and Monitor for
   progress updates. Round-number row counts (500k, 1M, 20M) = suspected truncation —
   verify, don't celebrate.
4. **Fetch traps already known:** cpsc.gov TLS-blocks curl (python-requests works);
   sec.gov, fsis.usda.gov, cbp.gov, phmsa.dot.gov, unece.org 403 automated fetches
   site-wide. None of those hosts are in this plan's confirmed list, but if a redirect
   lands on one, stop and note it — don't fight it.
5. **Before loading anything, check it isn't already there.** COLUMN_CATALOG only
   covers pack tables — check `INFORMATION_SCHEMA` too. Known must-checks are flagged
   in phases below.
6. **Receipts:** each phase ends with a 3–5 bullet report — what landed, row counts,
   what broke, any key that failed verification. Update the memory directory if a new
   trap is found. No walls of text.
7. **RED gates:** two sources need Chris's explicit go-ahead BEFORE any download —
   sex-offender registries (Phase 6) and they're marked at their phase. ICE
   person-level detention data got a standing question to Chris; if he hasn't ruled by
   Phase 1, load everything else in the phase and hold ICE.
8. **AI at build time only.** Everything lands as plain tables + dbt models. Nothing
   at runtime depends on a model call.

---

## Phase 0 — Prep (half a session)

- Create `CONTROL.INGEST_LOG` (source, url, fetched_at, rows_landed, rows_claimed,
  keys_verified, status, note) and `CONTROL.INGEST_QUEUE` seeded from
  `ready_to_build_sources.csv` with phase assignments from this file.
- Dedupe check against the warehouse: confirm whether USAspending award data, GLEIF
  Level 1, and any EPA/ECHO tables already exist. Mark queue rows `already-have`
  accordingly. (The recon's "likely already have" 40 were excluded upstream, but these
  three sat near the boundary.)
- Confirm warehouse compute is alive and which role/PAT to load under (RIPPLE_READER
  is read-only enforced; loading needs the writer path).
- Receipt to Chris: queue counts per phase, anything marked already-have.

## Phase 1 — Quick harm wins + tiny radars (one session)

The cheap, high-harm loaders plus every trivial "banned list."

| Source | Note |
|---|---|
| CFPB Consumer Complaint Database | One big CSV, refreshes daily — capture snapshot date |
| VAERS | Yearly zips, 3 files per year (data/symptoms/vax) — load all years |
| ICE Detention Stints + Detainers + facility codes (DDP + Vera) | **HOLD unless Chris has ruled on person-level records.** Facility-code file is safe either way |
| JPML Pending MDLs | One small table |
| Consolidated Screening List | One file, three ban lists |
| UN Consolidated Sanctions List | XML, small |
| UK Sanctions List | Small |
| FHFA Suspended Counterparty List | ~241 rows |
| OEHHA Prop 65 chemicals | Trivial, useful for later EPA/FDA joins |

## Phase 2 — EPA facility family (one session)

One facility-ID family, one loader style, five sources. Verify the facility-ID join
across all of them at the end — that cross-check IS the deliverable.

TRI Basic Files → ECHO ICIS-Air + ICIS-NPDES → RCRAInfo handlers → Superfund SEMS →
GHGRP. Then: National Response Center incidents (bigger, own loader, joins facilities
and vessels/AIS). Optional if time: CAMPD, pesticide establishments.

## Phase 3 — FDA family (one session, maybe two)

One openFDA pagination loader, reused. Order: FAERS → MAUDE → Enforcement/recalls →
510(k)+PMA → CAERS → GUDID (bulk file, not API) → Establishment Reg/Listing (FEI).
openFDA also publishes bulk JSON dumps for most endpoints — prefer the dump over
paginating the API where it exists; check `api.fda.gov/download.json` first.
End-of-phase join test: MAUDE event → GUDID device → manufacturer → FEI establishment.

## Phase 4 — Money block (one session)

- SBA PPP loan-level (multiple large CSVs)
- HMDA Historic LAR (large flat files; load a 3-year slice first, verify layout against
  the record-format PDF, then backfill all years)
- Federal Audit Clearinghouse (bulk; EINs are the join key — COUNT(DISTINCT) them)
- PBGC Trusteed Plans (join-test against DOL Form 5500 SPONS_DFE_PN same session —
  that join existing is the point)
- NHTSA Recalls API (fits here by loader type)

## Phase 5 — Entity spine block (one session)

OpenSanctions default (FTM JSON — flatten to entities + relations tables) → ICIJ
Offshore Leaks (nodes + edges CSVs) → UK Companies House PSC (10M records, chunked
files) → FATCA FFI list → GLEIF Level 2 (only if Level 1 confirmed present in Phase 0)
→ OCC/NCUA/FHLB institution lists (trivial filler). End-of-phase test: pick 20 names
from CFPB/PPP data, probe them against the spine tables.

## Phase 6 — Sector A/B remainder (two sessions, split by feel)

Justice/labor: USSC sentencing datafiles (SPSS-style formats — budget annoyance),
NLRB cases (verify access mechanics first — recon flagged it), BJS PREA audits, ATF
FFL list, FJC judges, NPDB public use file.
**RED gate: sex-offender registries — do not download without Chris's explicit yes.**

Housing/health/infra: HUD Section 8 + multifamily + FHA snapshot, ASC appraiser/AMC
registries, College Scorecard, HRSA UDS + HPSA, National Inventory of Dams, NTSB
aviation, EIA-860/861, FracFocus, FEMA Individual Assistance, PCAOB AuditorSearch,
SBIR awards, NIH RePORTER + NSF (API loaders — reuse the openFDA pagination pattern),
Retraction Watch, state lobbyist bulk (CA + TX only), IRS 527, FCC Political File
(chunkiest — last).

## Phase 7 — C-tier scaffolding (on demand, never a dedicated session)

Everything in the C-tier table of the rankings file. Rule: a C-tier source gets loaded
only when a story or a join in flight needs it. Add to the queue, load in whatever
session needs it, follow the standing rules. Exception: DailyMed SPL + UNII load
alongside any serious FAERS analysis push; DOT National Address Database loads when
entity-resolution work starts in earnest.

---

## What "done" looks like

Every queue row is `landed-verified`, `already-have`, `held-red`, or `deferred-c-tier`
with a note. INGEST_LOG holds a verification receipt per table. Nothing published,
nothing analyzed — this plan is acquisition only. The analysis lives in later mission
packets, and what gets looked at first stays a RED call.

## Paste-this to start a session

> Read CLAUDE.md, then read outputs/ingestion_master_plan_2026-08-05.md and execute
> Phase N. Follow the standing rules exactly — verification protocol on every table,
> detached processes for long downloads, receipts at the end. Rankings context is in
> outputs/source_rankings_2026-08-05.md if you need the why behind any source.
