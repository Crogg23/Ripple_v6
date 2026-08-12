"""Census grid — step 1: extract per-model metadata from the dbt manifest.

Reads target/manifest.json (built 2026-08-11) and emits one JSON record per
model with: identity, layer, subject, grain declaration, spine hint, and the
full output column list recovered from the model SQL (star-selects resolved
through CTEs and upstream refs). Deterministic, no LLM, no warehouse access.

Output: models.jsonl (one line per model) + extract_report.json (coverage
accounting: how many models parsed clean, how many degraded, how many failed —
the failures stay visible, they are rows in the census, not dropped).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "library-onboarding" / "ripple_dbt" / "target" / "manifest.json"

# ---------------------------------------------------------------- SQL helpers

JINJA_BLOCK = re.compile(r"\{%.*?%\}", re.S)
JINJA_COMMENT = re.compile(r"\{#.*?#\}", re.S)
JINJA_EXPR = re.compile(r"\{\{.*?\}\}", re.S)
LINE_COMMENT = re.compile(r"--[^\n]*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
REF_EXPR = re.compile(r"\{\{\s*ref\(\s*['\"]([A-Za-z0-9_]+)['\"]\s*\)\s*\}\}")
SOURCE_EXPR = re.compile(r"\{\{\s*source\(\s*['\"]([A-Za-z0-9_]+)['\"]\s*,\s*['\"]([A-Za-z0-9_.]+)['\"]\s*\)\s*\}\}")


def strip_sql(sql: str) -> str:
    """Remove comments; replace jinja with stable placeholders so refs survive."""
    sql = JINJA_COMMENT.sub(" ", sql)
    sql = BLOCK_COMMENT.sub(" ", sql)
    sql = LINE_COMMENT.sub(" ", sql)
    # keep ref()/source() targets recoverable: turn them into pseudo identifiers
    sql = REF_EXPR.sub(lambda m: f"__REF__{m.group(1)}", sql)
    sql = SOURCE_EXPR.sub(lambda m: f"__SRC__{m.group(1)}__{m.group(2)}", sql)
    sql = JINJA_BLOCK.sub(" ", sql)
    sql = JINJA_EXPR.sub(" __JINJA__ ", sql)
    return sql


def split_top_level(text: str, sep: str = ",") -> list[str]:
    """Split on sep at paren depth 0 (quotes respected)."""
    parts, buf, depth, i, n = [], [], 0, 0, len(text)
    in_squote = in_dquote = False
    while i < n:
        c = text[i]
        if in_squote:
            buf.append(c)
            if c == "'":
                in_squote = False
        elif in_dquote:
            buf.append(c)
            if c == '"':
                in_dquote = False
        elif c == "'":
            in_squote = True
            buf.append(c)
        elif c == '"':
            in_dquote = True
            buf.append(c)
        elif c == "(":
            depth += 1
            buf.append(c)
        elif c == ")":
            depth -= 1
            buf.append(c)
        elif c == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(c)
        i += 1
    parts.append("".join(buf))
    return parts


KW = re.compile(r"\b(select|from|where|group\s+by|order\s+by|qualify|union|window|having|limit)\b", re.I)


def find_final_select(sql: str) -> tuple[str, str] | None:
    """Return (select_list, from_target_token) of the last top-level SELECT."""
    depth = 0
    in_squote = in_dquote = False
    positions = []  # (index, keyword) at depth 0
    i, n = 0, len(sql)
    while i < n:
        c = sql[i]
        if in_squote:
            if c == "'":
                in_squote = False
        elif in_dquote:
            if c == '"':
                in_dquote = False
        elif c == "'":
            in_squote = True
        elif c == '"':
            in_dquote = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0 and c.isalpha():
            m = KW.match(sql, i)
            if m and (i == 0 or not (sql[i - 1].isalnum() or sql[i - 1] == "_")):
                positions.append((i, m.group(1).lower()))
                i = m.end()
                continue
        i += 1
    # last top-level select
    sel_idx = None
    for idx, kw in positions:
        if kw == "select":
            sel_idx = idx
    if sel_idx is None:
        return None
    # matching top-level FROM after it
    from_idx = None
    end_idx = len(sql)
    for idx, kw in positions:
        if idx > sel_idx:
            if kw == "from" and from_idx is None:
                from_idx = idx
            elif kw != "from" and from_idx is not None and idx > from_idx:
                end_idx = min(end_idx, idx)
                break
    if from_idx is None:
        return sql[sel_idx + 6 :], ""
    from_clause = sql[from_idx + 4 : end_idx].strip()
    target = from_clause.split()[0].strip() if from_clause else ""
    return sql[sel_idx + 6 : from_idx], target


IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")
AS_ALIAS = re.compile(r"\bas\s+(\"[^\"]+\"|[A-Za-z_][A-Za-z0-9_$]*)\s*$", re.I)
STAR_MODS = re.compile(r"^(?:[A-Za-z_][A-Za-z0-9_]*\.)?\*\s*(?:exclude|except)\s*\(([^)]*)\)", re.I)


def item_to_column(item: str) -> str | list[str] | None:
    """One select-list item -> column name, '*', ['*', excl1, ...] for
    star-with-exclude, or None."""
    item = item.strip()
    if not item:
        return None
    if item == "*" or item.endswith(".*"):
        return "*"
    if re.match(r"^(?:[A-Za-z_][A-Za-z0-9_]*\.)?\*\s*replace\s*\(", item, re.I):
        return "*"  # replaced columns keep their names
    m = STAR_MODS.match(item)
    if m:
        excludes = [c.strip().strip('"').lower() for c in m.group(1).split(",") if c.strip()]
        return ["*"] + excludes
    m = AS_ALIAS.search(item)
    if m:
        return m.group(1).strip('"').lower()
    # bare column, possibly qualified: t.col or "COL"
    tail = item.split(".")[-1].strip().strip('"')
    if IDENT.match(tail):
        return tail.lower()
    return None


CTE_DEF = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s+as\s*\(", re.I)


def parse_ctes(sql: str) -> dict[str, str]:
    """Map cte_name -> body text (top-level 'name as (' only)."""
    ctes = {}
    for m in CTE_DEF.finditer(sql):
        # verify at top level: count unbalanced parens before match
        prefix = sql[: m.start()]
        depth = prefix.count("(") - prefix.count(")")
        if depth != 0:
            continue
        # extract balanced body
        i = m.end()
        d = 1
        while i < len(sql) and d > 0:
            if sql[i] == "(":
                d += 1
            elif sql[i] == ")":
                d -= 1
            i += 1
        ctes[m.group(1).lower()] = sql[m.end() : i - 1]
    return ctes


def resolve_columns(sql: str) -> tuple[list[str], str, str]:
    """Return (columns, quality, star_target).

    quality: 'clean' | 'star-cte-resolved' | 'star-upstream' (needs pass 2)
             | 'no-select' (failed)
    star_target: pseudo identifier the star points to (for pass 2), else ''.
    """
    stripped = strip_sql(sql)
    ctes = parse_ctes(stripped)
    seen_ctes: set[str] = set()
    body = stripped
    quality = "clean"
    carry: list[str] = []  # explicit columns picked up on outer hops
    excludes: set[str] = set()  # star-exclude'd columns, dropped at the end

    def finish(cols: list[str]) -> list[str]:
        merged = cols + [c for c in carry if c not in cols]
        return [c for c in merged if c not in excludes]

    for _hop in range(12):
        fs = find_final_select(body)
        if fs is None:
            return finish([]), "no-select" if not carry else quality, ""
        select_list, target = fs
        items = [item_to_column(p) for p in split_top_level(select_list)]
        cols: list[str] = []
        has_star = False
        for it in items:
            if it is None:
                continue
            if it == "*":
                has_star = True
            elif isinstance(it, list):  # ['*', excl1, ...]
                has_star = True
                excludes.update(it[1:])
            else:
                cols.append(it)
        if not has_star:
            return finish(cols), quality, ""
        carry.extend(c for c in cols if c not in carry)
        # star: chase the from-target
        t = target.lower().strip('"')
        if t in ctes and t not in seen_ctes:
            seen_ctes.add(t)
            body = ctes[t]
            quality = "star-cte-resolved"
            continue
        if t.startswith("__ref__"):
            return finish([]), "star-upstream", t.removeprefix("__ref__")
        if t.startswith("__src__"):
            return finish([]), "star-source", t
        return finish([]), "star-unresolved", t
    return finish([]), "star-loop", ""


# ------------------------------------------------------------- grain parsing

GRAIN_RE = re.compile(r"GRAIN:\s*one row per\s+([^(.;\n]+)", re.I)
SPINE_RE = re.compile(r"SPINE_ENTITY:\s*([^\n(]+)", re.I)
NATKEY_RE = re.compile(r"natural_key:\s*([A-Za-z0-9_,\s]+)\)", re.I)
GRAIN_LOOSE = re.compile(r"\bone row per\s+([^(.;\n]+)", re.I)


def parse_grain(description: str, raw_sql: str) -> dict:
    text = (description or "") + "\n" + (raw_sql[:2000] if raw_sql else "")
    g = GRAIN_RE.search(text) or GRAIN_LOOSE.search(text)
    s = SPINE_RE.search(text)
    k = NATKEY_RE.search(text)
    grain = g.group(1).strip().rstrip(",- ") if g else ""
    spine = s.group(1).strip() if s else ""
    if spine.lower().startswith("(not determined"):
        spine = ""
    return {
        "grain_phrase": grain,
        "spine_entity": spine,
        "natural_key": k.group(1).strip() if k else "",
        "grain_declared": bool(g),
    }


# --------------------------------------------------------------------- main

def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "reports" / "census_grid_2026-08-12" / "build"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    models = {}
    for uid, node in manifest["nodes"].items():
        if node.get("resource_type") != "model":
            continue
        path = node.get("path", "").replace("\\", "/")
        parts = path.split("/")
        layer = parts[0] if parts else ""
        subject = parts[1] if len(parts) > 1 else ""
        raw = node.get("raw_code") or node.get("raw_sql") or ""
        cols, quality, star_target = resolve_columns(raw)
        grain = parse_grain(node.get("description", ""), raw)
        models[node["name"]] = {
            "name": node["name"],
            "unique_id": uid,
            "layer": layer,
            "subject": subject,
            "database": node.get("database", ""),
            "schema": node.get("schema", ""),
            "alias": node.get("alias") or node["name"],
            "description": (node.get("description") or "")[:500],
            "tags": node.get("tags", []),
            "materialized": (node.get("config") or {}).get("materialized", ""),
            "depends_on": [d.split(".")[-1] for d in (node.get("depends_on") or {}).get("nodes", [])],
            "columns_documented": list((node.get("columns") or {}).keys()),
            "columns": cols,
            "column_quality": quality,
            "star_target": star_target,
            **grain,
        }

    # pass 2: resolve star-upstream via the referenced model's columns
    resolved = 0
    for m in models.values():
        if m["column_quality"] == "star-upstream":
            up = models.get(m["star_target"])
            if up and up["columns"] and up["column_quality"] not in ("no-select", "star-loop"):
                extra = [c for c in up["columns"] if c not in m["columns"]]
                m["columns"] = m["columns"] + extra
                m["column_quality"] = "star-upstream-resolved"
                resolved += 1

    # last resort: yml-documented columns (partial but honest — flagged as such)
    for m in models.values():
        if not m["columns"] and m["columns_documented"]:
            m["columns"] = [c.lower() for c in m["columns_documented"]]
            m["column_quality"] = "documented-only-partial"
        elif not m["columns"]:
            m["column_quality"] = "columns-unknown"

    # sources (raw landing tables) from the manifest
    sources = []
    for _uid, s in manifest.get("sources", {}).items():
        sources.append(
            {
                "source_name": s.get("source_name", ""),
                "table": s.get("name", ""),
                "database": s.get("database", ""),
                "schema": s.get("schema", ""),
                "description": (s.get("description") or "")[:300],
            }
        )

    with (out_dir / "models.jsonl").open("w", encoding="utf-8") as f:
        for m in models.values():
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    with (out_dir / "raw_sources.jsonl").open("w", encoding="utf-8") as f:
        for s in sources:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # coverage accounting — failures stay visible
    from collections import Counter

    q = Counter(m["column_quality"] for m in models.values())
    layers = Counter(m["layer"] for m in models.values())
    grain_declared = sum(1 for m in models.values() if m["grain_declared"])
    report = {
        "models_total": len(models),
        "by_layer": dict(layers),
        "column_parse_quality": dict(q),
        "star_upstream_resolved_pass2": resolved,
        "grain_declared": grain_declared,
        "grain_missing": len(models) - grain_declared,
        "raw_source_tables": len(sources),
        "models_with_zero_columns": [m["name"] for m in models.values() if not m["columns"]][:50],
    }
    (out_dir / "extract_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2)[:3000])


if __name__ == "__main__":
    main()
