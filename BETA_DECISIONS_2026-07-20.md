# BETA DECISIONS — 2026-07-20

Chris's instruction this session: **"You make the decisions. Consider it building me a beta. I will adjust AT THE END."**

This file is the ledger of every call I made under that instruction. Each entry says what was decided, what was built, and the one-line way to reverse it. Nothing here is presented as your ruling — it's the beta default until you adjust.

---

## B1 — Confirm vs. published (roadmap §6.4): **TWO-STEP**

**Decision:** a ✅ Confirm in the Reading Room is a private **nomination**. `PUBLISHED=TRUE` now requires a second, explicit `'published'` verdict, written only by `scripts/publish_lead.py` (which refuses unless the latest verdict is `'confirmed'`, previews by default, and requires `--reason` on `--apply`).

**Why this default:** it's the reversible direction. One-click-publish can be restored with a one-line view change; the opposite mistake (a historical Confirm silently going public when the SBA door opens) can't be un-shipped. It also makes the Constitution's "auto-publish is structurally blocked" literal: the auto-confirm hook can no longer publish even in code.

**Built:** `provision_review_lane.sql` (PUBLISHED = 'published'; ran nowhere yet, so zero migration), `connect/safety.py` (+`PUBLISHED_VERDICT`, gate change, 'published' deliberately NOT writable by `record()`), `connect/leads.py` (docstrings + CLI hint), `reading_room/queries.py` (published leads never re-enter the queue), `scripts/publish_lead.py` (new), 4 test files updated — 16/16 offline gate tests pass.

**Adjust by:** ruling "confirm = published." One view edit + revert of the `gate_rows` line + drop the helper. ~15 minutes.

## B2 — DR: spend or accept risk (roadmap §6.6): **PREPARED + RECOMMENDED GO, spend awaits your line**

**Decision boundary honored:** real money is RED, no exceptions — so this one is *prepared*, not executed. The zero-spend sizing ran today: **the whole warehouse is ~15.8 GB compressed; a full parquet backup is ~$0.25–0.47/month + ≤1 credit one-time** (`outputs/DR_SIZING_2026-07-20.md`). Recommendation: GO. The verdict micro-export (`scripts/export_review_decisions.py`) shipped today regardless, so human decisions are protected from verdict #1.

**Adjust by:** saying GO (an agent then builds the export on the A00 lane) or "risk accepted" (recorded, done).

## B3 — The 30-day freeze (roadmap §6.7): **ADOPTED for the sprint**

No new sources, no new detectors, no new instruments, frontier stays parked. The sprint brief already scoped the Atlas out, so the freeze costs nothing and kills scope-creep for free. The SBA page is not a new instrument — it's the existing evidence.dev surface doing its job on an existing finding.

**Adjust by:** one line, any time; nothing built today depends on the freeze either way.

## B4 — `foundation_before_detectives` (roadmap §6.8): **RE-AFFIRMED**

3a spine feeds are foundation work by the policy's own terms and stay in-plan; 3b detectors stay out of the sprint. No conflict remains.

**Adjust by:** one line if you want 3b earlier (the Nov-2026 midterms clock is the only cost of waiting).

---

## Build decisions taken inside those rulings

- **B5 — Lane pinning:** `connect/db.py` and dbt `profiles.yml` now prefer `SNOWFLAKE_ETL_WAREHOUSE` when set (commented placeholder added to `.env`; uncomment after Step 0 confirms the name). dbt's default role changed **ACCOUNTADMIN → RIPPLE_TRANSFORM_RW** so an unexported shell fails loudly instead of silently escalating. *Adjust by: revert two files.*
- **B6 — Spine fixes landed:** NPPES single-underscore names (verified live against 333 columns) and removal of the dropped `FED_CMS_FACILITY_AFFILIATION` from the spine spec. The spine rerun itself still waits for the A00 lane (Snowsight hour) per the checklist.
- **B7 — SBA page runs on a frozen, re-derived extract:** every number was re-derived live TODAY (cell-for-cell match, receipts in `outputs/SPRINT_VERIFY_2026-07-20.md`) and frozen into CSVs under `evidence/sources/sba/`. The page never touches the warehouse at build time — no credential in the public build path, zero runtime cost, and the SQL receipts are printed on the page for re-derivation.
- **B8 — Nothing went public.** The page is built and proven locally. A stranger-loadable URL is a finding leaving the building — that stays behind your sign-off (and B1's publish step). No exceptions, including in beta mode.
- **B9 — Honesty-engine writeup (§5.2)** is the next build block after this beta lands, per the sprint's own two-front discipline; not started today to keep WIP honest.
