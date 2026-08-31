# Scope — Value-Shape Key Sniffer ("the ABCD problem")
2026-08-18. Written for a go/no-go. Nothing built, nothing run beyond four
read-only metadata queries.

## The problem, precisely

Two separate mechanisms find connections today, and only one is name-blind.

1. **The spine (the merge path).** `connect/spine.py`, `connect/entity_index.py`
   and `connect/incremental.py` iterate `entity_index_specs.DISPLAY_SPECS`
   exclusively. Each entry hand-declares `key` + `key_col`. Column NAME is
   irrelevant — `FRS_ID`, `MINE_ID`, `FEC_CMTE_ID`, `FEC_CAND_ID` all carry
   EMPTY token sets in the shared tagger and work purely because a human pointed
   at the column. **The ABCD case is already handled here — by hand.**

2. **The auto-discovery graph.** `connect/fingerprint.py` calls
   `keys.detect_key(column_name)` on every column of every landed table, and
   `detect_key` is 100% name-token based (`KEY_TOKENS`, `PAIR_RULES`,
   `EXACT_TOKEN_KEYS`). Verified token lists:
   - `EIN` -> {`ein`} only. `TAX_ID`, `FEIN`, `EMPLOYER_ID`, `ORG_TAX_NUM` are invisible.
   - `NPI` -> {`npi`}. `CIK` -> {`cik`}. `DUNS` -> {`duns`}. `LEI` -> {`lei`}.
     `CCN` -> {`ccn`}. `DEA_NO` -> {`dea`}. All single-token.
   - Only ZIP / FIPS / LATLON / COUNTRY / GEOM / NAME / ADDRESS have real
     synonym lists.
   - `PAIR_RULES` adds 7 two-token rules (postal+code, frs+id, registry+id,
     pws+id, mine+id, cmte+id, cand+id).
   **Nothing anywhere inspects VALUES to infer key type.** Confirmed by reading
   `keys.py`, `fingerprint.py`, `discover.py` end-to-end.

Consequence: the connection count is a **floor**. Missed links, never false
ones — the design is fail-closed. But we cannot say how big the floor's gap is,
because nothing has ever looked.

## Measured universe (queried live today)

- `LIBRARY_RAW.LANDING`: **64,035 columns across 1,871 tables**.
- Portal tables: **51,294 columns** (already excluded from edge generation by
  `EDGE_UNIVERSE_EXCLUDE_PREFIXES`).
- **Non-portal: ~12,741 columns** — the real target.
- 63,963 of 64,035 columns are TEXT/VARCHAR/NUMBER, so type filtering saves
  nothing; shape testing is the filter.
- `LIBRARY_META.REGISTRY.COLUMN_CATALOG` — which already stores sample values
  per column — covers only **25 tables / 751 columns**. It is NOT a free input
  at warehouse scale. (Matches the known "pack tables only" limit.)
- NOTE / unexplained: STATUS.md says 2,216 live raw tables; INFORMATION_SCHEMA
  reports 1,871 base-table rows in LANDING. Difference not chased. Do not treat
  either number as settled until reconciled.

## Design — four stages, each independently killable

**Stage 0 — name-synonym sweep. Cost: ~$0. One metadata query.**
Pull all 12,741 non-portal column names. Match against a hand-written synonym
list per key (`tax_id`/`fein`/`employer_id` -> EIN, `provider_id`/`prov_num` ->
NPI candidate, etc.). Output: ranked list of name-suspicious columns.
Catches the cheapest tier of the ABCD problem with zero compute.
**Critically: this list is NOT merged into `KEY_TOKENS`** (see Blast radius).

**Stage 1 — value-shape sniff. Cost: ~$3–6, ~30–90 min.**
Per table, one aggregate query over a `LIMIT 50,000` subsample, computing per
column: normalized-distinct count, non-null %, and REGEXP hit-rate against each
known key's shape (9 digits after stripping punctuation -> EIN candidate;
10 digits -> NPI; 12 alnum -> UEI; 20 alnum -> LEI; 2 letters + 7 digits ->
DEA/PWSID; etc.). Columns batched ~30 per query -> ~2,500 queries.
Serial on X-Small ≈ 2h; 6 parallel lanes ≈ 25–35 min wall.
Checkpoint + resume to disk after every table (same pattern `fingerprint.py`
already uses — a crash must not restart the bill).
Output: candidate (table, column, suspected key, shape hit-rate).

**Stage 2 — overlap confirmation. Cost: ~$2–5, depends on candidate count.**
Shape alone proves nothing. Every survivor is joined against the LIVE value set
of that key already in the spine, and scored with the EXISTING
`discover.confidence()` collision math using the EXISTING `KEY_DOMAIN` value
spaces. A candidate is only reported if it beats chance by the same
`COLLISION_MULT = 5.0` factor real edges must beat. This is the identical gate
the 41-candidate batch went through.

**Stage 3 — human review, then the normal path. Cost: $0 compute.**
Output is a ranked markdown table for Chris: column, suspected key, live
overlap %, distinct count, five sample values. Approved entries are added to
`DISPLAY_SPECS` by hand — the same route the current 48 staged spec tables took.
No auto-registration, ever.

## Blast radius — what this can and cannot break

Traced every consumer of `detect_key` in the repo (excluding vendored venvs):
`connect/fingerprint.py`, `connect/spine_entity.py`,
`scripts/build_column_catalog.py`. Nothing else.

**Zero-risk by construction, IF these five rules hold:**

1. **Do not touch `KEY_TOKENS` / `PAIR_RULES` / `EXACT_TOKEN_KEYS`.** Adding
   synonyms there silently changes: the graph's key detection, the registry's
   spine-entity classification (`spine_entity.candidate_keys_for_columns`), and
   every `DETECTED_KEY` value in the column dictionary. Wide, silent, and it
   would re-tag existing columns retroactively. The sniffer lives in its own
   module and writes its own report file. `keys.py` is READ, never edited.
2. **Read-only lane.** Stage 1/2 run on the viz read lane. No landing DDL, no
   writes to `LIBRARY_META`. (Landing DDL is classifier-blocked anyway.)
3. **Never auto-add to `DISPLAY_SPECS`.** Auto-registration would change spine
   membership, which changes `ENTITY_MAP`, which is the merge path. Human gate,
   per the fail-closed rule.
4. **Sentinel-aware, per constitution §7.** Every candidate reports
   `COUNT(DISTINCT)` + a five-value sample alongside fill %. A bare non-null
   count is not evidence — that exact mistake produced two false "100%
   populated" readings already (NPPES EIN, AIS IMO). Also test for the `'nan'`
   string sentinel and for zero-padding differences before claiming an overlap.
5. **Shape is a candidate generator, never a verdict.** Nine digits is also an
   SSN, a ZIP+4, a phone number, a dollar amount, and a row sequence. Only the
   Stage-2 live-overlap score is allowed to promote anything.

**Things it genuinely cannot affect:** the spine's current 173 tables, the
entity map, the incremental updater's config fingerprint, the dbt tests, the
marts. It does not write to anything they read.

**Real residual risks:**
- *Warehouse time on a shared X-Small.* Stage 1 competing with an incremental
  run slows both. Run it when nothing else is scheduled.
- *False-positive fatigue.* If Stage 2's floor is set too loose the review list
  becomes hundreds of junk rows and gets ignored. Mitigation: reuse the
  existing MIN_MATCH / COLLISION_MULT thresholds unchanged rather than inventing
  looser ones.
- *A confirmed find costs a spine rebuild to take effect* (~$12–20, ~4.5h).
  Finding keys is cheap; USING them is not. Batch approvals, never one at a time.

## Price tag summary

| Stage | Compute | Wall clock |
|---|---|---|
| 0 — name synonyms | ~$0 | minutes |
| 1 — value-shape sniff (non-portal) | $3–6 | 30–90 min |
| 2 — overlap confirmation | $2–5 | 20–60 min |
| 3 — review + hand-registration | $0 | Chris's time |
| **Total** | **$5–11** | **~1–2.5 h** |

Including portal tables would roughly 5x Stage 1 (51k extra columns, ~$15–30).
Recommend non-portal first; decide on portals after seeing the hit rate.

Estimates are inferred from the 2026-08-17 41-candidate verification (~$1–2)
and the 2026-08-17 census-grid fill (589 marts, 1.23B rows, ~$2). Not measured
for this specific workload.
