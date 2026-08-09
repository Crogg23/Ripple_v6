import sys, json, time, hashlib
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
import zipfile
import pandas as pd
from snow import connect
from ingest import _load_landing, assess_density

ZIP_PATH = r"c:\Code\Ripple_v6\library-onboarding\_dl\ch_psc_snapshot.zip"
INNER = "persons-with-significant-control-snapshot-2026-08-05.txt"
TABLE = "UK_COMPANIES_HOUSE_PSC"
CHUNK = 250_000

conn = connect()
run_id = f"manual-{int(time.time())}"
gate_failed = []
chunk_num = 0

def flat(rec):
    d = rec.get("data", {}) or {}
    name_elements = d.get("name_elements", {}) or {}
    addr = d.get("address", {}) or {}
    dob = d.get("date_of_birth", {}) or {}
    ident = d.get("identification", {}) or {}
    noc = d.get("natures_of_control", []) or []
    return {
        "COMPANY_NUMBER": rec.get("company_number"),
        "KIND": d.get("kind"),
        "NAME": d.get("name"),
        "NAME_TITLE": name_elements.get("title"),
        "NAME_FORENAME": name_elements.get("forename"),
        "NAME_MIDDLE": name_elements.get("middle_name"),
        "NAME_SURNAME": name_elements.get("surname"),
        "NATIONALITY": d.get("nationality"),
        "COUNTRY_OF_RESIDENCE": d.get("country_of_residence"),
        "DOB_MONTH": dob.get("month"),
        "DOB_YEAR": dob.get("year"),
        "ADDRESS_PREMISES": addr.get("premises"),
        "ADDRESS_LINE_1": addr.get("address_line_1"),
        "ADDRESS_LOCALITY": addr.get("locality"),
        "ADDRESS_POSTAL_CODE": addr.get("postal_code"),
        "ADDRESS_COUNTRY": addr.get("country"),
        "REGISTRATION_NUMBER": ident.get("registration_number"),
        "LEGAL_FORM": ident.get("legal_form"),
        "COUNTRY_REGISTERED": ident.get("country_registered"),
        "NATURES_OF_CONTROL": ";".join(noc) if isinstance(noc, list) else str(noc),
        "CEASED_ON": d.get("ceased_on"),
        "NOTIFIED_ON": d.get("notified_on"),
        "ETAG": d.get("etag"),
        "LINK_SELF": (d.get("links", {}) or {}).get("self"),
    }

def load_chunk(rows, overwrite):
    global chunk_num
    chunk_num += 1
    df = pd.DataFrame(rows)
    df = df.astype(object).where(pd.notnull(df), None).astype(str)
    df["_INGESTED_AT"] = int(time.time() * 1_000_000)
    df["_SOURCE_RUN_ID"] = run_id
    df["_SRC_SHA256"] = "streamed-see-source-zip"
    _load_landing(conn, df, TABLE, overwrite=overwrite)
    # QUALITY GATE: same density gate ingest.py's own run_ingest() uses -- a load
    # that landed but carries no real data (parse failure / schema drift) must not
    # be waved through as a clean success.
    dens = assess_density(df)
    if dens["empty"]:
        print(f"  QUALITY GATE FAILED for chunk {chunk_num}: {dens['reason']} ({dens})", flush=True)
        gate_failed.append(f"chunk {chunk_num}")

sha = hashlib.sha256()
z = zipfile.ZipFile(ZIP_PATH)
total = 0
buf = []
first = True
with z.open(INNER) as f:
    for raw_line in f:
        line = raw_line.decode("utf-8", "replace").strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        buf.append(flat(rec))
        if len(buf) >= CHUNK:
            load_chunk(buf, overwrite=first)
            total += len(buf)
            print("loaded", total, flush=True)
            buf = []
            first = False
    if buf:
        load_chunk(buf, overwrite=first)
        total += len(buf)
        print("loaded", total, flush=True)

print("TOTAL ROWS:", total)
if gate_failed:
    raise RuntimeError(f"QUALITY GATE FAILED for: {', '.join(gate_failed)}")
