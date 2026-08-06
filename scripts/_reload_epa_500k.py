"""One-off: reload the EPA ECHO zip packages whose tables landed truncated at 500,000
rows before commit 29186d54 added the truncation guard. Calls bulk.load_zip_csvs
directly (bypasses the "already loaded" skip in epa_echo_bulk_load.main so it
overwrites the stale tables) with a corrected max_rows.
"""
import sys, io, datetime as dt
sys.path.insert(0, "scripts")
sys.path.insert(0, "library-onboarding")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import snow
import _bulk_load_utils as bulk
import epa_echo_bulk_load as epa

conn = snow.connect()

TARGETS = ["FRS", "ICIS_AIR", "AIR_EMISSIONS", "NPDES", "SDWA"]
manifest = {e["name"]: e for e in epa.ECHO_MANIFEST}

for name in TARGETS:
    entry = manifest[name]
    print(f"\n=== {name} === {dt.datetime.now().isoformat()}", flush=True)
    try:
        results = bulk.load_zip_csvs(
            conn, entry["url"], f"{epa.TABLE_PREFIX}_{name}", epa.ENTITY_KEYS,
            user_agent=epa.USER_AGENT, max_rows=5_000_000, timeout=900,
        )
        for tbl, rows, keys in results:
            print(f"  DONE {tbl}: {rows:,} rows", flush=True)
    except Exception as e:
        print(f"  FAILED {name}: {e}", flush=True)

print("\nALL DONE", dt.datetime.now().isoformat(), flush=True)
