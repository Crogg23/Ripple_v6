import sys, hashlib, time
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
import pandas as pd, openpyxl
from snow import connect
from ingest import _load_landing, _sf_col, assess_density

conn = connect()
run_id = f"manual-{int(time.time())}"

files = {
    "FED_OCC_NATIONAL_BANKS": ("occ_national_by_name.xlsx", "national bank / federal thrift"),
    "FED_OCC_THRIFTS": ("occ_thrifts_by_name.xlsx", "federal thrift"),
}

gate_failed = []
for table, (fname, kind) in files.items():
    path = f"c:\\Code\\Ripple_v6\\library-onboarding\\_dl\\{fname}"
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    # find header row (first row where first cell looks like a header keyword)
    header_idx = None
    for i, r in enumerate(rows):
        if r and r[0] and str(r[0]).strip().upper() in ("CHARTER NO", "CHARTER"):
            header_idx = i
            break
    header = [str(c).strip() if c else f"col{j}" for j, c in enumerate(rows[header_idx])]
    data = rows[header_idx+1:]
    df = pd.DataFrame(data, columns=header)
    df = df.dropna(how="all")
    df.columns = [_sf_col(c) for c in df.columns]
    df = df.astype(str)
    df["_INGESTED_AT"] = int(time.time() * 1_000_000)
    df["_SOURCE_RUN_ID"] = run_id
    df["_SRC_SHA256"] = sha
    print(table, "rows:", len(df), list(df.columns))
    _load_landing(conn, df, table, overwrite=True)
    # QUALITY GATE: same density gate ingest.py's own run_ingest() uses -- a load
    # that landed but carries no real data (parse failure / schema drift) must not
    # be waved through as a clean success.
    dens = assess_density(df)
    if dens["empty"]:
        print(f"  QUALITY GATE FAILED for {table}: {dens['reason']} ({dens})")
        gate_failed.append(table)

print("done")
if gate_failed:
    raise RuntimeError(f"QUALITY GATE FAILED for: {', '.join(gate_failed)}")
