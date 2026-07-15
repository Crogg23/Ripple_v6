#!/usr/bin/env python3
"""Library Snapshot — read-only inventory of this repo + the connected Snowflake account.

Answers "what do I actually have?" in one command:

    python3 scripts/library_snapshot.py

Writes LIBRARY_SNAPSHOT.md at the repo root (overwrites; git history is the
version trail). Strictly read-only: metadata queries only (INFORMATION_SCHEMA,
SHOW), no COUNT(*) table scans, no DDL/DML, nothing written to Snowflake.
Credentials come from library-onboarding/.env via the repo's own snow.py —
no secret is ever printed or written to the report.

Every number in the report comes from a live query or file scan at run time.
Anything that can't be verified is written as "unknown — could not verify".
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ONBOARDING = REPO / "library-onboarding"
DBT_DIR = ONBOARDING / "ripple_dbt"
OUT_PATH = REPO / "LIBRARY_SNAPSHOT.md"
RERUN_CMD = "python3 scripts/library_snapshot.py"

STALE_BRANCH_DAYS = 30
STALE_TABLE_DAYS = 90
MAX_INLINE_ROWS = 15  # sections longer than this collapse into the appendix

# Databases that are Snowflake's own / per-user workspaces — excluded from the
# detailed breakdown but noted so they aren't silently dropped.
SYSTEM_DB_PREFIXES = ("SNOWFLAKE", "USER$")

# How non-dbt objects got there (fallthrough = "unclassified — inspect manually").
NON_DBT_CLASSIFICATION = [
    ("LIBRARY_RAW", "LANDING", "raw landing — loaded by Python (onboard.py loaders / scripts/*_load.py)"),
    ("LIBRARY_RAW", "RETIRED", "retired raw tables — parked by cleanup, not dbt"),
    ("LIBRARY_META", None, "meta/system — agent-written (registry, ingest logs, connect graph, build ledger)"),
    ("THE_LIBRARY", None, "serve-layer domain views — built by scripts/thelibrary_build.py (reads the catalog, not dbt)"),
    ("LIBRARY_MARTS", "_RESTORE_20260701", "restore artifact from 2026-07-01 backup recovery — not dbt-managed"),
]

TABLE_REF_RE = re.compile(
    r"\b(LIBRARY_RAW|LIBRARY_META|LIBRARY_STAGING|LIBRARY_MARTS|THE_LIBRARY)"
    r"(?:\.[A-Za-z0-9_$\"]+){1,2}"
)
WRITE_RE = re.compile(
    r"\b(INSERT\s+INTO|CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW|SCHEMA|STAGE|ROLE)|"
    r"MERGE\s+INTO|COPY\s+INTO|TRUNCATE|DELETE\s+FROM|DROP\s+(?:TABLE|VIEW|SCHEMA)|write_pandas|"
    # privilege mutations count as writes too; keyword pairs so prose ("grant the
    # read-only role") doesn't false-positive
    r"GRANT\s+(?:SELECT|USAGE|ALL|INSERT|OWNERSHIP|ROLE|CREATE|MONITOR)|"
    r"REVOKE\s+(?:SELECT|USAGE|ALL|INSERT|OWNERSHIP|ROLE|CREATE|MONITOR))",
    re.IGNORECASE,
)


# ---------------------------------------------------------------- helpers

def sh(args: list[str], cwd: Path = REPO) -> str:
    """Run a command, return stdout; empty string on failure (never raises)."""
    try:
        return subprocess.run(
            args, cwd=cwd, capture_output=True, text=True, timeout=60
        ).stdout.strip()
    except Exception:
        return ""


def sanitize_error(exc: Exception) -> str:
    """One plain-English line about a failure. Never leaks account/user/token
    fragments that Snowflake likes to embed in messages."""
    msg = str(exc).splitlines()[0] if str(exc) else ""
    msg = re.sub(r"[A-Z0-9]{6,}-[A-Z0-9]{6,}", "<account>", msg)  # account locators
    msg = re.sub(r"(user|token|password|pat)\s*[=:]\s*\S+", r"\1=<redacted>", msg, flags=re.I)
    low = (msg + type(exc).__name__).lower()
    if any(w in low for w in ("auth", "token", "password", "credential", "incorrect username")):
        return f"{type(exc).__name__}: looks like an authentication problem (the PAT in .env may have been rotated)"
    return f"{type(exc).__name__}: {msg[:160]}"


def fmt_n(n) -> str:
    if n is None:
        return "—"
    n = int(n)
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 10_000:
        return f"{n/1_000:.0f}k"
    return f"{n:,}"


def fmt_date(dt) -> str:
    if dt is None:
        return "—"
    if isinstance(dt, str):
        return dt[:10]
    return dt.strftime("%Y-%m-%d")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def capped_table(headers, rows, title_for_appendix, appendix):
    """Render at most MAX_INLINE_ROWS rows inline; push the full set to the appendix."""
    if len(rows) <= MAX_INLINE_ROWS:
        return md_table(headers, rows)
    appendix.append((title_for_appendix, md_table(headers, rows)))
    shown = md_table(headers, rows[:MAX_INLINE_ROWS])
    return f"{shown}\n\n*Top {MAX_INLINE_ROWS} of {len(rows)} — full list in Appendix: “{title_for_appendix}”.*"


# ---------------------------------------------------------------- git audit

def git_audit() -> dict:
    now = datetime.now(timezone.utc)
    branch = sh(["git", "branch", "--show-current"])
    # the report itself is always dirty right after a run — not a real signal
    dirty = [l for l in sh(["git", "status", "--porcelain"]).splitlines()
             if l.strip() and not l.endswith("LIBRARY_SNAPSHOT.md")]

    def refs(pattern):
        raw = sh(["git", "for-each-ref", "--sort=-committerdate", pattern,
                  "--format=%(refname:short)\t%(committerdate:iso8601)\t%(subject)"])
        out = []
        for line in raw.splitlines():
            parts = line.split("\t")
            if len(parts) < 2 or parts[0].endswith("/HEAD") or parts[0] == "origin":
                continue
            try:
                when = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S %z")
                age = (now - when).days
            except Exception:
                age = None
            out.append({"name": parts[0], "date": parts[1][:10], "age_days": age,
                        "subject": parts[2] if len(parts) > 2 else ""})
        return out

    local = refs("refs/heads")
    remote = refs("refs/remotes")
    # a remote branch is only "extra" if no local branch shadows it
    local_names = {b["name"] for b in local}
    remote = [b for b in remote if b["name"].removeprefix("origin/") not in local_names]
    stale = [b for b in local + remote
             if b["age_days"] is not None and b["age_days"] > STALE_BRANCH_DAYS]
    return {"branch": branch, "dirty": dirty, "local": local, "remote": remote, "stale": stale}


# ---------------------------------------------------------------- dbt audit

def find_dbt_projects() -> dict:
    """All dbt_project.yml files — in this repo and in sibling GitHub dirs."""
    def scan(root: Path) -> list[str]:
        hits = []
        for p in root.rglob("dbt_project.yml"):
            s = str(p)
            if any(x in s for x in ("dbt_packages", "/.venv/", "/venv/", "node_modules", "/backups/")):
                continue
            hits.append(s)
        return hits

    in_repo = scan(REPO)
    siblings = {}
    for sib in sorted(REPO.parent.iterdir()):
        if not sib.is_dir() or sib == REPO or sib.name.startswith("."):
            continue
        found = scan(sib)
        if found:
            siblings[sib.name] = found
    return {"in_repo": in_repo, "siblings": siblings}


def dbt_audit() -> dict:
    result = {"project": str(DBT_DIR / "dbt_project.yml"), "source": None, "layers": {},
              "manifest_mtime": None, "manifest_stale_note": None, "relations": [],
              "seeds": 0, "tests": 0, "sources": 0, "file_scan_total": 0, "notes": []}

    # --- file scan (always: cross-check + fallback) ---------------------
    models_dir = DBT_DIR / "models"
    folder_defaults = _project_folder_materializations()
    scan = defaultdict(lambda: defaultdict(int))
    scanned_models = set()
    for sql in sorted(models_dir.rglob("*.sql")):
        rel = sql.relative_to(models_dir)
        layer = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        text = sql.read_text(errors="replace")
        m = re.search(r"materialized\s*=\s*['\"](\w+)['\"]", text)
        mat = m.group(1) if m else folder_defaults.get(layer, "view")
        scan[layer][mat] += 1
        scanned_models.add(sql.stem.lower())
        result["file_scan_total"] += 1

    # --- manifest (ground truth for lineage when fresh) ------------------
    manifest_path = DBT_DIR / "target" / "manifest.json"
    manifest_ok = False
    if manifest_path.exists():
        result["manifest_mtime"] = datetime.fromtimestamp(manifest_path.stat().st_mtime)
        newer = sorted(p for p in models_dir.rglob("*.sql")
                       if p.stat().st_mtime > manifest_path.stat().st_mtime)
        if newer:
            names = ", ".join(f"`{p.relative_to(models_dir)}`" for p in newer[:3])
            result["manifest_stale_note"] = (
                f"{len(newer)} model file(s) modified after manifest.json was compiled "
                f"({names}{'…' if len(newer) > 3 else ''}) — manifest counts may lag the files")
        try:
            manifest = json.loads(manifest_path.read_text())
            nodes = manifest.get("nodes", {})
            layers = defaultdict(lambda: defaultdict(int))
            relations, manifest_models = [], set()
            for node in nodes.values():
                rt = node.get("resource_type")
                if rt == "test":
                    result["tests"] += 1
                    continue
                if rt == "seed":
                    result["seeds"] += 1
                if rt not in ("model", "seed"):
                    continue
                mat = (node.get("config") or {}).get("materialized", "view")
                if rt == "model":
                    parts = node.get("path", "").replace("\\", "/").split("/")
                    layer = parts[0] if len(parts) > 1 else "(root)"
                    layers[layer][mat] += 1
                    manifest_models.add((node.get("name") or "").lower())
                relations.append({
                    "database": (node.get("database") or "").upper(),
                    "schema": (node.get("schema") or "").upper(),
                    "name": (node.get("alias") or node.get("name") or "").upper(),
                    "materialized": mat, "resource_type": rt,
                })
            result["sources"] = len(manifest.get("sources", {}))
            result["layers"] = {k: dict(v) for k, v in layers.items()}
            result["relations"] = relations
            manifest_ok = True
            result["source"] = "manifest.json (compiled dbt state)"
            disabled_names = set()
            for node_list in (manifest.get("disabled") or {}).values():
                for node in node_list:
                    if isinstance(node, dict) and node.get("name"):
                        disabled_names.add(node["name"].lower())
            only_files = scanned_models - manifest_models
            only_manifest = manifest_models - scanned_models
            known_disabled = only_files & disabled_names
            truly_new = only_files - disabled_names
            if known_disabled:
                result["notes"].append(
                    f"{len(known_disabled)} model file(s) on disk are deliberately disabled "
                    f"(enabled=false — excluded from builds): {', '.join(sorted(known_disabled)[:8])}"
                    + ("…" if len(known_disabled) > 8 else ""))
            if truly_new:
                result["notes"].append(
                    f"{len(truly_new)} model file(s) on disk are NOT in the manifest "
                    f"(new since last compile): {', '.join(sorted(truly_new)[:8])}"
                    + ("…" if len(truly_new) > 8 else ""))
            if only_manifest:
                result["notes"].append(
                    f"{len(only_manifest)} manifest model(s) have no .sql file on disk "
                    f"(deleted since last compile): {', '.join(sorted(only_manifest)[:8])}"
                    + ("…" if len(only_manifest) > 8 else ""))
        except Exception as exc:
            result["notes"].append(f"manifest.json parse failed ({type(exc).__name__}) — "
                                   "fell back to scanning models/ directly")
    else:
        result["notes"].append("no target/manifest.json — counts come from scanning models/ directly")

    if not manifest_ok:
        result["layers"] = {k: dict(v) for k, v in scan.items()}
        result["source"] = "file scan of models/ (manifest unavailable/unparseable)"
    return result


def _project_folder_materializations() -> dict:
    """Folder-level +materialized defaults out of dbt_project.yml (regex parse —
    good enough for one level of nesting, and only used when a model has no
    inline config)."""
    out = {}
    try:
        text = (DBT_DIR / "dbt_project.yml").read_text()
        block = text[text.index("models:"):]
        current = None
        for line in block.splitlines()[1:]:
            if line and not line[0].isspace():
                break  # left the models: block
            m_dir = re.match(r"\s{4,6}(\w+):\s*$", line)
            m_mat = re.match(r"\s+\+?materialized:\s*(\w+)", line)
            if m_dir:
                current = m_dir.group(1)
            elif m_mat and current:
                out[current] = m_mat.group(1)
    except Exception:
        pass
    return out


# ---------------------------------------------------------------- scripts audit

def scripts_audit() -> dict:
    """Standalone Python outside the dbt project: per-file for entry points,
    per-directory rollups for packages."""
    entries = []

    def describe(py: Path) -> dict:
        text = py.read_text(errors="replace")
        doc = re.match(r'\s*(?:#!.*\n)?(?:#.*\n|\s)*(?:"""|\'\'\')(.*?)(?:\n|"""|\'\'\')', text)
        purpose = (doc.group(1).strip() if doc and doc.group(1).strip() else "")
        confidence = "confirmed (docstring)" if purpose else "likely (inferred from code)"
        if not purpose:
            if "argparse" in text:
                purpose = "CLI utility (no docstring)"
            elif "def main" in text or '__main__' in text:
                purpose = "runnable script (no docstring)"
            else:
                purpose = "module (no docstring)"
        refs = sorted({m.group(0).replace('"', "").rstrip(".").upper()
                       for m in TABLE_REF_RE.finditer(text)})
        dbs = sorted({r.split(".")[0] for r in refs})
        return {"path": str(py.relative_to(REPO)), "purpose": purpose[:140],
                "confidence": confidence, "touches": dbs,
                "writes": bool(WRITE_RE.search(text)) and bool(refs)}

    for py in sorted((REPO / "scripts").glob("*.py")):
        entries.append(describe(py))
    for py in sorted(ONBOARDING.glob("*.py")):
        entries.append(describe(py))
    if (REPO / "ripple.py").exists():
        entries.append(describe(REPO / "ripple.py"))

    dir_rollups = []
    for d in ["ripple", "connect", "viz", "loadkit", "serve", "politics",
              "portal_recon", "reading_room", "infra", "tests"]:
        p = REPO / d
        if not p.is_dir():
            continue
        pys = [f for f in p.rglob("*.py")
               if ".venv" not in str(f) and "node_modules" not in str(f)]
        touched = sorted({m.group(1) for f in pys
                          for m in TABLE_REF_RE.finditer(f.read_text(errors="replace"))})
        dir_rollups.append({"dir": d + "/", "py_files": len(pys),
                            "touches": touched})
    return {"entries": entries, "dirs": dir_rollups}


# ---------------------------------------------------------------- warehouse audit

def warehouse_audit() -> dict:
    sys.path.insert(0, str(ONBOARDING))
    try:
        from dotenv import load_dotenv
        load_dotenv(ONBOARDING / ".env", override=True)
    except Exception:
        pass
    try:
        from snow import connect  # repo's own helper; PAT auth from .env
        conn = connect()
    except Exception as exc:
        return {"error": sanitize_error(exc)}

    out = {"error": None, "session": {}, "databases": {}, "system_dbs": [],
           "schemas": [], "tables": [], "empty_schemas": [], "known_hidden": [],
           "account_usage_accessible": None}
    try:
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_USER()")
        role, wh, user = cur.fetchone()
        out["session"] = {"role": role, "warehouse": wh, "user": user}

        cur.execute("SHOW DATABASES")
        names = [r[1] for r in cur.fetchall()]
        detail_dbs = []
        for n in names:
            if n.upper().startswith(SYSTEM_DB_PREFIXES):
                out["system_dbs"].append(n)
            else:
                detail_dbs.append(n)

        # measured, not assumed: is ACCOUNT_USAGE actually reachable for this role?
        try:
            cur.execute("SELECT 1 FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES LIMIT 1")
            cur.fetchall()
            out["account_usage_accessible"] = True
        except Exception:
            out["account_usage_accessible"] = False

        # DBs documented in CLAUDE.md that this role can't see (visibility limit,
        # not nonexistence)
        upper_names = {n.upper() for n in names}
        out["known_hidden"] = [d for d in ("LIBRARY_TOOLS",) if d not in upper_names]

        all_schemas = set()
        for db in detail_dbs:
            try:
                cur.execute(f'''SELECT schema_name FROM "{db}".INFORMATION_SCHEMA.SCHEMATA
                                WHERE schema_name <> 'INFORMATION_SCHEMA' ''')
                all_schemas |= {(db, r[0]) for r in cur.fetchall()}
            except Exception:
                pass

        for db in detail_dbs:
            try:
                cur.execute(f'''
                    SELECT table_schema, table_name, table_type,
                           row_count, bytes, last_altered
                    FROM "{db}".INFORMATION_SCHEMA.TABLES
                    WHERE table_schema <> 'INFORMATION_SCHEMA'
                    ORDER BY table_schema, table_name''')
                rows = cur.fetchall()
            except Exception as exc:
                out["databases"][db] = {"error": sanitize_error(exc)}
                continue
            out["databases"][db] = {"error": None, "objects": len(rows)}
            for schema, name, ttype, rc, byt, alt in rows:
                out["tables"].append({
                    "database": db, "schema": schema, "name": name,
                    "is_view": ttype == "VIEW",
                    "row_count": rc, "bytes": byt, "last_altered": alt,
                })
        agg = defaultdict(lambda: {"tables": 0, "views": 0, "rows": 0, "last": None})
        for t in out["tables"]:
            k = (t["database"], t["schema"])
            a = agg[k]
            a["views" if t["is_view"] else "tables"] += 1
            a["rows"] += t["row_count"] or 0
            if t["last_altered"] and (a["last"] is None or t["last_altered"] > a["last"]):
                a["last"] = t["last_altered"]
        out["schemas"] = [{"database": d, "schema": s, **v} for (d, s), v in sorted(agg.items())]
        out["empty_schemas"] = sorted(all_schemas - set(agg.keys()))
    except Exception as exc:
        # e.g. warehouse suspended or network drop mid-run: degrade to
        # "could not verify" instead of a traceback
        out["error"] = sanitize_error(exc)
    finally:
        try:
            conn.close()  # session ends; SERVE_WH auto-suspends on its own policy
        except Exception:
            pass
    return out


# ---------------------------------------------------------------- cross-reference

def cross_reference(wh: dict, dbt: dict) -> dict:
    rel_index = {(r["database"], r["schema"], r["name"]): r for r in dbt.get("relations", [])}
    dbt_built, non_dbt, orphans = [], [], []
    dbt_dbs = {r["database"] for r in dbt.get("relations", [])}

    for t in wh.get("tables", []):
        key = (t["database"].upper(), t["schema"].upper(), t["name"].upper())
        if key in rel_index:
            dbt_built.append({**t, "materialized": rel_index[key]["materialized"],
                              "resource_type": rel_index[key]["resource_type"]})
        else:
            label = None
            for db, schema, desc in NON_DBT_CLASSIFICATION:
                if t["database"].upper() == db and (schema is None or t["schema"].upper() == schema):
                    label = desc
                    break
            if label is None and t["database"].upper() in dbt_dbs:
                orphans.append(t)  # lives in a dbt target DB but dbt doesn't know it
                label = "orphan in a dbt database (not in manifest — old run, restore, or manual)"
            non_dbt.append({**t, "classification": label or "unclassified — inspect manually"})

    missing = [r for (k, r) in rel_index.items()
               if r["resource_type"] in ("model", "seed")
               and k not in {(t["database"].upper(), t["schema"].upper(), t["name"].upper())
                             for t in wh.get("tables", [])}]
    return {"dbt_built": dbt_built, "non_dbt": non_dbt, "orphans": orphans, "missing": missing}


# ---------------------------------------------------------------- flags

def build_flags(git: dict, projects: dict, dbt: dict, wh: dict, xref: dict) -> list[str]:
    flags = []
    if len(projects["in_repo"]) > 1:
        flags.append(f"**Multiple dbt projects in this repo** ({len(projects['in_repo'])}): "
                     + "; ".join(projects["in_repo"]))
    for sib, paths in projects["siblings"].items():
        flags.append(f"**Sibling repo `{sib}` also contains a dbt project** "
                     f"({len(paths)} dbt_project.yml) — stale duplicate? Not audited here.")
    if git["dirty"]:
        names = ", ".join(f"`{d.split(None, 1)[1]}`" for d in git["dirty"][:5])
        flags.append(f"**{_dirty_bit(git, plain=True)}** in the working tree: {names}"
                     + ("…" if len(git["dirty"]) > 5 else "")
                     + " (LIBRARY_SNAPSHOT.md itself is not counted).")
    for b in git["stale"]:
        flags.append(f"Stale branch `{b['name']}` — last commit {b['date']} ({b['age_days']}d ago).")
    if dbt.get("manifest_stale_note"):
        flags.append("dbt manifest is stale: " + dbt["manifest_stale_note"] + ".")
    for note in dbt.get("notes", []):
        flags.append("dbt: " + note)

    if not wh.get("error"):
        zero = [t for t in wh["tables"] if not t["is_view"] and (t["row_count"] or 0) == 0]
        if zero:
            worst = ", ".join(f"`{t['database']}.{t['schema']}.{t['name']}`" for t in zero[:6])
            flags.append(f"**{len(zero)} zero-row table(s)** — loaded but empty. "
                         f"First few: {worst}{'…' if len(zero) > 6 else ''} (full list in appendix).")
        cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_TABLE_DAYS)
        stale_dbt = [t for t in xref["dbt_built"] if not t["is_view"] and t["last_altered"]
                     and t["last_altered"].astimezone(timezone.utc) < cutoff]
        if stale_dbt:
            flags.append(f"{len(stale_dbt)} dbt-built table(s) not altered in {STALE_TABLE_DAYS}+ days.")
        if xref["orphans"]:
            worst = ", ".join(f"`{t['database']}.{t['schema']}.{t['name']}`" for t in xref["orphans"][:6])
            flags.append(f"**{len(xref['orphans'])} orphan object(s) in dbt databases** that the "
                         f"current manifest doesn't know about: {worst}"
                         f"{'…' if len(xref['orphans']) > 6 else ''} (full list in appendix).")
        if xref["missing"]:
            flags.append(f"{len(xref['missing'])} dbt model(s)/seed(s) declared but not found in the "
                         f"warehouse (never built, or dropped): "
                         + ", ".join(f"`{m['database']}.{m['schema']}.{m['name']}`"
                                     for m in xref["missing"][:6])
                         + ("…" if len(xref["missing"]) > 6 else ""))
    else:
        flags.append("Warehouse checks skipped — connection failed (see Warehouse section).")

    log_path = ONBOARDING / "onboarding_log.json"
    if log_path.exists():
        try:
            log = json.loads(log_path.read_text())
            statuses = defaultdict(int)
            items = log.values() if isinstance(log, dict) else log
            for entry in items:
                if isinstance(entry, dict):
                    statuses[entry.get("status", "?")] += 1
            if statuses:
                flags.append("Onboarding log statuses: "
                             + ", ".join(f"{k}={v}" for k, v in sorted(statuses.items())))
        except Exception:
            flags.append("onboarding_log.json exists but could not be parsed — unknown statuses.")
    return flags


# ---------------------------------------------------------------- render

def _dirty_bit(git: dict, plain: bool = False) -> str:
    if not git["dirty"]:
        return "clean" if plain else "no uncommitted changes"
    n = len(git["dirty"])
    word = "change" if n == 1 else "changes"
    return f"{n} uncommitted {word}" if plain else f"**{n} uncommitted {word}**"


def render(git, projects, dbt, scripts, wh, xref, flags) -> str:
    now = datetime.now().astimezone()
    appendix: list[tuple[str, str]] = []
    L = []
    add = L.append

    add(f"# Library Snapshot\n")
    add(f"Generated at {now.strftime('%Y-%m-%d %H:%M %Z')} · rerun with `{RERUN_CMD}`\n")

    # ---- 1. plain-english summary
    add("## The 2-minute version\n")
    if wh.get("error"):
        add(f"**Warehouse: unknown — could not verify (connection failed: {wh['error']}).** "
            "Repo-side numbers below are still real.\n")
        n_db = n_tab = n_view = total_rows = 0
        last = None
    else:
        n_db = len(wh["databases"])
        n_tab = sum(1 for t in wh["tables"] if not t["is_view"])
        n_view = sum(1 for t in wh["tables"] if t["is_view"])
        total_rows = sum(t["row_count"] or 0 for t in wh["tables"] if not t["is_view"])
        last = max((t["last_altered"] for t in wh["tables"] if t["last_altered"]), default=None)
        n_empty = len(wh.get("empty_schemas") or [])
        n_schemas = len({(t['database'], t['schema']) for t in wh['tables']}) + n_empty
        empty_bit = f" ({n_empty} of them empty)" if n_empty else ""
        add(f"You have **{n_db} databases**, **{n_schemas} schemas**{empty_bit}, "
            f"**{n_tab:,} tables** and **{n_view:,} views** in Snowflake, holding about "
            f"**{fmt_n(total_rows)} rows** in total. The most recent change to any of them "
            f"was **{fmt_date(last)}**.\n")
    total_models = sum(sum(m.values()) for m in dbt["layers"].values())
    add(f"On the code side: **{total_models} dbt models** ({dbt['source']}), "
        f"**{len(scripts['entries'])} standalone Python scripts/entry points**, plus "
        f"{sum(d['py_files'] for d in scripts['dirs'])} more .py files inside "
        f"{len(scripts['dirs'])} packages. "
        f"Git is on `{git['branch']}` with {_dirty_bit(git)}.\n")
    if not wh.get("error"):
        built = len(xref["dbt_built"])
        add(f"Of everything in the warehouse, **{built:,} objects are dbt-built** and "
            f"**{len(xref['non_dbt']):,} are not** (raw landing tables, agent-written meta, serve views). "
            f"**{len(flags)} flag(s)** need eyes — see the last section.\n")

    # ---- 2. warehouse
    add("## Warehouse (Snowflake)\n")
    if wh.get("error"):
        add(f"unknown — could not verify ({wh['error']})\n")
    else:
        s = wh["session"]
        if wh.get("account_usage_accessible"):
            au_bit = "ACCOUNT_USAGE is accessible but unused — INFORMATION_SCHEMA has no lag"
        else:
            au_bit = "ACCOUNT_USAGE was not accessible to this role"
        hidden_bit = ""
        if wh.get("known_hidden"):
            hid = ", ".join(f"`{d}`" for d in wh["known_hidden"])
            hidden_bit = (f"Objects not granted to `{s['role']}` are invisible to this audit — "
                          f"per CLAUDE.md, {hid} exists (MCP host, no data) but isn't visible here. ")
        add(f"Audited as role `{s['role']}` on warehouse `{s['warehouse']}` (user `{s['user']}`). "
            f"Row counts are metadata-based (INFORMATION_SCHEMA — real-time, no COUNT(*) scans; "
            f"{au_bit}). "
            f"{hidden_bit}"
            f"System databases excluded from the breakdown but present: "
            f"{', '.join('`'+d+'`' for d in wh['system_dbs'])}.\n")
        if wh.get("empty_schemas"):
            add("Empty schemas (exist but hold no tables/views): "
                + ", ".join(f"`{d}.{sc}`" for d, sc in wh["empty_schemas"]) + ".\n")
        rows = [[f"`{r['database']}`", f"`{r['schema']}`", r["tables"], r["views"],
                 fmt_n(r["rows"]), fmt_date(r["last"])]
                for r in sorted(wh["schemas"], key=lambda r: -r["rows"])]
        add(capped_table(["Database", "Schema", "Tables", "Views", "Rows (metadata)", "Last altered"],
                         rows, "All schemas", appendix))
        add("\n*Views store no rows — the Rows column counts base tables only.*\n")

    # ---- 3. codebase
    add("## Codebase\n")
    add(f"dbt project: `{Path(dbt['project']).relative_to(REPO)}` — counts from {dbt['source']}"
        + (f" (compiled {dbt['manifest_mtime']:%Y-%m-%d %H:%M})" if dbt.get("manifest_mtime") else "")
        + ".\n")
    mat_names = sorted({m for layer in dbt["layers"].values() for m in layer})
    rows = [[f"`{layer}/`"] + [layer_mats.get(m, 0) for m in mat_names] + [sum(layer_mats.values())]
            for layer, layer_mats in sorted(dbt["layers"].items(), key=lambda kv: -sum(kv[1].values()))]
    add(md_table(["Layer"] + mat_names + ["total"], rows))
    add(f"\nPlus {dbt['seeds']} seeds, {dbt['tests']} tests, {dbt['sources']} declared sources.\n")

    add("### Standalone scripts (outside dbt)\n")
    rows = [[f"`{e['path']}`", e["purpose"],
             ("writes " if e["writes"] else "reads ") + ", ".join(e["touches"]) if e["touches"] else "—",
             e["confidence"]]
            for e in scripts["entries"]]
    add(capped_table(["Script", "What it does", "Warehouse touch", "Confidence"],
                     rows, "All standalone scripts", appendix))
    add("\n### Packages (rolled up)\n")
    add(md_table(["Directory", ".py files", "References"],
                 [[f"`{d['dir']}`", d["py_files"], ", ".join(d["touches"]) or "—"]
                  for d in scripts["dirs"]]))
    add("\n### Git\n")
    add(f"Current branch `{git['branch']}`, {_dirty_bit(git, plain=True)}.")
    rows = [[f"`{b['name']}`", b["date"], f"{b['age_days']}d", b["subject"][:60]]
            for b in git["local"] + git["remote"]]
    add(capped_table(["Branch", "Last commit", "Age", "Subject"], rows, "All branches", appendix))
    add("")

    # ---- 4. dbt-built vs raw
    add("## dbt-built vs. everything else\n")
    if wh.get("error"):
        add("unknown — could not verify (warehouse connection failed)\n")
    else:
        by_class = defaultdict(lambda: {"n": 0, "rows": 0})
        for t in xref["dbt_built"]:
            k = f"dbt {t['materialized']}"
            by_class[k]["n"] += 1
            by_class[k]["rows"] += t["row_count"] or 0
        for t in xref["non_dbt"]:
            by_class[t["classification"]]["n"] += 1
            by_class[t["classification"]]["rows"] += t["row_count"] or 0
        rows = [[k, v["n"], fmt_n(v["rows"])]
                for k, v in sorted(by_class.items(), key=lambda kv: -kv[1]["n"])]
        add(md_table(["How it got there", "Objects", "Rows (metadata)"], rows))
        add("")

    # ---- 5. flags
    add("## Flags — broken, duplicated, or stale\n")
    if flags:
        add("\n".join(f"- {f}" for f in flags))
    else:
        add("Nothing flagged.")
    add("")

    # ---- appendix extras: zero-row + orphans full lists
    if not wh.get("error"):
        zero = [t for t in wh["tables"] if not t["is_view"] and (t["row_count"] or 0) == 0]
        if zero:
            appendix.append(("Zero-row tables",
                             md_table(["Table", "Last altered"],
                                      [[f"`{t['database']}.{t['schema']}.{t['name']}`",
                                        fmt_date(t["last_altered"])] for t in zero])))
        if xref["orphans"]:
            appendix.append(("Orphans in dbt databases",
                             md_table(["Object", "Type", "Rows", "Last altered"],
                                      [[f"`{t['database']}.{t['schema']}.{t['name']}`",
                                        "view" if t["is_view"] else "table",
                                        fmt_n(t["row_count"]), fmt_date(t["last_altered"])]
                                       for t in xref["orphans"]])))

    if appendix:
        add("---\n\n## Appendix\n")
        for title, table in appendix:
            add(f"<details>\n<summary><b>{title}</b></summary>\n\n{table}\n\n</details>\n")

    add("---")
    add(f"Rerun this audit any time: `{RERUN_CMD}`")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- main

def main() -> int:
    print("library snapshot: auditing repo …", flush=True)
    git = git_audit()
    projects = find_dbt_projects()
    dbt = dbt_audit()
    scripts = scripts_audit()
    print("library snapshot: auditing warehouse (metadata only) …", flush=True)
    wh = warehouse_audit()
    xref = cross_reference(wh, dbt) if not wh.get("error") else {"dbt_built": [], "non_dbt": [],
                                                                 "orphans": [], "missing": []}
    flags = build_flags(git, projects, dbt, wh, xref)
    OUT_PATH.write_text(render(git, projects, dbt, scripts, wh, xref, flags))

    if wh.get("error"):
        wh_bit = "warehouse: could not verify (connection failed)"
    else:
        n_tab = sum(1 for t in wh["tables"] if not t["is_view"])
        n_view = sum(1 for t in wh["tables"] if t["is_view"])
        wh_bit = (f"{len(wh['databases'])} DBs / {n_tab:,} tables / {n_view:,} views; "
                  f"{len(xref['dbt_built'])} dbt-built")
    total_models = sum(sum(m.values()) for m in dbt["layers"].values())
    print(f"audit complete — {wh_bit}; {total_models} dbt models; "
          f"{len(flags)} flag(s). Report: {OUT_PATH.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
