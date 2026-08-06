"""Fingerprint every landed table: which join keys does it carry, and are they
ACTUALLY populated?

The portal index tags datasets by key *type* from column names alone. That's
what burned us today — a column literally named NPI that's 100% empty, a CCN
that's numeric noise. Fingerprinting adds the missing half: it goes to the data
and measures population (non-null %, distinct count) for every key column, so a
dead key never poses as a live connection.

Output: outputs/connect_fingerprints.json
  { "<TABLE>": {
      "rows": int,
      "fmt": 2,
      "keys": [ {column, key, tier, mode, nonnull, distinct, populated_pct,
                 min, max, prefixes, prefix_count} ... ]
  } }

fmt 2 (2026-08-01, Hunch Engine): value keys also carry the normalized value
RANGE (min/max) and the distinct 2-char prefix set (capped at PREFIX_CAP;
prefix_count says whether the cap truncated it). Collected in the SAME scan —
no extra pass. Why: partitioned ID spaces (CCN encodes facility type in its
ranges, dockets encode the court) make zero overlap boring-by-construction;
absence-surprise must condition on the two sides' ranges actually overlapping
(see reports/hunch_calibration_2026-08-01.md). fmt is also the resume marker:
run(resume=True) skips tables already fingerprinted at this format.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import db
from .keys import detect_key, join_mode, normalize_sql, quote_ident

OUT = Path(__file__).resolve().parents[1] / "outputs" / "connect_fingerprints.json"

# Tables that aren't real joinable sources (early proofs / archive captures / demos).
SKIP_TABLES = {
    "INTL_DEMO_QUOTES_TOSCRAPE_JS",
    # 2026-08-05 ingestion sweep: orphaned duplicate twins from parallel build agents.
    # Byte-identical row counts to their SOURCE_REGISTRY-registered canonical copies
    # (see CHRIS_DECISIONS.md "6 true duplicate raw tables" + the ICIJ/IRS527 pairs
    # found 2026-08-05). Skipped so the map never grows doubled edges; the tables
    # themselves await a manual DROP by someone with warehouse access.
    "FED_FHFA_SUSPENDED_COUNTERPARTY",      # canonical: FED_FHFA_SUSPENDED_COUNTERPARTY_PROGRAM
    "FED_JPML_PENDING_MDL",                 # canonical: FED_JPML_PENDING_MDLS
    "INTL_UK_SANCTIONS_LIST",               # canonical: XC_UK_SANCTIONS_LIST
    "INTL_UN_CONSOLIDATED_SANCTIONS",       # canonical: XC_UN_CONSOLIDATED_SANCTIONS_LIST
    "STATE_OEHHA_PROP65_CHEMICALS",         # canonical: ST_OEHHA_PROPOSITION_65_LIST
    "ICIJ_OFFSHORE_LEAKS_ADDRESSES",        # canonical: FED_ICIJ_OFFSHORELEAKS_ADDRESSES
    "ICIJ_OFFSHORE_LEAKS_ENTITIES",         # canonical: FED_ICIJ_OFFSHORELEAKS_ENTITIES
    "ICIJ_OFFSHORE_LEAKS_INTERMEDIARIES",   # canonical: FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES
    "ICIJ_OFFSHORE_LEAKS_OFFICERS",         # canonical: FED_ICIJ_OFFSHORELEAKS_OFFICERS
    "ICIJ_OFFSHORE_LEAKS_RELATIONSHIPS",    # canonical: FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS
    "FED_IRS_527_ORGS",                     # canonical: IRS527_8871_ORGS
    "FED_FDA_GUDID__STAGING",               # loader scratch table, not a source
}

MAX_KEY_COLS_PER_TABLE = 16  # guard against a runaway aggregate query
PREFIX_CAP = 128             # distinct LEFT(v,2) prefixes kept per key column
CHECKPOINT_EVERY = 25        # partial JSON write cadence (a 2h run must survive a crash)
FMT = 2                      # bump when per-key fields change; resume skips same-fmt entries


def landed_tables(conn) -> list[str]:
    """Return non-portal tables + portal tables that carry a STEEL/STRONG entity key.

    Portal tables are only included if their columns match at least one hard entity
    key (EIN/NPI/UEI/CIK/etc.) -- the connectable-first gate. This keeps NAME/ZIP-only
    city scrapes out while activating portals that can actually link to the spine.
    """
    from .keys import ENTITY_KEYS, detect_key

    # Core tables (non-portal) -- always included
    sql = f"""
        SELECT TABLE_NAME
        FROM {db.RAW_DB}.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{db.RAW_SCHEMA}' AND TABLE_TYPE = 'BASE TABLE'
              AND TABLE_NAME NOT LIKE 'PORTAL_%%'
        ORDER BY TABLE_NAME
    """
    core = [r[0] for r in db.rows(conn, sql) if r[0] not in SKIP_TABLES]

    # Portal tables -- only those with at least one STEEL/STRONG entity key column
    portal_sql = f"""
        SELECT t.TABLE_NAME, c.COLUMN_NAME
        FROM {db.RAW_DB}.INFORMATION_SCHEMA.TABLES t
        JOIN {db.RAW_DB}.INFORMATION_SCHEMA.COLUMNS c
            ON c.TABLE_SCHEMA = t.TABLE_SCHEMA AND c.TABLE_NAME = t.TABLE_NAME
        WHERE t.TABLE_SCHEMA = '{db.RAW_SCHEMA}' AND t.TABLE_TYPE = 'BASE TABLE'
              AND t.TABLE_NAME LIKE 'PORTAL_%%'
        ORDER BY t.TABLE_NAME
    """
    portal_rows = db.rows(conn, portal_sql)
    from collections import defaultdict
    table_cols = defaultdict(list)
    for tbl, col in portal_rows:
        if tbl not in SKIP_TABLES:
            table_cols[tbl].append(col)

    entity_key_set = set(ENTITY_KEYS)
    connectable_portals = []
    for tbl, cols in table_cols.items():
        for col in cols:
            key, _tier = detect_key(col)
            if key and key in entity_key_set:
                connectable_portals.append(tbl)
                break

    return core + sorted(set(connectable_portals))


def table_columns(conn, table: str) -> list[str]:
    sql = f"""
        SELECT COLUMN_NAME
        FROM {db.RAW_DB}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{db.RAW_SCHEMA}' AND TABLE_NAME = '{table}'
        ORDER BY ORDINAL_POSITION
    """
    return [r[0] for r in db.rows(conn, sql)]


def _key_columns(columns: list[str]) -> list[dict]:
    """Detect the key-bearing columns of a table (skip provenance columns)."""
    out = []
    for c in columns:
        if c.startswith("_"):  # _INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256
            continue
        key, tier = detect_key(c)
        if key:
            out.append({"column": c, "key": key, "tier": tier, "mode": join_mode(key)})
    return out


def fingerprint_table(conn, table: str) -> dict:
    cols = table_columns(conn, table)
    keycols = _key_columns(cols)
    rows_total = db.scalar(conn, f"SELECT COUNT(*) FROM {db.fqn(table)}") or 0

    # Measure population for the VALUE keys in one scan. Spatial keys (lat/lon,
    # geometry) get a plain non-null count (distinct is meaningless for geometry).
    measured = keycols[:MAX_KEY_COLS_PER_TABLE]
    if len(keycols) > MAX_KEY_COLS_PER_TABLE:
        print(f"    [cap] {table}: measuring {MAX_KEY_COLS_PER_TABLE}/{len(keycols)} key cols")

    selects = []
    for i, kc in enumerate(measured):
        qc = quote_ident(kc["column"])
        if kc["mode"] == "value":
            expr = normalize_sql(kc["key"], qc)
        else:
            expr = f"TRY_TO_DOUBLE(TO_VARCHAR({qc}))" if kc["key"] == "LATLON" else qc
        selects.append(f"COUNT({expr}) AS nn_{i}")
        if kc["mode"] == "value":
            selects.append(f"APPROX_COUNT_DISTINCT({expr}) AS nd_{i}")
            # fmt 2: value range + prefix set, same scan (absence-null conditioning)
            selects.append(f"MIN({expr}) AS mn_{i}")
            selects.append(f"MAX({expr}) AS mx_{i}")
            selects.append(f"ARRAY_SLICE(ARRAY_AGG(DISTINCT LEFT({expr}, 2)), 0, {PREFIX_CAP}) AS px_{i}")
            selects.append(f"APPROX_COUNT_DISTINCT(LEFT({expr}, 2)) AS pn_{i}")
        else:
            selects.append(f"COUNT(DISTINCT {qc}) AS nd_{i}")

    stats = {}
    if selects:
        row = db.dicts(conn, f"SELECT {', '.join(selects)} FROM {db.fqn(table)}")[0]
        for i, kc in enumerate(measured):
            entry = {"nn": int(row[f"NN_{i}"] or 0), "nd": int(row[f"ND_{i}"] or 0)}
            if kc["mode"] == "value":
                px = row.get(f"PX_{i}")
                if isinstance(px, str):
                    px = json.loads(px)
                entry.update({
                    "mn": row.get(f"MN_{i}"), "mx": row.get(f"MX_{i}"),
                    "px": sorted(px or []), "pn": int(row.get(f"PN_{i}") or 0),
                })
            stats[i] = entry

    keys_out = []
    for i, kc in enumerate(measured):
        st = stats.get(i, {"nn": 0, "nd": 0})
        out = {
            **kc,
            "nonnull": st["nn"],
            "distinct": st["nd"],
            "populated_pct": round(st["nn"] / rows_total * 100, 1) if rows_total else 0.0,
        }
        if kc["mode"] == "value":
            out.update({
                "min": st.get("mn"), "max": st.get("mx"),
                "prefixes": st.get("px", []), "prefix_count": st.get("pn", 0),
            })
        keys_out.append(out)
    return {"rows": rows_total, "fmt": FMT, "keys": keys_out}


def run(tables: list[str] | None = None, write: bool = True, resume: bool = False) -> dict:
    """resume=True keeps existing SAME-FMT entries and only fingerprints the
    rest — the crash-recovery path for the multi-hour full sweep. A fmt bump
    naturally invalidates every old entry."""
    result: dict = {}
    if resume and OUT.exists():
        prior = json.loads(OUT.read_text())
        result = {t: e for t, e in prior.items() if e.get("fmt") == FMT}
        if result:
            print(f"resume: keeping {len(result)} fmt-{FMT} entries")

    conn = db.connect()
    try:
        targets = tables or landed_tables(conn)
        todo = [t for t in targets if t not in result]
        print(f"fingerprinting {len(todo)} landed tables ({len(targets) - len(todo)} skipped) ...")
        for n, t in enumerate(todo, 1):
            try:
                fp = fingerprint_table(conn, t)
            except Exception as exc:
                print(f"  FAIL {t}: {exc}")
                continue
            live = [k for k in fp["keys"] if k["populated_pct"] > 0]
            tags = ", ".join(f"{k['key']}({k['populated_pct']:.0f}%)" for k in live) or "—"
            print(f"  [{n}/{len(todo)}] {t:<42} rows={fp['rows']:>10,}  keys: {tags}", flush=True)
            result[t] = fp
            if write and n % CHECKPOINT_EVERY == 0:
                OUT.parent.mkdir(parents=True, exist_ok=True)
                OUT.write_text(json.dumps(result, indent=2))
    finally:
        conn.close()

    if write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2))
        print(f"\nwrote {OUT}")
    return result


if __name__ == "__main__":
    run()
