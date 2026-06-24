"""The overlap engine — do two columns ACTUALLY share values, and how many?

This is the move I ran by hand three times today (NPI: empty, CCN: noise,
spatial: real), now a reusable primitive. Given two landing columns and the key
type, it normalizes both sides the same way, equi-joins on the canonical value,
and returns honest counts + a sample so a connection can never pose as real
without the numbers to back it.

Two modes:
  value_overlap   canonical equi-join (IDs, codes, names, country)
  spatial_overlap point-in-polygon (lat/lon point inside a geometry)
"""

from __future__ import annotations

from . import db
from .keys import normalize_sql, quote_ident


def value_overlap(conn, a_tbl: str, a_col: str, b_tbl: str, b_col: str,
                  key: str, sample: int = 6) -> dict:
    a_norm = normalize_sql(key, quote_ident(a_col))
    b_norm = normalize_sql(key, quote_ident(b_col))
    A, B = db.fqn(a_tbl), db.fqn(b_tbl)

    q = f"""
    WITH a AS (SELECT DISTINCT {a_norm} AS k FROM {A} WHERE {a_norm} IS NOT NULL),
         b AS (SELECT DISTINCT {b_norm} AS k FROM {B} WHERE {b_norm} IS NOT NULL)
    SELECT
      (SELECT COUNT(*) FROM a)                       AS a_distinct,
      (SELECT COUNT(*) FROM b)                       AS b_distinct,
      (SELECT COUNT(*) FROM a JOIN b USING (k))      AS matched
    """
    r = db.dicts(conn, q)[0]
    a_d, b_d, m = int(r["A_DISTINCT"]), int(r["B_DISTINCT"]), int(r["MATCHED"])

    samp = []
    if m:
        sq = f"""
        WITH a AS (SELECT DISTINCT {a_norm} AS k FROM {A} WHERE {a_norm} IS NOT NULL),
             b AS (SELECT DISTINCT {b_norm} AS k FROM {B} WHERE {b_norm} IS NOT NULL)
        SELECT k FROM a JOIN b USING (k) ORDER BY k LIMIT {int(sample)}
        """
        samp = [row[0] for row in db.rows(conn, sq)]

    denom = min(a_d, b_d) or 1
    return {
        "mode": "value",
        "a_distinct": a_d,
        "b_distinct": b_d,
        "matched": m,
        "match_rate": round(m / denom * 100, 1),   # vs the smaller side
        "sample": samp,
    }


def _is_lon(col: str) -> bool:
    c = col.lower()
    return "lon" in c or "lng" in c


def _state_col(columns: list[str]) -> str | None:
    """Best-effort 2-letter-state column for pruning a spatial join."""
    for c in columns:
        cl = c.lower()
        if cl == "state" or cl.endswith("_state") or "state_code" in cl or "state_name" in cl:
            return c
    return None


def spatial_overlap(conn, pt_tbl: str, lat_col: str, lon_col: str,
                    poly_tbl: str, geom_col: str, sample: int = 6) -> dict:
    """How many DISTINCT points in pt_tbl fall inside a geometry in poly_tbl?

    No state-prune: ST_CONTAINS fully determines geography, and a string-equality
    state filter could only DROP rows it accepted (CA != California != 06) -- a
    correctness loss. The point side is row-capped upstream, so the join is bounded.
    Rate is distinct-points-inside / distinct-points-total (same unit as value mode),
    so it's 0-100% and rankable in the same graph. TRY_TO_GEOGRAPHY skips bad geom.
    """
    P, G = db.fqn(pt_tbl), db.fqn(poly_tbl)
    lat = f"TRY_TO_DOUBLE(TO_VARCHAR({quote_ident(lat_col)}))"
    lon = f"TRY_TO_DOUBLE(TO_VARCHAR({quote_ident(lon_col)}))"

    q = f"""
    WITH pts AS (
      SELECT DISTINCT {lat} AS lat, {lon} AS lon
      FROM {P} WHERE {lat} IS NOT NULL AND {lon} IS NOT NULL
    ),
    poly AS (
      SELECT TRY_TO_GEOGRAPHY({quote_ident(geom_col)}) AS g
      FROM {G} WHERE TRY_TO_GEOGRAPHY({quote_ident(geom_col)}) IS NOT NULL
    ),
    hits AS (
      SELECT DISTINCT pts.lat, pts.lon
      FROM pts JOIN poly ON ST_CONTAINS(poly.g, ST_MAKEPOINT(pts.lon, pts.lat))
    )
    SELECT (SELECT COUNT(*) FROM pts)  AS a_distinct,
           (SELECT COUNT(*) FROM poly) AS b_polys,
           (SELECT COUNT(*) FROM hits) AS matched
    """
    r = db.dicts(conn, q)[0]
    a_d, b_p, m = int(r["A_DISTINCT"]), int(r["B_POLYS"]), int(r["MATCHED"])

    samp = []
    if m:
        sq = f"""
        WITH pts AS (SELECT DISTINCT {lat} AS lat, {lon} AS lon FROM {P}
                     WHERE {lat} IS NOT NULL AND {lon} IS NOT NULL),
             poly AS (SELECT TRY_TO_GEOGRAPHY({quote_ident(geom_col)}) AS g FROM {G}
                      WHERE TRY_TO_GEOGRAPHY({quote_ident(geom_col)}) IS NOT NULL)
        SELECT DISTINCT ROUND(pts.lat,4) || ',' || ROUND(pts.lon,4)
        FROM pts JOIN poly ON ST_CONTAINS(poly.g, ST_MAKEPOINT(pts.lon, pts.lat))
        LIMIT {int(sample)}
        """
        samp = [row[0] for row in db.rows(conn, sq)]

    return {
        "mode": "spatial",
        "a_distinct": a_d,
        "b_distinct": b_p,
        "matched": m,
        "match_rate": round(m / (a_d or 1) * 100, 1),   # % of distinct points inside a polygon
        "sample": samp,
    }
