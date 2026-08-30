---
name: senate-trades-reality
description: "Senate stock trades data - name-only source, coverage ends Dec 2020, journalism-use-only, verified live"
metadata: 
  node_type: memory
  type: project
  originSessionId: afbdf0c0-8d90-4e4c-bbba-d73c60bd0b93
  modified: 2026-08-01T20:16:56.627Z
---

FED_SENATE_STOCK_WATCHER landed 2026-08-01 (8,350 rows) + mart
POLITICS__SENATE_TRADES (100% bioguide-matched via surname+chamber+term-span
name match, MATCH_METHOD per row). Three facts that contradict older repo docs:
1. The source is NAME-ONLY — the FABLE_KEY_HUNT claim "bioguide-keyed" was
   WRONG (schema verified live). Member claims from it are lead-grade.
2. Coverage ENDS 2020-12-02 — the volunteer project went stale. Historical
   patterns only; current trades would need parsing Senate eFD directly.
3. JOURNALISM USE ONLY (5 USC 13107(c)(1)) — tagged in registry LICENSE_TERMS,
   bannered in the Playground, asserted by tests; must be excluded from any
   commercial release, same as House PTRs.
Also: AMOUNT is a disclosure band; 463 rows are the source's literal 'Unknown'
(legitimate). House PTRs remain unloaded (PDF/OCR build).

**Why:** prevents a new session from re-trusting the stale "bioguide-keyed"
scouting note or charting 2020 data as current activity.
**How to apply:** any trades analysis states the 2020 cutoff; never midpoint
amount bands; treat member attribution as a name-match lead.
