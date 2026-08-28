# Edge-Quality Fixes — 2026-08-27

Follow-up to `graph_structure.md` (same folder). Two bugs, both fixed in the
connect-layer code; the live edge tables still hold the old edges until Chris
runs one of the regeneration/prune commands below (writes are his call).

## Bug 1 — DOCKET key namespace collision (FDIC cert# vs court docket#)

**Root cause.** The DOCKET key normalized to a bare `code` value, and 17 landing
tables carry a DOCKET-tagged column: 10 court tables (CourtListener, FJC IDB,
Oyez, SCDB), 2 FDIC tables (whose "docket" column is the FDIC *certificate
number*), and 4 unrelated agency tables (MSHA, NTSB, Federal Register, EIA-860).
Small integers collide across issuers → 3 of 5 STRONG families (~1,300 row
edges) were FDIC-cert × SCOTUS-docket garbage.

**Fix (implemented).** New issuer namespace on the discover/edge lane:

- `connect/keys.py` — added `docket_issuer(table)` (court sources → `COURT`,
  `FED_FDIC*` → `FDIC`, anything else → its publisher prefix, e.g. `FED_MSHA`,
  which isolates it) and `edge_norm_sql(key, col, table, country_col)`, a
  wrapper over `normalize_sql` that prefixes DOCKET keyset values with
  `'<ISSUER>:'`. Cross-issuer values can no longer equi-join; same-issuer
  families (FDIC↔FDIC 7,905 edges; Oyez↔SCDB 22; the 3 STEEL
  FJC↔CourtListener families, ~1.69M edges) all survive because both sides get
  the same prefix.
- `connect/discover.py` `_build_keysets` and `connect/incremental.py`
  `_discover_keyset_inserts` now call `edge_norm_sql` (with the table name)
  instead of `normalize_sql` when building the discover keysets.

**Why `normalize_sql` itself was NOT touched:** the incremental config guard
(`incremental._config_fingerprint`) hashes `normalize_sql`'s output per key;
changing it would freeze `connect-one`/`connect-changed` until the parked full
spine rebuild. `edge_norm_sql` leaves that surface byte-identical (verified:
pass-through for all non-DOCKET/FIPS keys), and DOCKET is not a spine key
(parked in `entity_index_specs.py`), so entities never re-key. Stale-vs-new
keyset values in the incremental lane can only *miss* an edge, never fake one —
the safe direction. The staged 2026-08 key-batch flag was not touched.

## Bug 2 — GEO tier noise (state / country-code "matches")

Full GEO enumeration (both edge tables, samples inspected per family):

| key | verdict | CONNECT_EDGES | CONNECT_EDGES_INC |
|---|---|---|---|
| FIPS, coarse (all sample values ≤3 chars: bare state codes '18'/'54' or state-less county codes '393') | **NOISE — prune** | 197 fams / 11,414 edges | 125 fams / 6,859 edges |
| FIPS, county-level+ (5-char '39083'/'TX273') | legit geo-affiliation — keep | 78 fams / 228,187 edges | 50 fams / 136,494 edges |
| COUNTRY (all families: ISO/spelled country codes) | **NOISE — prune** | 18 fams / 314 edges | 18 fams / 314 edges |
| ZIP | legit geo-affiliation — keep | 8 fams / 2,231 edges | 925 fams / 1,108,038 edges |
| GEO_IN (point-in-polygon) | legit spatial context — keep | 52 fams / 335,480 edges | (n/a in GEO tier there) |

**Fix (implemented).**

- `connect/keys.py` — `GEO_MIN_LEN = {"FIPS": 5}`: `edge_norm_sql` NULLs any
  FIPS value shorter than 5 chars (county-level or finer only; kills both bare
  state codes and state-less county codes at the value level, so mixed-format
  tables keep their real county rows). Also applied inside the NAME@FIPS
  corroborated composite — a name pinned to a bare state code is not
  corroboration.
- `connect/discover.py` — new `CONTEXT_NOISE_KEYS = {"COUNTRY"}` gate in
  `confidence()` (same pattern as the D17 `VOCAB_KEYS` gate): COUNTRY stays
  tagged and in the keyset (it still powers the ZIP country-gate), but never
  becomes an edge. `incremental.py` scores through the same `confidence()`, so
  the gate covers both lanes.

## What Chris must run (writes — not done here)

**Clean path — regenerate the edge tables** (rebuilds keysets for ~450 tables;
same class of sweep as prior discover runs, rough cost $1–3 on the serve/compute
lane, ~15–30 min):

```
python -m connect discover
```

**Or surgical prune of the live tables now** (each a single statement; repeat
the COUNTRY/FIPS ones for `CONNECT_EDGES_INC`):

```sql
DELETE FROM LIBRARY_META."CONNECT".CONNECT_EDGES
WHERE "KEY" = 'DOCKET' AND TIER = 'STRONG'
  AND NOT (A = 'FED_FDIC_BANK_DATA' AND B = 'FED_FDIC_SOD_BRANCH_DEPOSITS')
  AND NOT (A = 'FED_OYEZ' AND B = 'FED_SCDB');
```

```sql
DELETE FROM LIBRARY_META."CONNECT".CONNECT_EDGES
WHERE TIER = 'GEO' AND "KEY" = 'COUNTRY';
```

```sql
DELETE FROM LIBRARY_META."CONNECT".CONNECT_EDGES e
USING (SELECT x.A, x.B
       FROM LIBRARY_META."CONNECT".CONNECT_EDGES x,
            LATERAL FLATTEN(input => PARSE_JSON(x."SAMPLE")) f
       WHERE x.TIER = 'GEO' AND x."KEY" = 'FIPS'
       GROUP BY x.A, x.B
       HAVING MAX(LENGTH(f.value::string)) <= 3) d
WHERE e.TIER = 'GEO' AND e."KEY" = 'FIPS' AND e.A = d.A AND e.B = d.B;
```

(The INC table's only STRONG DOCKET family is the legitimate Oyez↔SCDB one — no
DOCKET delete needed there.)

## Tests

`tests/test_keys_normalize.py`, `test_discover_keyguard.py`,
`test_connect_incremental.py`, `test_spine_map_visibility.py`,
`test_politics_spine_keys.py`: **71 passed, 1 failed** —
`test_incremental_state_matches_full_rebuild_backstop` fails on `noop_spine`
(the LEIE source table's content drifted vs its pinned watermark). **Confirmed
pre-existing**: the identical failure reproduces on the unmodified tree
(`git stash` → rerun → same FAIL). Likely cause: today's fresh LEIE pull
(`scripts/hhs_oig_leie_load.py`, untracked, from the parallel pull-sweep
session) changed the table after the watermark was pinned. Not caused by these
edits; resolved by the next incremental `connect` run picking the table up.
