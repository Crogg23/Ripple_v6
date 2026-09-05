"""Refresh the Join Handbook's inputs from the live warehouse, then rebuild.

The handbook builder (build_chain_handbook.py) merges STATIC files in ./chain/
with repo_payload.json. Nothing in that chain reads the warehouse, so every row
count, every table listing and every edge is frozen at whatever the last export
saw. On 2026-09-05 that meant the page claimed FED_CFPB_HMDA_HISTORIC held
19,136,434 rows when the live table held 44,992,667, and listed six tables that
no longer exist.

This script closes that gap. It reads the live warehouse and rewrites, in place:

  chain/base_context.js   row counts per table
  chain/base_schema.js    row counts per table
  chain/base_tables.js    drops tables that no longer exist, adds missing edges
  chain/repo_payload.json drops the same tables, refreshes notes.traps

Then run build_chain_handbook.py to produce reports/viz/join_handbook.html.

    python reports/viz/_build/refresh_handbook_from_warehouse.py
    python reports/viz/_build/build_chain_handbook.py

Deliberate exclusions, so a future reader does not "fix" them:

  ZIP and NAME@ZIP edges are LEFT OUT. CONNECT_EDGES carries 2,513 of them.
  They top the raw reach list and identify nobody -- two different people in one
  postcode match. Including them would triple the edge count and every new edge
  would be noise. See .claude/traps.md.

  PORTAL_ tables are LEFT OUT. 1,563 of them exist and they are not in the join
  graph. Adding them means wiring them into CONNECT first, which is a separate
  job. Their absence is recorded in META.excluded so the page can say so.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

BUILD = Path(__file__).resolve().parent
CHAIN = BUILD / "chain"
REPO = BUILD.parent.parent.parent          # c:/Code/Ripple_v6
TRAPS = REPO / ".claude" / "traps.md"

sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

# Keys that are location, not identity. An edge on one of these is not a join.
NON_IDENTITY_KEYS = {"ZIP", "NAME@ZIP"}


def load_global(path: Path):
    txt = path.read_text(encoding="utf-8")
    txt = txt[txt.index("=") + 1:].strip()
    obj, _ = json.JSONDecoder().raw_decode(txt)
    return obj


def write_global(path: Path, name: str, obj) -> None:
    s = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    path.write_text(f"window.{name} = {s};\n", encoding="utf-8")


def live_tables(conn) -> dict[str, str]:
    """Every table in the warehouse, bare name -> fully qualified name.

    A bare name can exist in more than one database. RAW wins, because that is
    where the handbook's own ids come from, and MARTS models carry a schema
    prefix that would not collide anyway.
    """
    out: dict[str, str] = {}
    for dbn in ("LIBRARY_MARTS", "LIBRARY_META", "THE_LIBRARY", "LIBRARY_RAW"):
        q = (f"select TABLE_SCHEMA, TABLE_NAME, ROW_COUNT "
             f"from {dbn}.INFORMATION_SCHEMA.TABLES")
        for s, t, n in db.rows(conn, q):
            fq = f"{dbn}.{s}.{t}"
            # A mart table name appears twice: once as the real table and once
            # as a TIMELINE view over it. The view reports no row count. Last
            # write wins in a dict, so without this the view can shadow the
            # table and the name looks uncountable.
            if t in out and n is None:
                continue
            out[t] = fq
            # dbt names a model SCHEMA__TABLE. Index the suffix too, so a
            # handbook id like FED_EPA_RCRA_RCRA_FACILITIES still finds
            # ENVIRONMENT__FED_EPA_RCRA_RCRA_FACILITIES.
            if "__" in t:
                suf = t.split("__", 1)[1]
                if suf not in out or n is not None:
                    out.setdefault(suf, fq)
                    if n is not None:
                        out[suf] = fq
    return out


def live_counts(conn) -> dict[str, int]:
    """Row count per fully qualified name, straight from INFORMATION_SCHEMA.

    ROW_COUNT was checked against count(*) on 32 freshly rewritten tables on
    2026-09-05: zero mismatches. It is safe here and vastly cheaper.

    VIEWS report ROW_COUNT null. That is why this map is never used on its own
    to decide whether a table exists -- a marts view over a live landing table
    would look dead and get silently deleted from the page. Ask exists() first.
    """
    out: dict[str, int] = {}
    for dbn in ("LIBRARY_MARTS", "LIBRARY_META", "THE_LIBRARY", "LIBRARY_RAW"):
        q = (f"select TABLE_SCHEMA, TABLE_NAME, ROW_COUNT "
             f"from {dbn}.INFORMATION_SCHEMA.TABLES where ROW_COUNT is not null")
        for s, t, n in db.rows(conn, q):
            out[f"{dbn}.{s}.{t}"] = int(n)
    return out


def resolve(tid: str, fqn: str | None, names: dict[str, str],
            counts: dict[str, int]) -> tuple[str | None, int | None]:
    """Where this entry lives now, and how many rows it has.

    Three candidate homes, in order: the fqn the page already carries, the bare
    id, and the fqn read as a bare name. The first that EXISTS wins for identity.
    The first that also carries a row count wins for the count -- so a marts view
    with a null count still resolves, and borrows the landing table's number.
    """
    cands = []
    if fqn and fqn.count(".") == 2:
        cands.append(fqn)
        # Schemas get renamed. MONEY became MONEY_FINANCE and REF became
        # REFERENCE, which stranded five entries pointing at a database path
        # that no longer exists while the table itself sat there under a new
        # schema. Match on the mart table name, which did not change.
        leaf = fqn.rsplit(".", 1)[-1]
        if names.get(leaf):
            cands.append(names[leaf])
    if names.get(tid):
        cands.append(names[tid])
    if fqn and names.get(fqn):
        cands.append(names[fqn])
    home = next((c for c in cands if c in names.values() or c in counts), None)
    rows = next((counts[c] for c in cands if c in counts), None)
    return home, rows


def read_traps() -> list[str]:
    """One line per dated trap in .claude/traps.md, newest first.

    The handbook carried 9 traps while the file held 62. The file is the record
    Chris keeps; the page should not quietly hold an older subset of it.
    """
    if not TRAPS.exists():
        return []
    out = []
    for line in TRAPS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if re.match(r"^20\d\d-\d\d-\d\d\s+[-—]", line):
            out.append(line)
    return list(reversed(out))


def main() -> int:
    conn = db.connect()
    names = live_tables(conn)
    counts = live_counts(conn)

    tables = load_global(CHAIN / "base_tables.js")
    context = load_global(CHAIN / "base_context.js")
    schema = load_global(CHAIN / "base_schema.js")
    payload = json.loads((CHAIN / "repo_payload.json").read_text(encoding="utf-8"))

    # ---- 1. which listed tables still exist -------------------------------
    dead: list[str] = []
    fqn_of: dict[str, str] = {}
    rows_of: dict[str, int] = {}
    for t in tables:
        tid = t["id"]
        home, rows = resolve(tid, (schema.get(tid) or {}).get("fqn"), names, counts)
        if home is None:
            dead.append(tid)          # resolves nowhere in any database: really gone
            continue
        fqn_of[tid] = home
        if rows is not None:
            rows_of[tid] = rows       # no count is not the same as no table
    print(f"listed {len(tables)}  resolved {len(fqn_of)}  "
          f"counted {len(rows_of)}  gone {len(dead)}")
    for d in dead:
        print(f"   DROP {d}")

    tables = [t for t in tables if t["id"] not in dead]
    keep = {t["id"] for t in tables}
    for t in tables:
        t["conns"] = [c for c in t["conns"] if c["id"] in keep]
    for m in (context, schema):
        for d in dead:
            m.pop(d, None)
    payload["tables"] = [p for p in payload["tables"] if p["name"] not in dead]
    payload["edges"] = {k: [e for e in v if e.get("other") not in dead]
                        for k, v in payload["edges"].items() if k not in dead}

    # ---- 2. row counts, live ----------------------------------------------
    drift = []
    for tid, n in rows_of.items():
        f = fqn_of[tid]
        for m in (context, schema):
            if tid in m:
                was = m[tid].get("rows")
                if was != n:
                    if m is context:
                        drift.append((tid, was, n))
                    m[tid]["rows"] = n
        if tid in schema:
            schema[tid]["fqn"] = f
    # Four base entries had a schema record and no context record, so the page
    # could show their columns and not their size. Give every schema key a
    # context row rather than leaving a hole the reader cannot see.
    for tid, sv in schema.items():
        if tid not in context:
            context[tid] = {"rows": sv.get("rows") or 0, "dom": sv.get("dom", ""),
                            "one": "", "life": sv.get("life", "modeled")}

    drift.sort(key=lambda x: -abs((x[2] or 0) - (x[1] or 0)))
    print(f"\nrow counts refreshed, {len(drift)} tables drifted")
    for tid, was, now in drift[:12]:
        print(f"   {tid[:44]:<46} {was:>13,} -> {now:>13,}")

    # ---- 3. edges the graph has and the page does not ---------------------
    by_id = {t["id"]: t for t in tables}
    have = set()
    for t in tables:
        for c in t["conns"]:
            have.add((t["id"], c["id"], c.get("jk")))
    added = 0
    q = ('select A,B,KEY,TIER,A_COL,B_COL,MATCHED,MATCH_RATE '
         'from LIBRARY_META."CONNECT".CONNECT_EDGES')
    for a, b, key, tier, acol, bcol, matched, rate in db.rows(conn, q):
        if key in NON_IDENTITY_KEYS or a not in by_id or b not in by_id:
            continue
        for lhs, rhs, lc, rc in ((a, b, acol, bcol), (b, a, bcol, acol)):
            if (lhs, rhs, key) in have:
                continue
            by_id[lhs]["conns"].append({
                "id": rhs, "lbl": by_id[rhs]["label"], "tier": "solid",
                "pct": float(rate) if rate is not None else None,
                "n": int(matched) if matched is not None else None,
                "lc": lc, "rc": rc, "jk": key, "src": "connect_edges",
            })
            have.add((lhs, rhs, key))
            added += 1
    print(f"\nedges added from CONNECT_EDGES: {added}")

    # ---- 4. traps + what is deliberately missing --------------------------
    traps = read_traps()
    notes = payload.setdefault("notes", {})
    was_traps = len(notes.get("traps") or [])
    notes["traps"] = traps or notes.get("traps") or []
    print(f"traps: {was_traps} -> {len(notes['traps'])}")

    zip_edges = sum(1 for r in db.rows(conn, 'select KEY from LIBRARY_META."CONNECT".CONNECT_EDGES')
                    if r[0] in NON_IDENTITY_KEYS)
    portal_n = db.rows(conn, """select count(*) from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
                                where TABLE_SCHEMA='LANDING' and TABLE_NAME like 'PORTAL\\_%' escape '\\\\'""")[0][0]
    notes["excluded"] = {
        "refreshed_on": date.today().isoformat(),
        "zip_edges": zip_edges,
        "portal_tables": portal_n,
        "why": ("ZIP and NAME@ZIP edges identify a postcode, not a party. "
                f"{portal_n} PORTAL_ tables are landed but not wired into CONNECT."),
    }

    # ---- 5. live rows for the 364 tables the BUILDER adds -----------------
    # base_tables.js holds 209; build_chain_handbook.py appends the rest from
    # the payload and reads their row counts out of a CSV from a location scan.
    # That CSV is a snapshot too.
    #
    # Hand the builder the WHOLE warehouse keyed by fully qualified name, not a
    # guess keyed by bare table id. A bare id is ambiguous: FED_FDA_GUDID is
    # 2,542 rows in LANDING and 5,083,948 in HEALTH__FED_FDA_GUDID, and the
    # handbook entry points at the mart. Only the builder knows which fqn it
    # assigned, so only the builder can pick. This file just tells the truth
    # about every name.
    (CHAIN / "live_rows.json").write_text(
        json.dumps({"by_fqn": counts, "by_name": {k: v for k, v in names.items()}},
                   separators=(",", ":")), encoding="utf-8")
    print(f"live_rows.json: {len(counts):,} fully qualified names counted")

    # ---- 6. write ---------------------------------------------------------
    write_global(CHAIN / "base_tables.js", "HANDBOOK_TABLES", tables)
    write_global(CHAIN / "base_context.js", "HANDBOOK_CONTEXT", context)
    write_global(CHAIN / "base_schema.js", "HANDBOOK_SCHEMA", schema)
    (CHAIN / "repo_payload.json").write_text(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote chain/ inputs. tables now {len(tables)}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
