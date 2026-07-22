# BETA DECISIONS — 2026-07-20

Chris's instruction this session: **"You make the decisions. Consider it building me a beta. I will adjust AT THE END."**

This file is the ledger of every call I made under that instruction. Each entry says what was decided, what was built, and the one-line way to reverse it. Nothing here is presented as your ruling — it's the beta default until you adjust.

---

## B1 — Confirm vs. published (roadmap §6.4): **TWO-STEP**

**Decision:** a ✅ Confirm in the Reading Room is a private **nomination**. `PUBLISHED=TRUE` now requires a second, explicit `'published'` verdict, written only by `scripts/publish_lead.py` (which refuses unless the latest verdict is `'confirmed'`, previews by default, and requires `--reason` on `--apply`).

**Why this default:** it's the reversible direction. One-click-publish can be restored with a one-line view change; the opposite mistake (a historical Confirm silently going public when the SBA door opens) can't be un-shipped. It also makes the Constitution's "auto-publish is structurally blocked" literal: the auto-confirm hook can no longer publish even in codes.

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

---

## 2026-07-21 FOLLOW-UP (Chris's ordered checks — findings and receipts)

**STEP 0 — commit:** already done by Chris himself, 2026-07-20 15:47 — commit `03577e5`, pushed to origin/main. Nothing left to commit from the beta.

**STEP 1 — the Reading Room credential blocker: DOES NOT EXIST, proven executably.** `reading_room/connections.py` already hard-pins verdict writes to `RIPPLE_REVIEW_PAT` + role `RIPPLE_REVIEW_WRITER` with a no-fallback rule (missing PAT → `RuntimeError`, app runs read-only with a banner; `SNOWFLAKE_PAT`/`SNOWFLAKE_SERVE_PAT` are never used for writes), and clamps `USE SECONDARY ROLES NONE`. No code change was needed. Proof run (connection kwargs intercepted at the `snowflake.connector` boundary with the default lane deliberately set to a fake BUILD PAT — i.e. the mid-checklist Steps 5–7 state):

```
PROOF 1: PASS — no RIPPLE_REVIEW_PAT -> RuntimeError (no fallback to any other PAT)
PROOF 2: resolved role='RIPPLE_REVIEW_WRITER' warehouse='SERVE_WH' credential_is_RIPPLE_REVIEW_PAT=True credential_is_build_pat=False
PROOF 3: reader resolved role='RIPPLE_READER' warehouse='SERVE_WH' rides_swapped_default_PAT=False
```

(Proof 3: the read lane rides `SNOWFLAKE_SERVE_PAT`, role pinned to `RIPPLE_READER` — also immune to the swap.) A 🟢 reassurance line was added to checklist Step 5.

**STEP 2 — investigations (findings only; nothing built, publish path untouched):**

- **(a) The publish wall is a promise, not a grant.** `RIPPLE_REVIEW_WRITER` holds blanket `INSERT` on `REVIEW.DECISIONS` (`provision_review_lane.sql:77`); Snowflake does not enforce CHECK constraints and has no triggers, so a raw `INSERT … DECISION='published'` with the review PAT walks straight past `publish_lead.py`. And `publish_lead.py` itself runs as the same `RIPPLE_REVIEW_WRITER` (`publish_lead.py:72`) — the database cannot tell the helper from a hand INSERT. What the design does guarantee: any bypass is append-only-recorded with reviewer + timestamp, and neither the Reading Room buttons nor the `connect review` CLI can emit the verdict. A real database wall needs a role/table split (e.g. a dedicated publisher role as the only INSERT path the view trusts for `'published'` rows) — post-sprint design call, deliberately not built.
- **(b) The SBA page's receipt SQL is internal-only.** It names `LIBRARY_RAW.LANDING.FED_SBA_LOANS`, so a stranger cannot execute it — as printed it proves re-derivability only to someone inside the warehouse. The page links the public FOIA dataset, but carries no public-executable variant of the query. A known gap to close before any public ship; untouched per orders.
- **(c) DR lands off-account by design, and the credentials do not exist yet.** B2/`DR_SIZING` specify export → download → off-account storage (external). No cloud-storage credential exists anywhere checked this session: `.env` keys are Snowflake/SAM/Anthropic only; no `~/.aws`, `~/.config/gcloud`, or `~/.azure`. A Snowflake **internal** stage would be a second copy in the same building and does not satisfy B2. Acquiring a bucket + keys is part of the GO line.

**STEP 3 — checklist corrections landed:**
- **Step 6 rewritten.** Verified live: `RIPPLE_TRANSFORM_RW`'s grants are all object-level (no user-management privilege), but `SHOW USER PROGRAMMATIC ACCESS TOKENS` succeeded self-service as `RIPPLE_READER` — all 8 tokens visible, both drop-targets (`ripple_loader`, `RIPPLE_LOADER_PAT2`) present, 6 keepers intact. Self-service `ALTER USER` is unproven, so the default path is now: script **preview** in the terminal (works on any lane) → **drop in Snowsight as ACCOUNTADMIN**.
- **Step 8 marked OPTIONAL** — the `SERVE_MON` grant only feeds the Atlas budget meter, and the Atlas is post-sprint under B3.

---

## 2026-07-21 (later) — B9 DELIVERED: the honesty engine

Sprint brief §5.2, built and adversarially verified. **`honesty/` package** (~600 lines + 35 offline tests, zero dependencies, zero warehouse contact — reads the committed dbt manifest, writes committed artifacts):

- **The lineage walker** (`python -m honesty`): walks every mart's full dbt DAG + literal-FQN reads, grades `fact` / `lead` / `unverified`, fail-closed. Live result over all 47 marts: **46 fact · 1 lead (`lead_queue`, via its `V_LEADS_PUBLISHED` claim ancestry — exactly right) · 0 unverified.** Artifacts: `honesty/mart_grades.json` (every receipt) + `honesty/MART_GRADES.md`, fingerprinted by the manifest's own `generated_at` (deterministic — a diff means models or rules changed, never the calendar).
- **The refusal** (`honesty.assert_composable`): refuses at compose time to blend fact-grade and lead-grade rows into one scalar; traps travel as mandatory disclosures; `measure_input_for_mart()` ties labels to the committed grades so callers can't hand-type `fact`.
- **The trap axis**: the five source-data POLICY traps mirrored verbatim with a drift-tripwire test.
- **Adversarially verified before trusting it:** 4 hostile auditors hand-walked all 20 joined marts + 8 spot-checks — **all 47 grades confirmed correct**; a 5th agent code-reviewed the walker and proved **5 fail-open holes** (comma/LATERAL joins invisible, jinja-in-ON reading as neutral, `NPI_NAME` upgrading to hard, ghost dependencies vanishing, WHERE-clause identity logic unseen) plus 2 fail-closed bugs. **Every one is fixed and pinned by a test**; grades were re-derived after hardening — unchanged, now with coverage that earns them.
- **Two repo defects noted by the auditors, not fixed here (out of scope):** `stg_fed_noaa_ais`'s header claims a single-day AIS snapshot while the verified POLICY says 8 days (the policy is receipt-backed; the header is wrong); and out-of-dbt warehouse views are opaque to any manifest walker — `V_LEADS_PUBLISHED` is caught by name, but the limitation is documented in `honesty/README.md`.

**Adjust by:** the taxonomy (one judgment call — hard-anchored composite joins count as fact-compatible) is documented in `honesty/README.md`; say the word and the rule flips with its tests.
