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
    sub.add_parser("explore", help="render the interactive map")
    a = sub.add_parser("all", help="fingerprint -> discover -> explore")
    a.add_argument("--name-max-rows", type=int, default=None)

    p = sub.add_parser("probe", help="overlap of one ad-hoc pair")
    p.add_argument("--a", required=True); p.add_argument("--akey", required=True)
    p.add_argument("--b", required=True); p.add_argument("--bkey", required=True)
    p.add_argument("--key", required=True, help="key type, e.g. NPI / CCN / ZIP / NAME")

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

    args = ap.parse_args()

    if args.cmd in ("fingerprint", "all"):
        from . import fingerprint
        fingerprint.run()
    if args.cmd in ("discover", "all"):
        from . import discover
        kw = {}
        if getattr(args, "name_max_rows", None):
            kw["name_max_rows"] = args.name_max_rows
        discover.run(**kw)
    if args.cmd in ("explore", "all"):
        from . import explore
        explore.render()
    if args.cmd == "probe":
        from . import db
        from .overlap import value_overlap
        conn = db.connect()
        try:
            print(value_overlap(conn, args.a, args.akey, args.b, args.bkey, args.key))
        finally:
            conn.close()
    if args.cmd == "harvest":
        from . import portal_loader
        portal_loader.run(platform=args.platform, with_key=args.with_key,
                          limit=args.limit, max_rows=args.max_rows,
                          do_run=args.run, force=args.force,
                          connectable=args.connectable, verify=args.verify)
    return 0


if __name__ == "__main__":
    sys.exit(main())
