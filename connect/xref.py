"""Mine the warehouse for tables that are secretly ID crosswalks.

WHY THIS EXISTS
The spine connects rows that share ONE id value ("same NPI = same doctor"). That is
identity, and it is zero-false-merge by construction. But it can only ever connect
datasets that use the SAME id system. A table keyed on NPI and a table keyed on EIN
are strangers forever, no matter how much data each holds.

The unlock: some tables carry TWO DIFFERENT id types ON THE SAME ROW. When CMS puts
an NPI and a CCN in one row, or EPA puts a facility id and an LEI in one row, the
publisher has ASSERTED that those two ids describe the same real-world thing. That is
a translation dictionary between two id systems, published by the agency, requiring no
fuzzy matching and no inference.

Nobody had ever swept for these. This does, mechanically, over every landing table.

WHAT THIS IS NOT
These are BRIDGES (relationships), not IDENTITIES, and they do NOT go in the spine.
spine.py's docstring already makes this argument: fusing an NPI and a CCN into one
entity would merge a doctor with the hospital they work at. So a bridge is written to
ENTITY_XREF as a traversable edge, and a query hops it explicitly. The hop stays
visible to whoever reads the finding.

THE TRAP THIS GUARDS AGAINST (CLAUDE.md section 7)
Two id columns existing in a table's schema proves nothing. The pair is only a bridge
if BOTH ids are populated ON THE SAME ROWS. A table can have a fully-populated NPI and
an EIN column that is 100% empty string -- that is not a crosswalk, it is a column
someone forgot to fill. So every candidate pair is measured with
COUNT(DISTINCT normalized) on BOTH sides plus a co-populated row count, using the
spine's own normalizers, and anything that fails is rejected to a CSV rather than
written.

    python -m connect.xref                  # sweep + report, writes nothing
    python -m connect.xref --write          # persist ENTITY_XREF
    python -m connect.xref --min-pairs 100  # raise the bar
"""

from __future__ import annotations

import argparse
import csv
import os
import uuid

from . import db, store
from .keys import NORM_RULES, normalize_sql, quote_ident

XREF_FQN = store.cfqn("ENTITY_XREF")

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")

# Id types worth bridging. Deliberately narrower than keys.ENTITY_KEYS: a bridge is
# only meaningful between things that ARE entities. Excluded on purpose:
#   NAICS / SIC / NCES -- classification codes, not identities (D17, discover.py)
#   ZIP / STATE / FIPS / COUNTRY -- geography, not identity
#   NAME / PERSON / ADDRESS -- fuzzy by nature; belongs in the gated resolver
#   ACCESSION_NUMBER / CUSIP -- a filing is not an entity, a security is not an org
#                               (2026-07-30 call); these wire as edges off CIK later
BRIDGEABLE = [
    "NPI", "CCN", "EIN", "CIK", "UEI", "LEI", "DUNS", "DEA_NO",
    "FRS_ID", "PWSID", "MINE_ID", "NPDES_ID",
    "FEC_CMTE_ID", "FEC_CAND_ID", "BIOGUIDE", "ICPSR", "IMO", "MMSI",
]

# Column-name -> id type. Explicit rather than via keys.detect_key() because a bridge
# needs to know WHICH physical column carries WHICH id, and detect_key() answers
# "does this column carry an id?" not "which of three NPI-ish columns is the subject".
#
# CAUTION on the commented-out entries: these are columns that LOOK like a second id
# but name a DIFFERENT party than the row is about. Wiring them would assert that two
# parties to a relationship are one thing.
COL_TO_KEY = {
    # --- NPI ---------------------------------------------------------------
    "NPI": "NPI", "PROVIDER_NPI": "NPI", "ORG_NPI": "NPI",
    "RNDRNG_NPI": "NPI", "PRSCRBR_NPI": "NPI", "PRESCRIBER_NPI": "NPI",
    "SUPPLIER_NPI": "NPI", "COVERED_RECIPIENT_NPI": "NPI",
    # REFERRING_NPI deliberately excluded: the referrer is a DIFFERENT doctor
    # than the rendering provider on the same claim row.
    # --- CCN ---------------------------------------------------------------
    "CCN": "CCN", "PROVIDER_CCN": "CCN", "PRVDR_NUM": "CCN",
    "CMS_CERTIFICATION_NUMBER": "CCN", "CMS_CERTIFICATION_NUMBER_CCN": "CCN",
    "CMS_CERTIFICATION_NUMBER__CCN": "CCN", "FEDERAL_PROVIDER_NUMBER": "CCN",
    "CAH_OR_HOSPITAL_CCN": "CCN",
    # --- EIN ---------------------------------------------------------------
    "EIN": "EIN", "TAX_ID": "EIN", "EMPLOYER_IDENTIFICATION_NUMBER": "EIN",
    "EIN_NUMBER": "EIN", "AUDITEE_EIN": "EIN",
    # AUDITOR_EIN excluded: the audit FIRM is not the audited organization.
    # That pair is a real edge (who audits whom) but a different KIND of edge --
    # see the shared-paperwork idea; it is not an identity crosswalk.
    # --- CIK / securities issuers ------------------------------------------
    "CIK": "CIK", "CENTRAL_INDEX_KEY": "CIK", "CIK_NUMBER": "CIK",
    "RPTOWNERCIK": "CIK", "PARENT_CIK": "CIK",
    # --- UEI / federal award recipients ------------------------------------
    "UEI": "UEI", "RECIPIENT_UEI": "UEI", "AWARDEE_UEI": "UEI",
    "UNIQUE_ENTITY_ID": "UEI", "PARENT_UEI": "UEI",
    # --- LEI ---------------------------------------------------------------
    "LEI": "LEI", "LEI_CODE": "LEI", "LEGAL_ENTITY_IDENTIFIER": "LEI",
    "MATCHED_LEI": "LEI", "ULTIMATE_PARENT_LEI": "LEI",
    # --- misc org ids ------------------------------------------------------
    "DUNS": "DUNS", "DUNS_NUMBER": "DUNS",
    "DEA_NO": "DEA_NO", "DEA_NUMBER": "DEA_NO",
    # ARCOS BUYER_DEA_NO / REPORTER_DEA_NO are the two SIDES of a shipment --
    # excluded, they are a flow edge not an identity.
    # --- environmental facility ids ----------------------------------------
    "FRS_ID": "FRS_ID", "REGISTRY_ID": "FRS_ID", "EPA_REGISTRY_ID": "FRS_ID",
    "PWSID": "PWSID", "PWS_ID": "PWSID",
    # SELLER_PWSID excluded: that is the water system SELLING to this one.
    "MINE_ID": "MINE_ID", "MINE_ID_NUMBER": "MINE_ID",
    "NPDES_ID": "NPDES_ID",
    # --- political ---------------------------------------------------------
    "CMTE_ID": "FEC_CMTE_ID", "FEC_CMTE_ID": "FEC_CMTE_ID",
    "CAND_ID": "FEC_CAND_ID", "FEC_CAND_ID": "FEC_CAND_ID",
    "BIOGUIDE": "BIOGUIDE", "BIOGUIDE_ID": "BIOGUIDE",
    "ICPSR": "ICPSR", "ICPSR_ID": "ICPSR",
    # --- vessels -----------------------------------------------------------
    "IMO": "IMO", "IMO_NUMBER": "IMO", "MMSI": "MMSI",
}

# A pair must clear ALL of these to be written.
MIN_PAIRS = 25        # fewer distinct pairs than this is an accident, not a dictionary
MIN_COPOP_PCT = 1.0   # under this % of rows carrying BOTH ids, the pair is incidental


def candidate_tables(conn, only_tables=None) -> dict[str, dict[str, str]]:
    """Landing tables carrying 2+ distinct bridgeable id types.

    Returns {table_name: {key_type: column_name}}. PORTAL_* is skipped -- those are
    the harvested open-data portal tables, one level down in the raw layer, and
    discover.py already excludes them from the edge universe for the same reason.
    """
    rows = db.rows(conn, """
        SELECT TABLE_NAME, COLUMN_NAME
        FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'LANDING' AND TABLE_NAME NOT LIKE 'PORTAL_%'
    """)
    per_table: dict[str, dict[str, str]] = {}
    for tbl, col in rows:
        key = COL_TO_KEY.get(col.upper())
        if not key or key not in BRIDGEABLE or key not in NORM_RULES:
            continue
        # First column wins per key type -- COL_TO_KEY is already curated so that a
        # table's several NPI-ish columns collapse to the subject one.
        per_table.setdefault(tbl.upper(), {}).setdefault(key, col)
    out = {t: k for t, k in per_table.items() if len(k) >= 2}
    if only_tables:
        out = {t: k for t, k in out.items() if t in only_tables}
    return out


def measure_pair(conn, table: str, key_a: str, col_a: str, key_b: str, col_b: str) -> dict:
    """Measure one candidate pair with the SPINE'S normalizers.

    The number that decides is CO-POPULATED rows -- rows where BOTH ids survive
    normalization. Everything else (either id alone) is already covered by the spine.
    """
    na = normalize_sql(key_a, quote_ident(col_a))
    nb = normalize_sql(key_b, quote_ident(col_b))
    row = db.rows(conn, f'''
        SELECT COUNT(*),
               COUNT({na}),
               COUNT({nb}),
               COUNT(CASE WHEN {na} IS NOT NULL AND {nb} IS NOT NULL THEN 1 END),
               COUNT(DISTINCT CASE WHEN {na} IS NOT NULL AND {nb} IS NOT NULL
                                   THEN {na} || '>' || {nb} END)
        FROM {db.fqn(table)}
    ''')[0]
    total, a_pop, b_pop, copop, distinct_pairs = (int(v or 0) for v in row)

    sample = []
    if copop:
        sample = db.rows(conn, f'''
            SELECT DISTINCT {na}, {nb} FROM {db.fqn(table)}
            WHERE {na} IS NOT NULL AND {nb} IS NOT NULL LIMIT 3
        ''')

    # Fan-out: how many B values does a single A map to, at worst. A clean crosswalk
    # is near 1. A high number means this is a one-to-many relationship table, which
    # is still useful but is NOT a translation dictionary -- flagged, not rejected,
    # because "this hospital has 400 affiliated doctors" is a true and useful edge.
    max_fanout = 0
    if copop:
        max_fanout = int(db.scalar(conn, f'''
            SELECT MAX(n) FROM (
              SELECT COUNT(DISTINCT {nb}) AS n FROM {db.fqn(table)}
              WHERE {na} IS NOT NULL AND {nb} IS NOT NULL GROUP BY {na})
        ''') or 0)

    ev = {
        "table": table, "key_a": key_a, "col_a": col_a, "key_b": key_b, "col_b": col_b,
        "rows": total, "a_populated": a_pop, "b_populated": b_pop,
        "copopulated": copop,
        "copop_pct": round(100.0 * copop / (total or 1), 2),
        "distinct_pairs": distinct_pairs, "max_fanout": max_fanout,
        "sample": " | ".join(f"{a}>{b}" for a, b in sample),
        "reject_reason": "",
    }
    reasons = []
    if copop == 0:
        # The exact trap this script exists for: both columns present in the schema,
        # never both filled on one row.
        reasons.append(f"0 rows carry both ids ({key_a} populated on {a_pop:,}, "
                       f"{key_b} on {b_pop:,}) -- schema pair, not a crosswalk")
    elif distinct_pairs < MIN_PAIRS:
        reasons.append(f"only {distinct_pairs} distinct pair(s)")
    elif ev["copop_pct"] < MIN_COPOP_PCT:
        reasons.append(f"only {ev['copop_pct']}% of rows carry both ids")
    ev["reject_reason"] = "; ".join(reasons)
    return ev


def _write_xref(conn, verified: list[dict], run_id: str) -> int:
    """Materialize ENTITY_XREF from the verified pairs.

    One row per (key_a, value_a, key_b, value_b, source_table). Deliberately stores
    BOTH directions' worth of information in one row rather than duplicating -- a
    traversal query does its own UNION, and duplicating would double a 10M-row table
    for no gain.

    RELATION defaults to 'asserted_same_row': the publisher put these two ids on one
    row. That is the whole claim, and it is exactly as strong as the publisher. Rows
    from a crosswalk that carries its own confidence (the EPA corporate crosswalk has
    MATCH_METHOD / MATCH_CONFIDENCE) should later be upgraded to carry it; until then
    every row is labelled honestly as an assertion, not a verified identity.
    """
    store.ensure_schema(conn)
    staging = store.cfqn("ENTITY_XREF__STAGING")
    db.rows(conn, f'''CREATE OR REPLACE TABLE {staging} (
        KEY_A STRING, VALUE_A STRING, KEY_B STRING, VALUE_B STRING,
        SOURCE_TABLE STRING, RELATION STRING, FANOUT NUMBER,
        RUN_ID STRING, BUILT_AT TIMESTAMP_NTZ)''')

    written = 0
    for ev in verified:
        na = normalize_sql(ev["key_a"], quote_ident(ev["col_a"]))
        nb = normalize_sql(ev["key_b"], quote_ident(ev["col_b"]))
        # one-to-one pairs are a dictionary; one-to-many is a relationship
        relation = "asserted_same_row" if ev["max_fanout"] <= 1 else "asserted_affiliation"
        db.rows(conn, f'''
            INSERT INTO {staging}
            SELECT DISTINCT '{ev["key_a"]}', {na}, '{ev["key_b"]}', {nb},
                   '{ev["table"]}', '{relation}', {ev["max_fanout"]},
                   '{run_id}', CURRENT_TIMESTAMP()
            FROM {db.fqn(ev["table"])}
            WHERE {na} IS NOT NULL AND {nb} IS NOT NULL
        ''')
        written += ev["distinct_pairs"]

    db.rows(conn, f'''CREATE TABLE IF NOT EXISTS {XREF_FQN} (
        KEY_A STRING, VALUE_A STRING, KEY_B STRING, VALUE_B STRING,
        SOURCE_TABLE STRING, RELATION STRING, FANOUT NUMBER,
        RUN_ID STRING, BUILT_AT TIMESTAMP_NTZ)''')
    db.rows(conn, f"ALTER TABLE {staging} SWAP WITH {XREF_FQN}")
    db.rows(conn, f"DROP TABLE IF EXISTS {staging}")
    return int(db.scalar(conn, f"SELECT COUNT(*) FROM {XREF_FQN}") or 0)


def run(write: bool = False, only_tables=None, min_pairs: int = MIN_PAIRS) -> dict:
    global MIN_PAIRS
    MIN_PAIRS = min_pairs
    run_id = uuid.uuid4().hex[:16]
    conn = db.connect()
    verified, rejected = [], []
    try:
        cands = candidate_tables(conn, only_tables)
        print(f"xref sweep: {len(cands)} landing tables carry 2+ bridgeable id types\n")

        for table in sorted(cands):
            keys = cands[table]
            items = sorted(keys.items())
            # every unordered pair of id types on this table
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    (ka, ca), (kb, cb) = items[i], items[j]
                    try:
                        ev = measure_pair(conn, table, ka, ca, kb, cb)
                    except Exception as exc:
                        print(f"  ERR    {table:52} {ka}<->{kb}: "
                              f"{type(exc).__name__}: {str(exc)[:70]}")
                        continue
                    if ev["reject_reason"]:
                        rejected.append(ev)
                        print(f"  reject {table:52} {ka}<->{kb}: {ev['reject_reason']}")
                    else:
                        verified.append(ev)
                        kind = "1:1" if ev["max_fanout"] <= 1 else f"1:{ev['max_fanout']}"
                        print(f"  BRIDGE {table:52} {ka:>11}<->{kb:<11} "
                              f"{ev['distinct_pairs']:>9,} pairs  {kind:>8}  "
                              f"{ev['copop_pct']:>6}% co-pop")

        os.makedirs(OUT_DIR, exist_ok=True)
        cols = ["table", "key_a", "col_a", "key_b", "col_b", "rows", "a_populated",
                "b_populated", "copopulated", "copop_pct", "distinct_pairs",
                "max_fanout", "sample", "reject_reason"]
        for path, data in ((os.path.join(OUT_DIR, "xref_bridges.csv"), verified),
                           (os.path.join(OUT_DIR, "xref_rejects.csv"), rejected)):
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
                w.writeheader()
                for r in data:
                    w.writerow(r)

        total_pairs = sum(e["distinct_pairs"] for e in verified)
        print(f"\n{len(verified)} bridges verified, {len(rejected)} rejected; "
              f"{total_pairs:,} distinct id pairs available")
        # Which id systems does this connect that the spine cannot?
        links = sorted({tuple(sorted((e["key_a"], e["key_b"]))) for e in verified})
        print(f"id systems bridged: " + ", ".join(f"{a}<->{b}" for a, b in links))

        if write:
            n = _write_xref(conn, verified, run_id)
            print(f"\nENTITY_XREF written: {n:,} rows -> {XREF_FQN}")
        else:
            print("\n(dry run -- pass --write to persist ENTITY_XREF)")
    finally:
        conn.close()
    return {"bridges": len(verified), "rejected": len(rejected)}


def main() -> int:
    ap = argparse.ArgumentParser(prog="connect.xref")
    ap.add_argument("--write", action="store_true", help="persist ENTITY_XREF")
    ap.add_argument("--tables", help="comma-separated landing tables to limit the sweep")
    ap.add_argument("--min-pairs", type=int, default=MIN_PAIRS)
    args = ap.parse_args()
    only = ({t.strip().upper() for t in args.tables.split(",") if t.strip()}
            if args.tables else None)
    run(write=args.write, only_tables=only, min_pairs=args.min_pairs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
