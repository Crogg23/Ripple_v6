"""ripple panel -- the Control Panel: one local page to see Library health and push
real refreshes. Stdlib server; reads on COMPUTE_WH; jobs run like heartbeat runs them.

    python3 ripple.py panel                 # http://127.0.0.1:8899, auto-opens
    python3 ripple.py panel --port 9000 --no-open
"""
from __future__ import annotations


def add_arguments(parser) -> None:
    parser.add_argument("--port", type=int, default=8899, help="listen port (default 8899)")
    parser.add_argument("--no-open", action="store_true", help="don't auto-open the browser")


def run(args) -> int:
    # heavy imports stay inside run() -- verb modules must import stdlib-only
    from . import panel_server
    return panel_server.serve(port=args.port, open_browser=not args.no_open)
