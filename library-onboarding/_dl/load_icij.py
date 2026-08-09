import sys, hashlib, time
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
import pandas as pd
from snow import connect
from ingest import _load_landing, _sf_col, assess_density

conn = connect()
run_id = f"manual-{int(time.time())}"

files = {
    "ICIJ_OFFSHORE_LEAKS_ENTITIES": "nodes-entities.csv",
    "ICIJ_OFFSHORE_LEAKS_OFFICERS": "nodes-officers.csv",
    "ICIJ_OFFSHORE_LEAKS_INTERMEDIARIES": "nodes-intermediaries.csv",
    "ICIJ_OFFSHORE_LEAKS_ADDRESSES": "nodes-addresses.csv",
    "ICIJ_OFFSHORE_LEAKS_RELATIONSHIPS": "relationships.csv",
}

base = r"c:\Code\Ripple_v6\library-onboarding\_dl\icij_extract"

gate_failed = []
for table, fname in files.items():
    path = f"{base}\\{fname}"
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    df = pd.read_csv(path, dtype=str, keep_default_na=False, low_memory=False)
    df.columns = [_sf_col(c) for c in df.columns]
    df["_INGESTED_AT"] = int(time.time() * 1_000_000)
    df["_SOURCE_RUN_ID"] = run_id
    df["_SRC_SHA256"] = sha
    print(table, "rows:", len(df))
    _load_landing(conn, df, table, overwrite=True)
    # QUALITY GATE: same density gate ingest.py's own run_ingest() uses -- a load
    # that landed but carries no real data (parse failure / schema drift) must not
    # be waved through as a clean success.
    dens = assess_density(df)
    if dens["empty"]:
        print(f"  QUALITY GATE FAILED for {table}: {dens['reason']} ({dens})")
        gate_failed.append(table)
    cur = conn.cursor()
    cur.execute(f"select count(*), count(distinct node_id) from library_raw.landing.{table}" if "NODE_ID" in df.columns else f"select count(*) from library_raw.landing.{table}")
    print(" ->", cur.fetchall())

print("done")
if gate_failed:
    raise RuntimeError(f"QUALITY GATE FAILED for: {', '.join(gate_failed)}")
