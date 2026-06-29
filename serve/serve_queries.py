"""Every read the reading room makes — the SAME queries the connect engine uses.

Resolution + dossier mirror connect/dossier.py exactly: normalize the typed value
with the spine's own SQL expression, look it up in ENTITY_MAP, then fan out
ENTITY_INDEX. The normalize expressions are reproduced from connect/keys.py rather
than imported, so this module has no dependency on the connect/ package and lifts
cleanly into Streamlit-in-Snowflake.

FRESHNESS + PROVENANCE degrade gracefully: V_SOURCE_FRESHNESS may be absent (it is
today), so we probe INFORMATION_SCHEMA first and fall back to INGEST_RUNS, labelling
any timestamp honestly as \"last loaded\" — never as data-recency.
"""

from __future__ import annotations

import hashlib
import json
import re

import streamlit as st

from serve_session import run_df

CONNECT = 'LIBRARY_META."CONNECT"'  # CONNECT is a reserved word -> always quoted
CATALOG = "LIBRARY_META.REGISTRY.CATALOG"
RUNS = "LIBRARY_META.INGEST_LOGS.INGEST_RUNS"
FRESH_VIEW = "LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS"
LANDING = "LIBRARY_RAW.LANDING"

# Hard keys actually resolvable in the v1 backbone (verified live coverage):
# NPI 10.55M · UEI 93k · CCN 78k · CIK 8k · IMO 6.7k. EIN normalizes but has no
# rows in the index yet, so it is deliberately NOT offered (no false promises).
SEARCH_KEYS = ["NPI", "CCN", "UEI", "CIK", "IMO"]

_IDENT_RE = re.compile(r"^[A-Z0-9_]+$")


# --------------------------------------------------------------------------- #
# Normalizers — reproduced verbatim from connect/keys.py (NORM_RULES).
# We PAD (never strip) fixed-width IDs; NULL the all-zero placeholder.
# --------------------------------------------------------------------------- #
_NAME_NOISE = sorted({
    "INC", "INCORPORATED", "LLC", "LLP", "LP", "LTD", "CO", "CORP", "CORPORATION",
    "COMPANY", "PC", "PLLC", "PA", "PLC", "GROUP", "HOLDINGS", "THE", "AND", "OF",
    "MD", "DO", "DDS", "DMD", "RN", "NP", "PHD", "ESQ", "JR", "SR", "II", "III", "IV",
    "MR", "MRS", "MS", "DR",
})
_NORM = {"NPI": ("pad", 10), "EIN": ("pad", 9), "CIK": ("pad", 10), "CCN": ("pad", 6),
         "UEI": ("fixed", 12), "IMO": ("imo", 7)}


def _alnum(col: str) -> str:
    return f"UPPER(REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9A-Za-z]', ''))"


def _name_canon(col: str) -> str:
    base = f"TRIM(REGEXP_REPLACE(UPPER(TO_VARCHAR({col})), '[^A-Z0-9]+', ' '))"
    noise = ", ".join(f"'{t}'" for t in _NAME_NOISE)
    return (f"NULLIF(ARRAY_TO_STRING(ARRAY_SORT(ARRAY_EXCEPT("
            f"SPLIT({base}, ' '), ARRAY_CONSTRUCT({noise}))), ' '), '')")


def normalize_sql(key: str, col: str) -> str:
    """SQL expression canonicalizing `col` for an equi-join on `key`."""
    if key in ("NAME", "PERSON"):
        return _name_canon(col)
    mode, width = _NORM[key]
    clean = _alnum(col)
    if mode == "pad":
        return (f"CASE WHEN LENGTH({clean}) = 0 OR LENGTH({clean}) > {width} "
                f"OR LPAD({clean}, {width}, '0') = REPEAT('0', {width}) THEN NULL "
                f"ELSE LPAD({clean}, {width}, '0') END")
    if mode == "fixed":
        return f"CASE WHEN LENGTH({clean}) = {width} THEN {clean} ELSE NULL END"
    if mode == "imo":
        d = f"REGEXP_REPLACE(TO_VARCHAR({col}), '[^0-9]', '')"
        return f"CASE WHEN LENGTH({d}) <> {width} OR {d} = REPEAT('0', {width}) THEN NULL ELSE {d} END"
    raise KeyError(key)


def entity_id_for(key_type: str, key_value: str) -> str:
    """Content-addressed entity id — the same scheme spine.py builds, so we can
    deep-link a facility (CCN) from an affiliation row with no extra query."""
    h = hashlib.md5(f"{key_type}|{key_value}".encode()).hexdigest()[:16]
    return f"ENT_{h}"


def safe_json(x):
    if x in (None, "", "null"):
        return None
    if isinstance(x, (dict, list)):
        return x
    try:
        return json.loads(x)
    except Exception:
        return None


def preview_pairs(preview) -> list:
    p = safe_json(preview)
    if not isinstance(p, dict):
        return []
    return [(k, v) for k, v in p.items() if v not in (None, "", "null")]


# --------------------------------------------------------------------------- #
# SEARCH
# --------------------------------------------------------------------------- #
@st.cache_data(ttl=300, show_spinner=False)
def resolve_hard_id(key_type: str, raw: str):
    """Typed NPI/CCN/UEI/CIK/IMO -> matching entity rows (normalize inline, bind raw once)."""
    norm = normalize_sql(key_type, "V")
    sql = f"""
        SELECT ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE, SOURCE_COUNT, MEMBER_TABLES
        FROM {CONNECT}.ENTITY_MAP
        WHERE KEY_TYPE = %s
          AND KEY_VALUE = (SELECT {norm} FROM (SELECT %s AS V))
        ORDER BY SOURCE_COUNT DESC NULLS LAST
        LIMIT 25"""
    return run_df(sql, (key_type, raw))


@st.cache_data(ttl=300, show_spinner=False)
def normalize_name(raw: str) -> str:
    df = run_df(f"SELECT {_name_canon('V')} AS NN FROM (SELECT %s AS V)", (raw,))
    return (df.iloc[0]["NN"] or "") if len(df) else ""


@st.cache_data(ttl=300, show_spinner=False)
def search_names(raw: str, limit: int = 50):
    """Token-AND name search (dossier.py path) over token-SORTED NAME_NORM, enriched
    with SOURCE_COUNT so common-name disambiguation is actually pickable."""
    nn = normalize_name(raw)
    tokens = [t for t in nn.split(" ") if t]
    if not tokens:
        return run_df("SELECT NULL AS ENTITY_ID WHERE 1=0")
    where = " AND ".join(["g.NAME_NORM LIKE %s"] * len(tokens))
    sql = f"""
        SELECT g.ENTITY_ID, g.CANONICAL_NAME, g.ENTITY_TYPE, g.KEY_TYPE, g.KEY_VALUE,
               m.SOURCE_COUNT
        FROM {CONNECT}.ENTITY_GOLDEN g
        LEFT JOIN {CONNECT}.ENTITY_MAP m ON m.ENTITY_ID = g.ENTITY_ID
        WHERE {where}
        ORDER BY m.SOURCE_COUNT DESC NULLS LAST, LENGTH(g.CANONICAL_NAME), g.CANONICAL_NAME
        LIMIT %s"""
    return run_df(sql, tuple(f"%{t}%" for t in tokens) + (limit,))


@st.cache_data(ttl=300, show_spinner=False)
def search_sources(q: str, limit: int = 50):
    like = f"%{q}%"
    sql = f"""
        SELECT SOURCE_ID, NAME, DOMAIN_PRIMARY, JURISDICTION, LIFECYCLE,
               LANDED_ROW_COUNT, JOIN_KEYS_STD, LANDING_FQN, PUBLISHER, URL
        FROM {CATALOG}
        WHERE (NAME ILIKE %s OR SOURCE_ID ILIKE %s OR DOMAIN_PRIMARY ILIKE %s)
          AND LIFECYCLE IN ('landed','modeled')
        ORDER BY LANDED_ROW_COUNT DESC NULLS LAST
        LIMIT %s"""
    return run_df(sql, (like, like, like, limit))


# --------------------------------------------------------------------------- #
# DOSSIER — the four parameterized SELECTs, keyed on ENTITY_ID.
# --------------------------------------------------------------------------- #
@st.cache_data(ttl=180, show_spinner=False)
def get_dossier(eid: str):
    golden = run_df(f"SELECT * FROM {CONNECT}.ENTITY_GOLDEN WHERE ENTITY_ID = %s", (eid,))
    emap = run_df(f"SELECT * FROM {CONNECT}.ENTITY_MAP WHERE ENTITY_ID = %s", (eid,))
    sources = run_df(f"""
        SELECT SOURCE_TABLE, DOMAIN, DISPLAY_LABEL, ROW_COUNT, PREVIEW
        FROM {CONNECT}.ENTITY_INDEX
        WHERE ENTITY_ID = %s
        ORDER BY DOMAIN, SOURCE_TABLE""", (eid,))
    return golden, emap, sources


@st.cache_data(ttl=180, show_spinner=False)
def get_affiliations(npi_value: str):
    """Provider -> CMS facilities (works-at relationship, NOT identity). Reads the
    LIVE landing table; the one part of the dossier that hits LIBRARY_RAW directly."""
    npi_n = normalize_sql("NPI", '"NPI"')
    ccn_n = normalize_sql("CCN", '"CCN"')
    sql = f"""
        WITH ccns AS (
            SELECT DISTINCT {ccn_n} AS CCN
            FROM {LANDING}.FED_CMS_FACILITY_AFFILIATION
            WHERE {npi_n} = %s)
        SELECT x.CCN, g.CANONICAL_NAME, g.CANONICAL_ADDR
        FROM ccns x
        LEFT JOIN {CONNECT}.ENTITY_GOLDEN g ON g.KEY_TYPE = 'CCN' AND g.KEY_VALUE = x.CCN
        WHERE x.CCN IS NOT NULL
        ORDER BY g.CANONICAL_NAME NULLS LAST
        LIMIT 100"""
    return run_df(sql, (npi_value,))


# --------------------------------------------------------------------------- #
# SOURCE detail
# --------------------------------------------------------------------------- #
@st.cache_data(ttl=300, show_spinner=False)
def get_source(source_id: str):
    sql = f"""
        SELECT SOURCE_ID, NAME, PUBLISHER, DOMAIN_PRIMARY, JURISDICTION, LIFECYCLE,
               LANDED_ROW_COUNT, JOIN_KEYS_STD, JOIN_KEY_TIER, TRUST_LAYER,
               LANDING_FQN, URL, IS_SAMPLE
        FROM {CATALOG}
        WHERE LOWER(SOURCE_ID) = %s
        LIMIT 1"""
    return run_df(sql, (source_id.lower(),))


@st.cache_data(ttl=120, show_spinner=False)
def sample_rows(source_id: str, n: int = 25):
    tbl = source_id.strip().upper()
    if not _IDENT_RE.match(tbl):
        raise ValueError(f"unsafe table identifier: {source_id!r}")
    return run_df(f"SELECT * FROM {LANDING}.{tbl} SAMPLE ({int(n)} ROWS)")


@st.cache_data(ttl=600, show_spinner=False)
def catalog_enrichment() -> dict:
    """source_id(lower) -> {domain, rows, name} for graph-node enrichment.
    node.domain/node.rows in the JSON are unreliable; CATALOG carries the truth."""
    df = run_df(f"""
        SELECT LOWER(SOURCE_ID) AS SID, DOMAIN_PRIMARY, LANDED_ROW_COUNT, NAME, IS_SAMPLE
        FROM {CATALOG}""")
    out = {}
    for r in df.itertuples(index=False):
        out[r.SID] = {"domain": r.DOMAIN_PRIMARY, "rows": r.LANDED_ROW_COUNT,
                      "name": r.NAME, "is_sample": r.IS_SAMPLE}
    return out


# --------------------------------------------------------------------------- #
# FRESHNESS + PROVENANCE  (probe-then-degrade; keyed on SOURCE_ID)
# --------------------------------------------------------------------------- #
@st.cache_data(ttl=600, show_spinner=False)
def freshness_view_exists() -> bool:
    df = run_df("""
        SELECT COUNT(*) AS C FROM LIBRARY_META.INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = 'REGISTRY' AND TABLE_NAME = 'V_SOURCE_FRESHNESS'""")
    return int(df.iloc[0]["C"]) > 0


@st.cache_data(ttl=180, show_spinner=False)
def decorations_for(source_ids: tuple) -> dict:
    """Batch freshness badge + provenance receipt for a set of sources, in <=2
    round-trips. Returns {source_id(lower): {...}}. Always degrades gracefully:
    no run -> receipt None; no freshness view -> state 'unknown' + last-loaded."""
    ids = sorted({s.lower() for s in source_ids if s})
    if not ids:
        return {}
    ph = ",".join(["%s"] * len(ids))

    # Provenance: latest SUCCESSFUL run per source (the run-it-yourself receipt).
    prov = run_df(f"""
        WITH lr AS (
            SELECT SOURCE_ID, RUN_ID, SHA256, SOURCE_URL, STATUS, ROW_COUNT, FILE_BYTES,
                   COALESCE(ENDED_AT, STARTED_AT, _LOADED_AT) AS LOADED_AT
            FROM {RUNS}
            WHERE STATUS = 'success' AND LOWER(SOURCE_ID) IN ({ph})
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY SOURCE_ID
                ORDER BY COALESCE(ENDED_AT, STARTED_AT, _LOADED_AT) DESC NULLS LAST) = 1)
        SELECT LOWER(SOURCE_ID) AS SID, RUN_ID, SHA256, SOURCE_URL, STATUS,
               ROW_COUNT, FILE_BYTES, LOADED_AT
        FROM lr""", tuple(ids))

    out: dict = {}
    for r in prov.itertuples(index=False):
        out[r.SID] = {
            "freshness_state": "unknown", "data_through": None, "data_age_days": None,
            "cadence": None, "note": None,
            "run_id": r.RUN_ID, "sha256": r.SHA256, "source_url": r.SOURCE_URL,
            "loaded_at": r.LOADED_AT, "run_rows": r.ROW_COUNT, "file_bytes": r.FILE_BYTES,
        }
    for sid in ids:
        out.setdefault(sid, {"freshness_state": "unknown", "run_id": None,
                             "sha256": None, "source_url": None, "loaded_at": None,
                             "data_through": None, "data_age_days": None,
                             "cadence": None, "note": None, "run_rows": None,
                             "file_bytes": None})

    # Freshness: only if the ledger view has been built (--apply). Else stay 'unknown'.
    if freshness_view_exists():
        try:
            fr = run_df(f"""
                SELECT LOWER(SOURCE_ID) AS SID, FRESHNESS_STATE, DATA_THROUGH_ISO,
                       DATA_AGE_DAYS, CADENCE_BUCKET, NOTE
                FROM {FRESH_VIEW}
                WHERE LOWER(SOURCE_ID) IN ({ph})""", tuple(ids))
            for r in fr.itertuples(index=False):
                d = out.setdefault(r.SID, {})
                d["freshness_state"] = (r.FRESHNESS_STATE or "unknown")
                d["data_through"] = r.DATA_THROUGH_ISO
                d["data_age_days"] = r.DATA_AGE_DAYS
                d["cadence"] = r.CADENCE_BUCKET
                d["note"] = r.NOTE
        except Exception:
            pass  # view vanished mid-session -> keep 'unknown'
    return out
