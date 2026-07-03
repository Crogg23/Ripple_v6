"""ripple chart — ask the Library a question, get a real, editable Plotly chart.

    ripple chart "SELECT ..."             run SQL, auto-pick a plug, open the chart
    ripple chart q.sql                    same, SQL from a file (BOM-safe)
    ripple chart run --file q.sql --plug bar --x STATE --y TOTAL --slug fec_money
    ripple chart find <term>              search everything chartable (live catalog)
    ripple chart shelves                  the browse menu, by domain
    ripple chart cols <fqn>               columns of any table (no warehouse needed)
    ripple chart profile <fqn>            chart-roles per column (all-TEXT friendly)
    ripple chart cast <fqn>               draft the casted SELECT for a landing table
    ripple chart last                     re-run the newest card
    ripple chart eject <card.py>          inline the plug's Plotly source into the card
    ripple chart budget                   the serving budget line

Every chart becomes a card: investigations/<slug>_<date>/qNN_<plug>.py — edit the
SQL or kwargs in the card, run it, refresh the browser. That is the loop.

This module stays stdlib-only at import time (the dispatcher imports every verb
eagerly; offline tests must collect without plotly). All viz imports live in run().
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ACTIONS = {"run", "find", "shelves", "cols", "profile", "cast", "last", "eject", "budget"}


def add_arguments(parser) -> None:
    parser.add_argument("args", nargs="*",
                        help="action (run|find|shelves|cols|profile|cast|last|eject|budget) "
                             "+ target; bare SQL or a .sql path implies run")
    parser.add_argument("--file", help="read SQL from a file (utf-8/utf-16 BOM-sniffed)")
    parser.add_argument("--sql", help="the SQL itself (equivalent to passing it positionally)")
    parser.add_argument("--plug", help="plug name (default: auto-suggest from the result)")
    parser.add_argument("--x")
    parser.add_argument("--y")
    parser.add_argument("--color")
    parser.add_argument("--arg", action="append", default=[], metavar="K=V",
                        help="extra plug kwarg, repeatable (e.g. --arg log_y=true)")
    parser.add_argument("--slug", help="investigation folder slug (reused across questions)")
    parser.add_argument("--name", help="card name (default: the plug name)")
    parser.add_argument("--new", action="store_true", help="always fork a new card")
    parser.add_argument("--limit", type=int, help="row cap (default 10000)")
    parser.add_argument("--title")
    parser.add_argument("--no-open", action="store_true", help="don't open the browser")
    parser.add_argument("--unsafe-claims", action="store_true",
                        help="allow raw LEADS reads (LEAD badge is baked into the chart)")
    parser.add_argument("--portals", action="store_true", help="include portal_ tables in find")
    parser.add_argument("--refresh", action="store_true", help="bust the discovery cache")


def run(args) -> int:
    tokens = list(args.args or [])
    action = tokens.pop(0) if tokens and tokens[0] in ACTIONS else "run"
    target = " ".join(tokens).strip()
    try:
        return _dispatch(action, target, args)
    except Exception as exc:  # keep the console usable — one clean line, not a traceback wall
        print(f"[XX] {exc}")
        return 1


def _dispatch(action: str, target: str, args) -> int:
    from ripple import common as C

    if action == "budget":
        from viz import sqlrun
        st = sqlrun.lane_status()
        print(C.header("ripple chart - budget / lane"))
        print(f"lane: {st['lane']}  warehouse: {st['warehouse']}")
        for n in st["notes"]:
            print(n)
        print(sqlrun.budget_line(refresh=True))
        return 0

    if action == "shelves":
        from viz import catalog
        rows = catalog.shelves()
        print(C.header("the Library - what's on the shelves (live)"))
        data = [[r.get("ARM", r.get("arm")), r.get("DOMAIN"), r.get("SOURCES"),
                 C.human_int(r.get("TOTAL_ROWS") or 0)] for r in rows]
        print(C.table(["arm", "domain", "datasets", "rows"], data))
        return 0

    if action == "find":
        from viz import catalog
        hits = catalog.find(target, include_portals=args.portals, refresh=args.refresh)
        print(C.header(f"chartable matches for '{target or '*'}' ({len(hits)})"))
        data = [[h["kind"], (h["name"] or "")[:44], h["domain"] or "", h["lifecycle"],
                 "sample" if h["is_sample"] else "", C.human_int(h["rows"] or 0),
                 h["fqn"] or ""] for h in hits[:40]]
        print(C.table(["kind", "name", "domain", "state", "", "rows", "fqn"], data))
        if len(hits) > 40:
            print(f"... and {len(hits) - 40} more (narrow the term)")
        return 0

    if action == "cols":
        from viz import catalog
        for c in catalog.columns(target):
            print(f"{c['column']:<40s} {c['sf_type']}")
        return 0

    if action == "profile":
        from viz import catalog
        rows = catalog.profile(target, refresh=args.refresh)
        print(C.header(f"column chart-roles - {target}"))
        data = [[p["column"][:44], p["role"], p["how"],
                 p.get("nonnull_pct", ""), p.get("distinct_sampled", "")] for p in rows]
        print(C.table(["column", "role", "how", "nonnull%", "~distinct"], data))
        return 0

    if action == "cast":
        from viz import catalog
        print(catalog.cast_sql(target))
        return 0

    if action == "eject":
        from viz import card as cardmod
        path = cardmod.eject(target)
        print(f"[OK] plug source inlined into {path}")
        print("     edit the function body, then: python " + str(path))
        return 0

    if action == "last":
        from viz import card as cardmod
        path = cardmod.latest_card()
        if not path:
            print("[!!] no cards yet - run a question first")
            return 1
        return _exec_card(path, args)

    # ---- run ----
    sql = _read_sql(target, args)
    if not sql:
        print("[!!] no SQL - pass it inline, via --file, or pipe it on stdin")
        return 1
    return _run_question(sql, args)


def _read_sql(target: str, args) -> str:
    if getattr(args, "sql", None):
        return args.sql
    if args.file:
        return _read_sql_file(args.file)
    if target == "-":
        return sys.stdin.read()
    if target and Path(target).suffix.lower() == ".sql" and Path(target).exists():
        return _read_sql_file(target)
    return target


def _read_sql_file(path: str) -> str:
    """PowerShell 5.1 redirection writes UTF-16 LE with BOM - sniff, don't assume."""
    raw = Path(path).read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    return raw.decode("utf-8")


def _plug_kwargs(args) -> dict:
    kw = {}
    for k, v in (("x", args.x), ("y", args.y), ("color", args.color), ("title", args.title)):
        if v:
            kw[k] = v
    for pair in args.arg:
        if "=" not in pair:
            raise ValueError(f"--arg wants K=V, got {pair!r}")
        k, v = pair.split("=", 1)
        kw[k.strip()] = _coerce(v.strip())
    return kw


def _coerce(v: str):
    low = v.lower()
    if low in ("true", "false"):
        return low == "true"
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def _run_question(sql: str, args) -> int:
    from viz import card as cardmod
    from viz import plugs, safety, sqlrun, theme

    st = sqlrun.lane_status()
    for n in st["notes"]:
        print(n)

    df, meta = sqlrun.run(sql, limit_rows=args.limit or 10_000,
                          unsafe_claims=args.unsafe_claims)
    print(f"[OK] {len(df)} rows in {meta['elapsed_s']}s on {meta['warehouse']}"
          + (" (truncated)" if meta["truncated"] else "") + f" | {meta['budget']}")

    classification = safety.classify_query(sql, df)
    kwargs = _plug_kwargs(args)
    plug_name = args.plug
    if not plug_name:
        ranked = plugs.suggest(df)
        plug_name, auto_kwargs, why = ranked[0]
        auto_kwargs.update(kwargs)
        kwargs = auto_kwargs
        print(f"[OK] plug: {plug_name} ({why}) - override with --plug/--x/--y")
    if plug_name not in plugs.PLUGS:
        print(f"[XX] unknown plug '{plug_name}' - one of: {', '.join(sorted(plugs.PLUGS))}")
        return 1

    path = cardmod.new_card(
        slug=args.slug or "adhoc", sql=sql, plug=plug_name, plug_kwargs=kwargs,
        classification=classification, unsafe_claims=args.unsafe_claims,
        limit_rows=args.limit, name=args.name, new=args.new,
    )

    fig = plugs.PLUGS[plug_name](df, as_of=meta["as_of"], **kwargs)
    ba = safety.badge_args(classification)
    if ba:
        fig = safety.badge(fig, *ba)
        print(f"[!!] {ba[0].upper()}: {ba[1]}")
    out = path.with_suffix(".html")
    fig.write_html(out, include_plotlyjs="directory", config=theme.PLOT_CONFIG)
    print(f"[OK] card: {path}")
    print(f"[OK] chart: {out}")
    if not args.no_open and not os.environ.get("RIPPLE_NO_OPEN"):
        import webbrowser
        webbrowser.open(out.resolve().as_uri())
    print("     loop: edit the card's SQL/kwargs -> python <card> -> refresh the tab")
    return 0


def _exec_card(path, args) -> int:
    import subprocess
    env = dict(os.environ)
    if args.no_open:
        env["RIPPLE_NO_OPEN"] = "1"
    print(f"[OK] re-running {path}")
    return subprocess.run([sys.executable, str(path)], env=env).returncode
