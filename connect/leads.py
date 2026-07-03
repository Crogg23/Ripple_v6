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
import re
import uuid
from datetime import date

import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

from . import db, receipt, safety, store
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
    RUN_ID          STRING,
    -- the receipt: the run-it-yourself proof that travels with every lead
    COMPILED_SQL    STRING,          -- the EXACT query this lead was produced by (clock frozen)
    SQL_SHA256      STRING,          -- content hash of COMPILED_SQL (skeptic re-hashes + runs)
    AS_OF_DATE      DATE,            -- the frozen wall-clock baked into the SQL -> reproducible
    SOURCE_SNAPSHOTS VARIANT         -- per source: _SOURCE_RUN_ID + INGEST_RUNS SHA256 + status
)
"""

# the receipt columns added to a pre-existing LEADS table, in order (idempotent ALTERs)
_RECEIPT_COLS = [
    ("COMPILED_SQL", "STRING"), ("SQL_SHA256", "STRING"),
    ("AS_OF_DATE", "DATE"), ("SOURCE_SNAPSHOTS", "VARIANT"),
]


def _norm(key: str, col: str) -> str:
    """Canonicalize a landing column the SAME way the rest of the engine does."""
    return normalize_sql(key, quote_ident(col))


# --------------------------------------------------------------------------- #
# Compile a JobSpec -> one targeted SQL query.
# Shape: left ⋈ right on a shared key, optional enrich-name lookup, optional
# surname corroboration, aggregate to one lead per LEFT entity, score.
# --------------------------------------------------------------------------- #
def _names_of(side: dict):
    """How a side carries a display/corroboration name.

    ('person', [last,first])  person columns — used for surname corroboration + display
    ('single', col)           one org/vessel name — display only (never corroborate)
    (None, None)              no name on this side
    Accepts the legacy last_col/first_col shape as 'person'.
    """
    if side.get("name_cols"):
        return "person", side["name_cols"]
    if side.get("last_col"):                       # legacy shape
        return "person", [side["last_col"], side["first_col"]]
    if side.get("name_col"):
        return "single", side["name_col"]
    return None, None


def compile_sql(spec: dict, as_of: str | None = None) -> str:
    """Compile a JobSpec to ONE targeted SQL query.

    The general shape is a hard-key INTERSECTION: a LEFT "flag" list (sanctions /
    exclusions / debarment) ⋈ a RIGHT "active" list (affiliations / broadcasts /
    awards) on a shared normalized key, aggregated to one lead per LEFT entity.
    Person names (optional) add surname corroboration; org/vessel names are display
    only. This is domain-agnostic: NPI doctors, IMO vessels, UEI contractors all
    compile from config — only the spec changes, never this function.

    ``as_of`` (ISO 'YYYY-MM-DD') FREEZES the clock: the recency window is computed
    against ``DATE '<as_of>'`` instead of ``CURRENT_DATE``, so the emitted SQL string
    is reproducible forever (re-running it later yields the same RECENCY_SCORE, the
    same lead). This is the receipt's load-bearing property — without it a published
    number silently drifts as the wall clock crosses each recency boundary. ``as_of``
    omitted keeps ``CURRENT_DATE`` (legacy / ad-hoc preview only; never persisted).

    OPTIONAL date gate (``date_mode`` + ``left_date_field`` + ``right_date_field`` or
    ``right_year_field``): the "flagged AND active" intersection alone can't say the
    activity happened AFTER the flag — that timeline is the difference between
    "appears in the data" and "did it while banned". Two modes:
      'gate'      adds the predicate right_date >= left_date to the join, so only
                  post-flag activity survives into the lead at all.
      'annotate'  adds NO predicate; both raw dates ride into each evidence item
                  under a 'timeline' key so a human reviewer can rank on it.
    Date fields are a bare column name (Snowflake auto-parses) or
    ``{"col": ..., "format": ...}`` (TRY_TO_DATE format, e.g. 'YYYYMMDD').
    ``right_year_field`` compares a bare year column against YEAR(left_date).
    A spec WITHOUT these fields compiles to BYTE-IDENTICAL SQL as before this
    capability existed — persisted SQL_SHA256 receipts must never churn for the
    rules that don't use it (tests pin the hashes).
    """
    L, R = spec["left"], spec["right"]
    jk = L["key"]
    if as_of is not None and not re.match(r"^\d{4}-\d{2}-\d{2}$", as_of):
        raise ValueError(f"as_of must be ISO 'YYYY-MM-DD', got {as_of!r}")
    today = f"DATE '{as_of}'" if as_of else "CURRENT_DATE"
    if R["key"] != jk:
        raise ValueError(f"{spec['rule_name']}: left/right join keys differ ({jk} vs {R['key']})")

    lkey, rkey = _norm(jk, L["key_col"]), _norm(jk, R["key_col"])
    lkind, lname = _names_of(L)
    rkind, rname = _names_of(R)
    person_pair = lkind == "person" and rkind == "person"

    # NULLIF blank names: a blank surname must NOT satisfy the require_surname gate
    # ('' = '' is TRUE in SQL), and a blank first name must not score as a match.
    def _nm(col):
        return f"NULLIF(UPPER(TRIM({quote_ident(col)})), '')"

    en = spec.get("enrich_name")
    ek = R.get("enrich_key")
    r_enrich = _norm(ek, R["enrich_key_col"]) if ek else "NULL"

    # ----- optional date gate / timeline (see docstring) -----
    # Everything below is guarded on date_mode so a spec without it contributes ZERO
    # bytes to the compiled SQL (receipt hashes for the existing rules must not churn).
    dmode = spec.get("date_mode")
    ldf, rdf, ryf = (spec.get("left_date_field"), spec.get("right_date_field"),
                     spec.get("right_year_field"))
    if dmode is not None:
        if dmode not in ("gate", "annotate"):
            raise ValueError(f"{spec['rule_name']}: date_mode must be 'gate' or "
                             f"'annotate', got {dmode!r}")
        if not ldf or not (rdf or ryf):
            raise ValueError(f"{spec['rule_name']}: date_mode needs left_date_field and "
                             "right_date_field (or right_year_field)")

    def _dcol(field) -> str:
        return field["col"] if isinstance(field, dict) else field

    def _dexpr(field, aliased: str) -> str:
        fmt = field.get("format") if isinstance(field, dict) else None
        return f"TRY_TO_DATE({aliased}, '{fmt}')" if fmt else f"TRY_TO_DATE({aliased})"

    # ----- LEFT (the "flag" list): key + optional name + carry + recency col -----
    l_sel = [f"{lkey} AS K_N"]
    if lkind == "person":
        l_sel += [f"{_nm(lname[0])} AS L_LAST", f"{_nm(lname[1])} AS L_FIRST"]
    elif lkind == "single":
        l_sel.append(f"{_nm(lname)} AS L_NAME")
    for alias, col in L.get("carry", {}).items():
        l_sel.append(f"{quote_ident(col)} AS L_{alias}")
    rec = L.get("recency")
    if rec:
        l_sel.append(f"{quote_ident(rec['col'])} AS L_RECENCY")
    if dmode is not None:
        l_sel.append(f"{quote_ident(_dcol(ldf))} AS L_DATEGATE")
    lft = f"SELECT {', '.join(l_sel)} FROM {db.fqn(L['table'])} WHERE {lkey} IS NOT NULL"

    # ----- RIGHT (the "active" list): key + enrich + optional name + carry -----
    r_sel = [f"{rkey} AS K_N", f"{r_enrich} AS ENRICH_N"]
    if rkind == "person":
        r_sel += [f"{_nm(rname[0])} AS R_LAST", f"{_nm(rname[1])} AS R_FIRST"]
    for alias, col in R.get("carry", {}).items():
        r_sel.append(f"{quote_ident(col)} AS R_{alias}")
    if dmode is not None:
        r_sel.append(f"{quote_ident(_dcol(rdf or ryf))} AS R_DATEGATE")
    rgt = f"SELECT {', '.join(r_sel)} FROM {db.fqn(R['table'])} WHERE {rkey} IS NOT NULL"

    # enrich-key -> human label (e.g. CCN -> facility name). DEDUPED to one name per
    # key: the rosters are a UNION ALL, so without this the LEFT JOIN fans out a key
    # that appears in multiple rosters, silently re-weighting AVG(name_match).
    if en:
        ne = _norm(en["key"], en["key"])
        union = " UNION ALL ".join(
            f"SELECT {ne} AS ENRICH_N, UPPER(TRIM({quote_ident(name)})) AS FAC_NAME "
            f"FROM {db.fqn(tbl)} WHERE {ne} IS NOT NULL"
            for tbl, name in en["tables"])
        fac_cte = f"SELECT ENRICH_N, ANY_VALUE(FAC_NAME) AS FAC_NAME FROM ( {union} ) GROUP BY ENRICH_N"
    else:
        fac_cte = "SELECT NULL AS ENRICH_N, NULL AS FAC_NAME WHERE 1=0"
    fac_join = "LEFT JOIN fac f ON f.ENRICH_N = a.ENRICH_N" if en else ""

    # surname corroboration + name score only make sense person-vs-person
    require = "AND l.L_LAST = a.R_LAST" if (spec.get("require_surname") and person_pair) else ""
    # 'gate' mode: only activity dated ON/AFTER the flag date survives the join. A year-only
    # right column compares against YEAR(left_date) — the coarsest honest comparison.
    dategate = ""
    if dmode == "gate":
        lexpr = _dexpr(ldf, "l.L_DATEGATE")
        dategate = (f" AND TRY_TO_NUMBER(a.R_DATEGATE) >= YEAR({lexpr})" if ryf
                    else f" AND {_dexpr(rdf, 'a.R_DATEGATE')} >= {lexpr}")
    if person_pair:
        name_match = ("IFF(l.L_FIRST = a.R_FIRST, 1.0, "
                      "IFF(LEFT(l.L_FIRST, 1) = LEFT(a.R_FIRST, 1), 0.85, 0.6))")
        name_agg = f"AVG({name_match})"
    else:
        name_agg = "1.0"

    # breadth = how many distinct active records the flagged entity reaches
    breadth = "COUNT(DISTINCT a.ENRICH_N)" if ek else "COUNT(*)"

    rec = L.get("recency")
    if rec:
        rexpr = f"TRY_TO_DATE(MAX(l.L_RECENCY), '{rec['format']}')"
        recency = f"IFF({rexpr} >= DATEADD('month', -{int(rec['months'])}, {today}), 1.0, 0.4)"
    else:
        recency = "1.0"

    # evidence object: enrich key + its label + any right-carry fields. Keys named
    # so the flagship's downstream stays stable ('ccn'/'facility'/'facility_type').
    ev = []
    if ek:
        ev.append(f"'{ek.lower()}', a.ENRICH_N")
    if en:
        ev.append(f"'{en.get('label', 'facility')}', f.FAC_NAME")
    for alias in R.get("carry", {}):
        ev.append(f"'{alias.lower()}', a.R_{alias}")
    if dmode is not None:
        # both raw date values ride with every evidence item (both modes: even a gated
        # lead should SHOW its timeline, not just imply it survived the predicate)
        ev.append("'timeline', OBJECT_CONSTRUCT('left_date', l.L_DATEGATE, "
                  "'right_date', a.R_DATEGATE)")
    if not ev:
        ev.append("'matched', TRUE")
    evidence = (f"TO_JSON(ARRAY_SLICE(ARRAY_AGG(DISTINCT "
                f"OBJECT_CONSTRUCT({', '.join(ev)})), 0, 50))")

    # left display fields -> a generic object the title template formats from
    tf = []
    if lkind == "person":
        tf += ["'l_last', ANY_VALUE(l.L_LAST)", "'l_first', ANY_VALUE(l.L_FIRST)"]
    elif lkind == "single":
        tf.append("'l_name', ANY_VALUE(l.L_NAME)")
    for alias in L.get("carry", {}):
        tf.append(f"'{alias.lower()}', ANY_VALUE(l.L_{alias})")
    title_fields = f"OBJECT_CONSTRUCT_KEEP_NULL({', '.join(tf)})" if tf else "OBJECT_CONSTRUCT()"

    sc = spec["score"]
    return f"""
WITH lft AS ( {lft} ),
rgt AS ( {rgt} ),
fac AS ( {fac_cte} ),
matched AS (
  SELECT l.K_N AS LEFT_KEY_VALUE,
         {name_agg} AS NAME_SCORE,
         {recency} AS RECENCY_SCORE,
         {breadth} AS BREADTH,
         {title_fields} AS TITLE_FIELDS,
         {evidence} AS EVIDENCE_JSON
  FROM lft l
  JOIN rgt a ON a.K_N = l.K_N {require}{dategate}
  {fac_join}
  GROUP BY l.K_N )
SELECT LEFT_KEY_VALUE, BREADTH, TITLE_FIELDS, EVIDENCE_JSON,
       ROUND({sc.get('name_w', 0)} * NAME_SCORE
           + {sc.get('recency_w', 0)} * RECENCY_SCORE
           + {sc.get('breadth_w', 0)} * LEAST(BREADTH / {sc.get('breadth_div', 1)}, 1.0), 3) AS SCORE
FROM matched
ORDER BY SCORE DESC, BREADTH DESC
"""


def _lead_id(rule: str, key: str, val: str) -> str:
    return "LEAD_" + hashlib.md5(f"{rule}|{key}:{val}".encode()).hexdigest()[:16]


def _fmt_date(v) -> str:
    s = str(v or "")
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 and s.isdigit() else s


class _SafeDict(dict):
    """format_map helper: a missing {field} renders empty instead of raising."""

    def __missing__(self, key):
        return ""


def _title(spec: dict, fields: dict, count: int) -> str:
    f = {k: ("" if v is None else v) for k, v in (fields or {}).items()}
    for k in spec.get("title_titlecase", []):       # nice-case raw UPPER source names
        if f.get(k):
            f[k] = str(f[k]).title()
    for k in spec.get("title_dates", []):           # YYYYMMDD -> YYYY-MM-DD
        f[k] = _fmt_date(f.get(k))
    f["count"] = count
    f["plural"] = "y" if count == 1 else "ies"
    return spec["title_template"].format_map(_SafeDict(f))


def run_job(conn, spec: dict, run_id: str, dry_run: bool = False) -> pd.DataFrame:
    if not spec.get("no_fanout_guard"):
        raise ValueError(f"{spec['rule_name']}: lead jobs must set no_fanout_guard=True "
                         "(they run targeted SQL, never the bridge engine).")
    jk = spec["left"]["key"]
    # FREEZE the clock, then run the EXACT SQL we will store: the persisted COMPILED_SQL must be
    # byte-identical to what produced these rows, or the receipt's "run it yourself" is a lie.
    as_of = date.today().isoformat()
    sql = compile_sql(spec, as_of=as_of)
    sha = receipt.sql_sha256(sql)
    # Pin each source's data version — but only when persisting (resolve hits the warehouse;
    # a dry-run preview stays free). The SQL + hash are computed offline, so previews still show them.
    snapshots = json.dumps([] if dry_run else receipt.resolve_snapshots(conn, spec))
    rows = db.dicts(conn, sql)
    recs = []
    for r in rows:
        evidence = r["EVIDENCE_JSON"] or "[]"
        tf = r.get("TITLE_FIELDS")
        fields = json.loads(tf) if isinstance(tf, str) else (tf or {})
        count = int(r["BREADTH"] or 0)
        recs.append({
            "LEAD_ID": _lead_id(spec["rule_name"], jk, r["LEFT_KEY_VALUE"]),
            "RULE_NAME": spec["rule_name"],
            "LEFT_KEY_TYPE": jk,
            "LEFT_KEY_VALUE": r["LEFT_KEY_VALUE"],
            "TITLE": _title(spec, fields, count),
            "SCORE": float(r["SCORE"]),
            "EVIDENCE": evidence,
            "EVIDENCE_COUNT": len(json.loads(evidence)),  # actual array length
            "RUN_ID": run_id,
            "COMPILED_SQL": sql,            # the receipt: run-it-yourself proof
            "SQL_SHA256": sha,
            "AS_OF_DATE": as_of,
            "SOURCE_SNAPSHOTS": snapshots,
        })
    return pd.DataFrame(recs)


# The dashboard read path calls _ensure_leads_table per request; the CREATE/ALTERs are
# idempotent but they're still DDL round-trips on every page load. Run them once per process.
_LEADS_TABLE_READY = False


def _ensure_leads_table(conn) -> None:
    global _LEADS_TABLE_READY
    if _LEADS_TABLE_READY:
        return
    db.rows(conn, LEADS_DDL)
    # STATUS marks staleness: a lead absent from the latest run is expired, so a person cleared by
    # the source drops out of publication. Added in place so the live table gains the column.
    db.rows(conn, f"ALTER TABLE {LEADS_FQN} ADD COLUMN IF NOT EXISTS STATUS STRING")
    # receipt columns — additive + idempotent, so an existing live LEADS table gains them in place.
    for col, typ in _RECEIPT_COLS:
        db.rows(conn, f"ALTER TABLE {LEADS_FQN} ADD COLUMN IF NOT EXISTS {col} {typ}")
    _LEADS_TABLE_READY = True   # only after every statement succeeded


def _merge_leads(conn, df: pd.DataFrame) -> None:
    """Stage the run's leads, then MERGE — preserving FIRST_SEEN, bumping LAST_SEEN."""
    write_pandas(conn, df, table_name="LEADS_STAGE", database=store.CONNECT_DB,
                 schema=store.CONNECT_SCHEMA, auto_create_table=True, overwrite=True,
                 quote_identifiers=False)
    db.rows(conn, f"""
        MERGE INTO {LEADS_FQN} t USING {STAGE_FQN} s ON t.LEAD_ID = s.LEAD_ID
        WHEN MATCHED THEN UPDATE SET
            t.RULE_NAME = s.RULE_NAME, t.LEFT_KEY_TYPE = s.LEFT_KEY_TYPE,
            t.LEFT_KEY_VALUE = s.LEFT_KEY_VALUE, t.TITLE = s.TITLE, t.SCORE = s.SCORE,
            t.EVIDENCE = PARSE_JSON(s.EVIDENCE), t.EVIDENCE_COUNT = s.EVIDENCE_COUNT,
            t.LAST_SEEN = CURRENT_TIMESTAMP(), t.RUN_ID = s.RUN_ID,
            t.COMPILED_SQL = s.COMPILED_SQL, t.SQL_SHA256 = s.SQL_SHA256,
            t.AS_OF_DATE = TO_DATE(s.AS_OF_DATE, 'YYYY-MM-DD'),
            t.SOURCE_SNAPSHOTS = PARSE_JSON(s.SOURCE_SNAPSHOTS)
        WHEN NOT MATCHED THEN INSERT
            (LEAD_ID, RULE_NAME, LEFT_KEY_TYPE, LEFT_KEY_VALUE, TITLE, SCORE,
             EVIDENCE, EVIDENCE_COUNT, FIRST_SEEN, LAST_SEEN, RUN_ID,
             COMPILED_SQL, SQL_SHA256, AS_OF_DATE, SOURCE_SNAPSHOTS)
            VALUES (s.LEAD_ID, s.RULE_NAME, s.LEFT_KEY_TYPE, s.LEFT_KEY_VALUE, s.TITLE,
             s.SCORE, PARSE_JSON(s.EVIDENCE), s.EVIDENCE_COUNT,
             CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), s.RUN_ID,
             s.COMPILED_SQL, s.SQL_SHA256, TO_DATE(s.AS_OF_DATE, 'YYYY-MM-DD'),
             PARSE_JSON(s.SOURCE_SNAPSHOTS))
    """)
    db.rows(conn, f"DROP TABLE IF EXISTS {STAGE_FQN}")


def _expire_rule(conn, rule: str, run_id: str) -> None:
    """Mark this rule's leads active if they reappeared in THIS run, else stale — so a lead whose
    supporting rows vanished drops out of publication EVEN WHEN the rule now returns zero leads."""
    db.rows(conn, f"UPDATE {LEADS_FQN} SET STATUS = IFF(RUN_ID = %s, 'active', 'stale') "
                  f"WHERE RULE_NAME = %s", (run_id, rule))


def _auto_publishable(row: dict) -> bool:
    """Auto-confirm hook: may a lead publish WITHOUT a human review?

    Only if it clears a CALIBRATED high-confidence bar. Leads today carry an UNCALIBRATED
    composite SCORE, and minting a "fact" from it is exactly the overreach this safety
    layer exists to stop — so this returns False: nothing about a named person reads as
    published fact until a human confirms it (`connect review lead <LEAD_ID> confirmed`).
    When leads gain a held-out precision tier (mirror the matcher's MATCH_RUNGS), gate it
    here, e.g. `return row.get("CONF_TIER") == "CONFIRMED"`.
    """
    return False


def _gate(rows: list[dict], decisions: dict[str, str],
          only_publishable: bool = False) -> list[dict]:
    """Apply the publish-safety gate to lead rows. PURE (no DB) so it is offline-testable.

    Drops review-suppressed leads (rejected / retracted / stale verdict) and stamps every
    survivor with REVIEW_STATE + PUBLISHED via safety.gate_rows. PUBLISHED is true only for
    a human-confirmed lead or one clearing the (currently off) auto-confirm tier.
    only_publishable keeps just the PUBLISHED=True set — the strict 'safe as fact' read.
    """
    for r in rows:
        r.setdefault("auto_ok", _auto_publishable(r))
    gated = safety.gate_rows(rows, decisions)
    return [r for r in gated if r["PUBLISHED"]] if only_publishable else gated


def published(conn, rule: str | None = None, only_publishable: bool = False) -> list[dict]:
    """Canonical PUBLISH read: active leads, gated by the safety spine.

    Two surfaces must BOTH pass. STATUS handles staleness (a lead whose supporting rows
    vanished is 'stale' and filtered here). safety.DECISIONS handles review: rejected /
    retracted / stale verdicts are dropped, and only a human-CONFIRMED lead (or the auto
    tier, off today) reads PUBLISHED=True. Every returned row carries REVIEW_STATE +
    PUBLISHED, so a caller can never mistake an unreviewed 'pending' lead for fact. Pass
    only_publishable=True for the strict set that is safe to present as established fact.
    """
    _ensure_leads_table(conn)
    decisions = safety.latest(conn, "lead")
    rows = db.dicts(conn, f"SELECT * FROM {LEADS_FQN} "
                          f"WHERE COALESCE(STATUS, 'active') = 'active' ORDER BY SCORE DESC", ())
    if rule is not None:
        rows = [r for r in rows if r["RULE_NAME"] == rule]
    return _gate(rows, decisions, only_publishable)


def rung_display(rung: str, measured_precision: float | None = None,
                 calibration: str = "health-provider calibration only") -> str:
    """Human display for a MATCH_RUNGS tier name — never show the bare word.

    'CONFIRMED' measured at 87.6% precision is wrong roughly 1 in 8 times; printing the
    bare tier name to a reader overclaims exactly the way the safety layer forbids. Any
    surface that shows a rung (dossier, receipts, serve) must route through this so the
    measured number travels WITH the label. Pass the MEASURED_PRECISION from the
    MATCH_RUNGS row for the model version that scored the link; without one the label
    must say so instead of implying confidence. DB rung names are unchanged — this is
    display only.
    """
    if measured_precision is None:
        return f"{rung} (no measured precision on file — treat as uncalibrated)"
    return f"{rung} ({measured_precision * 100:.1f}% measured precision, {calibration})"


def _print_leads(df: pd.DataFrame, top: int) -> None:
    for i, r in enumerate(df.head(top).itertuples(index=False), 1):
        ev = json.loads(r.EVIDENCE)
        # prefer the human label ('facility'); else the first non-id string per item
        labels = [e.get("facility") for e in ev if e.get("facility")]
        if not labels:
            for e in ev:
                for k, v in e.items():
                    if isinstance(v, str) and v and k not in ("ccn", "key"):
                        labels.append(v)
                        break
        labels = list(dict.fromkeys(labels))  # dedupe, keep order
        shown = ", ".join(labels[:4]) + (" …" if len(labels) > 4 else "")
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
        if not dry_run:
            _ensure_leads_table(conn)
        sup = safety.suppressed(conn, "lead")   # rejected/retracted -> never shown as fact
        for name in names:
            spec = JOBS[name]
            df = run_job(conn, spec, run_id, dry_run=dry_run)
            shown = df[~df["LEAD_ID"].isin(sup)] if len(df) else df
            hidden = len(df) - len(shown)
            print(f"\n[{name}] {len(shown)} leads  ({'DRY-RUN' if dry_run else 'writing'})"
                  + (f" — {hidden} hidden by review/retraction" if hidden else ""))
            _print_leads(shown, top)
            if not dry_run:
                if len(df):
                    _merge_leads(conn, df)
                _expire_rule(conn, name, run_id)   # fires even when the rule returned ZERO leads
                print(f"  merged {len(df)} into {LEADS_FQN}; staleness swept (run {run_id})")
            out[name] = len(df)
        if not dry_run:
            print("\n  ⚑ these leads are UNREVIEWED — none read as PUBLISHED fact until a human "
                  "confirms:\n     `connect review lead <LEAD_ID> confirmed --by <you>`  "
                  "(`connect safety` shows the ledger)")
    finally:
        conn.close()
    return out


if __name__ == "__main__":
    run()
