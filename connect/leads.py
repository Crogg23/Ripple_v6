"""Codified cross-domain LEAD jobs -> a ranked, persisted LIBRARY_META.CONNECT.LEADS.

A "lead" is a cross-domain finding that raises its own hand instead of waiting to
be hunted: e.g. an OIG-excluded provider still affiliated with CMS facilities. Each
job is declarative config in ``leads_specs.JOBS``; this module compiles the job to
ONE targeted SQL query, scores each hit, and MERGEs the result into ``LEADS`` so
``FIRST_SEEN`` / ``LAST_SEEN`` track when a lead first appeared and was last seen
(a brand-new affiliation surfaces as a new LEAD_ID — the alerting delta).

IMPORTANT — lead jobs run their OWN SQL and MUST NOT route through ``connect.bridge``.
The bridge fan-out guard (FANOUT_MAX=40) and its dedup-vs-direct rule correctly tame
the global graph, but they silently drop high-value leads: 21 of the 38
banned-provider affiliations were gated, and the surviving edge is hidden behind a
weak ZIP edge (see build-state.md, "ENGINE NUANCE"). So this module never imports
bridge, and every job must set ``no_fanout_guard: True``.

    python -m connect leads                       # dry-run all jobs (preview, no write)
    python -m connect leads --job banned_but_operating --run
"""

from __future__ import annotations

import hashlib
import json
import uuid

import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

from . import db, store
from .keys import normalize_sql, quote_ident
from .leads_specs import JOBS

LEADS_FQN = store.cfqn("LEADS")
STAGE_FQN = store.cfqn("LEADS_STAGE")

LEADS_DDL = f"""
CREATE TABLE IF NOT EXISTS {LEADS_FQN} (
    LEAD_ID         STRING NOT NULL,
    RULE_NAME       STRING NOT NULL,
    LEFT_ENTITY_ID  STRING,          -- FK ENTITY_MAP (Phase 2 backfill)
    RIGHT_ENTITY_ID STRING,
    LEFT_KEY_TYPE   STRING,
    LEFT_KEY_VALUE  STRING,
    RIGHT_KEY_TYPE  STRING,
    RIGHT_KEY_VALUE STRING,
    TITLE           STRING,
    SCORE           FLOAT,
    EVIDENCE        VARIANT,
    EVIDENCE_COUNT  INTEGER,
    FIRST_SEEN      TIMESTAMP_NTZ,
    LAST_SEEN       TIMESTAMP_NTZ,
    RUN_ID          STRING
)
"""


def _norm(key: str, col: str) -> str:
    """Canonicalize a landing column the SAME way the rest of the engine does."""
    return normalize_sql(key, quote_ident(col))


# --------------------------------------------------------------------------- #
# Compile a JobSpec -> one targeted SQL query.
# Shape: left ⋈ right on a shared key, optional enrich-name lookup, optional
# surname corroboration, aggregate to one lead per LEFT entity, score.
# --------------------------------------------------------------------------- #
def compile_sql(spec: dict) -> str:
    L, R = spec["left"], spec["right"]
    jk = L["key"]
    if R["key"] != jk:
        raise ValueError(f"{spec['rule_name']}: left/right join keys differ ({jk} vs {R['key']})")

    l_npi, r_npi = _norm(jk, L["key_col"]), _norm(jk, R["key_col"])
    en = spec.get("enrich_name")
    ek = R.get("enrich_key")
    r_enrich = _norm(ek, R["enrich_key_col"]) if ek else "NULL"

    l_carry = "".join(f", {quote_ident(c)} AS {a}" for a, c in L.get("carry", {}).items())
    r_carry = "".join(f", {quote_ident(c)} AS {a}" for a, c in R.get("carry", {}).items())

    # NULLIF blank names: a blank surname must NOT satisfy the require_surname gate
    # ('' = '' is TRUE in SQL), and a blank first name must not score as a match.
    def _nm(col):
        return f"NULLIF(UPPER(TRIM({quote_ident(col)})), '')"

    leie = (f"SELECT {l_npi} AS NPI_N, "
            f"{_nm(L['last_col'])} AS L_LAST, {_nm(L['first_col'])} AS L_FIRST{l_carry} "
            f"FROM {db.fqn(L['table'])} WHERE {l_npi} IS NOT NULL")

    aff = (f"SELECT {r_npi} AS NPI_N, {r_enrich} AS ENRICH_N, "
           f"{_nm(R['last_col'])} AS R_LAST, {_nm(R['first_col'])} AS R_FIRST{r_carry} "
           f"FROM {db.fqn(R['table'])} WHERE {r_npi} IS NOT NULL")

    # CCN -> human facility name. DEDUPED to one name per CCN: the rosters are a
    # UNION ALL, so without this the LEFT JOIN fans out a CCN that appears in
    # multiple rosters, silently re-weighting AVG(name_match) before the GROUP BY.
    if en:
        ne = _norm(en["key"], en["key"])  # rosters all carry a `CCN` column
        union = " UNION ALL ".join(
            f"SELECT {ne} AS ENRICH_N, UPPER(TRIM({quote_ident(name)})) AS FAC_NAME "
            f"FROM {db.fqn(tbl)} WHERE {ne} IS NOT NULL"
            for tbl, name in en["tables"])
        fac_cte = f"SELECT ENRICH_N, ANY_VALUE(FAC_NAME) AS FAC_NAME FROM ( {union} ) GROUP BY ENRICH_N"
    else:
        fac_cte = "SELECT NULL AS ENRICH_N, NULL AS FAC_NAME WHERE 1=0"

    require = "AND l.L_LAST = a.R_LAST" if spec.get("require_surname") else ""
    name_match = ("IFF(l.L_FIRST = a.R_FIRST, 1.0, "
                  "IFF(LEFT(l.L_FIRST, 1) = LEFT(a.R_FIRST, 1), 0.85, 0.6))")
    fac_join = "LEFT JOIN fac f ON f.ENRICH_N = a.ENRICH_N" if en else ""

    # evidence object: ccn + facility name + any right-carry fields (e.g. facility type)
    ev = ["'ccn', a.ENRICH_N"]
    if en:
        ev.append("'facility', f.FAC_NAME")
    for alias in R.get("carry", {}):
        ev.append(f"'{alias.lower()}', a.{alias}")
    evidence = (f"TO_JSON(ARRAY_SLICE(ARRAY_AGG(DISTINCT "
                f"OBJECT_CONSTRUCT({', '.join(ev)})), 0, 50))")

    rec = L.get("recency")
    if rec:
        rexpr = f"TRY_TO_DATE(MAX({quote_ident(rec['col'])}), '{rec['format']}')"
        recency = f"IFF({rexpr} >= DATEADD('month', -{int(rec['months'])}, CURRENT_DATE), 1.0, 0.4)"
    else:
        recency = "0.7"

    sc = spec["score"]
    return f"""
WITH leie AS ( {leie} ),
aff  AS ( {aff} ),
fac  AS ( {fac_cte} ),
matched AS (
  SELECT l.NPI_N AS LEFT_KEY_VALUE,
         ANY_VALUE(l.L_LAST) AS L_LAST, ANY_VALUE(l.L_FIRST) AS L_FIRST,
         ANY_VALUE(l.EXCLTYPE) AS EXCLTYPE, MAX(l.EXCLDATE) AS EXCLDATE,
         AVG({name_match}) AS NAME_SCORE,
         {recency} AS RECENCY_SCORE,
         COUNT(DISTINCT a.ENRICH_N) AS FAC_COUNT,
         {evidence} AS EVIDENCE_JSON
  FROM leie l
  JOIN aff a ON a.NPI_N = l.NPI_N {require}
  {fac_join}
  GROUP BY l.NPI_N )
SELECT LEFT_KEY_VALUE, L_LAST, L_FIRST, EXCLTYPE, EXCLDATE, FAC_COUNT, EVIDENCE_JSON,
       ROUND({sc['name_w']} * NAME_SCORE
           + {sc['recency_w']} * RECENCY_SCORE
           + {sc['breadth_w']} * LEAST(FAC_COUNT / {sc['breadth_div']}, 1.0), 3) AS SCORE
FROM matched
ORDER BY SCORE DESC, FAC_COUNT DESC
"""


def _lead_id(rule: str, key: str, val: str) -> str:
    return "LEAD_" + hashlib.md5(f"{rule}|{key}:{val}".encode()).hexdigest()[:16]


def _fmt_date(v) -> str:
    s = str(v or "")
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 and s.isdigit() else s


def _title(spec: dict, r: dict) -> str:
    cnt = int(r["FAC_COUNT"])
    return spec["title_template"].format(
        l_first=(r.get("L_FIRST") or "").title(),
        l_last=(r.get("L_LAST") or "").title(),
        excltype=r.get("EXCLTYPE") or "?",
        excldate=_fmt_date(r.get("EXCLDATE")),
        count=cnt, plural=("y" if cnt == 1 else "ies"))


def run_job(conn, spec: dict, run_id: str) -> pd.DataFrame:
    if not spec.get("no_fanout_guard"):
        raise ValueError(f"{spec['rule_name']}: lead jobs must set no_fanout_guard=True "
                         "(they run targeted SQL, never the bridge engine).")
    jk = spec["left"]["key"]
    rows = db.dicts(conn, compile_sql(spec))
    recs = []
    for r in rows:
        evidence = r["EVIDENCE_JSON"] or "[]"
        recs.append({
            "LEAD_ID": _lead_id(spec["rule_name"], jk, r["LEFT_KEY_VALUE"]),
            "RULE_NAME": spec["rule_name"],
            "LEFT_KEY_TYPE": jk,
            "LEFT_KEY_VALUE": r["LEFT_KEY_VALUE"],
            "TITLE": _title(spec, r),
            "SCORE": float(r["SCORE"]),
            "EVIDENCE": evidence,
            "EVIDENCE_COUNT": len(json.loads(evidence)),  # actual array length, not distinct-CCN
            "RUN_ID": run_id,
        })
    return pd.DataFrame(recs)


def _merge_leads(conn, df: pd.DataFrame) -> None:
    """Stage the run's leads, then MERGE — preserving FIRST_SEEN, bumping LAST_SEEN."""
    db.rows(conn, LEADS_DDL)
    write_pandas(conn, df, table_name="LEADS_STAGE", database=store.CONNECT_DB,
                 schema=store.CONNECT_SCHEMA, auto_create_table=True, overwrite=True,
                 quote_identifiers=False)
    db.rows(conn, f"""
        MERGE INTO {LEADS_FQN} t USING {STAGE_FQN} s ON t.LEAD_ID = s.LEAD_ID
        WHEN MATCHED THEN UPDATE SET
            t.RULE_NAME = s.RULE_NAME, t.LEFT_KEY_TYPE = s.LEFT_KEY_TYPE,
            t.LEFT_KEY_VALUE = s.LEFT_KEY_VALUE, t.TITLE = s.TITLE, t.SCORE = s.SCORE,
            t.EVIDENCE = PARSE_JSON(s.EVIDENCE), t.EVIDENCE_COUNT = s.EVIDENCE_COUNT,
            t.LAST_SEEN = CURRENT_TIMESTAMP(), t.RUN_ID = s.RUN_ID
        WHEN NOT MATCHED THEN INSERT
            (LEAD_ID, RULE_NAME, LEFT_KEY_TYPE, LEFT_KEY_VALUE, TITLE, SCORE,
             EVIDENCE, EVIDENCE_COUNT, FIRST_SEEN, LAST_SEEN, RUN_ID)
            VALUES (s.LEAD_ID, s.RULE_NAME, s.LEFT_KEY_TYPE, s.LEFT_KEY_VALUE, s.TITLE,
             s.SCORE, PARSE_JSON(s.EVIDENCE), s.EVIDENCE_COUNT,
             CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), s.RUN_ID)
    """)
    db.rows(conn, f"DROP TABLE IF EXISTS {STAGE_FQN}")


def _print_leads(df: pd.DataFrame, top: int) -> None:
    for i, r in enumerate(df.head(top).itertuples(index=False), 1):
        facs = [e.get("facility") for e in json.loads(r.EVIDENCE) if e.get("facility")]
        shown = ", ".join(facs[:4]) + (" …" if len(facs) > 4 else "")
        print(f"  {i:>2}. [{r.SCORE:.3f}] {r.TITLE}")
        if shown:
            print(f"      ↳ {shown}")


def run(job: str = "all", dry_run: bool = True, top: int = 20) -> dict:
    run_id = uuid.uuid4().hex[:16]
    names = list(JOBS) if job in (None, "all") else [job]
    unknown = [n for n in names if n not in JOBS]
    if unknown:
        raise SystemExit(f"unknown job(s): {unknown}. known: {list(JOBS)}")

    out = {}
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        for name in names:
            spec = JOBS[name]
            df = run_job(conn, spec, run_id)
            print(f"\n[{name}] {len(df)} leads  ({'DRY-RUN' if dry_run else 'writing'})")
            _print_leads(df, top)
            if not dry_run and len(df):
                _merge_leads(conn, df)
                print(f"  merged {len(df)} leads into {LEADS_FQN} (run {run_id})")
            out[name] = len(df)
    finally:
        conn.close()
    return out


if __name__ == "__main__":
    run()
