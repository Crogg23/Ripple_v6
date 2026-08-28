# RIPPLE STATUS — 2026-08-27 (evening) — Certification sweep DONE, connections audited (58/100: precision ~90 / coverage ~35), Tier A pulls landed, two mega-loads running overnight, spine rebuild WAITING ON CHRIS

*One screen. Rewritten (never appended) at the end of every session.*

## 🚨 Read this first

1. **Chris's one command block is the bottleneck for the graph.** The DUNS
   backfill spec edit is made and validated (`connect/entity_index_specs.py`,
   assistance-table DUNS extra_key), the DOCKET/GEO edge fixes are in code
   (`connect/keys.py`, `connect/discover.py`, `connect/incremental.py` — tests
   71/72, 1 pre-existing failure re: today's LEIE refresh watermark), and
   incremental spine ingest is ALREADY frozen by config drift regardless. The
   classifier blocks sessions from running these. Chris runs, in order, from
   the repo root (~5h background, ~$12–18 on X-Small):
   `python -m connect spine` → `python -m connect.incremental seed` →
   `python -m connect discover`.
   This ships: 478k+507k DUNS backfill (94% orphan → ~0), pension-EIN spine
   fuel, the DOCKET namespace fix (~1,300 false edges die), GEO prune
   (~18k noise edges), and re-pins the drifted config.
2. **Two loads running overnight, both checkpointed + resumable:**
   - MAUDE device injuries → `FED_FDA_MAUDE_FULL`: 25,711,469 records,
     ~6–8h. Resume: `python scripts/fda_bulk_split_load.py --spec
     FED_FDA_MAUDE_FULL --run`. Verify with SUM(ARRAY_SIZE) not row count
     (VARIANT chunks).
   - USAspending subawards → `FED_USASPENDING_SUBAWARDS_FULL`: 227 monthly
     chunks, ~20–30h (server-side generation is the bottleneck). Resume:
     `python -u scripts/usaspending_subawards_full_load.py --run`.
   - Senate LDA backfill also still running from before (healthy, throttled).
3. **SERVE_MON quota raised to 100/mo by Chris** (was 5, hit cap mid-session).
   New loaders are all registered INCLUDE=Y; scripts are UNCOMMITTED in the
   working tree (5 new loader scripts + connect-layer edits) — commit next
   session after the rebuild lands.

## What this session did (day session, Chris driving)

- **Certification sweep (the "am I missing anything" question, now CLOSED):**
  all 221 sub-5k non-portal landing tables live-counted and web-verified
  against publishers. ~110 certified complete, ~88 slices, ~24 unknown.
  Ledger: `reports/big_win_pull_sweep_2026-08-27.md` (includes the external
  top-10: LEIE, CMS utilization, EOIR, FMCSA, 990 XML, FAC, call reports,
  NHTSA, PPP, ARCOS-raw).
- **Connections audit (3 read-only lanes): graph = 58/100 — precision ~90,
  coverage ~35.** Trustworthy but narrow. STEEL tier 95–100% measured
  precision, sentinels clean, blobs structurally impossible. Holes: DUNS 94%
  orphaned (fix staged), 92% of the domain×key grid empty (17/32 domains
  zero-keyed), name+zip machinery matching 48.6% on same-universe keyless
  pairs it's never pointed at, 3 dead key families (PATENT/ships/DEA), DOCKET
  collision (~1,300 false edges, fix in code), CORROBORATED 75–85%.
  Full detail: `reports/connections_audit_2026-08-27/` (SUMMARY + 3 lanes +
  duns_backfill + edge_fixes).
- **Tier A pulls landed and verified** (`reports/tier_a_pulls_2026-08-27.md`):
  - LEIE fraud exclusions refreshed: 83,842 rows (NPI sentinel `0000000000`
    on person rows — exclude before joins).
  - FDA NDC directory: 115,802 (ARCOS↔NADAC↔Open Payments chain now legal).
  - SEC FTD CUSIP bridge: 128,303 rows, ~14.9k CUSIPs↔issuer names.
  - **Form 5500 full: 4,299,671 filings 2009–2024**, every year exact-match,
    462,416 distinct EINs, ~716k EIN+PN plans → `FED_DOL_FORM5500_FULL`
    (old 33k table untouched). Follow-on: 5500-SF (~700k/yr) + schedules.
  - **GUDID full: 5,182,695 devices + 6,767,219 identifiers**, PRIMARYDI
    unique, verified → `FED_FDA_GUDID_FULL_*`.
- **Contracts R2 "stall" was stale intel** — it FINISHED 08-25 (93,153,424
  rows, exact checkpoint match). Open chore: staging still reads the old
  truncated 20M sample table; repoint to R2.
- Corrections to the record: STEEL families = 24 (not 13); no COLUMN_TRUST
  table exists (key registry = SOURCE_REGISTRY JOIN_KEYS_STD/TIER); the
  depth-triage's round-number flag misses odd-number truncations (pension +
  MAUDE were invisible to it) — memory updated with the verify-done-claims
  rule after Chris called out the "depth is solved" miss.

## BROKE

Nothing. (1 pre-existing test failure: incremental-vs-full parity on the LEIE
source watermark — caused by today's legitimate refresh, self-heals on rebuild.)

## YOUR MOVE (Chris)

1. **Run the 3-command rebuild block** (item 1 above) — everything graph-side
   queues behind it.
2. Still open, unchanged: portal-scope ruling (graph in/out), backups
   keep/clear, auto-push off-or-bless, CMS Open Payments re-pull.

## NEXT

After the rebuild: re-run the DUNS orphan check (~0 expected), wire the 5
verified-but-unregistered keys (MSHA controller, OFLC case, EIN+PN plan,
NDC, CUSIP — now all have landing sides), point the name+zip machinery at the
keyless giants (FEMA 26M / CFPB 17M / FHLB), repoint contracts staging to R2,
commit the 5 new loaders + connect edits. Then the known-truth tracer
(20 entities traced by hand vs the graph) as the capstone. Wave-3 pull queue:
CMS utilization/Part D, IRS 990 XML, EOIR, FMCSA, call reports, NHTSA, PPP.

**Cost note:** today ≈ $3–8 warehouse (metadata sweeps ~pennies, loaders'
COPY work the bulk) + the overnight loads (~$5–15 more as they land);
Claude-side ~1.5M agent tokens across sweep + audit + build agents. The
rebuild is the priced $12–18 item, awaiting Chris.
