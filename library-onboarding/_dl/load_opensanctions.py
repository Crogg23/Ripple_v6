import sys, hashlib, time
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
import pandas as pd
from snow import connect
from ingest import _load_landing, _sf_col, assess_density

path = r"c:\Code\Ripple_v6\library-onboarding\_dl\opensanctions_targets.csv"
sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
run_id = f"manual-{int(time.time())}"

df = pd.read_csv(path, dtype=str, keep_default_na=False)
df.columns = [_sf_col(c) for c in df.columns]
df["_INGESTED_AT"] = int(time.time() * 1_000_000)
df["_SOURCE_RUN_ID"] = run_id
df["_SRC_SHA256"] = sha
print("rows to load:", len(df), "cols:", list(df.columns))

conn = connect()
_load_landing(conn, df, "INTL_OPENSANCTIONS_DEFAULT", overwrite=True)
# QUALITY GATE: same density gate ingest.py's own run_ingest() uses -- a load
# that landed but carries no real data (parse failure / schema drift) must not
# be waved through as a clean success.
dens = assess_density(df)
if dens["empty"]:
    raise RuntimeError(
        f"QUALITY GATE FAILED for INTL_OPENSANCTIONS_DEFAULT: {dens['reason']} ({dens})"
    )
print("loaded.")

cur = conn.cursor()
cur.execute("select count(*), count(distinct id) from library_raw.landing.intl_opensanctions_default")
print(cur.fetchall())
cur.execute("select schema, count(*) from library_raw.landing.intl_opensanctions_default group by 1 order by 2 desc limit 15")
for r in cur.fetchall(): print(r)
