"""Load NPDB (National Practitioner Data Bank) Public Use Data File.

Source: HRSA (npdb.hrsa.gov) -- requires a POST to a click-through Data Use
Agreement form (name/city/email + agree checkbox), no login/account needed.
Form fields: reportType=allRecords, professionGroup=allProfessions, format=C
(CSV) -- ASCII is the default if the 'All' option values aren't the exact
select option values ('allRecords'/'allProfessions', not 'A'). This is a NEW
form-quirk trap: the wrong-but-plausible value silently returns the wrong
file format with no error.

    python scripts/npdb_load.py --fetch   # submit form + download zip
    python scripts/npdb_load.py --run     # load the already-downloaded CSV
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

SCRATCH = Path(
    r"C:/Users/wroge/AppData/Local/Temp/claude/c--Code-Ripple-v6/"
    r"41f6e34a-95da-42ce-a581-c79ae645147e/scratchpad/npdb"
)
TABLE = "FED_HRSA_NPDB"
UA = {"User-Agent": "Mozilla/5.0 (Ripple-Library research; w.rogers9999@gmail.com)"}


def fetch():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    s.headers.update(UA)
    s.get("https://www.npdb.hrsa.gov/resources/publicData.jsp", timeout=30)
    data = {
        "name": "Ripple Library Research",
        "title": "",
        "city": "Remote",
        "state": "",
        "email": "w.rogers9999@gmail.com",
        "reportType": "allRecords",
        "professionGroup": "allProfessions",
        "format": "C",
        "terms": "on",
    }
    r = s.post("https://www.npdb.hrsa.gov/servlet/PublicUseFileServlet",
               data=data, timeout=120)
    m = re.search(r'href="(/resources/NpdbPublicUseData[^"]+\.zip)"', r.text)
    if not m:
        raise RuntimeError("Could not find download link in confirmation page")
    zip_url = "https://www.npdb.hrsa.gov" + m.group(1)
    print("Downloading", zip_url)
    zr = requests.get(zip_url, headers=UA, timeout=180)
    zip_path = SCRATCH / "npdb.zip"
    zip_path.write_bytes(zr.content)
    print("Saved", zip_path, len(zr.content), "bytes")

    with zipfile.ZipFile(zip_path) as z:
        csv_names = [n for n in z.namelist() if n.upper().endswith(".CSV")]
        print("CSV members:", csv_names)
        for n in csv_names:
            z.extract(n, SCRATCH)
    print("Extracted to", SCRATCH)


def run():
    csv_files = list(SCRATCH.glob("*.CSV")) + list(SCRATCH.glob("*.csv"))
    if not csv_files:
        raise RuntimeError("No CSV found -- run --fetch first")
    path = csv_files[0]
    content = path.read_bytes()
    sha = hashlib.sha256(content).hexdigest()
    print("sha256", sha, "bytes", len(content))

    df = pd.read_csv(path, dtype=str, encoding_errors="replace", low_memory=False)
    print("shape", df.shape)

    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    df.columns = [bulk.sf_col(c) for c in df.columns]
    df[bulk.META_INGESTED_AT] = started
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha

    conn = snow.connect()
    from snowflake.connector.pandas_tools import write_pandas
    ok, _c, nrows, _ = write_pandas(
        conn, df, table_name=TABLE,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    print("loaded", ok, nrows)
    passed, _report = bulk.run_quality_gate(
        conn, TABLE, TABLE, run_id, sha256=sha,
        source_url="https://www.npdb.hrsa.gov/resources/publicData.jsp")
    conn.close()
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if args.fetch:
        fetch()
    if args.run:
        run()
    if not args.fetch and not args.run:
        print("Pass --fetch and/or --run")
