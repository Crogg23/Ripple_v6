# GOVERN RECON — 2026-07-12 (Move 1 of "Ripple, Govern Thyself") — FINAL

**Recon complete.** Two passes: filesystem (morning, while Snowflake was locked out) + full warehouse battery
(10:08, on the fresh `READER` PAT). Nothing was mutated — every warehouse statement was SELECT/SHOW/DESC.

**Session receipt:** account `ONEAFDA-UMB20733` (locator `UKB67948` — see guardrail corrections), user `CROGG23`,
role `RIPPLE_READER`, warehouse `SERVE_WH`. Battery cost: ~0.02 credits on SERVE_MON (5/mo cap, 4.98 remaining).
Raw results: `outputs/govern_recon_results_2026-07-12.json` (41 checks) + a 5-check follow-up pass.

---

## ⚠️ MOVE 0 IS NOT DONE — the leaked token is still live

`SHOW USER PROGRAMMATIC ACCESS TOKENS` returns **10 ACTIVE tokens**:

| Token | Role restriction | Expires | Verdict |
|---|---|---|---|
| **THE_LIBRARY** | **ACCOUNTADMIN** | 2027-07-05 | **The 07-05 token — the one pasted in the public chat. STILL ACTIVE. Revoke it.** |
| **Ripple_v6** | *(none — unrestricted)* | 2027-06-19 | Full-account key. Revoke target since 07-07. Still active. |
| **LIBRARY_PAT** | **ACCOUNTADMIN** | 2026-09-20 | The old "main write lane." Still active. Decide: keep for writes, or replace with a scoped write role. |
| ripple_loader | RIPPLE_ROLE | 2027-05-19 | Superseded loader role. Revoke target. Still active. |
| RIPPLE_LOADER_PAT2 | RIPPLE_LOADER | 2026-08-25 | Duplicate. Revoke target. Still active. |
| RIPPLE_LOADER_PAT | RIPPLE_LOADER | 2026-08-25 | Keep-list. |
| CLAUDE_MCP_RO | CLAUDE_MCP_READONLY | 2026-09-16 | Keep-list. |
| PORTAL_RECON | CLAUDE_MCP_READONLY | 2026-09-19 | Keep-list. |
| WAVE3_LOAD | CLAUDE_MCP_READONLY | 2026-09-19 | Keep-list. |
| **READER** | RIPPLE_READER | **2027-07-12** | Minted today — the token this recon ran on. Note: 1-year expiry (the read-lane runbook suggested 90 days). |

Unexplained and flagged, not hand-waved: the old `.env` secret (JWT exp exactly matching THE_LIBRARY's expiry)
was **rejected** at auth this morning even though THE_LIBRARY shows ACTIVE. Whatever the cause (wrong secret in
the file vs. a network-policy gate on PAT auth), the safe read is: **treat THE_LIBRARY as live and leaked until
it is explicitly revoked in Snowsight.**

**`revoke_straggler_pats.py` will fail-safe ABORT as written:** its DROP list names `LIBRARY_CLAUDE_PAT`, which
no longer exists (expired off), and its KEEP list doesn't know about `READER`. The guards will refuse to drop
anything. It needs a list refresh + re-preview before `--apply`. It was **not** superseded by the 07-08 commit —
that commit *created* it; it has never run (no snapshot artifact, ledger untouched, 4 of 5 targets still active).

---

## Q1 — `LIBRARY_META.BUILD` does not exist

`SHOW SCHEMAS LIKE 'BUILD' IN DATABASE LIBRARY_META` → 0 rows. No table collisions. **Move 2 has a clean slate.**

---

## Q2 — §8 defects: final verdicts

Every number below is from a live query today (check name in parens). V_STATE snapshot for context:
**1,785 landing tables · 288,749,856 landing rows · 41,241 edges · 9,788,419 entities · 1,030 active leads · 0 decisions.**

| § | Defect | Verdict | Live receipt |
|---|---|---|---|
| 8.1a | "~31 junk sources read `landed`" | **MOSTLY FIXED — 8 remain** | Of 199 landed/modeled catalog sources: 0 missing tables, 0 zero-row, **8 at 1–3 rows** (`d1a`): fed_cdc_wonder, fed_cms_hpt_mrf, fed_doj_crt_cases, fed_fbi_cde, fed_fincen_boi, fed_fra_safety, intl_austlii, intl_ge_datagov — all "landed", all 1 row. |
| 8.1b | FED_FHFA_NMDB misread as `sampled` | **FIXED** | lifecycle=`landed`, 19,054,246 rows (`d1b`). |
| 8.1c | OP-2022 invisible (13.25M rows) | **STILL REAL** | Physical table = 13,250,000 rows; INGEST_RUNS run `60f19a4a…` still `error`/0 ("I/O operation on closed file"); catalog lifecycle=`failed` (`d1c`). The data is there; the ledger still says it isn't. |
| 8.1d | fed_irs_eo_bmf = exact 2× dup of fed_irs_bmf | **CONFIRMED LIVE** | EO_BMF: 3,949,660 rows / 1,974,830 distinct EIN. BMF: 1,974,830 / 1,974,830. Ratio exactly 2.00 (`d1d`). No RETIRED schema exists → never quarantined. **§12's "Pour IRS EO BMF" parked idea = `already_done`. The brief's founding receipt checks out.** |
| 8.2a | Staging views all-TEXT | **STILL REAL, grew** | **819 of 1,033** staging views are 100% TEXT (`d2a`; audit said 789). |
| 8.2b | 171/233 reading-room views zero-cast | **APPEARS FIXED — confirm** | Only **3 of 233** THE_LIBRARY views are zero-cast today (`d2b`). The typed layer measurably landed. Five typed-view plan files were generated 07-07; no apply record exists on disk — Chris: did you run `thelibrary_typed_views` / `thelibrary_build --typed`? If yes, §9.7 is done and undocumented. |
| 8.2c | 95/199 landed sources unstaged | **STILL REAL** | **99 of 199** have no `STG_*` view (`d2c`). |
| 8.3 | No role-restricted serving PAT | **HALF-FIXED TODAY** | `RIPPLE_READER` + `SERVE_WH` + SERVE_MON live and verified (this recon ran inside them — including the libel firewall, see Q4). The `READER` PAT now exists (minted today). **Still open:** evidence.dev is wired to the dead interim token in `connection.options.yaml` → the reading room is dark until you do the `connection.yaml.serve` swap; `SNOWFLAKE_SERVE_PAT` still unset. |
| 8.4 | Graph 53% bare-ZIP; no core view | **CONFIRMED LIVE** | Tiers: GEO 21,912 / PROBABILISTIC 14,861 / STRONG 2,224 / CORROBORATED 1,611 / STEEL 473 / BRIDGE 160 (`d4`). ZIP-key edges: **21,538 of 41,241 = 52.2%**. `V_CONNECTIONS_CORE` **does not exist**; the core tiers sum to exactly **4,308** — the predicted view size. |
| 8.5 | Empty-tables gates have holes | **STILL REAL (bounded)** | LANDING: 1,785 tables, 0 zero-row, **49 at 1–3 rows** (`d5`). Gate code unfixed. |
| 8.6 | Query traps | **ALL CONFIRMED LIVE** | Open Payments now split across **three** tables (base 15.4M / 2022 13.25M / 2023 14.7M). AIS = 58,106,517 rows spanning exactly **2024-01-01 → 2024-01-08**. LEIE zero-NPI = **74,780 / 83,464 = 89.6%** (table is `FED_HHS_OIG_LEIE`). OFAC `SDN_TYPE` sentinel `[-0- ]` on 9,785 rows (table is `FED_OFAC_SDN`). → These are permanent facts: **POLICY rows, not DEFECT rows** in Move 2. |
| 8.7 | RLIKE whole-string | **DEMONSTRATED LIVE** | `'catalog' RLIKE 'cat'` → FALSE; `'.*cat.*'` → TRUE (`d7`). Policy row. |
| 8.8 | Politics marts clobberable | **STILL REAL — count stale** | **24** `POLITICS__*` tables live in `LIBRARY_MARTS.POLITICS` (not 13, and not in DBT_CROGERS). Protection is still convention-only. |
| 8.9 | Append loaders leave silent partials | **STILL REAL** | Admitted in the loaders' own docstrings (`noaa_ais_backfill.py:3`, `noaa_storm_events_backfill.py:3`). |
| 8.10 | leads_overlay.html stale | **STILL REAL, worse** | Baked-in: 4 detectors / 353 leads (file Jun 27). Live: **6 detectors / 1,030 active leads** (V_STATE), 0 published, 0 human decisions ever (`d10`: V_LEADS_PUBLISHED shows 1,030 visible / 0 published; DECISIONS=0). |
| 8.11 | CDN Plotly | **STILL REAL** | Both HTML artifacts pull `cdn.plot.ly`; vendored `outputs/plotly.min.js` (4.8MB) sits unwired beside them. |

---

## Q3 — §9 pending queue: definitive apply-state

| # | Script | Applied? | Live proof |
|---|---|---|---|
| 1 | `reconcile_op2022.py` | **NO** | Run still `error`/0; lifecycle `failed`; 13.25M rows physically present. |
| 2 | `build_v_connections_core.py` | **NO** | View absent (SQL error 42S02 on read). Would hold exactly 4,308 rows today. |
| 3 | `revoke_straggler_pats.py` | **NO — and now stale** | 4 of 5 DROP targets still ACTIVE; 5th (`LIBRARY_CLAUDE_PAT`) vanished → script will ABORT by design. Needs list refresh (+ add `READER` to KEEP) and re-preview. Manual-only, correctly. |
| 4 | `dedup_irs_eo_bmf.py` | **NO** | Duplicate confirmed live; no `LIBRARY_RAW.RETIRED` schema exists. |
| 5 | `rebuild_frozen_marts.py` | **NO — and 4 of 7 targets are GONE** | In DBT_CROGERS only 3 of 7 marts exist: BORME=3 rows (frozen), FCA=12 (frozen), FED_REGISTER=5,000. CRO survives only as a 1-row copy in `_RESTORE_20260701`; SLAVEVOYAGES / NAAG / TAGGS marts exist nowhere in LIBRARY_MARTS (dropped in the 07-01 housekeeping). The script's rebuild-from-landing approach still works, but its preview will look very different from 07-07 — re-preview is mandatory. |
| 6 | `build_giant_aggs.py` | **NO** | Zero `%_AGG` tables in LIBRARY_MARTS.PUBLIC. |
| 7 | `thelibrary_*_build --typed` | **LOOKS ALREADY DONE — confirm** | 230/233 reading-room views carry typed columns today (audit had it at 62/233). If Chris applied it 07-07, mark applied; if not, find out what typed them. |
| 8 | `backfill_join_keys_std.py` | **NO** | **142 of 199** landed/modeled sources still `JOIN_KEY_TIER_PROVISIONAL=TRUE` — the exact figure the script was written against. |
| 9 | `gen_evidence_pages.py` | **NO** | `evidence/pages/` holds only the 7 hand-authored pages. (Correctly last — and now also gated on the evidence.dev credential swap, §8.3.) |

**Move 5 confirmation:** re-preview everything — the warehouse moved (marts dropped, tokens changed, THE_LIBRARY typed) since the 07-07 previews.

---

## Q4 — `connect/` tests + the ladder as persisted

**Correction to the brief: `connect/` is not test-free.** ~73 connect-adjacent offline tests exist
(leads gate ×27, key-normalize ×14, receipt ×9, leads ×8, safety ×6, keyguard ×4, resolve ×5). What Move 4
genuinely adds: auto-merge-unreachable, NPI-leakage, calibrated precision *band* (current eval only asserts a
0.40 floor on a name-sim scorer), blocking recall, and the end-to-end `published()` refusal. The proposed
`ladder_holdout.parquet` fixture does not exist (`tests/fixtures/` has only `gold_pairs_sample.csv`).

**The auto-publish door, precisely:** `_auto_publishable()` at `connect/leads.py:412` is a hardcoded
`return False` — stronger than "the numbers happen to come out right," but `test_safety.py` proves the gate
honors `auto_ok=True` with zero human decisions, so the door is one edited line from live. Move 4 test #1
should pin both the hook and the rungs.

**MATCH_MODEL** (model `fs_emp_95b289e0`): surname m=.9997/u=.5081 · first .9898/.0675 · middle .9869/.0781 ·
zip .2477/.0034 · address .1668/.000172.
**MATCH_RUNGS:** CONFIRMED (M≥11) precision **.8764** (lo95 .8602), recall .4615 · STRONG (M≥8) .5769 · LEAD (M≥0) .1186.
→ Matches the handoff exactly. No rung within sight of the 0.99 auto-merge bar. **Live bonus verification:** the
libel firewall works — this session's reader role was *refused* on raw `LEADS`/`MATCH_PAIRS` and could only read
`V_LEADS_PUBLISHED`, exactly as designed.

---

## Q5 — Credential state (end of day)

| Key | State |
|---|---|
| `SNOWFLAKE_PAT` | ✅ **NEW — working.** The `READER` token (RIPPLE_READER-restricted, exp 2027-07-12). |
| `SNOWFLAKE_ROLE` | ✅ `RIPPLE_READER` (added today; PAT sessions can't `USE ROLE`, so this must match the mint). |
| `SNOWFLAKE_WAREHOUSE` | ✅ **Changed today `RIPPLE_WH` → `SERVE_WH`** (reader has USAGE only on SERVE_WH/COMPUTE_WH). Flip back only when a write-role PAT returns. |
| `SAM_API_KEY` | ✅ exp 2026-09-22. |
| `ANTHROPIC_API_KEY` | ✅ present (0 API credits at last check). |
| `CENSUS_API_KEY`, `COURTLISTENER_TOKEN`, `SOCRATA_APP_TOKEN`, `RIPPLE_CONTACT_UA` | ❌ still missing since the 07-05 rewrite. `RIPPLE_CONTACT_UA` is the one-line SEC-EDGAR/CIK unblock. |
| `SNOWFLAKE_SERVE_PAT` | ❌ unset — evidence.dev still points at a dead token; do the `connection.yaml.serve` swap (the new READER token is exactly what it wants). |
| `infra/keys_ledger.json` | ❌ stale twice over: PAT row says exp 2026-09-20 (that's LIBRARY_PAT, not the live token) and knows nothing of READER. |

**Consequence of the reader-only lane:** the write lane is gone until a scoped write PAT exists. Every §9
`--apply` script needs one (they write to REGISTRY/INGEST_LOGS/MARTS). Candidates already exist as roles:
`RIPPLE_INGEST_RW`, `RIPPLE_TRANSFORM_RW` (built for GitHub Actions, least-privilege). That's the natural
Move-0-completion: mint the write PAT against a scoped role, never ACCOUNTADMIN.

---

## Guardrail corrections (brief vs. today's reality)

1. **The `connections.toml` "wrong account" scare was a false alarm.** Live session proves `UKB67948` is the
   *locator* of `ONEAFDA-UMB20733` (org `ONEAFDA`, account `UMB20733`) — same account, two naming schemes.
   The toml is empty (0 bytes) anyway. Keep printing the resolved account before dbt, but the landmine §6/§14
   describes never existed.
2. **`connect/` has tests** (see Q4) — Move 4 should be framed as *closing five named gaps*, not greenfield.
3. **The brief is not in the repo** (`RIPPLE_GOVERN_THYSELF_BRIEF.md` absent — it was pasted in chat). Commit it
   if later moves will cite it.

---

## The payoff list — what the docs believe that the warehouse contradicts

Seed data for Move 2's `DEFECTS`/`PARKED` tables; every row here was doc-vs-live divergence found today:

- §12 "Pour IRS EO BMF" → **already in the Library, twice** → `already_done`, and defect 8.1d stays open until dedup applies.
- "~31 junk landed sources" → **8** today.
- "171/233 zero-cast reading-room views" → **3/233** today (typed pass landed, apparently unrecorded).
- "13 politics marts" → **24**.
- Overlay says 4 detectors/353 leads → live **6/1,030**, 0 published, 0 human decisions ever.
- "789 all-TEXT staging views" → **819/1,033** (got worse, not better).
- 4 of the 7 "frozen marts" aren't frozen — they're **absent** (dropped 07-01, never rebuilt).
- `revoke_straggler_pats.py`'s world (10 tokens incl. LIBRARY_CLAUDE_PAT) → today's world (10 tokens, one gone, one new READER).
- keys_ledger PAT row ↔ no live token.
- build-state.md "Last updated 2026-07-07", 1,629 hand-typed lines — 5 days and one credential regime behind.

---

## Checkpoint

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECKPOINT — MOVE 1 COMPLETE  [recon final; nothing mutated]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verified:   §8 (all 11 groups, live) · §9 (all 9, definitive) · tests · creds · PATs
Blockers:   THE_LIBRARY + Ripple_v6 tokens still ACTIVE (Move 0 unfinished)
            No write lane exists (reader-only PAT) — all §9 applies gated on a scoped write PAT
Next:       Chris reads this → Move 2 (LIBRARY_META.BUILD, clean slate confirmed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
