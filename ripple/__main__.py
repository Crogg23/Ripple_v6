"""ripple CLI dispatcher.  python -m ripple <verb>  (or  python ripple.py <verb>)

Each feature lives in its own module exposing add_arguments(subparser) + run(args) -> int.
The dispatcher wires them all so no single module owns the arg table.
"""
from __future__ import annotations

import argparse
import sys

from . import deck, doctor, pour, review

VERBS = {
    "status": (deck, "the Morning Deck — your whole world on one screen"),
    "doctor": (doctor, "one GREEN/RED go/no-go health check"),
    "review": (review, "the batch review cockpit — drain the decision queues"),
    "pour": (pour, "plan / watch / run the onboarding pour (deterministic-first)"),
}


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="ripple", description="The single front door to the Library.")
    sub = ap.add_subparsers(dest="verb")
    for name, (mod, help_) in VERBS.items():
        p = sub.add_parser(name, help=help_)
        if hasattr(mod, "add_arguments"):
            mod.add_arguments(p)
    return ap


def main(argv=None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    if not args.verb:
        ap.print_help()
        return 0
    mod, _ = VERBS[args.verb]
    return int(mod.run(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
