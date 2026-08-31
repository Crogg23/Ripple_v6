# FABLE MISSION PACKET — Value-Shape Key Sniffer

Hand this whole file to a fresh Fable session. It is self-contained.
Written 2026-08-18. Companion scope doc: `reports/value_shape_sniffer_scope_2026-08-18.md`.

---

## 0. THE ONE-LINE MISSION

Find columns in the warehouse that **hold** a known hard identifier but whose
**name** doesn't say so — then prove each one by live value overlap, and hand
back a ranked list for human approval. Finding nothing is a valid, useful
result. Report it either way.

You are NOT authorized to change how anything connects. You produce evidence.

---

## 1. WHY THIS EXISTS (read before touching anything)

Ripple connects public datasets by hard identifiers (EIN, NPI, CIK, DUNS, LEI,
UEI, CCN, DEA number, EPA facility ID, mine ID, FEC IDs, and more).

There are two mechanisms, and only one is name-blind:

- **The spine (the actual merge path)** — `connect/spine.py`,
  `connect/entity_index.py`, `connect/incremental.py`. These iterate
  `connect/entity_index_specs.py :: DISPLAY_SPECS` and nothing else. Every
  entry hand-declares `key` (the ID type) and `key_col` (the physical column).
  Column naming is irrelevant here. This is correct and is NOT the problem.

- **The automatic connection finder** — `connect/fingerprint.py` calls
  `connect/keys.py :: detect_key(column_name)`, which is **100% name-token
  based**. Its whole vocabulary for EIN is the single token `ein`. A column
  named `TAX_ID`, `FEIN`, `EMPLOYER_ID`, or `ORG_TAX_NUM` full of real EINs is
  invisible to it. Same single-token story for NPI, CIK, DUNS, LEI, CCN, DEA.
  Only ZIP / FIPS / LATLON / COUNTRY / GEOM / NAME / ADDRESS have real synonym
  lists. Seven two-token pair rules exist (postal+code, frs+id, registry+id,
  pws+id, mine+id, cmte+id, cand+id).

**Nothing in the platform has ever inspected VALUES to infer key type.** That is
the gap you are filling.

The failure mode is missed links, never false ones — the design is fail-closed.
So today's connection count is a **floor**, and nobody knows how far below the
ceiling it sits.

---

## 2. MEASURED FACTS (queried live 2026-08-18 — trust these, re-verify if stale)

- `LIBRARY_RAW.LANDING`: **64,035 columns / 1,871 base tables**.
- Portal-crawl tables (`PORTAL_%`): **51,294 of those columns**. Already excluded
  from edge generation by `discover.EDGE_UNIVERSE_EXCLUDE_PREFIXES`.
- **Non-portal target universe: ~12,741 columns.**
- 63,963 of 64,035 columns are TEXT/VARCHAR/NUMBER — type filtering saves
  nothing. Shape testing is the filter.
- `LIBRARY_META.REGISTRY.COLUMN_CATALOG` (which already stores 5 sample values
  per column) covers only **25 tables / 751 columns**. Not a shortcut at scale.
- **UNRESOLVED DISCREPANCY:** `STATUS.md` claims 2,216 live raw tables;
  INFORMATION_SCHEMA reports 1,871 base tables in LANDING. Not chased. Do not
  cite either number as settled. If you can cheaply explain it, do, and say so.

---

## 3. HARD RULES — VIOLATING ANY OF THESE FAILS THE MISSION

1. **DO NOT EDIT `connect/keys.py`.** Not `KEY_TOKENS`, not `PAIR_RULES`, not
   `EXACT_TOKEN_KEYS`, not `NORM_RULES`. Adding a synonym there silently changes
   the graph's key detection, the registry's spine-entity classification
   (`connect/spine_entity.py`), and every `DETECTED_KEY` in the column
   dictionary — retroactively, across everything. **Read it. Never write it.**
2. **DO NOT EDIT `connect/entity_index_specs.py :: DISPLAY_SPECS`.** That is the
   merge path. Additions there change the entity map and require a full spine
   rebuild. Human decision only.
3. **READ-ONLY WAREHOUSE ACCESS.** No DDL, no writes to `LIBRARY_META`, no
   scratch tables in `LIBRARY_RAW`. If you believe you need one, stop and ask.
4. **NEVER auto-register anything.** Your output is a markdown report. Full stop.
5. **A bare `COUNT(col)` is not evidence.** This platform has produced two false
   "100% populated" readings from sentinel-masked columns (NPPES EIN, AIS IMO —
   blank strings and placeholder text passing a null check). Every claim about a
   column carries `COUNT(*)`, `COUNT(col)`, `COUNT(DISTINCT normalized_col)`,
   and **five real sample values**. No exceptions.
6. **Shape is a candidate generator, never a verdict.** Nine digits is also an
   SSN, a ZIP+4, a phone number, a dollar amount, and a row sequence number.
   Only live value overlap (Stage 2) may promote anything.
7. **Reuse the existing thresholds. Do not invent looser ones.** See §5.
8. **Checkpoint to disk after every table.** A crash must never restart the bill.
9. **Stop and report at any stage gate if cost is running over estimate.**

---

## 4. THE EXISTING MACHINERY YOU MUST REUSE (do not re-implement)

- `connect/keys.py :: normalize_sql(key, col_expr)` — emits the canonicalization
  SQL for a key type. **Import it.** A hand-rolled copy drifting from this
  function already caused a bug on 2026-07-31.
- `connect/keys.py :: NORM_RULES` — the per-key normalization mode and width.
  Read it to learn each key's real shape. Live-verified examples:
  - `pad`: NPI 10, EIN 9, DUNS 9, CIK 10, CCN 6, MMSI 9, MINE_ID 7
  - `fixed`: UEI 12, LEI 20, FRS_ID 12, PWSID 9, COMPANY_NO 8
  - `alnum_upper` (no pad, no zero-strip): DEA_NO, BIOGUIDE, ICPSR,
    FEC_CMTE_ID, FEC_CAND_ID
  - `code` / `zip5` / `country` / `imo`: NAICS, SIC, NCES, DOCKET, PATENT, FIPS,
    ZIP, COUNTRY, IMO
- `connect/discover.py :: KEY_DOMAIN` — the honest value-space size per key,
  used by the collision math. Read; do not change.
- `connect/discover.py :: confidence(key, tier, a_distinct, b_distinct, matched)`
  — the scoring gate. `MIN_MATCH = 3`, `MIN_MATCH_PROB = 5`,
  `COLLISION_MULT = 5.0`. **Use it unchanged.**
- `connect/fingerprint.py` — read it for the checkpoint/resume pattern
  (`CHECKPOINT_EVERY`, format-marker resume) and copy that discipline.
- The live spine entity table lives in `LIBRARY_META."CONNECT"` — note
  `CONNECT` is a **reserved word and must always be quoted**. See
  `connect/store.py :: cfqn()`; the entity table is `ENTITY_MAP`.
- Read lane / credentials: load `library-onboarding/.env` with `override=True`,
  then use `viz.sqlrun`. Copy the pattern verbatim from
  `scripts/build_column_catalog.py` (top ~45 lines).

---

## 5. THE WORK — FOUR STAGES, EACH A COST GATE

### Stage 0 — name-synonym sweep. Cost ~$0. Do this first, always.
- One metadata query over `LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS`
  (`TABLE_SCHEMA='LANDING'`, exclude `PORTAL_%`).
- Match the ~12,741 column names against a synonym list YOU write, per key.
  Starters: EIN <- tax_id, fein, employer_id, taxpayer_id, tin, ein_number;
  NPI <- provider_id, prov_num, npi_number, rendering_provider;
  CIK <- sec_id, filer_id, registrant_id; DUNS <- dnb, duns_number, dandb;
  LEI <- legal_entity_id; UEI <- unique_entity_id, sam_id;
  CCN <- provider_number, medicare_number, ccn_number, prvdr_num;
  FRS_ID <- facility_id, epa_facility, registry_id.
  **Expand this list yourself — that is part of the job, not a checklist.**
- Deliverable: ranked candidate list, zero compute spent.
- **GATE: report the candidate count before spending anything.**

### Stage 1 — value-shape sniff. Cost $3-6, 30-90 min.
- Per table, ONE aggregate query over a `LIMIT 50000` subsample.
- Batch ~30 columns per query (`build_column_catalog.py` shows the batched
  `ARRAY_AGG` sample-probe pattern). ~2,500 queries total.
- Per column compute: non-null %, `COUNT(DISTINCT normalized)`, and the REGEXP
  hit-rate against each known key's shape after stripping punctuation.
- Also flag: the literal string `'nan'` (a known corruption — 4.2M cells were
  written that way by a pandas loader), empty strings, and columns holding one
  repeated value. These are sentinel traps, not keys.
- Serial on X-Small ~2h; ~6 parallel lanes ~25-35 min wall. Parallelize.
- Checkpoint after every table.
- Deliverable: candidate (table, column, suspected key, shape hit-rate,
  distinct count).
- **GATE: report candidate count + spend before Stage 2.**

### Stage 2 — live overlap confirmation. Cost $2-5.
- For each survivor: normalize its values with `normalize_sql`, then measure
  overlap against the live value set of that key already in the spine.
- Score with `discover.confidence()` **unchanged**. A candidate is reported only
  if it beats chance by the existing 5.0x factor.
- Watch the two known traps: **zero-padding differences** (pension EINs only
  joined once zero-padded) and **masked/sentinel columns** that look full but
  hold one repeated placeholder.
- Deliverable: confirmed list with overlap %, matched-distinct count, score.

### Stage 3 — the report. Cost $0.
Write `reports/value_shape_findings_<date>.md`, ranked best-first:

| table | column | suspected key | shape hit % | distinct (normalized) | live overlap % | matched distinct | confidence | 5 sample values |

Plus, in plain English at the top:
- How many columns scanned, how many candidates, how many confirmed.
- **What this unlocks** — for each confirmed column, which dataset it newly
  wires to which, and what question that lets someone ask. A key with no human
  on the other end of it is trivia; say so if that is what you found.
- What you rejected and why, so nobody re-tries it.
- Actual spend vs. estimate.

---

## 6. WHAT COMES AFTER (context, not your job)

Confirmed columns get hand-added to `DISPLAY_SPECS` by a human, then require a
**full spine rebuild (~$12-20, ~4.5h)** to take effect. Finding keys is cheap;
using them is not. That is why the deliverable is a **ranked batch**, never a
trickle of one-at-a-time finds.

---

## 7. REPORTING BACK

- One line at start with your time estimate, a heartbeat if it drags, one line
  at the end. No play-by-play.
- Lead with 3-5 bullets: what you found, what is confirmed, what it cost, what
  decision is needed. Full detail goes in the report file.
- Bad news first and uncut — if Stage 1 found nothing, or the estimate blew up,
  or a rule in §3 turned out to be impossible to follow, that is sentence one.
- Plain words in the summary. Table names and function names belong in the
  report file, not the brief.
