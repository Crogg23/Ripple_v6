"""Registry-driven onboarding queue.

Instead of a hand-curated list, pull the next onboarding candidates straight from
``LIBRARY_META.REGISTRY.SOURCE_REGISTRY`` -- the ~900-source catalog -- prioritized
by ``PRIORITY_TIER``. This is the scaling unlock: the catalog already knows what we
want in the Library, so the catalog drives the queue.

A row is a *candidate* when it is:
  - not already onboarded   (``INCLUDE`` is not ``'Y'``)
  - not already landed      (no ``success`` row in ``INGEST_LOGS.INGEST_RUNS``)
  - has a URL to recon
  - carries a conforming ``SOURCE_ID`` (``fed_`` / ``intl_`` / ``xc_`` / ``loc_`` / ``st_``)

Pinning each candidate's registry ``SOURCE_ID`` is the linchpin: the agent's recon
honours a pinned ``source_id``, so onboarding *updates that exact row* (flipping
``INCLUDE`` blank -> ``Y``) instead of inserting a duplicate. The registry is then
both the queue and the completion ledger -- drained by construction, safe to re-run.
"""

from __future__ import annotations

import re
from typing import List, Optional

import snow

# canonical SOURCE_REGISTRY.JURISDICTION -> the agent's build-plan "layer" label.
_JURISDICTION_LAYER = {
    "federal": "us_federal",
    "international": "international",
    "cross-cutting": "investigative",
    "local": "local",
    "state": "state",
}

# JOIN_KEYS tokens that aren't real identifiers -- dropped from the seed list.
_IDENT_JUNK = {"custom", "none", "(none)", "n/a", "na", "varies", "various", "unknown", ""}

# Auth policies, widest-to-narrowest. The default ('none') is the only one safe to
# run fully unattended -- no secret needed. The others need keys wired in .env.
_AUTH_CLAUSE = {
    "none": "LOWER(TRIM(COALESCE(AUTH_REQUIRED,'none'))) = 'none'",
    "no-secret": "LOWER(TRIM(COALESCE(AUTH_REQUIRED,''))) IN ('none','')",
    "any": "1=1",
}


def fetch_candidates(
    limit: int = 5,
    tier: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    source_id: Optional[str] = None,
    auth: str = "none",
    include_landed: bool = False,
) -> List[dict]:
    """Return onboarding-ready source dicts selected from the live registry.

    Ordered by ``PRIORITY_TIER`` (1 first), then ``SOURCE_ID`` for a stable queue.
    Each dict is shaped for ``onboard.onboard_source`` (name/url/source_id/
    jurisdiction/layer/identifiers) plus ``_``-prefixed preview fields.
    """
    conds = [
        "TRIM(COALESCE(INCLUDE,'')) <> 'Y'",
        "URL IS NOT NULL AND TRIM(URL) <> ''",
        "REGEXP_LIKE(SOURCE_ID, '^(fed|intl|xc|loc|st)_.*')",
    ]
    params: dict = {"limit": int(limit)}

    if not include_landed:
        conds.append(
            "SOURCE_ID NOT IN (SELECT DISTINCT SOURCE_ID FROM "
            "LIBRARY_META.INGEST_LOGS.INGEST_RUNS WHERE STATUS = 'success')"
        )
    conds.append(_AUTH_CLAUSE.get(auth, _AUTH_CLAUSE["none"]))
    if tier:
        conds.append("TRIM(PRIORITY_TIER) = %(tier)s")
        params["tier"] = str(tier).strip()
    if jurisdiction:
        conds.append("LOWER(TRIM(JURISDICTION)) = %(jur)s")
        params["jur"] = jurisdiction.strip().lower()
    if source_id:
        conds.append("SOURCE_ID = %(sid)s")
        params["sid"] = source_id.strip()

    sql = (
        "SELECT SOURCE_ID, NAME, URL, JURISDICTION, JOIN_KEYS, PRIORITY_TIER, "
        "ACCESS_METHOD, FORMAT, AUTH_REQUIRED, CATEGORY "
        "FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY "
        f"WHERE {' AND '.join(conds)} "
        "ORDER BY TRY_TO_NUMBER(PRIORITY_TIER) NULLS LAST, SOURCE_ID "
        "LIMIT %(limit)s"
    )

    conn = snow.connect()
    try:
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            cols = [c[0] for c in cur.description]
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        finally:
            cur.close()
    finally:
        conn.close()
    return [_to_source(r) for r in rows]


def _to_source(row: dict) -> dict:
    """Map a SOURCE_REGISTRY row to the agent's source-dict shape."""
    jur = (row.get("JURISDICTION") or "").strip().lower()
    identifiers = [
        tok.strip()
        for tok in re.split(r"[,;]", row.get("JOIN_KEYS") or "")
        if tok.strip() and tok.strip().lower() not in _IDENT_JUNK
    ]
    return {
        # --- consumed by onboard_source / recon -------------------------
        "name": row["NAME"],
        "source_id": row["SOURCE_ID"],  # pinned -> updates THIS registry row
        "url": row["URL"],
        "jurisdiction": jur,
        "layer": _JURISDICTION_LAYER.get(jur, "investigative"),
        "identifiers": identifiers,
        # --- preview only (ignored by the agent) ------------------------
        "_tier": (row.get("PRIORITY_TIER") or "").strip(),
        "_access_method": row.get("ACCESS_METHOD") or "",
        "_format": row.get("FORMAT") or "",
        "_category": row.get("CATEGORY") or "",
    }
