"""The lineage walker + provenance grader.

Everything here is mechanical and FAIL-CLOSED: when the walker cannot prove a
join is hard-ID-anchored, the grade drops. The one deliberate judgment call,
made once and documented (honesty/README.md), is the join taxonomy:

  hard-anchored  the ON/USING clause contains at least one equality on a hard
                 identifier (NPI/CCN/UEI/EIN/CIK/DUNS/LEI/IMO/MMSI/BIOGUIDE/
                 ICPSR). Extra name predicates only further RESTRICT a
                 hard-anchored join (they cannot merge strangers), so
                 hard+name composites stay fact-compatible.
  name-join      identity established by name-ish columns with NO hard ID in
                 the clause -> the mart can merge strangers -> 'unverified'.
  neutral        conformed-dimension equalities (state, date, county, codes):
                 they group rows, they don't assert identity.
  unparseable    the walker cannot extract any column from the clause ->
                 'unverified' (fail closed, never fail open).

Claim-layer ancestry (LEADS / V_LEADS_PUBLISHED / REVIEW.DECISIONS / the spine
claim tables, mirrored from viz/guard.py CLAIM_TABLES) grades 'lead': those
rows are review-gated claims by construction, not re-derivable landing facts.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .traps import traps_for_source

FACT = "fact"
LEAD = "lead"
UNVERIFIED = "unverified"
_STRENGTH = {FACT: 2, LEAD: 1, UNVERIFIED: 0}

# Hard identifiers — the same key set the connect spine indexes on
# (connect/entity_index_specs.py ENTITY_TYPE_BY_KEY / connect/keys.py STEEL).
# 2026-07-30: added DEA_NO/FRS_ID/PWSID/MINE_ID/FEC_CMTE_ID/FEC_CAND_ID — a
# same-day connect/ wiring pass (35 new sources, 6 new key types) had drifted
# this list 6 keys behind connect's actual STEEL set; this comment's own claim
# of parity was false until this fix. Keep these two lists in lockstep by hand
# until they're generated from one shared source.
HARD_ID_TOKENS = {
    "NPI", "CCN", "UEI", "EIN", "CIK", "DUNS", "LEI",
    "IMO", "MMSI", "BIOGUIDE", "ICPSR",
    "DEA_NO", "FRS_ID", "PWSID", "MINE_ID", "FEC_CMTE_ID", "FEC_CAND_ID", "PATENT",
}

# Claim/review surfaces: viz/guard.py:36 CLAIM_TABLES + the review lane +
# the queue mart. Ancestry through ANY of these = 'lead'.
CLAIM_SURFACES = {
    "LEADS", "ENTITY_LINKS", "ENTITY_MAP", "ENTITY_GOLDEN", "MATCH_PAIRS",
    "V_LEADS_PUBLISHED", "V_LATEST_DECISIONS", "DECISIONS", "LEAD_QUEUE",
}

_SQL_KEYWORDS = {
    "AND", "OR", "NOT", "ON", "IN", "IS", "NULL", "LIKE", "ILIKE", "BETWEEN",
    "CASE", "WHEN", "THEN", "ELSE", "END", "TRUE", "FALSE", "AS", "CAST",
    "COALESCE", "NULLIF", "UPPER", "LOWER", "TRIM", "LTRIM", "RTRIM",
    "REGEXP_REPLACE", "SUBSTR", "SUBSTRING", "LENGTH", "LEFT", "RIGHT",
    "TRY_TO_NUMBER", "TRY_TO_DATE", "TRY_TO_TIMESTAMP_NTZ", "TRY_CAST",
    "TO_CHAR", "TO_DATE", "ABS", "ROUND", "FLOOR", "GREATEST", "LEAST",
    "CONCAT", "SPLIT_PART", "LPAD", "RPAD", "REPLACE", "IFF", "VARCHAR",
    "NUMBER", "INT", "INTEGER", "STRING", "DATE", "USING",
}

_COMMENT_RE = re.compile(r"--[^\n]*|/\*.*?\*/", re.DOTALL)
# {# … #} jinja comments included — a prose "joined to AIS" inside one once
# produced a phantom join finding (caught on the first live run, 2026-07-21).
_JINJA_RE = re.compile(r"\{\{.*?\}\}|\{%-?.*?-?%\}|\{#.*?#\}", re.DOTALL)
_STRING_RE = re.compile(r"'[^']*'")
# Boundary note: LEFT/RIGHT are both join keywords AND SQL functions — a bare
# \bleft\b boundary would truncate "ON LEFT(a.borrname,3) = …" mid-clause and
# let a name-join slip through as neutral (fail OPEN). The (?!\s*\() guard
# keeps LEFT(/RIGHT( inside the captured clause.
_JOIN_RE = re.compile(
    r"\bjoin\b\s+(?P<rest>.*?)(?=\b(?:left|right|full|inner|cross|outer)\b(?!\s*\()|"
    r"\b(?:join|where|group|qualify|window|order|limit|having|union|select)\b|\Z)",
    re.IGNORECASE | re.DOTALL,
)
_USING_RE = re.compile(r"\busing\s*\(([^)]*)\)", re.IGNORECASE)
_ON_RE = re.compile(r"\bon\b(?P<expr>.*)", re.IGNORECASE | re.DOTALL)
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_$]*(?:\s*\.\s*[A-Za-z_][A-Za-z0-9_$]*)*")


@dataclass
class Reason:
    kind: str    # name_join | unparseable_join | claim_ancestry | no_sql
    node: str    # which ancestor model/source earned the demotion
    detail: str  # the receipt — the clause or surface that triggered it

    def as_dict(self) -> dict:
        return {"kind": self.kind, "node": self.node, "detail": self.detail}


@dataclass
class Grade:
    node_id: str
    grade: str
    reasons: list[Reason] = field(default_factory=list)
    traps: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    n_ancestors: int = 0

    def as_dict(self) -> dict:
        return {
            "model": self.node_id,
            "grade": self.grade,
            "reasons": [r.as_dict() for r in self.reasons],
            "traps": list(self.traps),
            "sources": list(self.sources),
            "n_ancestors": self.n_ancestors,
        }


def load_manifest(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _is_namey(col: str) -> bool:
    return "NAME" in col.upper()


def _is_hard(col: str) -> bool:
    # A name column never counts as hard, even when it wears an ID prefix:
    # NPI_NAME / UEI_NAME are names that mention a register, and letting the
    # prefix win would UPGRADE a pure name-join to fact (fail open — caught
    # by the 2026-07-21 adversarial review).
    if _is_namey(col):
        return False
    c = col.upper()
    return any(c == t or c.endswith("_" + t) or c.startswith(t + "_") for t in HARD_ID_TOKENS)


def _clause_columns(expr: str) -> list[str]:
    cols = []
    for m in _IDENT_RE.finditer(expr):
        ident = m.group(0)
        col = re.split(r"\s*\.\s*", ident)[-1]
        if col.upper() in _SQL_KEYWORDS:
            continue
        cols.append(col)
    return cols


def classify_join_clause(expr: str) -> str:
    """'hard' | 'name' | 'neutral' | 'unparseable' for one ON/USING clause."""
    expr = (expr or "").strip()
    if not expr:
        return "unparseable"
    # A jinja fragment inside the predicate means the clause is assembled at
    # parse time — unknowable here, so it demotes. (The placeholder used to
    # read as a neutral column and sail through: fail open, caught 2026-07-21.)
    if re.search(r"\bJINJA_REF\b", expr):
        return "unparseable"
    cols = _clause_columns(expr)
    if not cols:
        return "unparseable"
    if any(_is_hard(c) for c in cols):
        return "hard"
    if any(_is_namey(c) for c in cols):
        return "name"
    return "neutral"


def _split_subqueries(sql: str) -> tuple[str, list[str], bool]:
    """Replace each parenthesized (SELECT …) group with ' SUBQ ' and return
    (outer_sql, [inner_sql, …], balanced_ok). Inner texts are analyzed
    recursively so a name-join INSIDE a subquery can never hide (that would
    be the fail-open direction). Unbalanced parens -> balanced_ok=False and
    the caller records an unparseable finding (fail closed)."""
    inners: list[str] = []
    pat = re.compile(r"\(\s*select\b", re.IGNORECASE)
    while True:
        m = pat.search(sql)
        if not m:
            return sql, inners, True
        depth, end = 0, None
        for j in range(m.start(), len(sql)):
            if sql[j] == "(":
                depth += 1
            elif sql[j] == ")":
                depth -= 1
                if depth == 0:
                    end = j
                    break
        if end is None:
            inners.append(sql[m.start() + 1:])
            return sql[:m.start()] + " SUBQ ", inners, False
        inners.append(sql[m.start() + 1:end])
        sql = sql[:m.start()] + " SUBQ " + sql[end + 1:]


_FROM_LIST_RE = re.compile(
    r"\bfrom\b(?P<fl>.*?)(?=\b(?:where|join|left|right|full|inner|cross|outer|natural|"
    r"group|qualify|window|order|limit|having|union|select|on)\b(?!\s*\()|\Z)",
    re.IGNORECASE | re.DOTALL,
)
_WHERE_RE = re.compile(
    r"\bwhere\b(?P<expr>.*?)(?=\b(?:group|qualify|window|order|limit|having|union|select)\b|\Z)",
    re.IGNORECASE | re.DOTALL,
)
# Tolerates function wrapping on either side: upper(a.entity_name) = upper(b.name)
_CROSS_ALIAS_EQ_RE = re.compile(
    r"([A-Za-z_][\w$]*)\s*\.\s*([A-Za-z_][\w$]*)\s*\)*\s*=\s*"
    r"(?:[A-Za-z_][\w$]*\s*\(\s*|\(\s*)*([A-Za-z_][\w$]*)\s*\.\s*([A-Za-z_][\w$]*)"
)
_IN_SUBQ_RE = re.compile(
    r"(?:([A-Za-z_][\w$]*)\s*\.\s*)?([A-Za-z_][\w$]*)\s+(?:not\s+)?in\s+SUBQ\b",
    re.IGNORECASE,
)


def _top_level_commas(text: str) -> list[int]:
    """Positions of commas at paren depth 0 (relation separators, not args)."""
    depth, out = 0, []
    for i, c in enumerate(text):
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        elif c == "," and depth == 0:
            out.append(i)
    return out


def _classify_cols(cols: list[str]) -> str:
    if any(_is_hard(c) for c in cols):
        return "hard"
    if any(_is_namey(c) for c in cols):
        return "name"
    return "neutral"


def _joins_in_flat_sql(sql: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for jm in _JOIN_RE.finditer(sql):
        seg = jm.group("rest")
        head = sql[max(0, jm.start() - 16):jm.start()].lower()
        um = _USING_RE.search(seg)
        if um:
            out.append((classify_join_clause(um.group(1)), "USING(" + um.group(1).strip()[:120] + ")"))
            continue
        om = _ON_RE.search(seg)
        if om:
            expr = om.group("expr").strip()
            out.append((classify_join_clause(expr), "ON " + " ".join(expr.split())[:160]))
            continue
        if re.search(r"\bnatural\s*$", head):
            out.append(("unparseable", "NATURAL JOIN — implicit predicate (fail closed)"))
            continue
        if re.search(r"\bcross\s*$", head):
            out.append(("neutral", "CROSS JOIN (no predicate by design)"))
            continue
        out.append(("unparseable", " ".join(seg.split())[:120] or "<empty join segment>"))

    # Comma-style FROM lists carry no JOIN keyword at all (fail-open hole,
    # caught 2026-07-21 — the shape is live in production via LATERAL FLATTEN).
    for fm in _FROM_LIST_RE.finditer(sql):
        fl = fm.group("fl")
        for pos in _top_level_commas(fl):
            tail = fl[pos + 1:].lstrip().lower()
            if tail.startswith("lateral") or tail.startswith("table"):
                out.append(("neutral", "comma + LATERAL/TABLE — row expansion of the same row, no cross-relation identity"))
            else:
                out.append(("unparseable", "comma-join — predicates live in WHERE; the walker cannot bind them (fail closed)"))

    # WHERE-clause identity logic: cross-alias equalities (joins in disguise —
    # comma-join predicates and semi-join correlations) and IN-(SELECT …)
    # anchors. A name-based one merges strangers just like a name ON-clause.
    for wm in _WHERE_RE.finditer(sql):
        expr = wm.group("expr")
        for q1, c1, q2, c2 in _CROSS_ALIAS_EQ_RE.findall(expr):
            if q1.lower() != q2.lower() and q1.upper() not in _SQL_KEYWORDS and q2.upper() not in _SQL_KEYWORDS:
                out.append((_classify_cols([c1, c2]),
                            f"WHERE {q1}.{c1} = {q2}.{c2} (cross-alias equality)"))
        for _, col in _IN_SUBQ_RE.findall(expr):
            out.append((_classify_cols([col]), f"WHERE {col} IN (subquery) — semi-join anchor"))
    return out


def _analyze_sql_text(sql: str) -> list[tuple[str, str]]:
    outer, inners, balanced = _split_subqueries(sql)
    out = _joins_in_flat_sql(outer)
    if not balanced:
        out.append(("unparseable", "<unbalanced parentheses — fail closed>"))
    for inner in inners:
        out.extend(_analyze_sql_text(inner))
    return out


def analyze_model_sql(raw_code: str) -> list[tuple[str, str]]:
    """[(classification, clause_snippet)] for every join in one model's SQL,
    including joins inside subqueries (analyzed recursively).

    Fail-closed: a JOIN whose predicate can't be located classifies
    'unparseable'. CROSS JOIN (no predicate by design) is 'neutral'.
    """
    if not (raw_code or "").strip():
        return [("unparseable", "<empty raw_code>")]
    sql = _COMMENT_RE.sub(" ", raw_code)
    sql = _JINJA_RE.sub(" JINJA_REF ", sql)
    sql = _STRING_RE.sub("''", sql)   # a '(' inside a string literal must not unbalance the scanner
    return _analyze_sql_text(sql)


def _scrub(raw_code: str) -> str:
    """Comments, jinja (incl. {# #}), and string literals removed — the same
    scrubbing analyze_model_sql does, applied everywhere raw SQL is scanned
    (a display string mentioning CONNECT.LEADS must not mint a demotion, and
    one mentioning LANDING.X must not mint a trap)."""
    sql = _COMMENT_RE.sub(" ", raw_code or "")
    sql = _JINJA_RE.sub(" JINJA_REF ", sql)
    return _STRING_RE.sub("''", sql)


def _claim_refs_in_sql(raw_code: str) -> set[str]:
    """Claim surfaces referenced by LITERAL name in SQL (catches hardcoded
    FQNs that bypass ref()/source()) — same trick as viz/guard.py. Prefix set
    deliberately broad: a claim table read through any schema mirror demotes."""
    hits = set()
    sql = _scrub(raw_code)
    for t in CLAIM_SURFACES:
        if re.search(
            rf'(?:"?CONNECT"?|"?REVIEW"?|DBT_CROGERS|PUBLIC|LIBRARY_MARTS|LIBRARY_META)\s*\.\s*"?{t}"?\b',
            sql, re.IGNORECASE,
        ):
            hits.add(t)
    return hits


def _ancestors(manifest: dict, node_id: str) -> tuple[set[str], set[str], set[str]]:
    """(model node_ids incl. self+seeds, source node_ids, UNRESOLVED ids).

    An unresolved dependency (disabled model, deleted node, cross-project ref)
    is lineage the walker literally cannot see — it must demote, never vanish
    (fail-open hole caught by the 2026-07-21 adversarial review)."""
    nodes, sources = manifest["nodes"], manifest.get("sources", {})
    seen_models: set[str] = set()
    seen_sources: set[str] = set()
    unresolved: set[str] = set()
    stack = [node_id]
    while stack:
        nid = stack.pop()
        if nid in seen_models or nid in seen_sources or nid in unresolved:
            continue
        if nid in sources:
            seen_sources.add(nid)
            continue
        node = nodes.get(nid)
        if node is None:
            unresolved.add(nid)
            continue
        seen_models.add(nid)
        for dep in (node.get("depends_on") or {}).get("nodes", []):
            stack.append(dep)
    return seen_models, seen_sources, unresolved


def grade_model(manifest: dict, node_id: str) -> Grade:
    nodes, sources = manifest["nodes"], manifest.get("sources", {})
    model_ids, source_ids, unresolved = _ancestors(manifest, node_id)

    reasons: list[Reason] = []
    traps: set[str] = set()
    src_tables: set[str] = set()

    for uid in sorted(unresolved):
        reasons.append(Reason(
            "unknown_ancestor", uid,
            "dependency not found in the manifest (disabled/deleted/cross-project) — "
            "unwalkable lineage fails closed"))

    for sid in source_ids:
        ident = (sources[sid].get("identifier") or sources[sid].get("name") or "").upper()
        src_tables.add(ident)
        traps.update(traps_for_source(ident))
        if ident in CLAIM_SURFACES:
            reasons.append(Reason("claim_ancestry", sid, f"reads claim surface {ident}"))

    for mid in sorted(model_ids):
        node = nodes[mid]
        if node.get("resource_type") == "seed":
            continue
        raw = node.get("raw_code") or ""
        if not raw.strip():
            reasons.append(Reason("no_sql", mid, "model has no raw_code in the manifest"))
            continue
        for surface in sorted(_claim_refs_in_sql(raw)):
            reasons.append(Reason("claim_ancestry", mid, f"literal reference to claim surface {surface}"))
        for cls, snippet in analyze_model_sql(raw):
            if cls == "name":
                reasons.append(Reason("name_join", mid, snippet))
            elif cls == "unparseable":
                reasons.append(Reason("unparseable_join", mid, snippet))
        for ident in re.findall(r"LANDING\s*\.\s*\"?([A-Za-z0-9_]+)\"?", _scrub(raw), re.IGNORECASE):
            traps.update(traps_for_source(ident))

    grade = FACT
    for r in reasons:
        demoted = LEAD if r.kind == "claim_ancestry" else UNVERIFIED
        if _STRENGTH[demoted] < _STRENGTH[grade]:
            grade = demoted

    return Grade(
        node_id=node_id,
        grade=grade,
        reasons=reasons,
        traps=tuple(sorted(traps)),
        sources=tuple(sorted(src_tables)),
        n_ancestors=len(model_ids) + len(source_ids) - 1,
    )


def mart_ids(manifest: dict) -> list[str]:
    return sorted(
        k for k, v in manifest["nodes"].items()
        if v.get("resource_type") == "model"
        and "/marts/" in (v.get("original_file_path") or "").replace("\\", "/")
    )


def grade_marts(manifest: dict) -> dict[str, Grade]:
    return {nid: grade_model(manifest, nid) for nid in mart_ids(manifest)}
