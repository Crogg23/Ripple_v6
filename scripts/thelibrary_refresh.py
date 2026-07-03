"""Post-pour refresh: rebuild the friendly layer + THE_LIBRARY reading room after
new sources land. CATALOG is a live view and self-updates; FRIENDLY_LAYER and the
THE_LIBRARY views are materialized snapshots that go stale, so re-run this once a
pour completes.

    python scripts/thelibrary_refresh.py            # rebuild names + views (content workflow separate)
    python scripts/thelibrary_refresh.py --apply    # same; --apply is passed through to the builder

NOTE: friendly NAMES + comments for brand-new datasets come from the content
workflow (see build-state). This script rebuilds the inventory + views/index from
whatever content JSON exists; new sources without generated content fall back to
their catalog description until the content workflow is re-run for them.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
PY = sys.executable
APPLY = "--apply" in sys.argv


def run(cmd):
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.call(cmd)


def main() -> int:
    rc = run([PY, str(_HERE / "thelibrary_inventory.py")])
    if rc != 0:
        print("inventory step failed; stopping.")
        return rc
    build = [PY, str(_HERE / "thelibrary_build.py")]
    if APPLY:
        build.append("--apply")
    return run(build)


if __name__ == "__main__":
    raise SystemExit(main())
