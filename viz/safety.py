"""Facts-vs-leads discipline for ad-hoc SQL. Same rule as the whole platform:

    same hard ID  = fact-grade co-occurrence (still phrased neutrally)
    same name only = a LEAD - pending, unpublished, never rendered as fact
    a human confirms before anything is treated as true

classify_query() is deliberately DOWNGRADE-ONLY. It can stamp a chart as a
lead or as unverified; it never certifies "fact" — a regex-grade SQL parser
must not make positive claims its coverage can't back. Anything it cannot
parse with confidence FAILS CLOSED to 'unverified'. The enforced read-only
role and the claim-table block in sqlrun are the real walls; this is the
honesty layer on top.

Three states:
  'lead'        a NAME/ADDRESS-tier join, or the query reads claim tables
                (LEADS etc.) — the chart carries a visible LEAD badge.
  'unverified'  the classifier could not confidently tier every join
                (aliases, USING it can't resolve, implicit joins, subquery
                predicates, OR'd conditions, geo-only joins) — neutral badge.
  'clean'       single-table query, or every join column resolved to a
                STEEL/STRONG hard-ID tier. No badge.
"""

from __future__ import annotations

import re

from viz import guard

# Badge copy per trigger — parametrized so the badge never mislabels itself.
BADGE_TEXT = {
    "claims": "reads unreviewed LEADS - unconfirmed until a human verdict; leads are not facts",
    "name-join": "name-based match - investigative lead, not established fact",
    "address-join": "address-based match - investigative lead, not established fact",
    "geo-join": "geo-tier join - shared geography is context, not a connection",
    "unverified": "join basis not verified by the classifier - treat cross-table claims as unconfirmed",
    "score": "SCORE is an uncalibrated composite - a ranking signal, not a probability",
}

_CLAIM_COLS = {"LEAD_ID", "RULE_NAME", "REVIEW_STATE"}

_STOP = r"(?=\bJOIN\b|\bWHERE\b|\bGROUP\b|\bORDER\b|\bQUALIFY\b|\bHAVING\b|\bLIMIT\b|\bUNION\b|$)"
_ON_RE = re.compile(rf"\bJOIN\b.*?\bON\b(.*?){_STOP}", re.IGNORECASE | re.DOTALL)
_USING_RE = re.compile(r"\bUSING\s*\(([^)]*)\)", re.IGNORECASE | re.DOTALL)
_EQ_RE = re.compile(r'([A-Z0-9_."]+)\s*=\s*([A-Z0-9_."]+)', re.IGNORECASE)


def classify_query(sql: str, df=None) -> dict:
    """-> {'state': 'lead'|'unverified'|'clean', 'triggers': [...], 'joins': [...]}"""
    triggers: list[str] = []
    joins: list[dict] = []

    if guard.claim_refs(sql):
        triggers.append("claims")
    if df is not None and _CLAIM_COLS & {str(c).upper() for c in df.columns}:
        triggers.append("claims")
    if df is not None and "SCORE" in {str(c).upper() for c in df.columns} and "claims" in triggers:
        triggers.append("score")

    skeleton = guard.strip_comments_and_strings(sql)
    upper = skeleton.upper()
    flat = _blank_parens(upper)  # subqueries/functions blanked for structure checks

    unverified = False
    if re.search(r"\bNATURAL\s+JOIN\b", upper):
        unverified = True
    if re.search(r"\b(IN|EXISTS)\s*\(\s*SELECT\b", upper):
        unverified = True  # semi-join: a cross-table claim the tier scan can't see
    for seg in re.findall(rf"\bFROM\b(.*?){_STOP}", flat, re.IGNORECASE | re.DOTALL):
        if "," in seg:
            unverified = True  # implicit comma-join: conditions live in WHERE

    # USING (col, ...) — columns are explicit, so tier them directly. The regex
    # is deliberately NOT anchored to JOIN: `JOIN (subquery) v USING (col)` puts
    # parens between JOIN and USING, and missing that join would fail OPEN.
    n_using = 0
    for cols in _USING_RE.findall(upper):
        n_using += 1
        for col in [c.strip() for c in cols.split(",") if c.strip()]:
            joins.append(_tier(col))

    # JOIN ... ON — tier both sides of every equality; anything else fails closed.
    n_on = 0
    for cond in _ON_RE.findall(upper):
        n_on += 1
        pairs = _EQ_RE.findall(cond)
        if re.search(r"\bOR\b", cond) or cond.count("=") != len(pairs) or not pairs:
            unverified = True
        for a, b in pairs:
            joins.append(_tier(a))
            joins.append(_tier(b))

    # THE fail-closed net: any JOIN whose condition we did not capture (CROSS
    # JOIN, subquery forms the scans missed, exotic syntax) means the classifier
    # cannot see the join basis — that must never read as clean.
    if len(re.findall(r"\bJOIN\b", upper)) > n_on + n_using:
        unverified = True

    for j in joins:
        if j["tier"] is None:
            unverified = True  # an alias/expression the tagger can't tier
        elif j["key"] in ("NAME", "PERSON"):
            triggers.append("name-join")
        elif j["key"] == "ADDRESS":
            triggers.append("address-join")
        elif j["tier"] == "GEO":
            triggers.append("geo-join")

    if "claims" in triggers or "name-join" in triggers or "address-join" in triggers:
        state = "lead"
    elif unverified or "geo-join" in triggers:
        state = "unverified"
        if unverified and "geo-join" not in triggers:
            triggers.append("unverified")
    else:
        state = "clean"
    return {"state": state, "triggers": _dedupe(triggers), "joins": joins}


def _tier(dotted: str) -> dict:
    """Tier one join operand by its column name (connect/keys tagger — pure)."""
    col = dotted.split(".")[-1].strip().strip('"')
    try:
        from connect.keys import detect_key
        key, tier = detect_key(col)
    except Exception:
        key, tier = None, None
    return {"column": col, "key": key, "tier": tier}


def _blank_parens(text: str) -> str:
    """Blank innermost (...) groups repeatedly so top-level structure scans
    (comma-FROM detection) aren't fooled by subqueries or function args."""
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"\([^()]*\)", "()", text)
    return text


def _dedupe(items):
    seen, out = set(), []
    for i in items:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


# --------------------------------------------------------------------------- #
# The badge — visible on the figure, serialized into the card as literal code
# --------------------------------------------------------------------------- #
def badge(fig, state: str, text: str):
    """Stamp a facts-vs-leads badge onto a figure. Called with LITERAL args from
    cards so the badge survives re-runs and eject."""
    from viz import theme
    color = theme.CATEGORICAL[5] if state == "lead" else theme.MUTED  # validated red
    fig.add_annotation(
        text=f"[{state.upper()}] {text}", xref="paper", yref="paper",
        x=0, y=1.10, xanchor="left", showarrow=False,
        font=dict(color=color, size=12),
    )
    return fig


def badge_args(classification: dict):
    """(state, text) for the badge, or None when no badge is due."""
    state = classification.get("state", "unverified")
    if state == "clean":
        return None
    for trig in classification.get("triggers", []):
        if trig in BADGE_TEXT:
            return state, BADGE_TEXT[trig]
    return state, BADGE_TEXT["unverified"]
