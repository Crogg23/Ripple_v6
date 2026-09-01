"""Incremental CONNECT — O(changed tables), not O(all 762).

The full rebuild (`connect all`) re-scans every landing table, CREATE-OR-REPLACEs a
38.3M-row keyset, self-joins it, and CREATE-OR-REPLACEs the 9.79M-row spine —
every run, regardless of what actually changed. On a ~30 credit/mo cap that's the
#1 cost hog. This module makes the spine update *proportional to what moved*:

    a source's data changes  ->  its INGEST_RUNS content-key changes
    ->  re-derive keys for ONLY that landing table
    ->  diff old-slice vs new-slice = the affected (key_type, value) set
    ->  MERGE just those entities into the live spine (never a full rebuild)

ADDITIVE BY CONSTRUCTION — but the old full rebuild is RETIRED (in the junk
drawer, zero importers, verified 2026-08-31). There is NO live reconciliation
backstop: validate() below needs the retired rebuild's transient scratch twins
and cannot run against a warehouse that no longer has them. This module writes
NEW persisted tables
(CONNECT_WATERMARK, SPINE_KEYSET_LIVE, KEYSET_LIVE, CONNECT_EDGES_INC) and MERGEs
into the SAME live tables the old rebuild once built (ENTITY_MAP / ENTITY_GOLDEN /
CONNECT_NODES / MATCH_PAIRS / ENTITY_INDEX). Because every id is content-addressed
(ENTITY_ID = 'ENT_'||LEFT(MD5(key_type|val),16)), a MERGE upsert renumbers no one —
incremental and full-rebuild converge on byte-identical rows.

The four correctness seams (all handled below, see the section banners):
  1 DELETION   per-table DELETE-then-INSERT on the persisted keyset + scoped
               DELETEs on map/golden/index so a vanished key actually retracts.
  2 MULTI-FILE the change signal is a per-SOURCE_ID digest over ALL success/empty
               INGEST_RUNS rows (LISTAGG of STATUS:SHA), never a single run SHA.
  3 MERGE SCOPE membership (keyset/map/nodes/pairs) + retraction recompute only for
               the symmetric difference of the table's old vs new key slice; ATTRIBUTE
               recompute (golden name/addr + index label/row_count/preview) covers the
               changed table's FULL current key slice, so an attribute-only refresh
               (same ids, new names — the common CMS-quarterly case, where the symmetric
               diff is empty) still converges on the full rebuild. Both stay O(one table).
  4 BOUNDED    the on-land self-join carries resolve.py's PAIR_BUDGET + a fan-out
               cap; high-tier (STEEL/STRONG) edges are never silently dropped.

CLI (also dispatched from `python -m connect ...` — see __main__.py edit spec):
    python -m connect.incremental seed                 # one-time: init state tables
    python -m connect.incremental connect-changed      # catch up the spine (the heartbeat)
    python -m connect.incremental connect-one --source fed_cms_nppes
    python -m connect.incremental validate             # non-destructive equivalence proof
"""

from __future__ import annotations

import os
import argparse
import hashlib
import sys
import uuid

from . import db, store
from .discover import (
    CONNECT_DB,
    CONNECT_SCHEMA,
    MIN_MATCH,
    NAME_MAX_ROWS,
    PROBABILISTIC,
    _best_value_col,
    _tier,
    confidence,
    domain_of,
    validate_key_config,
)
from .entity_index_specs import DISPLAY_SPECS, table_keys
from .entity_index_specs import entity_type_sql as _entity_type_sql_shared
from .keys import NORM_RULES, edge_norm_sql, normalize_sql, quote_ident
from .normalize import _addr_expr, _name_expr  # one definition of name/addr, shared

# --- persisted state (all NEW, all additive) -------------------------------- #
WATERMARK_FQN = store.cfqn("CONNECT_WATERMARK")     # per-table change signal
SKEYSET_FQN = store.cfqn("SPINE_KEYSET_LIVE")       # durable twin of SPINE_KEYSET (15 spec tables)
KEYSET_FQN = store.cfqn("KEYSET_LIVE")              # durable twin of KEYSET_SCRATCH (all 762 tables)
EDGES_FQN = store.cfqn("CONNECT_EDGES_INC")         # on-land discover edges (queryable immediately)

# --- the live spine tables we MERGE into (same names the backstop rebuilds) -- #
EMAP_FQN = store.cfqn("ENTITY_MAP")
GOLD_FQN = store.cfqn("ENTITY_GOLDEN")
NODES_FQN = store.cfqn("CONNECT_NODES")
PAIRS_FQN = store.cfqn("MATCH_PAIRS")
INDEX_FQN = store.cfqn("ENTITY_INDEX")
LEADS_FQN = store.cfqn("LEADS")

# --- the transient backstop keysets we seed FROM (read-only) ---------------- #
TRANSIENT_SPINE_FQN = store.cfqn("SPINE_KEYSET")
TRANSIENT_DISCOVER_FQN = store.cfqn("KEYSET_SCRATCH")

# --- bounded blocking (seam #4) --------------------------------------------- #
PAIR_BUDGET = 100_000   # carried from resolve.py:48 — cap the on-land self-join
FANOUT_MAX = 40         # one value touching > this many tables is logged (+ capped for soft tiers)

CONFIG_SENTINEL = "__CONFIG__"   # WATERMARK row that pins keys.py/DISPLAY_SPECS config

# compute_watermarks() scans all of INGEST_RUNS (LISTAGG+MD5 GROUP BY). It is called
# many times per run (changed_tables, every reslice tail). INGEST_RUNS is read-only
# while we reslice, so memoize the result per connection for the life of one driver.
# Keyed on id(conn) and CLEARED at every driver entry (_reset_caches) so a reused id()
# can never surface a previous run's watermarks.
_WM_MEMO: dict[int, dict[str, dict]] = {}


def _reset_caches() -> None:
    _WM_MEMO.clear()


# =========================================================================== #
# DDL — the new persisted state (CREATE TABLE IF NOT EXISTS, idempotent)
# =========================================================================== #
def _ddl(conn) -> None:
    store.ensure_schema(conn)
    # A fresh connection has a default DATABASE but no default SCHEMA (verified live:
    # CURRENT_SCHEMA() = NULL), so every bare (unqualified) CREATE TEMPORARY TABLE
    # below and in reslice_spine/validate -- _NEW, _OLD, _AFFECTED, _VKEYS, etc. --
    # fails with "session does not have a current schema". Pin one.
    db.rows(conn, f'USE SCHEMA "{CONNECT_DB}"."{CONNECT_SCHEMA}"')
    db.rows(conn, f"""
        CREATE TABLE IF NOT EXISTS {WATERMARK_FQN} (
            TABLE_NAME        STRING NOT NULL,   -- UPPER(source_id) == landing table; PK by convention
            SOURCE_ID         STRING,
            CONTENT_KEY       STRING,            -- MD5 over the source's STATUS:SHA run-log (seam #2)
            LAST_CHANGE_AT    TIMESTAMP_NTZ,     -- MAX(ENDED_AT) over success+empty (seam #1 high-water)
            N_SUCCESS         NUMBER,
            KEYSET_DERIVED_AT TIMESTAMP_NTZ,     -- when this table's keyset slice was last re-derived
            BUILT_AT          TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )""")
    db.rows(conn, f"""
        CREATE TABLE IF NOT EXISTS {SKEYSET_FQN} (
            TABLE_NAME STRING, KEY_TYPE STRING, VAL STRING
        ) CLUSTER BY (TABLE_NAME)""")
    db.rows(conn, f"""
        CREATE TABLE IF NOT EXISTS {KEYSET_FQN} (
            TABLE_NAME STRING, KEY STRING, VAL STRING
        ) CLUSTER BY (TABLE_NAME)""")
    db.rows(conn, f"""
        CREATE TABLE IF NOT EXISTS {EDGES_FQN} (
            A STRING, B STRING, KEY STRING, TIER STRING,
            MATCHED NUMBER, A_DISTINCT NUMBER, B_DISTINCT NUMBER,
            MATCH_RATE FLOAT, CONFIDENCE FLOAT, "SAMPLE" VARIANT,
            RUN_ID STRING, BUILT_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )""")   # "SAMPLE" is a Snowflake reserved word (TABLESAMPLE clause) -> must be quoted as an identifier


# =========================================================================== #
# SEAM #2 — the multi-file watermark: collapse the per-RUN log to one row/table
# =========================================================================== #
# INGEST_RUNS is per-RUN, not per-table: a source landed as N files has N success
# rows with N SHAs all pointing at ONE landing table (storm_events=31, ais=8).
# A single SHA is therefore the WRONG signal. The content key is a digest over the
# WHOLE ordered run-log for the source. We include STATUS='empty' (and put STATUS
# in the digest) so a success->empty table-mutation also flips the key -> the
# re-derive then reads the now-empty landing table and correctly RETRACTS its keys.
def compute_watermarks(conn, *, refresh: bool = False) -> dict[str, dict]:
    """{ UPPER(source_id): {source_id, content_key, last_change_at, n_success} }.

    Memoized per connection within a single driver run (see _WM_MEMO) so the
    INGEST_RUNS digest is scanned once, not once per changed table."""
    cid = id(conn)
    if not refresh and cid in _WM_MEMO:
        return _WM_MEMO[cid]
    rows = db.dicts(conn, """
        SELECT UPPER(SOURCE_ID) AS TABLE_NAME,
               MIN(SOURCE_ID)   AS SOURCE_ID,
               MD5(LISTAGG(STATUS || ':' || COALESCE(SHA256, ''), '|')
                     WITHIN GROUP (ORDER BY ENDED_AT, RUN_ID)) AS CONTENT_KEY,
               MAX(ENDED_AT)    AS LAST_CHANGE_AT,
               SUM(IFF(STATUS = 'success', 1, 0)) AS N_SUCCESS
        FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
        WHERE STATUS IN ('success', 'empty')
        GROUP BY 1
    """)
    out = {r["TABLE_NAME"]: {
        "source_id": r["SOURCE_ID"], "content_key": r["CONTENT_KEY"],
        "last_change_at": r["LAST_CHANGE_AT"], "n_success": int(r["N_SUCCESS"] or 0),
    } for r in rows}
    _WM_MEMO[cid] = out
    return out


def _stored_keys(conn) -> dict[str, str]:
    rows = db.dicts(conn, f"SELECT TABLE_NAME, CONTENT_KEY FROM {WATERMARK_FQN} "
                          f"WHERE TABLE_NAME <> '{CONFIG_SENTINEL}'")
    return {r["TABLE_NAME"]: r["CONTENT_KEY"] for r in rows}


def changed_tables(conn, scope: str = "spine") -> list[str]:
    """Tables whose content-key moved since the last connect. scope='spine' limits
    to the 15 DISPLAY_SPECS tables (the persisted moat); 'all' covers every table.

    Filtered to source_ids that ACTUALLY have a LIBRARY_RAW.LANDING table: ~31
    portal-harvest source_ids log success/empty in INGEST_RUNS but never materialize a
    landing table, and reslicing one would read a non-existent table mid-run."""
    wm = compute_watermarks(conn)
    stored = _stored_keys(conn)
    exists = _landing_tables(conn)
    universe = list(DISPLAY_SPECS) if scope == "spine" else sorted(wm)
    return [t for t in universe
            if t in wm and t in exists and wm[t]["content_key"] != stored.get(t)]


def _upsert_watermark(conn, table: str, wm: dict) -> None:
    db.rows(conn, f"""
        MERGE INTO {WATERMARK_FQN} t
        USING (SELECT %s AS TABLE_NAME) s ON t.TABLE_NAME = s.TABLE_NAME
        WHEN MATCHED THEN UPDATE SET
            SOURCE_ID = %s, CONTENT_KEY = %s, LAST_CHANGE_AT = %s,
            N_SUCCESS = %s, KEYSET_DERIVED_AT = CURRENT_TIMESTAMP(), BUILT_AT = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN INSERT
            (TABLE_NAME, SOURCE_ID, CONTENT_KEY, LAST_CHANGE_AT, N_SUCCESS, KEYSET_DERIVED_AT, BUILT_AT)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())
    """, (table,
          wm.get("source_id"), wm.get("content_key"), wm.get("last_change_at"), wm.get("n_success"),
          table, wm.get("source_id"), wm.get("content_key"), wm.get("last_change_at"), wm.get("n_success")))


# =========================================================================== #
# CONFIG GUARD — a NORM_RULES / DISPLAY_SPECS edit silently re-keys entities, so
# an incremental MERGE would create duplicates/orphans. Pin the config; refuse to
# run incrementally when it drifts (no incremental path; the retired full rebuild covered this).
# =========================================================================== #
def _config_fingerprint() -> str:
    """A digest over the ENTITY re-keying + survivorship surface. ENTITY_ID =
    hash(key_type | normalize_sql(key, col)), so a silent change to ANY of:
      (a) the NORM_RULES table,
      (b) the normalize_sql IMPLEMENTATION — the _name_canon noise list, the
          _addr_canon abbreviations, the pad/imo/fixed/code branch logic — even when
          the NORM_RULES dict is untouched,
      (c) a table's (key, key_col), or the survivorship spec (org/person/city/
          authority) that feeds golden+index,
    would re-key or re-attribute entities and make an incremental MERGE produce
    duplicates/orphans. (a)+(c) are dict reprs; (b) is captured by hashing the ACTUAL
    normalize_sql output for each key against a fixed placeholder column — so an edit
    to keys.py that changes the emitted SQL trips the guard and forces a full rebuild."""
    norm_surface = []
    for k in sorted(NORM_RULES):
        try:
            norm_surface.append((k, normalize_sql(k, '"__CFG__"')))
        except Exception as exc:   # a half-added key: fold the failure into the print
            norm_surface.append((k, f"ERR:{type(exc).__name__}"))
    blob = "||".join((
        repr(sorted(NORM_RULES.items())),
        repr(norm_surface),
        repr(sorted(DISPLAY_SPECS.items())),
    ))
    return hashlib.md5(blob.encode("utf-8")).hexdigest()


def _apply_config_drift_or_raise(conn) -> None:
    """NOT read-only (renamed from _guard_config, which sounded like a check):
    on drift with per-unit pins present this MUTATES the warehouse -- it runs
    the bounded apply (reslices + re-pins) before continuing. The legacy
    whole-config sentinel check below only bites when there are no per-unit
    pins yet, and that path raises instead of mutating."""
    if _config_drifted(conn):
        # GATED (2026-09-01): auto-applying here reshapes warehouse tables and
        # spends credits without a price shown -- a big staged batch drifting
        # in silently was the risk. Explicit `apply-config` stays ungated;
        # this implicit path refuses unless the env flag says go.
        if os.getenv("RIPPLE_APPLY_CONFIG", "").strip().lower() in ("1", "true", "yes", "on"):
            print("config drift detected -> applying bounded config change first "
                  "(RIPPLE_APPLY_CONFIG=1)")
            _apply_config_conn(conn, dry_run=False)
        else:
            raise RuntimeError(
                "config drift detected. Refusing to auto-reslice mid-run: preview with "
                "`python -m connect apply-config --dry-run`, price it, then either run "
                "`python -m connect apply-config` or set RIPPLE_APPLY_CONFIG=1.")
    stored = db.scalar(conn, f"SELECT CONTENT_KEY FROM {WATERMARK_FQN} "
                            f"WHERE TABLE_NAME = '{CONFIG_SENTINEL}'")
    if stored is not None and stored != _config_fingerprint():
        raise RuntimeError(
            "keys.py NORM_RULES / TABLE_COLUMN_KEYS / DISPLAY_SPECS changed since the last "
            "pin. Run `python -m connect apply-config` (bounded: reslices only the tables the "
            "change touches, then re-pins) -- no full rebuild is required.")


# =========================================================================== #
# CONFIG DRIFT AS A BOUNDED CHANGE (2026-08-29) -- the end of the "every new key
# needs a full rebuild" rule.
#
# The old guard hashed the WHOLE config and, on any drift, refused to run until a
# full rebuild. That was blunt: ENTITY_ID = hash(key_type | normalized value), so a
# NEW key family, a NEW spec table, or a NEW extra_keys column never re-keys an
# existing entity -- it only adds (key_type, value) rows, exactly what
# reslice_spine already handles per table (its _OLD/_NEW symmetric difference
# retracts what a config change removes and inserts what it adds, and its golden/
# index recompute re-derives the touched entities from every member table). Even a
# changed normalizer for an EXISTING family is bounded: reslice every table that
# carries the family and the old values retract while the new ones insert.
#
# So the config is now pinned PER UNIT (one row per norm rule, per table spec, per
# table's scoped graph keys). On drift, classify_config_drift() diffs the units and
# names the tables to touch; apply_config() reslices exactly those and re-pins. The
# full rebuild remains the backstop (validate() proves equivalence), never the
# ritual.
# =========================================================================== #
AFFECTED_SQL = """CREATE OR REPLACE TEMPORARY TABLE _AFFECTED AS
    (SELECT KEY_TYPE, VAL FROM _NEW MINUS SELECT KEY_TYPE, VAL FROM _OLD)
    UNION
    (SELECT KEY_TYPE, VAL FROM _OLD MINUS SELECT KEY_TYPE, VAL FROM _NEW)"""

PIN_FQN = store.cfqn("CONNECT_CONFIG_PIN")
_UNIT_NORM, _UNIT_SPEC, _UNIT_TCK = "norm", "spec", "tck"


def _ddl_pins(conn) -> None:
    db.rows(conn, f"""
        CREATE TABLE IF NOT EXISTS {PIN_FQN} (
            UNIT_KIND  STRING NOT NULL,   -- norm | spec | tck
            UNIT_NAME  STRING NOT NULL,   -- key family | spec table | landing table
            DIGEST     STRING NOT NULL,
            DETAIL     STRING,            -- the repr the digest was taken over (for diff prints)
            PINNED_AT  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )""")


def _config_units() -> dict[tuple[str, str], str]:
    """The current config as {(kind, name): detail}. Digest = MD5(detail).

    norm : the ACTUAL emitted SQL per key (catches an implementation edit, not just
           a NORM_RULES dict edit -- same reasoning as _config_fingerprint).
    spec : the DISPLAY_SPECS entry (key, key_col, extra_keys, survivorship).
    tck  : the table-scoped graph keys (keys.TABLE_COLUMN_KEYS) grouped by table --
           a new scoped key on a NON-spec table needs a discover reslice, not a
           spine one.
    """
    from .keys import TABLE_COLUMN_KEYS
    units: dict[tuple[str, str], str] = {}
    for k in sorted(NORM_RULES):
        try:
            units[(_UNIT_NORM, k)] = normalize_sql(k, '"__CFG__"')
        except Exception as exc:
            units[(_UNIT_NORM, k)] = f"ERR:{type(exc).__name__}"
    for t, spec in DISPLAY_SPECS.items():
        units[(_UNIT_SPEC, t)] = repr(sorted(spec.items(), key=lambda kv: kv[0]))
    by_table: dict[str, list] = {}
    for (t, col), (key, tier) in TABLE_COLUMN_KEYS.items():
        by_table.setdefault(t, []).append((col, key, tier))
    for t, cols in by_table.items():
        units[(_UNIT_TCK, t)] = repr(sorted(cols))
    return units


def _baseline_units_and_fingerprint():
    """Config units + legacy fingerprint with every staged batch flag OFF, computed
    by temporarily removing the staged dict entries and restoring them. Returns
    (None, None) when no staged batch is on (nothing to strip)."""
    from . import keys as K
    from . import entity_index_specs as S
    staged = []
    # BOTH staged batches strip, or the flags-off baseline is a half-truth:
    # the 2026-08 batch was forgotten here and the baseline was only correct
    # for one of two flags (hiring review, connect W3).
    if getattr(K, "ENABLE_SPINE_BATCH_2026_08", False):
        staged.append(("2026_08", K._SPINE_BATCH_NORM_RULES, {},
                       {**S.COURTLISTENER_DISPLAY_SPECS,
                        **S.SPINE_BATCH_2026_08_DISPLAY_SPECS},
                       {}))
    if getattr(K, "ENABLE_SPINE_BATCH_2026_08_29", False):
        staged.append(("2026_08_29", K._BATCH_2026_08_29_NORM_RULES,
                       K._BATCH_2026_08_29_TABLE_COLUMN_KEYS,
                       S.SPINE_BATCH_2026_08_29_DISPLAY_SPECS,
                       S._SPINE_BATCH_2026_08_29_EXTRA_KEYS))
    if not staged:
        return None, None
    saved_norm = dict(K.NORM_RULES)
    saved_tck = dict(K.TABLE_COLUMN_KEYS)
    saved_specs = {t: dict(sp, extra_keys=list(sp.get("extra_keys", [])))
                   for t, sp in S.DISPLAY_SPECS.items()}
    try:
        for _name, norms, tck, specs, extras in staged:
            for k in norms:
                K.NORM_RULES.pop(k, None)
            for tc in tck:
                K.TABLE_COLUMN_KEYS.pop(tc, None)
            for t in specs:
                S.DISPLAY_SPECS.pop(t, None)
            for t, ex in extras.items():
                sp = S.DISPLAY_SPECS.get(t)
                if sp is None:
                    continue
                drop = {(e["key"], e["key_col"]) for e in ex}
                kept = [e for e in sp.get("extra_keys", []) if (e["key"], e["key_col"]) not in drop]
                if kept:
                    sp["extra_keys"] = kept
                else:
                    sp.pop("extra_keys", None)
        # DISPLAY_SPECS / NORM_RULES here are the same dict objects this module
        # imported, so the legacy fingerprint sees the stripped state too.
        return _config_units(), _config_fingerprint()
    finally:
        K.NORM_RULES.clear(); K.NORM_RULES.update(saved_norm)
        K.TABLE_COLUMN_KEYS.clear(); K.TABLE_COLUMN_KEYS.update(saved_tck)
        S.DISPLAY_SPECS.clear()
        for t, sp in saved_specs.items():
            if not sp.get("extra_keys"):
                sp.pop("extra_keys", None)
            S.DISPLAY_SPECS[t] = sp


def _digest(detail: str) -> str:
    return hashlib.md5(detail.encode("utf-8")).hexdigest()


def _stored_pins(conn) -> dict[tuple[str, str], str]:
    rows = db.dicts(conn, f"SELECT UNIT_KIND, UNIT_NAME, DIGEST FROM {PIN_FQN}")
    return {(r["UNIT_KIND"], r["UNIT_NAME"]): r["DIGEST"] for r in rows}


def _pin_units(conn, units: dict[tuple[str, str], str] | None = None) -> int:
    """Overwrite the pin table with the CURRENT config (called after a full rebuild,
    a seed, or a successful apply_config)."""
    units = units if units is not None else _config_units()
    _ddl_pins(conn)
    db.rows(conn, f"TRUNCATE TABLE {PIN_FQN}")
    rows = [(k, n, _digest(d), d[:4000]) for (k, n), d in units.items()]
    cur = conn.cursor()
    try:
        cur.executemany(
            f"INSERT INTO {PIN_FQN} (UNIT_KIND, UNIT_NAME, DIGEST, DETAIL) VALUES (%s, %s, %s, %s)",
            rows)
    finally:
        cur.close()
    return len(rows)


def _tables_carrying(key: str, specs: dict | None = None) -> set[str]:
    specs = DISPLAY_SPECS if specs is None else specs
    return {t for t, s in specs.items() if any(k == key for k, _ in table_keys(s))}


def classify_config_drift(stored: dict[tuple[str, str], str],
                          current: dict[tuple[str, str], str],
                          specs: dict | None = None) -> dict:
    """Diff pinned vs current config units and name the bounded work.

    Returns {
      'changes':  [(kind, name, 'added'|'changed'|'removed'), ...],
      'reslice':  sorted spec tables to reslice_spine (additive OR re-normalized),
      'retract':  sorted tables whose spec was removed (their slice is retracted),
      'discover': sorted non-spec landing tables whose scoped graph keys moved,
    }
    Pure function (no warehouse) so the classification is unit-testable.
    """
    specs = DISPLAY_SPECS if specs is None else specs
    cur_d = {u: _digest(d) for u, d in current.items()}
    changes: list[tuple[str, str, str]] = []
    reslice: set[str] = set()
    retract: set[str] = set()
    discover: set[str] = set()
    for unit in sorted(set(stored) | set(cur_d)):
        kind, name = unit
        if unit not in stored:
            how = "added"
        elif unit not in cur_d:
            how = "removed"
        elif stored[unit] != cur_d[unit]:
            how = "changed"
        else:
            continue
        changes.append((kind, name, how))
        if kind == _UNIT_NORM:
            # new family: only its spec tables (their _OLD slice lacks it);
            # changed family: every table carrying it (old values retract, new insert);
            # removed family: its former tables show up as spec changes/removals.
            reslice |= _tables_carrying(name, specs)
        elif kind == _UNIT_SPEC:
            if how == "removed":
                retract.add(name)
            else:
                reslice.add(name)
        elif kind == _UNIT_TCK:
            if name in specs:
                reslice.add(name)      # reslice_spine refreshes the discover partition too
            else:
                discover.add(name)
    return {"changes": changes, "reslice": sorted(reslice - retract),
            "retract": sorted(retract), "discover": sorted(discover - reslice)}


def retract_spine_table(conn, table: str, run_id: str) -> dict:
    """Remove a table that LEFT DISPLAY_SPECS: its persisted slice is retracted, the
    entities it alone carried are deleted, shared entities are re-derived from their
    remaining members. Mirrors reslice_spine with an empty _NEW."""
    lit = table.replace("'", "''")
    db.rows(conn, f"CREATE OR REPLACE TEMPORARY TABLE _OLD AS "
                  f"SELECT KEY_TYPE, VAL FROM {SKEYSET_FQN} WHERE TABLE_NAME = '{lit}'")
    db.rows(conn, "CREATE OR REPLACE TEMPORARY TABLE _NEW AS SELECT * FROM _OLD WHERE 1 = 0")
    db.rows(conn, "CREATE OR REPLACE TEMPORARY TABLE _AFFECTED AS SELECT KEY_TYPE, VAL FROM _OLD")
    db.rows(conn, "CREATE OR REPLACE TEMPORARY TABLE _RECOMPUTE AS SELECT KEY_TYPE, VAL FROM _OLD")
    n_old = int(db.scalar(conn, "SELECT COUNT(*) FROM _OLD") or 0)
    db.rows(conn, f"CREATE OR REPLACE TEMPORARY TABLE _AFFENT AS "
                  f"SELECT DISTINCT {_entity_id_sql('KEY_TYPE', 'VAL')} AS ENTITY_ID FROM _AFFECTED")
    db.rows(conn, f"DELETE FROM {SKEYSET_FQN} WHERE TABLE_NAME = '{lit}'")
    db.rows(conn, f"DELETE FROM {INDEX_FQN} WHERE SOURCE_TABLE = '{lit}'")
    # Drop the watermark too (2026-08-31 skeptic): a surviving content-key makes
    # any future re-wiring of this table a silent no-op — connect_one sees
    # "unchanged" and never reslices, the exact stranded-table bug of this date.
    db.rows(conn, f"DELETE FROM {WATERMARK_FQN} WHERE TABLE_NAME = '{lit}'")
    stats = {"table": table, "old_keys": n_old, "mode": "retracted"}
    stats.update(_merge_entity_map(conn, run_id))
    db.rows(conn, f"DELETE FROM {NODES_FQN} WHERE TABLE_NAME = '{lit}'")
    db.rows(conn, f"DELETE FROM {PAIRS_FQN} WHERE TABLE_A = '{lit}' OR TABLE_B = '{lit}'")
    stats.update(_merge_golden(conn, run_id, "_RECOMPUTE"))
    return stats


def apply_config(dry_run: bool = False) -> dict:
    """Bring the live spine/graph up to the CURRENT code config with bounded work.

    1. diff pinned units vs current -> classify (pure)
    2. reslice_spine each touched spec table; retract removed ones; reslice_discover
       non-spec tables whose scoped graph keys moved
    3. re-pin units + the legacy sentinel
    First run (no pins yet): pins the current config IF the legacy sentinel matches
    (state is coherent) and does nothing else; otherwise refuses -- the operator
    must decide whether the live spine matches the code (seed) or not (rebuild).
    """
    conn = db.connect()
    try:
        _reset_caches()
        validate_key_config()
        _ddl(conn)
        return _apply_config_conn(conn, dry_run=dry_run)
    finally:
        conn.close()


def _config_drifted(conn) -> bool:
    _ddl_pins(conn)
    stored = _stored_pins(conn)
    if not stored:
        return False   # never pinned per-unit: the legacy sentinel guard decides
    return bool(classify_config_drift(stored, _config_units())["changes"])


def _apply_config_conn(conn, dry_run: bool = False) -> dict:
    run_id = uuid.uuid4().hex[:16]
    _ddl_pins(conn)
    current = _config_units()
    stored = _stored_pins(conn)
    if not stored:
        sentinel = db.scalar(conn, f"SELECT CONTENT_KEY FROM {WATERMARK_FQN} "
                                   f"WHERE TABLE_NAME = '{CONFIG_SENTINEL}'")
        if sentinel == _config_fingerprint():
            n = _pin_units(conn, current)
            return {"mode": "pinned-initial", "units": n}
        # The live spine was pinned by a rebuild that ran with the staged batch
        # flags OFF. If the flags-off config reproduces the sentinel, that IS the
        # baseline: pin it, then fall through and apply the flagged batch as an
        # ordinary bounded drift -- one command, no rebuild.
        base_units, base_fp = _baseline_units_and_fingerprint()
        if base_units is not None and sentinel == base_fp:
            _pin_units(conn, base_units)
            stored = _stored_pins(conn)
            print("apply-config: pinned the flags-off baseline (matches the live sentinel); "
                  "applying the staged batch as bounded drift")
        else:
            raise RuntimeError(
                "no per-unit pins yet AND the legacy config sentinel matches neither the "
                "current code nor the flags-off baseline, so the live spine's config is "
                "unknown. Either check out the code the last rebuild ran with and "
                "`apply-config` once to pin it, the retired full-rebuild backstop is gone.")
    plan = classify_config_drift(stored, current)
    plan["mode"] = "preview" if dry_run else "applied"
    print(f"apply-config: {len(plan['changes'])} config change(s) -> "
          f"reslice {len(plan['reslice'])}, retract {len(plan['retract'])}, "
          f"discover {len(plan['discover'])} table(s)")
    for kind, name, how in plan["changes"]:
        print(f"  [{kind}] {name}: {how}")
    if not plan["changes"]:
        return plan
    exists = _landing_tables(conn)
    results = []
    for t in plan["reslice"]:
        if t not in exists:
            results.append({"table": t, "mode": "skip (no landing table)"})
            continue
        r = reslice_spine(conn, t, run_id, dry_run=dry_run)
        print(f"  reslice {t}: {r.get('mode')} affected={r.get('affected'):,}")
        results.append(r)
    for t in plan["retract"]:
        if dry_run:
            results.append({"table": t, "mode": "preview-retract"})
            continue
        r = retract_spine_table(conn, t, run_id)
        print(f"  retract {t}: {r}")
        results.append(r)
    for t in plan["discover"]:
        if t not in exists:
            results.append({"table": t, "mode": "skip (no landing table)"})
            continue
        r = reslice_discover(conn, t, run_id, dry_run=dry_run)
        if not dry_run:
            _upsert_watermark(conn, t, compute_watermarks(conn).get(t, {}))
        print(f"  discover {t}: {r.get('mode')}")
        results.append(r)
    plan["results"] = results
    if not dry_run:
        _pin_units(conn, current)
        _upsert_watermark(conn, CONFIG_SENTINEL,
                          {"source_id": None, "content_key": _config_fingerprint(),
                           "last_change_at": None, "n_success": 0})
    return plan


# =========================================================================== #
# SEED — one-time init. Copies the EXISTING transient backstop keysets into the
# persisted twins (a metadata-cheap copy of already-materialized data, NOT a
# rebuild) and pins every table's current content-key. After seeding, incremental
# == the live full-rebuild by construction, so the first connect run is a no-op.
# =========================================================================== #
def seed(reseed: bool = False) -> dict:
    conn = db.connect()
    try:
        validate_key_config()
        _ddl(conn)
        out = sync_after_rebuild(conn, reseed=reseed)
    finally:
        conn.close()
    print(f"seed: SPINE_KEYSET_LIVE={out['spine_keyset']:,}  KEYSET_LIVE={out['discover_keyset']:,}  "
          f"watermarks={out['watermarks']:,} pinned")
    return out


def sync_after_rebuild(conn, reseed: bool = True) -> dict:
    """Make the persisted twins + watermark agree with the last rebuild output.
    The full rebuild is RETIRED: its transient tables only exist if a pre-drawer
    run left them behind; otherwise the twins are derived fresh from landing."""
    _reset_caches()
    _ddl(conn)
    # Persisted spine keyset twin <- transient SPINE_KEYSET (the last full-rebuild result).
    sk = int(db.scalar(conn, f"SELECT COUNT(*) FROM {SKEYSET_FQN}") or 0)
    src = int(db.scalar(conn, f"SELECT COUNT(*) FROM {TRANSIENT_SPINE_FQN}") or 0)
    if reseed or sk == 0:
        if src > 0:
            db.rows(conn, f"TRUNCATE TABLE {SKEYSET_FQN}")
            db.rows(conn, f"INSERT INTO {SKEYSET_FQN} (TABLE_NAME, KEY_TYPE, VAL) "
                          f"SELECT TABLE_NAME, KEY_TYPE, VAL FROM {TRANSIENT_SPINE_FQN}")
        else:
            _rebuild_spine_keyset_from_landing(conn)   # backstop transient is gone -> derive fresh
    # Persisted discover keyset twin <- transient KEYSET_SCRATCH.
    dk = int(db.scalar(conn, f"SELECT COUNT(*) FROM {KEYSET_FQN}") or 0)
    dsrc = int(db.scalar(conn, f"SELECT COUNT(*) FROM {TRANSIENT_DISCOVER_FQN}") or 0)
    if (reseed or dk == 0) and dsrc > 0:
        db.rows(conn, f"TRUNCATE TABLE {KEYSET_FQN}")
        db.rows(conn, f"INSERT INTO {KEYSET_FQN} (TABLE_NAME, KEY, VAL) "
                      f"SELECT TABLE_NAME, KEY, VAL FROM {TRANSIENT_DISCOVER_FQN}")
    # Pin every landed table's current content-key (so the next connect run is a clean no-op).
    wm = compute_watermarks(conn)
    for table, w in wm.items():
        _upsert_watermark(conn, table, w)
    _upsert_watermark(conn, CONFIG_SENTINEL,
                      {"source_id": None, "content_key": _config_fingerprint(),
                       "last_change_at": None, "n_success": 0})
    _pin_units(conn)   # per-unit pins: a later key add is a bounded apply-config, not a rebuild
    return {
        "spine_keyset": int(db.scalar(conn, f"SELECT COUNT(*) FROM {SKEYSET_FQN}") or 0),
        "discover_keyset": int(db.scalar(conn, f"SELECT COUNT(*) FROM {KEYSET_FQN}") or 0),
        "watermarks": len(wm),
    }


def _rebuild_spine_keyset_from_landing(conn) -> None:
    """Fallback seed: the transient SPINE_KEYSET is gone, so derive the persisted
    twin directly from the spec tables (same per-(table, key) INSERT the backstop
    uses -- see entity_index_specs.table_keys for tables with more than one key)."""
    db.rows(conn, f"TRUNCATE TABLE {SKEYSET_FQN}")
    for tbl, spec in DISPLAY_SPECS.items():
        for key, key_col in table_keys(spec):
            norm = normalize_sql(key, quote_ident(key_col))
            db.rows(conn, f"INSERT INTO {SKEYSET_FQN} (TABLE_NAME, KEY_TYPE, VAL) "
                          f"SELECT DISTINCT '{tbl}', '{key}', {norm} "
                          f"FROM {db.fqn(tbl)} WHERE {norm} IS NOT NULL")


# =========================================================================== #
# small SQL helpers
# =========================================================================== #
def _entity_type_sql(col_ref: str) -> str:
    """Delegates to entity_index_specs.entity_type_sql -- the ONE definition, shared
    with spine.py's full-rebuild path. Was a hand-copied duplicate of that CASE
    expression until 2026-07-30; if the two had ever drifted, a MERGE would have
    re-typed entities relative to the last full reconciliation."""
    return _entity_type_sql_shared(col_ref)


def _entity_id_sql(key_type_ref: str, val_ref: str) -> str:
    return f"'ENT_' || LEFT(MD5({key_type_ref} || '|' || {val_ref}), 16)"


# =========================================================================== #
# THE CORE — reslice ONE spine table into the live spine. Two scopes:
#   MEMBERSHIP (keyset partition / map / nodes / pairs) + retraction are scoped to
#   _AFFECTED, the symmetric difference of the table's old vs new normalized-key
#   slice — the only rows whose entity *membership* can have changed.
#   ATTRIBUTES (golden name/addr, index label/row_count/preview) are recomputed for
#   _RECOMPUTE = the table's FULL current key slice ∪ any removed keys. A content-key
#   bump can change attributes while leaving the id set identical (the CMS-quarterly
#   refresh), making _AFFECTED empty; scoping attributes to _AFFECTED there would
#   skip the recompute and diverge from a full rebuild. Both scopes are O(one table).
# =========================================================================== #
def reslice_spine(conn, table: str, run_id: str, dry_run: bool = False) -> dict:
    spec = DISPLAY_SPECS[table]
    keys = table_keys(spec)   # almost always one (key, key_col); a few tables carry two
    landing = db.fqn(table)
    lit = table.replace("'", "''")

    # --- the table's NEW normalized-key slice (deterministic, == full rebuild) --
    # UNION ALL across every key this table carries (e.g. FED_VOTEVIEW_MEMBERS
    # contributes both an ICPSR row and a BIOGUIDE row per member).
    new_arms = [
        f"SELECT DISTINCT '{key}' AS KEY_TYPE, {normalize_sql(key, quote_ident(key_col))} AS VAL "
        f"FROM {landing} WHERE {normalize_sql(key, quote_ident(key_col))} IS NOT NULL"
        for key, key_col in keys
    ]
    db.rows(conn, f"CREATE OR REPLACE TEMPORARY TABLE _NEW AS " + " UNION ALL ".join(new_arms))
    # --- the table's OLD slice (what the persisted keyset holds right now) ------
    db.rows(conn, f"CREATE OR REPLACE TEMPORARY TABLE _OLD AS "
                  f"SELECT KEY_TYPE, VAL FROM {SKEYSET_FQN} WHERE TABLE_NAME = '{lit}'")
    # --- SEAM #3 (membership): affected = symmetric difference (added UNION removed) --
    # PARENTHESES ARE LOAD-BEARING (bug found 2026-08-29): Snowflake gives MINUS and
    # UNION equal precedence, left to right, so the unparenthesized form
    #   NEW MINUS OLD UNION OLD MINUS NEW
    # evaluated as ((NEW - OLD) + OLD) - NEW == OLD - NEW: only REMOVED keys ever
    # reached _AFFECTED and every ADDED key was silently skipped by the map/nodes/
    # pairs merges (index + golden use _RECOMPUTE = NEW + AFFECTED, so they were
    # right). Live-verified: a brand-new spec table previewed affected=0 with
    # 54,406 new keys. tests/test_apply_config.py pins the parenthesized shape.
    db.rows(conn, AFFECTED_SQL)
    n_aff = int(db.scalar(conn, "SELECT COUNT(*) FROM _AFFECTED") or 0)
    n_new = int(db.scalar(conn, "SELECT COUNT(*) FROM _NEW") or 0)
    n_old = int(db.scalar(conn, "SELECT COUNT(*) FROM _OLD") or 0)
    stats = {"table": table, "affected": n_aff, "new_keys": n_new, "old_keys": n_old}

    if dry_run:
        stats["mode"] = "preview"
        return stats

    # entities whose MEMBERSHIP changed (content-addressed -> no ENTITY_MAP read).
    db.rows(conn, f"CREATE OR REPLACE TEMPORARY TABLE _AFFENT AS "
                  f"SELECT DISTINCT {_entity_id_sql('KEY_TYPE', 'VAL')} AS ENTITY_ID FROM _AFFECTED")
    # BLOCKER fix: the ATTRIBUTE-recompute scope. The full current slice (_NEW) re-stamps
    # golden/index even on an attribute-only refresh where _AFFECTED is empty; UNION the
    # removed keys (_AFFECTED carries them) so a removed-but-still-elsewhere id is
    # re-derived from its other tables instead of being wrongly dropped.
    db.rows(conn, """CREATE OR REPLACE TEMPORARY TABLE _RECOMPUTE AS
                     SELECT KEY_TYPE, VAL FROM _NEW
                     UNION SELECT KEY_TYPE, VAL FROM _AFFECTED""")

    # --- SEAM #1: replace the persisted keyset partition (DELETE then INSERT) ---
    db.rows(conn, f"DELETE FROM {SKEYSET_FQN} WHERE TABLE_NAME = '{lit}'")
    db.rows(conn, f"INSERT INTO {SKEYSET_FQN} (TABLE_NAME, KEY_TYPE, VAL) "
                  f"SELECT '{lit}', KEY_TYPE, VAL FROM _NEW")

    # KEYSET_LIVE fix: a spine table ALSO carries a discover KEYSET_LIVE partition
    # (its FULL key surface — BIOGUIDE + ICPSR + NAME@geo, not just the one spine key).
    # reslice_spine used to refresh only SPINE_KEYSET_LIVE, leaving that discover
    # partition stale. Refresh it here from the same fingerprint helper reslice_discover
    # uses, so both keysets stay coherent after a spine-table reslice.
    disc_keys = _refresh_discover_keyset(conn, table)
    stats["discover_key_partitions"] = [k for k, _ in disc_keys]

    # membership/retraction = _AFFECTED (a clean no-op when only attributes moved) ---
    stats.update(_merge_entity_map(conn, run_id))
    _merge_nodes(conn, table, run_id)
    stats.update(_merge_pairs(conn, table, run_id))
    # attributes = _RECOMPUTE, the table's full current slice (the BLOCKER fix) -------
    stats["index_rows"] = sum(
        _merge_index(conn, table, key, key_col, spec, run_id, "_RECOMPUTE") for key, key_col in keys)
    stats.update(_merge_golden(conn, run_id, "_RECOMPUTE"))
    stats["leads_restamped"] = _backfill_leads(conn)

    _upsert_watermark(conn, table, compute_watermarks(conn).get(table, {}))
    stats["mode"] = "merged" if n_aff else "attr-refresh (ids unchanged; attributes recomputed)"
    return stats


def _merge_entity_map(conn, run_id: str) -> dict:
    # recompute map rows for affected keys ONLY (bounded join to _AFFECTED)
    db.rows(conn, f"""
        CREATE OR REPLACE TEMPORARY TABLE _MAPCHG AS
        SELECT {_entity_id_sql('k.KEY_TYPE', 'k.VAL')} AS ENTITY_ID,
               k.KEY_TYPE AS KEY_TYPE, k.VAL AS KEY_VALUE,
               {_entity_type_sql('k.KEY_TYPE')} AS ENTITY_TYPE,
               ARRAY_AGG(DISTINCT k.TABLE_NAME) WITHIN GROUP (ORDER BY k.TABLE_NAME) AS MEMBER_TABLES,
               COUNT(DISTINCT k.TABLE_NAME) AS SOURCE_COUNT,
               '{run_id}' AS RUN_ID, CURRENT_TIMESTAMP() AS BUILT_AT
        FROM {SKEYSET_FQN} k
        JOIN _AFFECTED a ON a.KEY_TYPE = k.KEY_TYPE AND a.VAL = k.VAL
        GROUP BY k.KEY_TYPE, k.VAL""")
    db.rows(conn, f"""
        MERGE INTO {EMAP_FQN} t USING _MAPCHG s ON t.ENTITY_ID = s.ENTITY_ID
        WHEN MATCHED THEN UPDATE SET
            t.ENTITY_TYPE = s.ENTITY_TYPE, t.MEMBER_TABLES = s.MEMBER_TABLES,
            t.SOURCE_COUNT = s.SOURCE_COUNT, t.RUN_ID = s.RUN_ID, t.BUILT_AT = s.BUILT_AT
        WHEN NOT MATCHED THEN INSERT
            (ENTITY_ID, KEY_TYPE, KEY_VALUE, ENTITY_TYPE, MEMBER_TABLES, SOURCE_COUNT, RUN_ID, BUILT_AT)
            VALUES (s.ENTITY_ID, s.KEY_TYPE, s.KEY_VALUE, s.ENTITY_TYPE, s.MEMBER_TABLES,
                    s.SOURCE_COUNT, s.RUN_ID, s.BUILT_AT)""")
    # SEAM #1 retraction: affected entities that lost every member -> delete
    deleted = db.rows(conn, f"""
        DELETE FROM {EMAP_FQN}
        WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM _AFFENT)
          AND ENTITY_ID NOT IN (SELECT ENTITY_ID FROM _MAPCHG)""")
    ins = int(db.scalar(conn, "SELECT COUNT(*) FROM _MAPCHG") or 0)
    return {"map_upserts": ins, "map_deletes": _rowcount(deleted)}


def _merge_nodes(conn, table: str, run_id: str) -> None:
    # one row per (key_type, val, table). For THIS table, only affected vals move.
    lit = table.replace("'", "''")
    # (KEY_TYPE, KEY_VALUE) pair scope, matching the re-INSERT's join: a value
    # colliding across key types on a multi-key table must not be deleted for
    # a key type that wasn't affected -- it would never be restored.
    db.rows(conn, f"DELETE FROM {NODES_FQN} WHERE TABLE_NAME = '{lit}' "
                  f"AND (KEY_TYPE, KEY_VALUE) IN (SELECT KEY_TYPE, VAL FROM _AFFECTED)")
    db.rows(conn, f"""
        INSERT INTO {NODES_FQN} (NODE_ID, KEY_TYPE, KEY_VALUE, TABLE_NAME, RUN_ID, BUILT_AT)
        SELECT MD5(n.KEY_TYPE || '|' || n.VAL), n.KEY_TYPE, n.VAL, '{lit}',
               '{run_id}', CURRENT_TIMESTAMP()
        FROM _NEW n JOIN _AFFECTED a ON a.KEY_TYPE = n.KEY_TYPE AND a.VAL = n.VAL""")


def _merge_index(conn, table: str, key: str, key_col: str, spec: dict, run_id: str,
                  scope: str = "_AFFECTED") -> int:
    # ENTITY_INDEX is keyed (ENTITY_ID, SOURCE_TABLE, KEY_TYPE); each row depends ONLY
    # on its own SOURCE_TABLE's data (no sibling read), so replacing just this table's
    # `scope` slice is exact. ENTITY_ID is the content hash (no ENTITY_MAP join -> no
    # 9.7M scan). reslice_spine passes scope=_RECOMPUTE (the full current slice ∪
    # removed keys) so an attribute-only refresh re-stamps DISPLAY_LABEL/ROW_COUNT/
    # PREVIEW and a removed key's stale row is dropped. Mirrors entity_index.build.
    # key/key_col are explicit params (not read off spec) because a table can carry
    # MORE THAN ONE key (see entity_index_specs.table_keys) -- the caller loops once
    # per key, and `scope` itself may hold rows for several key types at once, so
    # every clause below is scoped by KEY_TYPE = '{key}', not just SOURCE_TABLE.
    norm = normalize_sql(key, quote_ident(key_col))
    lit = table.replace("'", "''")
    eid = _entity_id_sql(f"'{key}'", norm)
    preview_pairs = [f"'place', ANY_VALUE({_addr_expr(spec)})"]
    for label, col in spec.get("extra", {}).items():
        preview_pairs.append(f"'{label}', ANY_VALUE(TRIM({quote_ident(col)}))")
    preview = f"OBJECT_CONSTRUCT({', '.join(preview_pairs)})"

    db.rows(conn, f"DELETE FROM {INDEX_FQN} WHERE SOURCE_TABLE = '{lit}' AND KEY_TYPE = '{key}' "
                  f"AND KEY_VALUE IN (SELECT VAL FROM {scope} WHERE KEY_TYPE = '{key}')")
    inserted = db.rows(conn, f"""
        INSERT INTO {INDEX_FQN}
          (ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE, SOURCE_TABLE, DOMAIN,
           DISPLAY_LABEL, ROW_COUNT, PREVIEW, DISPLAY_NORM)
        SELECT ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE, SOURCE_TABLE, DOMAIN,
               DISPLAY_LABEL, ROW_COUNT, PREVIEW,
               UPPER(REGEXP_REPLACE(COALESCE(DISPLAY_LABEL, ''), '[^A-Za-z0-9]+', ' ')) AS DISPLAY_NORM
        FROM (
          SELECT {eid} AS ENTITY_ID, {_entity_type_sql("'" + key + "'")} AS ENTITY_TYPE,
                 '{key}' AS KEY_TYPE, ANY_VALUE({norm}) AS KEY_VALUE,
                 '{lit}' AS SOURCE_TABLE, '{domain_of(table)}' AS DOMAIN,
                 ANY_VALUE({_name_expr(spec)}) AS DISPLAY_LABEL,
                 COUNT(*) AS ROW_COUNT, {preview} AS PREVIEW
          FROM {db.fqn(table)} t
          WHERE {norm} IS NOT NULL AND {norm} IN (SELECT VAL FROM {scope} WHERE KEY_TYPE = '{key}')
          GROUP BY {eid}
        )""")
    # rows actually inserted this call -- not a recount of the slice, which
    # overstated work done when the scope overlapped rows already present.
    return _rowcount(inserted)


def _golden_attrs(scope_fqn: str = "_AFFECTED") -> str:
    """The spine's survivorship UNION ALL, scoped per-arm to `scope_fqn` AND gated by
    the persisted keyset twin (SKEYSET_FQN). The scope sub-select limits each arm to the
    values being recomputed; an arm of a non-matching key_type has an empty scope and
    contributes nothing, so only same-key-type member tables are scanned.

    The SKEYSET gate is the MAJOR-#2 fix. Golden reads the LIVE landing of EVERY member
    table to pick a survivorship winner, but membership lives in the persisted twin. A
    sibling whose landing changed but hasn't been resliced yet would otherwise leak its
    NEW rows into golden while ENTITY_MAP still reflects its OLD slice. Gating each arm to
    the (table, key, val) triples the twin actually records keeps golden's input
    consistent with the persisted membership: the changed table's own partition was just
    refreshed to its NEW slice (so it contributes fully), while an unchanged sibling
    contributes its persisted slice — so a winner that lives in a non-changed table is
    still preserved. In steady state the twin == every table's current landing slice, so
    the gate is a no-op and golden == the full rebuild."""
    arms = []
    for tbl, spec in DISPLAY_SPECS.items():
        lit = tbl.replace("'", "''")
        for key, key_col in table_keys(spec):
            norm = normalize_sql(key, quote_ident(key_col))
            arms.append(
                f"SELECT '{key}' AS KEY_TYPE, {norm} AS KEY_VALUE, "
                f"{_name_expr(spec)} AS NAME, {_addr_expr(spec)} AS ADDR, "
                f"{spec['authority']} AS AUTH, '{tbl}' AS SRC "
                f"FROM {db.fqn(tbl)} "
                f"WHERE {norm} IS NOT NULL "
                f"AND {norm} IN (SELECT VAL FROM {scope_fqn} WHERE KEY_TYPE = '{key}') "
                f"AND {norm} IN (SELECT VAL FROM {SKEYSET_FQN} "
                f"WHERE TABLE_NAME = '{lit}' AND KEY_TYPE = '{key}')")
    return " UNION ALL ".join(arms)


def _merge_golden(conn, run_id: str, scope: str = "_AFFECTED") -> dict:
    db.rows(conn, f"""
        CREATE OR REPLACE TEMPORARY TABLE _GOLDCHG AS
        WITH attrs AS ( {_golden_attrs(scope)} ),
        ranked AS (
          SELECT {_entity_id_sql('a.KEY_TYPE', 'a.KEY_VALUE')} AS ENTITY_ID,
                 {_entity_type_sql('a.KEY_TYPE')} AS ENTITY_TYPE,
                 a.KEY_TYPE, a.KEY_VALUE, a.NAME, a.ADDR, a.SRC,
                 ROW_NUMBER() OVER (PARTITION BY a.KEY_TYPE, a.KEY_VALUE
                     ORDER BY IFF(a.NAME IS NULL, 1, 0), a.AUTH, LENGTH(a.NAME) DESC NULLS LAST, a.SRC) AS RN
          FROM attrs a )
        SELECT ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE,
               NAME AS CANONICAL_NAME, {normalize_sql('NAME', 'NAME')} AS NAME_NORM,
               ADDR AS CANONICAL_ADDR, SRC AS NAME_SOURCE,
               '{run_id}' AS RUN_ID, CURRENT_TIMESTAMP() AS BUILT_AT
        FROM ranked WHERE RN = 1""")
    db.rows(conn, f"""
        MERGE INTO {GOLD_FQN} t USING _GOLDCHG s ON t.ENTITY_ID = s.ENTITY_ID
        WHEN MATCHED THEN UPDATE SET
            t.ENTITY_TYPE = s.ENTITY_TYPE, t.CANONICAL_NAME = s.CANONICAL_NAME,
            t.NAME_NORM = s.NAME_NORM, t.CANONICAL_ADDR = s.CANONICAL_ADDR,
            t.NAME_SOURCE = s.NAME_SOURCE, t.RUN_ID = s.RUN_ID, t.BUILT_AT = s.BUILT_AT
        WHEN NOT MATCHED THEN INSERT
            (ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE, CANONICAL_NAME, NAME_NORM,
             CANONICAL_ADDR, NAME_SOURCE, RUN_ID, BUILT_AT)
            VALUES (s.ENTITY_ID, s.ENTITY_TYPE, s.KEY_TYPE, s.KEY_VALUE, s.CANONICAL_NAME,
                    s.NAME_NORM, s.CANONICAL_ADDR, s.NAME_SOURCE, s.RUN_ID, s.BUILT_AT)""")
    # retraction: ENTITY_GOLDEN is one row per entity (live GOLDEN == MAP count), so it
    # MIRRORS ENTITY_MAP exactly: only a MEMBERSHIP-changed entity (_AFFENT) can leave
    # golden, and it does iff it has no surviving member (-> no _GOLDCHG row). _GOLDCHG
    # now spans the wider _RECOMPUTE attribute scope, but _AFFENT ⊆ _RECOMPUTE, so a
    # surviving _AFFENT entity is guaranteed a _GOLDCHG row and is kept; an attribute-only
    # entity (in _RECOMPUTE, not _AFFENT) is recomputed but never eligible for deletion.
    # A still-present entity always yields >=1 attrs row (NAME may be NULL), so it stays.
    # (An earlier draft also excluded entities still in EMAP, wrongly pinning stale rows.)
    deleted = db.rows(conn, f"""
        DELETE FROM {GOLD_FQN}
        WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM _AFFENT)
          AND ENTITY_ID NOT IN (SELECT ENTITY_ID FROM _GOLDCHG)""")
    ins = int(db.scalar(conn, "SELECT COUNT(*) FROM _GOLDCHG") or 0)
    return {"golden_upserts": ins, "golden_deletes": _rowcount(deleted)}


def _merge_pairs(conn, table: str, run_id: str) -> dict:
    # MATCH_PAIRS = same hard key in two tables. Only pairs that TOUCH this table
    # AND an affected value can change; everything else is left intact.
    lit = table.replace("'", "''")
    # SEAM #4 bounded blocking: log any affected value that fans out to many tables.
    fan = db.dicts(conn, f"""
        SELECT a.VAL, COUNT(DISTINCT k.TABLE_NAME) AS FAN
        FROM _AFFECTED a JOIN {SKEYSET_FQN} k ON k.KEY_TYPE = a.KEY_TYPE AND k.VAL = a.VAL
        GROUP BY a.VAL HAVING COUNT(DISTINCT k.TABLE_NAME) > {FANOUT_MAX}
        ORDER BY FAN DESC LIMIT 5""")
    if fan:
        worst = ", ".join(f"{r['VAL']}({int(r['FAN'])})" for r in fan)
        print(f"  [fanout] {table}: {len(fan)} hard-key value(s) exceed {FANOUT_MAX} tables "
              f"(kept — hard IDs are never dropped): {worst}")

    db.rows(conn, f"""
        DELETE FROM {PAIRS_FQN}
        WHERE (TABLE_A = '{lit}' OR TABLE_B = '{lit}')
          AND (KEY_TYPE, KEY_VALUE) IN (SELECT KEY_TYPE, VAL FROM _AFFECTED)""")
    db.rows(conn, f"""
        INSERT INTO {PAIRS_FQN} (KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B, RUN_ID, BUILT_AT)
        SELECT a.KEY_TYPE, a.VAL, a.TABLE_NAME, b.TABLE_NAME, '{run_id}', CURRENT_TIMESTAMP()
        FROM {SKEYSET_FQN} a
        JOIN {SKEYSET_FQN} b
          ON a.KEY_TYPE = b.KEY_TYPE AND a.VAL = b.VAL AND a.TABLE_NAME < b.TABLE_NAME
        JOIN _AFFECTED af ON af.KEY_TYPE = a.KEY_TYPE AND af.VAL = a.VAL
        WHERE a.TABLE_NAME = '{lit}' OR b.TABLE_NAME = '{lit}'""")
    n = int(db.scalar(conn, f"""
        SELECT COUNT(*) FROM {PAIRS_FQN}
        WHERE (TABLE_A = '{lit}' OR TABLE_B = '{lit}')
          AND (KEY_TYPE, KEY_VALUE) IN (SELECT KEY_TYPE, VAL FROM _AFFECTED)""") or 0)
    return {"pairs_touching_table": n}


def _backfill_leads(conn) -> int:
    if not _table_exists(conn, "LEADS"):
        return 0
    restamped = db.rows(conn, f"""
        UPDATE {LEADS_FQN} t SET LEFT_ENTITY_ID = e.ENTITY_ID
        FROM {EMAP_FQN} e
        WHERE e.KEY_TYPE = t.LEFT_KEY_TYPE AND e.KEY_VALUE = t.LEFT_KEY_VALUE
          AND (t.LEFT_KEY_TYPE, t.LEFT_KEY_VALUE) IN (SELECT KEY_TYPE, VAL FROM _AFFECTED)""")
    # rows this UPDATE actually touched -- the old COUNT of every non-null
    # LEFT_ENTITY_ID in the table overstated the run's work by orders.
    return _rowcount(restamped)


# =========================================================================== #
# ON-LAND DISCOVER (the non-spine path) — for ANY table with hard keys, refresh
# its persisted KEYSET_LIVE partition and self-join its NEW keys vs the existing
# keyset to surface connections immediately. Bounded by PAIR_BUDGET (seam #4).
# This is what "link a brand-new source the moment it lands" means for the ~747
# tables that aren't in the 15-table spine.
# =========================================================================== #
def _discover_keyset_inserts(conn, table: str) -> list[tuple[str, str]]:
    """Derive the (key_label, normalized_sql_expr) list for a table's discover
    KEYSET_LIVE partition — the full discover key surface (value keys + NAME@geo),
    NOT just the single spine key. Mirrors discover._build_keysets selection for one
    table. Factored out so BOTH reslice_discover (non-spine tables) and reslice_spine
    (spine tables — which ALSO carry a discover partition) refresh the same way."""
    from . import fingerprint
    fp = fingerprint.fingerprint_table(conn, table)   # reuse the single-table scan
    info_keys = fp["keys"]

    inserts: list[tuple[str, str]] = []   # (key_label, normalized_sql_expr)
    seen: set[str] = set()
    for k in info_keys:
        key = k["key"]
        if k["mode"] != "value" or key in seen:
            continue
        best = _best_value_col(info_keys, key)
        if not best:
            continue
        seen.add(key)
        if key in PROBABILISTIC and fp["rows"] > NAME_MAX_ROWS:
            continue   # huge fuzzy-name table: skip (mirrors discover's name cap)
        # ZIP country-gate (Chris 2026-08-09) — mirrors discover._build_keysets.
        ccol = _best_value_col(info_keys, "COUNTRY") if key == "ZIP" else None
        # edge_norm_sql (NOT normalize_sql): the discover keyset carries the
        # edge-quality gates (DOCKET issuer namespace, FIPS granularity floor) --
        # mirrors discover._build_keysets. The spine paths above stay on
        # normalize_sql, so the config fingerprint is untouched.
        inserts.append((key, edge_norm_sql(
            key, quote_ident(best["column"]), table=table,
            country_col=quote_ident(ccol["column"]) if ccol else None)))
    name_col = _best_value_col(info_keys, "NAME")
    for geo in ("ZIP", "FIPS"):
        geo_col = _best_value_col(info_keys, geo)
        if name_col and geo_col:
            nexpr = edge_norm_sql("NAME", quote_ident(name_col["column"]))
            ccol = _best_value_col(info_keys, "COUNTRY") if geo == "ZIP" else None
            gexpr = edge_norm_sql(geo, quote_ident(geo_col["column"]), table=table,
                                  country_col=quote_ident(ccol["column"]) if ccol else None)
            inserts.append((f"NAME@{geo}", f"{nexpr} || '|' || {gexpr}"))
            break
    return inserts


def _refresh_discover_keyset(conn, table: str) -> list[tuple[str, str]]:
    """SEAM #1 for the DISCOVER keyset (KEYSET_LIVE): replace this table's partition
    (DELETE then per-key INSERT). Returns the inserts list so callers can reason
    about which keys landed. NEVER derive this partition from a single spine slice --
    KEYSET_LIVE holds ALL fingerprinted keys per table (~4 partitions/table), so a
    naive spine-only refresh would wipe the other key partitions."""
    lit = table.replace("'", "''")
    inserts = _discover_keyset_inserts(conn, table)
    db.rows(conn, f"DELETE FROM {KEYSET_FQN} WHERE TABLE_NAME = '{lit}'")
    for key, expr in inserts:
        guard = " AND ".join(f"{p} IS NOT NULL" for p in expr.split(" || '|' || ")) \
            if key.startswith("NAME@") else f"{expr} IS NOT NULL"
        db.rows(conn, f"INSERT INTO {KEYSET_FQN} (TABLE_NAME, KEY, VAL) "
                      f"SELECT DISTINCT '{lit}', '{key}', {expr} FROM {db.fqn(table)} WHERE {guard}")
    return inserts


def reslice_discover(conn, table: str, run_id: str, dry_run: bool = False) -> dict:
    lit = table.replace("'", "''")

    if dry_run:
        inserts = _discover_keyset_inserts(conn, table)
        return {"table": table, "key_partitions": [k for k, _ in inserts], "mode": "preview"}

    # SEAM #1: replace this table's KEYSET_LIVE partition (DELETE then INSERT).
    inserts = _refresh_discover_keyset(conn, table)

    # SEAM #4: bounded self-join — new keys (this table) vs the rest of the keyset.
    counts = {(r["TABLE_NAME"], r["KEY"]): int(r["ND"]) for r in db.dicts(conn, f"""
        SELECT TABLE_NAME, KEY, COUNT(*) ND FROM {KEYSET_FQN}
        WHERE KEY IN (SELECT DISTINCT KEY FROM {KEYSET_FQN} WHERE TABLE_NAME = '{lit}')
        GROUP BY 1, 2""")}
    pairs = db.dicts(conn, f"""
        SELECT a.KEY AS JKEY, b.TABLE_NAME AS OTHER, COUNT(*) AS MATCHED,
               ARRAY_SLICE(ARRAY_AGG(a.VAL), 0, 4) AS SAMP
        FROM {KEYSET_FQN} a
        JOIN {KEYSET_FQN} b ON a.KEY = b.KEY AND a.VAL = b.VAL AND a.TABLE_NAME <> b.TABLE_NAME
        WHERE a.TABLE_NAME = '{lit}'
        GROUP BY 1, 2
        HAVING COUNT(*) >= {MIN_MATCH}
        ORDER BY MATCHED DESC
        LIMIT {PAIR_BUDGET}""")

    db.rows(conn, f"DELETE FROM {EDGES_FQN} WHERE A = '{lit}' OR B = '{lit}'")
    kept = 0
    for r in pairs:
        key, other, matched = r["JKEY"], r["OTHER"], int(r["MATCHED"])
        a_d = counts.get((table, key), 0)
        b_d = counts.get((other, key), 0)
        tier = "CORROBORATED" if key.startswith("NAME@") else _tier({}, key)
        conf, keep = confidence(key, tier, a_d, b_d, matched)
        if not keep:
            continue
        samp = r["SAMP"]
        db.rows(conn, f"""
            INSERT INTO {EDGES_FQN}
              (A, B, KEY, TIER, MATCHED, A_DISTINCT, B_DISTINCT, MATCH_RATE, CONFIDENCE, "SAMPLE", RUN_ID, BUILT_AT)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, TO_VARIANT(PARSE_JSON(%s)), %s, CURRENT_TIMESTAMP()
        """, (table, other, key, tier, matched, a_d, b_d,
              round(matched / (min(a_d, b_d) or 1) * 100, 1), conf,
              _json(samp), run_id))
        kept += 1
    return {"table": table, "key_partitions": [k for k, _ in inserts],
            "edges_kept": kept, "candidates": len(pairs), "mode": "linked"}


# =========================================================================== #
# DRIVERS
# =========================================================================== #
def connect_one(source_id: str, landing_table: str | None = None, dry_run: bool = False) -> dict:
    """Link ONE just-landed table. Spine tables (DISPLAY_SPECS) get the full
    incremental spine MERGE; any other table with hard keys gets the bounded
    on-land discover pass. A no-op when the content-key hasn't moved."""
    table = (landing_table or source_id).strip().upper()
    run_id = uuid.uuid4().hex[:16]
    conn = db.connect()
    try:
        _reset_caches()
        validate_key_config()
        _ddl(conn)
        _apply_config_drift_or_raise(conn)
        if int(db.scalar(conn, f"SELECT COUNT(*) FROM {SKEYSET_FQN}") or 0) == 0:
            raise RuntimeError("incremental state not seeded. Run `python -m connect.incremental seed` once.")
        wm = compute_watermarks(conn).get(table)
        stored = _stored_keys(conn).get(table)
        if wm is None:
            return {"table": table, "mode": "skip (no success/empty INGEST_RUNS row)"}
        # A source can log success/empty in INGEST_RUNS yet never materialize a landing
        # table (portal harvests, etc.); the discover path would read a missing table.
        if table not in DISPLAY_SPECS and table not in _landing_tables(conn):
            return {"table": table, "mode": "skip (no LIBRARY_RAW.LANDING table)"}
        if wm["content_key"] == stored and not dry_run:
            return {"table": table, "mode": "no-op (content-key unchanged)"}
        if table in DISPLAY_SPECS:
            out = reslice_spine(conn, table, run_id, dry_run=dry_run)
        else:
            out = reslice_discover(conn, table, run_id, dry_run=dry_run)
            if not dry_run:
                _upsert_watermark(conn, table, wm)
    finally:
        conn.close()
    print(f"connect-one {table}: {out}")
    return out


def connect_changed(scope: str = "spine", dry_run: bool = False) -> dict:
    """The heartbeat catch-up: reslice every table whose content-key moved. This
    is the additive incremental counterpart to a full `connect all`."""
    run_id = uuid.uuid4().hex[:16]
    conn = db.connect()
    results = []
    try:
        _reset_caches()
        validate_key_config()
        _ddl(conn)
        _apply_config_drift_or_raise(conn)
        if int(db.scalar(conn, f"SELECT COUNT(*) FROM {SKEYSET_FQN}") or 0) == 0:
            raise RuntimeError("incremental state not seeded. Run `python -m connect.incremental seed` once.")
        changed = changed_tables(conn, scope)
        print(f"connect-changed ({scope}): {len(changed)} table(s) moved: {changed or '—'}")
        for t in changed:
            if t in DISPLAY_SPECS:
                results.append(reslice_spine(conn, t, run_id, dry_run=dry_run))
            else:
                r = reslice_discover(conn, t, run_id, dry_run=dry_run)
                if not dry_run:
                    _upsert_watermark(conn, t, compute_watermarks(conn).get(t, {}))
                results.append(r)
    finally:
        conn.close()
    return {"scope": scope, "changed": len(results), "results": results}


# =========================================================================== #
# NON-DESTRUCTIVE EQUIVALENCE VALIDATION — CANNOT CURRENTLY RUN. It compares
# against transient scratch twins that only the RETIRED full rebuild wrote;
# with the rebuild in the junk drawer, those tables are stale or absent, so
# this is not a live backstop. Offline coverage for the MERGE logic lives in
# tests/test_connect_merge_offline.py (DuckDB). Reads live tables and writes
# only session TEMP/scratch when it does run.
# =========================================================================== #
def validate(table: str | None = None) -> dict:
    table = (table or "FED_HHS_OIG_LEIE").strip().upper()
    lit = table.replace("'", "''")
    conn = db.connect()
    checks: dict[str, str] = {}
    try:
        _reset_caches()
        _ddl(conn)
        # (1) seed equality: persisted twins == the transient backstop keysets
        checks["spine_keyset_twin"] = _two_way_equal(
            conn, f"SELECT TABLE_NAME, KEY_TYPE, VAL FROM {SKEYSET_FQN}",
            f"SELECT TABLE_NAME, KEY_TYPE, VAL FROM {TRANSIENT_SPINE_FQN}")
        checks["discover_keyset_twin"] = _two_way_equal(
            conn, f"SELECT TABLE_NAME, KEY, VAL FROM {KEYSET_FQN}",
            f"SELECT TABLE_NAME, KEY, VAL FROM {TRANSIENT_DISCOVER_FQN}")
        # (2) NO-OP: with state pinned, nothing should look changed
        checks["noop_spine"] = "PASS (0 changed)" if not changed_tables(conn, "spine") \
            else f"FAIL ({changed_tables(conn, 'spine')})"
        # (3-5) recompute equivalence for one spine table: recompute its FULL current
        #       key slice (== the attribute-only-refresh scope, where the symmetric diff
        #       is empty) and diff vs the live ENTITY_MAP / MATCH_PAIRS / ENTITY_GOLDEN.
        #       Proves the BLOCKER fix recomputes the whole slice (not a no-op) AND that
        #       the recompute is byte-equivalent to the full rebuild.
        spec = DISPLAY_SPECS.get(table)
        if spec:
            vkey_arms = [
                f"SELECT DISTINCT '{key}' KEY_TYPE, {normalize_sql(key, quote_ident(key_col))} VAL "
                f"FROM {db.fqn(table)} WHERE {normalize_sql(key, quote_ident(key_col))} IS NOT NULL"
                for key, key_col in table_keys(spec)
            ]
            db.rows(conn, f"CREATE OR REPLACE TEMPORARY TABLE _VKEYS AS " + " UNION ALL ".join(vkey_arms))
            # --- ENTITY_MAP ---
            db.rows(conn, f"""
                CREATE OR REPLACE TEMPORARY TABLE _MAP_SHADOW AS
                SELECT {_entity_id_sql('k.KEY_TYPE', 'k.VAL')} ENTITY_ID,
                       {_entity_type_sql('k.KEY_TYPE')} ENTITY_TYPE,
                       ARRAY_SORT(ARRAY_AGG(DISTINCT k.TABLE_NAME)) MEMBER_TABLES,
                       COUNT(DISTINCT k.TABLE_NAME) SOURCE_COUNT
                FROM {SKEYSET_FQN} k
                JOIN _VKEYS v ON v.KEY_TYPE = k.KEY_TYPE AND v.VAL = k.VAL
                GROUP BY k.KEY_TYPE, k.VAL""")
            checks[f"entity_map_recompute[{table}]"] = _two_way_equal(
                conn,
                "SELECT ENTITY_ID, ENTITY_TYPE, "
                "ARRAY_TO_STRING(MEMBER_TABLES, ',') AS MT, SOURCE_COUNT FROM _MAP_SHADOW",
                f"SELECT ENTITY_ID, ENTITY_TYPE, "
                f"ARRAY_TO_STRING(ARRAY_SORT(MEMBER_TABLES), ',') AS MT, SOURCE_COUNT "
                f"FROM {EMAP_FQN} WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM _MAP_SHADOW)")
            # --- MATCH_PAIRS (every pair touching this table, on its current slice) ---
            db.rows(conn, f"""
                CREATE OR REPLACE TEMPORARY TABLE _PAIR_SHADOW AS
                SELECT a.KEY_TYPE, a.VAL AS KEY_VALUE, a.TABLE_NAME AS TABLE_A, b.TABLE_NAME AS TABLE_B
                FROM {SKEYSET_FQN} a
                JOIN {SKEYSET_FQN} b
                  ON a.KEY_TYPE = b.KEY_TYPE AND a.VAL = b.VAL AND a.TABLE_NAME < b.TABLE_NAME
                JOIN _VKEYS af ON af.KEY_TYPE = a.KEY_TYPE AND af.VAL = a.VAL
                WHERE a.TABLE_NAME = '{lit}' OR b.TABLE_NAME = '{lit}'""")
            checks[f"match_pairs_recompute[{table}]"] = _two_way_equal(
                conn,
                "SELECT KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B FROM _PAIR_SHADOW",
                f"SELECT KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B FROM {PAIRS_FQN} "
                f"WHERE (TABLE_A = '{lit}' OR TABLE_B = '{lit}') "
                f"AND (KEY_TYPE, KEY_VALUE) IN (SELECT KEY_TYPE, VAL FROM _VKEYS)")
            # --- ENTITY_GOLDEN (survivorship over the gated arms, full current slice) ---
            db.rows(conn, f"""
                CREATE OR REPLACE TEMPORARY TABLE _GOLD_SHADOW AS
                WITH attrs AS ( {_golden_attrs('_VKEYS')} ),
                ranked AS (
                  SELECT {_entity_id_sql('a.KEY_TYPE', 'a.KEY_VALUE')} AS ENTITY_ID,
                         {_entity_type_sql('a.KEY_TYPE')} AS ENTITY_TYPE,
                         a.KEY_TYPE, a.KEY_VALUE, a.NAME, a.ADDR, a.SRC,
                         ROW_NUMBER() OVER (PARTITION BY a.KEY_TYPE, a.KEY_VALUE
                             ORDER BY IFF(a.NAME IS NULL, 1, 0), a.AUTH,
                                      LENGTH(a.NAME) DESC NULLS LAST, a.SRC) AS RN
                  FROM attrs a )
                SELECT ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE,
                       NAME AS CANONICAL_NAME, {normalize_sql('NAME', 'NAME')} AS NAME_NORM,
                       ADDR AS CANONICAL_ADDR, SRC AS NAME_SOURCE
                FROM ranked WHERE RN = 1""")
            # Compare the survivorship DECISION (winning source + canonical name), NOT
            # CANONICAL_ADDR: when the winning source carries several equal-rank rows for
            # one id (e.g. a provider excluded twice at different addresses, same name),
            # ROW_NUMBER() picks an address arbitrarily. spine._build_golden uses the
            # IDENTICAL ORDER BY, so the full rebuild resolves that tie the same
            # nondeterministic way — a spine rerun differs from itself there. Pinning addr
            # would falsely flag a backstop tie as an incremental defect.
            gcols = ("ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE, CANONICAL_NAME, "
                     "NAME_NORM, NAME_SOURCE")
            checks[f"entity_golden_recompute[{table}]"] = _two_way_equal(
                conn,
                f"SELECT {gcols} FROM _GOLD_SHADOW",
                f"SELECT {gcols} FROM {GOLD_FQN} "
                f"WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM _GOLD_SHADOW)")
        else:
            checks[f"entity_map_recompute[{table}]"] = "SKIP (not a spine table)"
    finally:
        conn.close()
    for name, verdict in checks.items():
        print(f"  {'OK ' if verdict.startswith('PASS') or verdict == 'PASS' else '   '}{name:<32} {verdict}")
    return checks


def _two_way_equal(conn, sql_a: str, sql_b: str) -> str:
    a = int(db.scalar(conn, f"SELECT COUNT(*) FROM (({sql_a}) MINUS ({sql_b}))") or 0)
    b = int(db.scalar(conn, f"SELECT COUNT(*) FROM (({sql_b}) MINUS ({sql_a}))") or 0)
    return "PASS" if a == 0 and b == 0 else f"FAIL (a-b={a}, b-a={b})"


# =========================================================================== #
# tiny utilities
# =========================================================================== #
def _rowcount(result) -> int:
    try:
        return int(result[0][0]) if result and result[0] and result[0][0] is not None else 0
    except Exception:
        return 0


def _table_exists(conn, name: str) -> bool:
    return bool(db.scalar(conn,
        f"SELECT COUNT(*) FROM {CONNECT_DB}.INFORMATION_SCHEMA.TABLES "
        f"WHERE TABLE_SCHEMA = '{CONNECT_SCHEMA}' AND TABLE_NAME = '{db.ident(name)}'"))


def _landing_tables(conn) -> set[str]:
    """The set of tables that actually exist in LIBRARY_RAW.LANDING. ~31 source_ids log
    a success/empty INGEST_RUNS row but never materialize a landing table (portal
    harvests, etc.); changed_tables/connect_one use this to skip them so a reslice never
    reads a non-existent table."""
    return {r[0] for r in db.rows(conn,
        f"SELECT TABLE_NAME FROM {db.RAW_DB}.INFORMATION_SCHEMA.TABLES "
        f"WHERE TABLE_SCHEMA = '{db.RAW_SCHEMA}'")}


def _json(v) -> str:
    import json
    if isinstance(v, str):
        return v
    return json.dumps(v or [])


# =========================================================================== #
# CLI
# =========================================================================== #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="connect.incremental",
                                 description="Incremental CONNECT — O(changed tables)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed", help="one-time: init state tables + pin current content-keys") \
        .add_argument("--reseed", action="store_true", help="overwrite persisted twins (rebuild scratch if present, else landing)")
    co = sub.add_parser("connect-one", help="link one just-landed table")
    co.add_argument("--source", required=True, help="source_id or landing table name")
    co.add_argument("--dry-run", action="store_true")
    cc = sub.add_parser("connect-changed", help="reslice every table whose content-key moved")
    cc.add_argument("--scope", choices=["spine", "all"], default="spine")
    cc.add_argument("--dry-run", action="store_true")
    va = sub.add_parser("validate",
                        help="BROKEN until re-pointed: needs scratch twins only the "
                             "retired rebuild wrote; offline MERGE coverage lives in "
                             "tests/test_connect_merge_offline.py")
    va.add_argument("--table", default=None)
    ac = sub.add_parser("apply-config", help="apply a keys.py / DISPLAY_SPECS change with bounded reslices (no full rebuild)")
    ac.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "seed":
        seed(reseed=getattr(args, "reseed", False))
    elif args.cmd == "connect-one":
        connect_one(args.source, dry_run=args.dry_run)
    elif args.cmd == "connect-changed":
        connect_changed(scope=args.scope, dry_run=args.dry_run)
    elif args.cmd == "validate":
        validate(table=args.table)
    elif args.cmd == "apply-config":
        apply_config(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
