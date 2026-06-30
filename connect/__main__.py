"""CLI for the connect engine.

    python -m connect fingerprint           # profile landed tables -> keys + population
    python -m connect discover              # compute the real connection edge-list
    python -m connect explore               # render the interactive map
    python -m connect all                   # do all three (the usual run)
    python -m connect probe --a A --akey C --b B --bkey C --key NPI   # one pair, ad hoc
"""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser(prog="connect", description="Ripple connection engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("fingerprint", help="profile landed tables")
    d = sub.add_parser("discover", help="compute real connections")
    d.add_argument("--name-max-rows", type=int, default=None, help="include name joins up to this table size")
    d.add_argument("--no-bridge", action="store_true", help="skip the transitive crosswalk/bridge pass (#2)")
    d.add_argument("--fanout-max", type=int, default=40, help="drop crosswalk values mapping to > this many targets")
    sub.add_parser("explore", help="render the interactive map")
    sub.add_parser("plane", help="render The Plane — Google-Earth flythrough of the warehouse")
    sub.add_parser("spine", help="build the persisted entity spine (who's who)")
    a = sub.add_parser("all", help="fingerprint -> discover -> spine -> explore")
    a.add_argument("--name-max-rows", type=int, default=None)
    a.add_argument("--no-bridge", action="store_true")
    a.add_argument("--fanout-max", type=int, default=40)

    # --- incremental engine (additive; full rebuild above stays the backstop) ---
    si = sub.add_parser("seed", help="incremental: init persisted keyset twins + watermark (run AFTER a full rebuild)")
    si.add_argument("--reseed", action="store_true", help="overwrite the twins from the current backstop output")
    c1 = sub.add_parser("connect-one", help="incremental: link ONE just-landed table into the spine/graph")
    c1.add_argument("--source", required=True, help="source_id or landing table")
    c1.add_argument("--dry-run", action="store_true")
    cch = sub.add_parser("connect-changed", help="incremental: reslice every table whose content-key moved (the heartbeat)")
    cch.add_argument("--scope", choices=["spine", "all"], default="spine")
    cch.add_argument("--dry-run", action="store_true")
    # `validate-incremental` here == the module CLI's `validate` verb (incremental.py:915); both dispatch to incremental.validate()
    vi = sub.add_parser("validate-incremental", help="non-destructive proof incremental == full rebuild")
    vi.add_argument("--table", default=None)

    p = sub.add_parser("probe", help="overlap of one ad-hoc pair")
    p.add_argument("--a", required=True); p.add_argument("--akey", required=True)
    p.add_argument("--b", required=True); p.add_argument("--bkey", required=True)
    p.add_argument("--key", required=True, help="key type, e.g. NPI / CCN / ZIP / NAME")

    sub.add_parser("entity-index", help="rebuild the entity search/dossier index")

    ds = sub.add_parser("dossier", help="every cross-domain row for one entity (name or id)")
    ds.add_argument("--npi"); ds.add_argument("--ccn"); ds.add_argument("--ein")
    ds.add_argument("--id", dest="entity_id", help="entity_id directly")
    ds.add_argument("--q", help="name search")
    ds.add_argument("--json", action="store_true", help="write outputs/dossier_<id>.json")
    ds.add_argument("--html", action="store_true", help="write outputs/dossier_<id>.html")

    ld = sub.add_parser("leads", help="run codified cross-domain lead jobs -> ranked LEADS table")
    ld.add_argument("--job", default="all", help="job name (e.g. banned_but_operating) or 'all'")
    ld.add_argument("--run", action="store_true", help="write to LIBRARY_META.CONNECT.LEADS (default previews only)")
    ld.add_argument("--top", type=int, default=20, help="how many leads to print")

    rc = sub.add_parser("receipt", help="the run-it-yourself proof for one lead (frozen SQL + data snapshot)")
    rc.add_argument("--id", dest="lead_id", required=True, help="LEAD_xxxx")
    rc.add_argument("--sql", action="store_true", help="print ONLY the runnable SQL (pipe to a worksheet)")
    rc.add_argument("--json", action="store_true", help="emit the receipt as JSON")
    rc.add_argument("--check", action="store_true", help="re-run the stored SQL read-only and confirm the entity reproduces")

    rs = sub.add_parser("resolve", help="fuzzy record linkage (GATED: writes ENTITY_LINKS, never the spine)")
    rs.add_argument("--pair", default="leie_nppes", help="recipe name")
    rs.add_argument("--write", action="store_true", help="persist ENTITY_LINKS (default previews only)")
    rs.add_argument("--min-score", type=float, default=0.80)
    rs.add_argument("--top", type=int, default=25)

    ev = sub.add_parser("eval", help="precision/recall sweep of the fuzzy resolver (the gate)")
    ev.add_argument("--pair", default="leie_nppes")
    ev.add_argument("--target", type=float, default=0.99, help="precision target for the HIGH bar")

    mt = sub.add_parser("match", help="Fellegi-Sunter match-weight scorer (the confidence ladder)")
    mt.add_argument("--pair", default="leie_nppes")

    cb = sub.add_parser("calibrate", help="estimate m/u from ground truth + set held-out tiers")
    cb.add_argument("--pair", default="leie_nppes")

    rv = sub.add_parser("review", help="record a human verdict on a claim (the safety spine)")
    rv.add_argument("--kind", default="lead", choices=["lead", "link", "entity"])
    rv.add_argument("--id", dest="target_id", required=True, help="stable id of the claim (e.g. LEAD_xxxx)")
    rv.add_argument("--decision", required=True, choices=["confirmed", "rejected", "retracted", "stale"])
    rv.add_argument("--by", dest="reviewer", default="")
    rv.add_argument("--reason", default="")

    sf = sub.add_parser("safety", help="show recorded review / suppression decisions")
    sf.add_argument("--kind", default=None, choices=["lead", "link", "entity"])

    h = sub.add_parser("harvest", help="bulk-load datasets from the portal index (no LLM)")
    h.add_argument("--platform", choices=["SOCRATA", "ARCGIS"], default=None)
    h.add_argument("--with-key", action="store_true", help="only datasets that carry a join key")
    h.add_argument("--connectable", action="store_true",
                   help="target ENTITY-key datasets, ordered to wire into data you already hold (#3)")
    h.add_argument("--verify", action="store_true", help="after load, check which new tables really connect")
    h.add_argument("--limit", type=int, default=10, help="max datasets this run")
    h.add_argument("--max-rows", type=int, default=500, help="row cap per dataset")
    h.add_argument("--run", action="store_true", help="actually load (default previews only)")
    h.add_argument("--force", action="store_true", help="reload even if already landed")
    h.add_argument("--refresh", action="store_true", help="re-fetch landed sources; skip if content SHA unchanged")

    args = ap.parse_args()

    if args.cmd in ("fingerprint", "all"):
        from . import fingerprint
        fingerprint.run()
    if args.cmd in ("discover", "all"):
        from . import discover
        kw = {"bridge_on": not getattr(args, "no_bridge", False),
              "fanout_max": getattr(args, "fanout_max", 40)}
        if getattr(args, "name_max_rows", None):
            kw["name_max_rows"] = args.name_max_rows
        discover.run(**kw)
    if args.cmd in ("spine", "all"):
        from . import spine
        spine.run()
    if args.cmd == "seed":
        from . import incremental
        incremental.seed(reseed=getattr(args, "reseed", False))
    if args.cmd == "connect-one":
        from . import incremental
        incremental.connect_one(args.source, dry_run=getattr(args, "dry_run", False))
    if args.cmd == "connect-changed":
        from . import incremental
        incremental.connect_changed(scope=getattr(args, "scope", "spine"),
                                    dry_run=getattr(args, "dry_run", False))
    if args.cmd == "validate-incremental":
        from . import incremental
        incremental.validate(table=getattr(args, "table", None))
    if args.cmd in ("explore", "all"):
        from . import explore
        explore.render()
    if args.cmd == "plane":
        from . import plane
        plane.render()
    if args.cmd == "probe":
        from . import db
        from .overlap import value_overlap
        conn = db.connect()
        try:
            print(value_overlap(conn, args.a, args.akey, args.b, args.bkey, args.key))
        finally:
            conn.close()
    if args.cmd == "entity-index":
        from . import entity_index
        entity_index.run()
    if args.cmd == "dossier":
        from . import dossier
        dossier.run(npi=args.npi, ccn=args.ccn, ein=args.ein, entity_id=args.entity_id,
                    q=args.q, as_json=args.json, as_html=args.html)
    if args.cmd == "leads":
        from . import leads
        leads.run(job=args.job, dry_run=not args.run, top=args.top)
    if args.cmd == "receipt":
        from . import receipt
        receipt.run(args.lead_id, sql_only=args.sql, as_json=args.json, check=args.check)
    if args.cmd == "resolve":
        from . import resolve
        resolve.run(pair=args.pair, write=args.write, top=args.top, min_score=args.min_score)
    if args.cmd == "eval":
        from . import evaluate
        evaluate.run(pair=args.pair, target=args.target)
    if args.cmd == "match":
        from . import match
        match.run(pair=args.pair)
    if args.cmd == "calibrate":
        from . import calibrate
        calibrate.run(pair=args.pair)
    if args.cmd == "review":
        from . import db, safety
        conn = db.connect()
        try:
            safety.record(conn, args.kind, args.target_id, args.decision,
                          reviewer=args.reviewer, reason=args.reason)
            print(f"recorded: {args.kind} {args.target_id} -> {args.decision}"
                  + (f" (by {args.reviewer})" if args.reviewer else ""))
        finally:
            conn.close()
    if args.cmd == "safety":
        from . import db, safety
        conn = db.connect()
        try:
            rows = safety.status(conn, args.kind)
            if not rows:
                print("no review decisions recorded yet.")
            for r in rows:
                print(f"  {r['TARGET_KIND']:>7} {r['DECISION']:>10}  {r['N']}")
        finally:
            conn.close()
    if args.cmd == "harvest":
        from . import portal_loader
        portal_loader.run(platform=args.platform, with_key=args.with_key,
                          limit=args.limit, max_rows=args.max_rows,
                          do_run=args.run, force=args.force,
                          connectable=args.connectable, verify=args.verify,
                          refresh=args.refresh)
    return 0


if __name__ == "__main__":
    sys.exit(main())
