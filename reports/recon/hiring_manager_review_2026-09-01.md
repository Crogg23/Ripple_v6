# Cynical hiring-manager review — connect + landing layers only
2026-09-01. Two fresh-context reviewers, code read cold, files and lines cited.
UI excluded on Chris's instruction — not started yet.

---

## CONNECT LAYER

**Verdict:** unusually strong domain reasoning and correctness instincts wrapped
in a codebase that has never been refactored — the entity-resolution design is
sound and would survive a hostile review; the engineering hygiene would not.

### Strengths

1. **The normalizer is the work of someone who has been burned.**
   `connect/keys.py:236-247, 608-635, 640-655`. "We PAD, never strip" with the
   Alabama/Puerto-Rico false match cited. EIN `999999999` incident (CVS + SK
   Telecom + "TEST Company" merged) cited inline. `zip5` accepts only lengths
   5 and 9 because `>=5` turned a stripped Boston ZIP+4 into a Pennsylvania
   ZIP5. Every rule states its failure mode and loses an edge rather than
   accuse the wrong company. `normalize_sql` raises on unmapped keys
   (`keys.py:585-586`).

2. **The two-scope reslice is subtle and correct.**
   `connect/incremental.py:668-752`. Membership scoped to `_AFFECTED`
   (symmetric diff old/new); attributes scoped to `_RECOMPUTE` (full slice ∪
   removed) — because a CMS refresh changes names with an identical ID set,
   making `_AFFECTED` empty. Most engineers ship the `_AFFECTED`-only version.
   `_golden_attrs` gate (`:842-871`) closes a real read-skew hole.
   `AFFECTED_SQL` extracted (`:280-283`) so `tests/test_apply_config.py:92-98`
   pins the parentheses after Snowflake MINUS/UNION precedence bit once.

3. **Duplication hunted down and generated.**
   `entity_index_specs.py:2362-2379`, `:40-46`; `keys.py:142-160`.
   `entity_type_sql()` generates the CASE from one dict (was hand-copied into
   four files). `tier_for` added after an EXACT_TOKEN key fell through to
   PROBABILISTIC and mislabelled a 2.3M-match STEEL link.

### Weaknesses

1. **The flagship correctness proof cannot run; docs claim it can.**
   `incremental.validate()` compares against `SPINE_KEYSET` scratch twins
   written only by the retired full rebuild (`incremental.py:1161-1167`,
   `__main__.py:123-127`). Live test is `@pytest.mark.snowflake` plus a
   staleness skip (`tests/test_connect_incremental.py:309, 322-325`).
   Net: the MERGE/keyset logic has ZERO executing coverage, while
   `incremental.py:13-16, :605, :216` still describe the backstop as live.

2. **`if True:` shipped in the config driver.** `incremental.py:514` — dead
   conditional wrapping 65 lines. `_guard_config` (`:244-257`) is named like a
   read-only check but silently mutates the warehouse on drift.

3. **Config baselining monkeypatches two modules' globals at runtime.**
   `incremental.py:327-374` mutates `keys.NORM_RULES`, `TABLE_COLUMN_KEYS`,
   `DISPLAY_SPECS` in place, restores in `finally`. Only strips the
   `2026_08_29` batch (`:334-338`); `ENABLE_SPINE_BATCH_2026_08` never
   stripped — the flags-off baseline is correct for one of two flags.
   Root cause: `DISPLAY_SPECS` built by six scattered import-time `update()`
   calls (`entity_index_specs.py:1372, 1431, 1595, 2170, 2275`).

4. **SQL string interpolation, escaping inconsistent.** `'{tbl}'` raw at
   `incremental.py:649, :866`; `_table_exists` unquoted (`:1271-1274`);
   `db.fqn` (`db.py:72-77`) no quoting or validation on the `--source` path.
   Safe today, but a reviewer must prove it call site by call site.

5. **`_merge_nodes` drops KEY_TYPE scope.** `incremental.py:789-790` deletes
   on TABLE_NAME + KEY_VALUE only; re-INSERT joins on both. A value colliding
   across key types on a two-key table is deleted and not restored. Latent
   today; contradicts `_merge_index`'s own comment (`:806-809`).
   Also: `index_rows` and `leads_restamped` stats overstate work done
   (`:837-839, :960-961`).

### Design caveat worth adopting in all outward claims

"Hard IDs only" holds for the identity layer, not the whole graph.
NAME@ZIP / NAME@FIPS composite keys exist in the discover edge lane
(`incremental.py:1002-1011`), tiered CORROBORATED, never in ENTITY_MAP.
Right containment — but say "no name matching in the identity layer,"
or a reviewer finds the NAME@geo path and assumes it was hidden.

**Hire signal:** interview — judgment is senior-level and rare; probe on why
none of the MERGE logic is testable without a warehouse.

---

## LANDING LAYER

**Verdict:** strong, self-aware ingestion with production scar tissue baked in —
but the safety story is inconsistent: atomicity is real for chunked/staging
loads and entirely absent for the incremental append path, and at least one
advertised guardrail is dead code.

Scale note: `library-onboarding/ripple_dbt` is ~39,363 .sql and ~4,846 .yml
files — generated at scale, not reviewed.

### Strengths

1. **Genuine atomic landing, correctly reasoned.** `loadkit/atomic_load.py:19-57`
   SWAP plan; pins INFORMATION_SCHEMA to the target database with the reason
   written down (`:42-51`). Chunked loader same pattern
   (`library-onboarding/ingest.py:712-719`).

2. **Failure modes encoded as named, cited defenses.** `_reject_html`
   (`ingest.py:824-886`) catches three shapes of HTML-landed-as-data, each tied
   to the source that broke. Density gate (`:435-452`) demotes a 4.1M-row
   all-blank load to 'empty'; `onboard.py:354-357` blocks it from dbt and
   registry. Watermark validate-after-except ordering (`:355-366`) prevents a
   swallowed bad cursor duplicating the whole backfill.

3. **Registry MERGE that refuses to clobber curated data.**
   `register.py:42-57` per-facet match expressions replacing naive COALESCE,
   with the defect it fixes named. Idempotent upsert done properly.

### Weaknesses

1. **CONFIRMED, worse than logged: incremental append = permanent silent data
   loss on crash.** `ingest.py:426` → `_load_landing` bare
   `write_pandas(overwrite=False)` (`:1006-1009`) — multi-file COPY, not
   atomic. The except at `:463-470` logs 'failed' and re-raises with no
   cleanup. Chunked path has resume logic (`:501-520, 1071-1084`); the
   incremental path never consults it. Next run reads MAX(cursor) off the
   half-loaded table (`:1027-1040`), advances past the gap, never backfills.

2. **A documented guardrail is dead code.** `_latest_success_rows`
   (`ingest.py:1053-1068`) — never-shrink floor, SAM-exclusions incident cited
   in the docstring, "callers refuse to overwrite a healthy table."
   No caller exists anywhere in library-onboarding/ or loadkit/.
   Reading cold: the comments cannot be trusted as documentation of behavior.

3. **`exec()` of LLM-generated Python is the ingestion engine.**
   `ingest.py:786`, guarded by foreman approval only (`:777-778`).
   `_safe_env` (`:54`) strips platform creds — thoughtful — but no sandbox, no
   subprocess, no resource cap. Correctness lives in a prompt
   (`prompts/generate_ingest.txt:50-115`). Defensible solo; blocker in a
   regulated shop.

4. **The zip largest-member trap: diagnosed, written down, never fixed, still
   being copied.** `scripts/issue_batch_load.py:101-105` max-by-size;
   `nobrainer_bulk_load_2026_08_29.py:283`; `bridge_fuel_load.py:253-254`;
   sort-take-first variants at `cftc_cot_history_load.py:114`,
   `dol_enforce_bulk_load.py:147`, `osha_ita_bulk_load.py:164`. Same file picks
   the biggest Excel sheet (`issue_batch_load.py:118`). The author's own recon
   (`recon_bulk_load_2026-08-07.py:569,578,605`) documents EIA-860/861 zips
   bundling 13-20 files where the heuristic picks wrong.

5. **Broad `except: pass` around things that matter; loader sprawl.**
   `_enrich` swallows all (`register.py:209-210`); `_watermark` returns None on
   any exception (`ingest.py:1039-1040`) — hides a permissions error, triggers
   full re-backfill append; `_apply_session_guards` swallows (`snow.py:128-129`)
   so the cost guard can be silently off. Dozens of near-identical hand-written
   loaders in scripts/ that don't import loadkit.

**Hire signal:** interview — has been burned by real data and writes it down;
probe on turning hard-won knowledge into enforced invariants, not comments.

---

## Combined read

Both reviewers landed on the same person: senior judgment, junior enforcement.
The knowledge is real and written down; the machine doesn't enforce it.
The recurring shape: a lesson becomes a comment, not an invariant.

Highest-severity fix list, in order:

1. Incremental append crash = silent permanent data loss (landing W1)
2. Wire or delete `_latest_success_rows` — dead guardrail (landing W2)
3. Fix or centralize the zip member heuristic — 6+ live copies (landing W4)
4. Give the MERGE logic runnable coverage without a warehouse (connect W1)
5. `_merge_nodes` KEY_TYPE scope — latent cross-key delete (connect W5)
