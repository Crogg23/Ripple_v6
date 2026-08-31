"""The Bench's tunable numbers, in one place, each overridable by env var.

Everything here has a sensible default and none of it needs setting to run
the app. Override by exporting the variable before launch:

    BENCH_DEBUG=1 python bench/app.py       # hot reload while hacking on it
    BENCH_PORT=9000 python bench/app.py

This module imports nothing but the standard library on purpose - anything
(tests, perf.py, data.py) can read it without dragging Dash in.
"""

from __future__ import annotations

import os


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, "") or default)
    except ValueError:
        return default


def _float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, "") or default)
    except ValueError:
        return default


def _bool(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


# How long the code panel waits after the last keystroke before reading it.
DEBOUNCE_MS = _int("BENCH_DEBOUNCE_MS", 600)

# How long a repaint may look like nothing before the spinner shows.
SPINNER_MS = _int("BENCH_SPINNER_MS", 250)

# How long custom code gets before the deadline tracer pulls the plug.
CUSTOM_TIMEOUT_S = _float("BENCH_CUSTOM_TIMEOUT_S", 5.0)

# Where the dev server listens.
PORT = _int("BENCH_PORT", 8051)

# The LIMIT starter SQL is written with.
SQL_LIMIT = _int("BENCH_SQL_LIMIT", 1000)

# How many tables the "look up" dropdown lists before asking you to narrow.
TABLE_CAP = _int("BENCH_TABLE_CAP", 200)

# Dash debug mode: hot reload + the in-page error console.
DEBUG = _bool("BENCH_DEBUG")
