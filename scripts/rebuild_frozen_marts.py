"""Recover real rows trapped behind stale / LIMIT-capped marts (evidence.dev readiness).

Seven marts froze because their dbt staging models selected columns that no longer exist
in the current landing table (schema drifted) or were LIMIT-capped -- so the mart (and the
THE_LIBRARY reading-room view over it) shows a fraction of, or none of, the real data while
the full rows sit in LIBRARY_RAW.LANDING. Verified live:

    source_id                          what evidence.dev sees now   real landing rows
    intl_ie_cro                        DARK (view def broken)       818,934
    fed_federal_register_documents     5,000 (LIMIT-capped mart)     94,731
    fed_slavevoyages_intraamerican     11,521 (raw, no clean mart)   11,521
    fed_naag_multistate_settlements    882 (raw, no clean mart)         882
    fed_hhs_taggs                      not surfaced at all               45
    intl_es_borme                      3 (frozen mart)                   25
    fed_doj_fca_settlements            12 (frozen mart)                  19
                                                          TOTAL     ~926,157

This script is SELF-CONTAINED -- NO dbt. For each mart it introspects the CURRENT landing
columns and rebuilds the mart as a clean projection straight over current landing:
snake_case rename, TRIM on text, TRY_TO_NUMBER on plain year columns, ingest-lineage columns
kept. NO dedup, NO LIMIT, NO WHERE -- so rebuilt rowcount == full landing count (that IS the
recovery proof). Deliberately conservative on typing: leading-zero codes (EIN/ZIP/FIPS) and
trap dates (LEIE-style YYYYMMDD, 8-digit epoch traps) stay TEXT so nothing is destroyed; real
casting belongs in a staging layer later.

  LIBRARY_MARTS.DBT_CROGERS.<mart>   rebuilt table (COPY GRANTS + explicit re-GRANT)
  THE_LIBRARY.<schema>.<view>        friendly reading-room view repointed at the clean mart
                                     (CREATE OR REPLACE VIEW ... COPY GRANTS + re-GRANT)

    python3 scripts/rebuild_frozen_marts.py           # PREVIEW: per-mart DDL + now/landing/rebuilt counts
    python3 scripts/rebuild_frozen_marts.py --apply    # rebuild marts + refresh views + verify

GRANTS (audit bug D04): CREATE OR REPLACE on an object a read role can see STRIPS its grants.
Every rebuild uses COPY GRANTS *and* an explicit GRANT SELECT to RIPPLE_READER +
CLAUDE_MCP_READONLY afterward (COPY GRANTS is a no-op on brand-new objects, so the explicit
grant is what keeps the read lane lit for the marts that don't exist yet). Verified with
SHOW GRANTS after apply.

Idempotent + re-runnable: CREATE OR REPLACE + idempotent grants. Rollback DDL for every object
touched is snapshotted to outputs/ before any --apply write. Chris runs --apply; the agent's
classifier blocks it as a shared-state write.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

MART_DB = "LIBRARY_MARTS"
MART_SCHEMA = "DBT_CROGERS"          # the canonical marts schema in this warehouse
READ_ROLES = ("RIPPLE_READER", "CLAUDE_MCP_READONLY")

# Ingest-lineage columns arrive under two spellings across sources -> one canonical alias.
META_ALIAS = {
    "_INGESTED_AT": "_ingested_at", "INGESTED_AT": "_ingested_at",
    "_SOURCE_RUN_ID": "_source_run_id", "SOURCE_RUN_ID": "_source_run_id",
    "_SRC_SHA256": "_src_sha256", "SRC_SHA256": "_src_sha256",
}
# Plain integer-year columns -- safe to TRY_TO_NUMBER (no '$', no leading-zero-code risk).
YEAR_COLS = {"YEAR", "FISCAL_YEAR", "YEARAM"}

# One entry per frozen mart. the_library_fqn=None -> mart is rebuilt but there is no
# reading-room view yet (reported so Chris can add it via thelibrary_build).
MARTS = [
    {"source_id": "intl_ie_cro", "landing": "INTL_IE_CRO",
     "mart": "CORPORATE_REGISTRY__INTL_IE_CRO",
     "view": "THE_LIBRARY.COMPANIES.IRELAND_COMPANIES",
     "comment": "Irish CRO company register -- every registered company, status, type, address, "
                "NACE code. Recovered from landing (was frozen at 1 row). Rebuilt straight over "
                "current landing; codes kept as text. company_num joins Irish corporate filings."},
    {"source_id": "fed_federal_register_documents", "landing": "FED_FEDERAL_REGISTER_DOCUMENTS",
     "mart": "REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS",
     "view": "THE_LIBRARY.GOVERNMENT.FEDERAL_REGISTER_DOCUMENTS",
     "comment": "US Federal Register documents -- rules, notices, proclamations, executive orders "
                "with agencies, citations, dates, URLs. Recovered from landing (was LIMIT-capped "
                "at 5,000). document_number is the key."},
    {"source_id": "fed_slavevoyages_intraamerican", "landing": "FED_SLAVEVOYAGES_INTRAAMERICAN",
     "mart": "HISTORY__FED_SLAVEVOYAGES_INTRAAMERICAN",
     "view": "THE_LIBRARY.HISTORY.INTRA_AMERICAN_SLAVE_VOYAGES",
     "comment": "SlaveVoyages Intra-American database -- one row per documented voyage (ship, "
                "captain, owners, ports, dates, counts). Clean projection over current landing; "
                "wide historical source, all fields kept as text."},
    {"source_id": "fed_naag_multistate_settlements", "landing": "FED_NAAG_MULTISTATE_SETTLEMENTS",
     "mart": "JUSTICE__FED_NAAG_MULTISTATE_SETTLEMENTS",
     "view": "THE_LIBRARY.JUSTICE.AG_MULTISTATE_SETTLEMENTS",
     "comment": "NAAG multistate settlements -- one row per multistate AG settlement (defendants, "
                "amounts, participating states, issue area, NAICS). Amounts kept as text (may carry "
                "currency formatting); cast in staging later."},
    {"source_id": "fed_hhs_taggs", "landing": "FED_HHS_TAGGS",
     "mart": "SPENDING__FED_HHS_TAGGS",
     "view": None,   # no reading-room view exists yet -- reported, not invented
     "comment": "HHS TAGGS grant awards -- award number, recipient (name/EIN/geo), amount, "
                "assistance-listing (CFDA) number. recipient_ein + recipient_fips are join keys; "
                "kept as text (leading zeros)."},
    {"source_id": "intl_es_borme", "landing": "INTL_ES_BORME",
     "mart": "CORPORATE_REGISTRY__INTL_ES_BORME",
     "view": "THE_LIBRARY.COMPANIES.SPAIN_COMPANY_FILINGS",
     "comment": "Spanish BORME company filings -- one row per registry act (company, act type, "
                "province, CVE, PDF). Recovered from landing (was frozen at 3 rows)."},
    {"source_id": "fed_doj_fca_settlements", "landing": "FED_DOJ_FCA_SETTLEMENTS",
     "mart": "JUSTICE__FED_DOJ_FCA_SETTLEMENTS",
     "view": "THE_LIBRARY.JUSTICE.FRAUD_SETTLEMENTS",
     "comment": "DOJ False Claims Act settlements -- defendant, amount, qui tam / relator, fraud "
                "type, agency defrauded, district. Recovered from landing (was frozen at 12 rows)."},
]


def esc(s: str) -> str:
    return (s or "").replace("'", "''")


def cols_of(cur, landing: str) -> list[str]:
    cur.execute(
        "SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION", (landing,))
    return [r[0] for r in cur.fetchall()]


def build_select(cols: list[str], landing_fqn: str) -> str:
    """Clean projection over CURRENT landing columns: snake_case + light, non-destructive typing."""
    proj = []
    for c in cols:
        if c in META_ALIAS:
            proj.append(f'"{c}" AS {META_ALIAS[c]}')          # lineage col, pass through as-is
        elif c in YEAR_COLS:
            proj.append(f'TRY_TO_NUMBER(TRIM("{c}")) AS {c.lower()}')
        else:
            proj.append(f'TRIM("{c}") AS {c.lower()}')         # everything else stays text, trimmed
    return "SELECT\n  " + ",\n  ".join(proj) + f"\nFROM {landing_fqn}"


def mart_ddl(m: dict, select_sql: str) -> str:
    fqn = f"{MART_DB}.{MART_SCHEMA}.{m['mart']}"
    return (f"CREATE OR REPLACE TABLE {fqn} COPY GRANTS\n"
            f"COMMENT='{esc(m['comment'])}' AS\n{select_sql}")


def view_ddl(m: dict) -> str | None:
    if not m["view"]:
        return None
    fqn = f"{MART_DB}.{MART_SCHEMA}.{m['mart']}"
    return (f"CREATE OR REPLACE VIEW {m['view']} COPY GRANTS\n"
            f"COMMENT='{esc(m['comment'])}' AS SELECT * FROM {fqn}")


def scalar(cur, sql: str):
    cur.execute(sql)
    return cur.fetchone()[0]


def try_get_ddl(cur, kind: str, fqn: str) -> str | None:
    try:
        cur.execute(f"SELECT GET_DDL('{kind}','{fqn}')")
        return cur.fetchone()[0]
    except Exception:
        return None


def mart_exists(cur, m: dict) -> bool:
    cur.execute(
        "SELECT COUNT(*) FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s", (MART_SCHEMA, m["mart"]))
    return cur.fetchone()[0] > 0


def view_now_count(cur, m: dict):
    """What the reading room currently shows (the frozen number). None if dark/absent."""
    if not m["view"]:
        return None
    try:
        return scalar(cur, f"SELECT COUNT(*) FROM {m['view']}")
    except Exception:
        return None   # e.g. IRELAND_COMPANIES -- broken view definition (fully dark)


def main() -> int:
    ap = argparse.ArgumentParser(description="Rebuild frozen marts from current landing.")
    ap.add_argument("--apply", action="store_true", help="rebuild (default: preview)")
    ap.add_argument("--only", help="comma-separated source_ids to limit to")
    args = ap.parse_args()

    from connect import db
    conn = db.connect()
    cur = conn.cursor()

    marts = MARTS
    if args.only:
        want = {s.strip().lower() for s in args.only.split(",")}
        marts = [m for m in MARTS if m["source_id"] in want]

    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    roll = REPO / "outputs" / f"_rollback_frozen_marts_{ts}.sql"

    plans = []
    total_now = total_land = total_rebuilt = 0
    print(f"{'[APPLY]' if args.apply else '[PREVIEW]'} rebuild_frozen_marts -- "
          f"{len(marts)} mart(s), schema {MART_DB}.{MART_SCHEMA}\n")

    for m in marts:
        landing_fqn = f"LIBRARY_RAW.LANDING.{m['landing']}"
        cols = cols_of(cur, m["landing"])
        if not cols:
            print(f"  !! {m['source_id']}: landing {m['landing']} not found -- skipping")
            continue
        select_sql = build_select(cols, landing_fqn)

        land_n = scalar(cur, f"SELECT COUNT(*) FROM {landing_fqn}")
        rebuilt_n = scalar(cur, f"SELECT COUNT(*) FROM (\n{select_sql}\n)")
        now_n = view_now_count(cur, m)
        exists = mart_exists(cur, m)

        total_land += land_n
        total_rebuilt += rebuilt_n
        total_now += (now_n or 0)

        now_disp = "DARK/absent" if now_n is None else f"{now_n:,}"
        print("=" * 78)
        print(f"  {m['source_id']}  ->  {MART_DB}.{MART_SCHEMA}.{m['mart']}"
              f"  ({'exists' if exists else 'NEW'})")
        print(f"    reading-room now: {now_disp:>12}   |   landing: {land_n:>10,}   "
              f"|   REBUILT: {rebuilt_n:>10,}   ({len(cols)} cols)")
        if m["view"]:
            print(f"    view -> {m['view']}")
        else:
            print(f"    view -> (none yet; add to THE_LIBRARY via thelibrary_build after apply)")
        if rebuilt_n != land_n:
            print(f"    !! WARN: rebuilt {rebuilt_n:,} != landing {land_n:,} "
                  f"(projection should be lossless) -- inspect before apply")
        plans.append((m, select_sql, exists))

    print("=" * 78)
    print(f"  TOTAL   reading-room now (sum): {total_now:>12,}   |   "
          f"landing: {total_land:>12,}   |   REBUILT: {total_rebuilt:>12,}")
    print(f"  net rows recovered into the marts: {total_rebuilt - total_now:,}")

    if not args.apply:
        print("\n  --- DDL that --apply would run (per mart) ---")
        for m, select_sql, _ in plans:
            print("\n" + "-" * 78)
            print(mart_ddl(m, select_sql) + ";")
            for role in READ_ROLES:
                print(f"GRANT SELECT ON TABLE {MART_DB}.{MART_SCHEMA}.{m['mart']} TO ROLE {role};")
            vd = view_ddl(m)
            if vd:
                print(vd + ";")
                for role in READ_ROLES:
                    print(f"GRANT SELECT ON VIEW {m['view']} TO ROLE {role};")
        print("\n  PREVIEW only -- nothing changed. Re-run with --apply.")
        conn.close()
        return 0

    # ---------------- APPLY ----------------
    # 1. snapshot rollback DDL for every object we are about to replace
    roll.parent.mkdir(parents=True, exist_ok=True)
    with open(roll, "w", encoding="utf-8") as f:
        f.write(f"-- Rollback for rebuild_frozen_marts ({ts}). Run to restore prior objects.\n\n")
        for m, _sel, exists in plans:
            mfqn = f"{MART_DB}.{MART_SCHEMA}.{m['mart']}"
            if exists:
                d = try_get_ddl(cur, "TABLE", mfqn)
                f.write(f"-- prior mart {mfqn}:\n{d};\n\n" if d else
                        f"-- prior mart {mfqn}: (GET_DDL unavailable)\n\n")
            else:
                f.write(f"-- mart {mfqn} did not exist before; to undo:\nDROP TABLE IF EXISTS {mfqn};\n\n")
            if m["view"]:
                vd = try_get_ddl(cur, "VIEW", m["view"])
                f.write(f"-- prior view {m['view']}:\n{vd};\n\n" if vd else
                        f"-- prior view {m['view']}: (GET_DDL unavailable / was broken)\n\n")
    print(f"\n  rollback DDL snapshotted -> {roll}")

    # 2. rebuild each mart + refresh its view, re-granting the read lane every time
    for m, select_sql, _exists in plans:
        mfqn = f"{MART_DB}.{MART_SCHEMA}.{m['mart']}"
        print(f"\n  rebuilding {mfqn} ...")
        cur.execute(mart_ddl(m, select_sql))
        for role in READ_ROLES:
            try:
                cur.execute(f"GRANT SELECT ON TABLE {mfqn} TO ROLE {role}")
            except Exception as e:
                print(f"    grant {role} on mart failed: {str(e)[:100]}")
        n = scalar(cur, f"SELECT COUNT(*) FROM {mfqn}")
        print(f"    mart rows now: {n:,}")

        vd = view_ddl(m)
        if vd:
            cur.execute(vd)
            for role in READ_ROLES:
                try:
                    cur.execute(f"GRANT SELECT ON VIEW {m['view']} TO ROLE {role}")
                except Exception as e:
                    print(f"    grant {role} on view failed: {str(e)[:100]}")
            vn = scalar(cur, f"SELECT COUNT(*) FROM {m['view']}")
            # verify grants preserved
            cur.execute(f"SHOW GRANTS ON VIEW {m['view']}")
            groles = {str(g[5]) for g in cur.fetchall()}
            ok = all(r in groles for r in READ_ROLES)
            print(f"    view {m['view']} rows now: {vn:,}  | read roles present: {ok}")
        else:
            print(f"    (no reading-room view -- add {m['source_id']} to THE_LIBRARY later)")

    print("\n  DONE. Verify a couple of THE_LIBRARY views in evidence.dev.")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
