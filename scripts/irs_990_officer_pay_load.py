"""Land Form 990 Part VII Section A (officer / director / key employee pay)
for the hospital slice of the 990 e-file index.

Docket line 124. Built 2026-09-07 from reports/dead_ends_scope_B_parsers_2026-09-07.md.

WHAT SITS WHERE
  The pay is not in any landed table. It sits inside each return's XML at
  /Return/ReturnData/IRS990/Form990PartVIISectionAGrp, one group per person.
  The IRS hosts the XML as monthly zips (2023+) or yearly multi-part zips
  (2019-2022) at apps.irs.gov/pub/epostcard/990/xml/<year>/. There is NO
  per-object URL any more: the old s3.amazonaws.com/irs-form-990 bucket
  answers 404 and ProPublica's download-xml is behind a bot wall (checked
  2026-09-07). Object IDs starting 2016-2018 are hosted nowhere the IRS
  points to; those returns cannot be fetched by this script.

HOW IT AVOIDS 25 GB OF DOWNLOAD
  apps.irs.gov answers HTTP Range requests. The script reads each zip's
  central directory over Range (a few MB), intersects the member names
  (<OBJECT_ID>_public.xml) with the hospital slice, and pulls only those
  members, each with one Range request, decompressed locally with zlib.
  About 33K members instead of 68 zips.

THE SLICE
  EINs in LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF with NTEE_CODE
  like 'E2%' (hospitals), joined to LIBRARY_RAW.LANDING.FED_IRS_990_EFILE_INDEX
  on EIN, RETURN_TYPE = '990' (full form; EZ and PF have no Part VII A).
  Join key back to the index is OBJECT_ID, which is unique there
  (5,544,626 rows, 5,544,626 distinct). RETURN_ID is NOT unique
  (4,601,737 distinct) -- do not join on it.

LANDS
  LIBRARY_RAW.LANDING.FED_IRS_990_OFFICER_PAY, one row per person per
  return, all VARCHAR plus INGESTED_AT and _SOURCE_RUN_ID. Appends.
  Resume: object ids already in the table are skipped on the next run, and
  a finished zip is recorded in logs/irs_990_officer_pay_checkpoint.json.

    python scripts/irs_990_officer_pay_load.py            # dry run: parse 20, print
    python scripts/irs_990_officer_pay_load.py --run      # land everything reachable
    python scripts/irs_990_officer_pay_load.py --run --years 2024 2025
"""
from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import re
import struct
import sys
import time
import uuid
import zipfile
import zlib
from pathlib import Path
from xml.etree import ElementTree as ET

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

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TABLE = "FED_IRS_990_OFFICER_PAY"
SOURCE_ID = "fed_irs_990_officer_pay"
DOWNLOADS_PAGE = "https://www.irs.gov/charities-non-profits/form-990-series-downloads"
ZIP_BASE = "https://apps.irs.gov/pub/epostcard/990/xml/"
USER_AGENT = "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"
HEADERS = {"User-Agent": USER_AGENT}

CHECKPOINT_FILE = _REPO / "logs" / "irs_990_officer_pay_checkpoint.json"
TARGETS_FILE = _REPO / "logs" / "irs_990_officer_pay_targets.json"
ZIPLIST_FILE = _REPO / "logs" / "irs_990_officer_pay_zips.json"

FLUSH_ROWS = 25_000
PROGRESS_EVERY = 500
FETCH_WORKERS = 6
DRY_RUN_RETURNS = 20

SLICE_SQL = """
select i.OBJECT_ID, i.EIN, i.TAX_PERIOD, i.TAXPAYER_NAME
from LIBRARY_RAW.LANDING.FED_IRS_990_EFILE_INDEX i
join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF b on b.EIN = i.EIN
where b.NTEE_CODE like 'E2%' and i.RETURN_TYPE = '990'
"""

COLUMNS = [
    "EIN", "TAX_YEAR", "TAX_PERIOD_END", "TAX_PERIOD", "OBJECT_ID", "RETURN_TYPE",
    "FILER_NAME", "PERSON_SEQ", "PERSON_NAME", "TITLE",
    "AVG_HOURS_PER_WEEK", "AVG_HOURS_PER_WEEK_RELATED_ORG",
    "IS_TRUSTEE_OR_DIRECTOR", "IS_INSTITUTIONAL_TRUSTEE", "IS_OFFICER",
    "IS_KEY_EMPLOYEE", "IS_HIGHEST_COMPENSATED", "IS_FORMER",
    "REPORTABLE_COMP_FROM_ORG", "REPORTABLE_COMP_FROM_RELATED_ORGS",
    "OTHER_COMPENSATION", "SCHEMA_VERSION", "SOURCE_ZIP",
]

# Two generations of the IRS schema. 2013+ ("new") and the older one that
# still shows up on late-filed returns. Same fields, different tag names.
FIELD_MAP = {
    "PERSON_NAME": ("PersonNm", "NamePerson", "BusinessName/BusinessNameLine1Txt",
                    "BusinessName/BusinessNameLine1"),
    "TITLE": ("TitleTxt", "Title"),
    "AVG_HOURS_PER_WEEK": ("AverageHoursPerWeekRt", "AverageHoursPerWeek"),
    "AVG_HOURS_PER_WEEK_RELATED_ORG": ("AverageHoursPerWeekRltdOrgRt",
                                       "AverageHoursPerWeekRelated"),
    "IS_TRUSTEE_OR_DIRECTOR": ("IndividualTrusteeOrDirectorInd", "IndividualTrusteeOrDirector"),
    "IS_INSTITUTIONAL_TRUSTEE": ("InstitutionalTrusteeInd", "InstitutionalTrustee"),
    "IS_OFFICER": ("OfficerInd", "Officer"),
    "IS_KEY_EMPLOYEE": ("KeyEmployeeInd", "KeyEmployee"),
    "IS_HIGHEST_COMPENSATED": ("HighestCompensatedEmployeeInd", "HighestCompensatedEmployee"),
    "IS_FORMER": ("FormerOfcrDirectorTrusteeInd", "Former"),
    "REPORTABLE_COMP_FROM_ORG": ("ReportableCompFromOrgAmt", "ReportableCompFromOrganization"),
    "REPORTABLE_COMP_FROM_RELATED_ORGS": ("ReportableCompFromRltdOrgAmt",
                                          "ReportableCompFromRelatedOrgs"),
    "OTHER_COMPENSATION": ("OtherCompensationAmt", "OtherCompensation"),
}
GROUP_TAGS = ("Form990PartVIISectionAGrp", "Form990PartVIISectionA")


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------
_session = requests.Session()
_session.headers.update(HEADERS)


def http_get(url: str, rng: tuple[int, int] | None = None, tries: int = 6) -> bytes:
    headers = {}
    if rng is not None:
        headers["Range"] = f"bytes={rng[0]}-{rng[1]}"
    for attempt in range(tries):
        try:
            r = _session.get(url, headers=headers, timeout=120)
            if r.status_code in (200, 206):
                return r.content
            if r.status_code in (429, 503, 502, 500):
                time.sleep(min(120, 10 * (attempt + 1)))
                continue
            r.raise_for_status()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout, requests.exceptions.ChunkedEncodingError):
            time.sleep(min(120, 10 * (attempt + 1)))
    raise RuntimeError(f"gave up on {url} range={rng}")


def http_size(url: str) -> int:
    r = _session.head(url, timeout=60, allow_redirects=True)
    r.raise_for_status()
    return int(r.headers["Content-Length"])


class RemoteFile(io.RawIOBase):
    """Seekable read-only view of a URL over HTTP Range. zipfile uses it to
    read the central directory without downloading the archive."""
    MIN_CHUNK = 1 << 20  # 1 MB

    def __init__(self, url: str):
        self.url = url
        self.size = http_size(url)
        self.pos = 0
        self._buf = b""
        self._buf_start = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            self.pos = off
        elif whence == io.SEEK_CUR:
            self.pos += off
        else:
            self.pos = self.size + off
        return self.pos

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        if n == 0 or self.pos >= self.size:
            return b""
        end = min(self.size, self.pos + n)
        if not (self._buf_start <= self.pos and end <= self._buf_start + len(self._buf)):
            want = max(n, self.MIN_CHUNK)
            start = self.pos
            stop = min(self.size, start + want) - 1
            self._buf = http_get(self.url, (start, stop))
            self._buf_start = start
        off = self.pos - self._buf_start
        out = self._buf[off:off + (end - self.pos)]
        self.pos += len(out)
        return out


def fetch_member(url: str, info: zipfile.ZipInfo) -> bytes:
    """One Range request for one member, decompressed locally."""
    start = info.header_offset
    # local header: 30 fixed + name + extra (may differ from central; slack)
    span = 30 + len(info.filename.encode("utf-8")) + len(info.extra) + 1024 + info.compress_size
    raw = http_get(url, (start, start + span - 1))
    sig, _, _, method, _, _, _, csize, _, fn_len, ex_len = struct.unpack("<IHHHHHIIIHH", raw[:30])
    if sig != 0x04034b50:
        raise ValueError(f"bad local header for {info.filename}")
    data_start = 30 + fn_len + ex_len
    data = raw[data_start:data_start + info.compress_size]
    if len(data) < info.compress_size:
        raise ValueError(f"short read for {info.filename}")
    if info.compress_type == zipfile.ZIP_STORED:
        return data
    if info.compress_type == zipfile.ZIP_DEFLATED:
        return zlib.decompress(data, -15)
    if info.compress_type == 9:
        # Deflate64. The 2020 CT1 zip and every 2025/2026 monthly zip use it;
        # zlib cannot inflate it and the first run lost 2,942 returns to that.
        # pip install inflate64.
        import inflate64
        d = inflate64.Inflater()
        return d.inflate(data)
    raise ValueError(f"unsupported compression {info.compress_type} on {info.filename}")


# ---------------------------------------------------------------------------
# Zip list
# ---------------------------------------------------------------------------
def list_zip_urls(refresh: bool = False) -> list[str]:
    if ZIPLIST_FILE.exists() and not refresh:
        return json.loads(ZIPLIST_FILE.read_text())
    html = _session.get(DOWNLOADS_PAGE, headers={"User-Agent": "Mozilla/5.0"}, timeout=60).text
    urls = sorted(set(re.findall(re.escape(ZIP_BASE) + r'[^"\']+\.zip', html)))
    ZIPLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    ZIPLIST_FILE.write_text(json.dumps(urls, indent=1))
    return urls


def zip_year(url: str) -> str:
    return url.split("/xml/")[1].split("/")[0]


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------
def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _find_text(el, paths) -> str | None:
    for p in paths:
        cur = el
        for part in p.split("/"):
            nxt = None
            for child in cur:
                if _strip_ns(child.tag) == part:
                    nxt = child
                    break
            if nxt is None:
                cur = None
                break
            cur = nxt
        if cur is not None and cur.text is not None and cur.text.strip():
            return cur.text.strip()
    return None


def parse_return(xml_bytes: bytes, object_id: str, source_zip: str) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    version = root.attrib.get("returnVersion")
    header = data = None
    for child in root:
        t = _strip_ns(child.tag)
        if t == "ReturnHeader":
            header = child
        elif t == "ReturnData":
            data = child
    if header is None or data is None:
        return []
    ein = _find_text(header, ("Filer/EIN",))
    tax_year = _find_text(header, ("TaxYr", "TaxYear"))
    period_end = _find_text(header, ("TaxPeriodEndDt", "TaxPeriodEndDate"))
    return_type = _find_text(header, ("ReturnTypeCd", "ReturnType"))
    filer_name = _find_text(header, ("Filer/BusinessName/BusinessNameLine1Txt",
                                     "Filer/Name/BusinessNameLine1",
                                     "Filer/BusinessName/BusinessNameLine1"))
    form = None
    for child in data:
        if _strip_ns(child.tag) == "IRS990":
            form = child
            break
    if form is None:
        return []
    rows = []
    seq = 0
    for grp in form:
        if _strip_ns(grp.tag) not in GROUP_TAGS:
            continue
        seq += 1
        row = {
            "EIN": ein, "TAX_YEAR": tax_year, "TAX_PERIOD_END": period_end,
            "OBJECT_ID": object_id, "RETURN_TYPE": return_type,
            "FILER_NAME": filer_name, "PERSON_SEQ": str(seq),
            "SCHEMA_VERSION": version, "SOURCE_ZIP": source_zip,
        }
        for col, tags in FIELD_MAP.items():
            row[col] = _find_text(grp, tags)
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Warehouse
# ---------------------------------------------------------------------------
_conn = None


def get_conn():
    global _conn
    if _conn is not None:
        try:
            _conn.cursor().execute("select 1")
            return _conn
        except Exception:
            try:
                _conn.close()
            except Exception:
                pass
            _conn = None
            print("    (snowflake session expired -- reconnecting)", flush=True)
    _conn = snow.connect()
    return _conn


def load_targets(refresh: bool = False) -> dict[str, dict]:
    """OBJECT_ID -> {ein, tax_period, name} for the hospital slice."""
    if TARGETS_FILE.exists() and not refresh:
        return json.loads(TARGETS_FILE.read_text())
    cur = get_conn().cursor()
    rows = cur.execute(SLICE_SQL).fetchall()
    cur.close()
    targets = {r[0]: {"ein": r[1], "tax_period": r[2], "name": r[3]} for r in rows}
    TARGETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TARGETS_FILE.write_text(json.dumps(targets))
    return targets


def landed_object_ids() -> set[str]:
    cur = get_conn().cursor()
    try:
        rows = cur.execute(
            f'select distinct OBJECT_ID from {bulk.LANDING_FQS}."{TABLE}"').fetchall()
    except Exception:
        return set()  # table does not exist yet
    finally:
        cur.close()
    return {r[0] for r in rows}


def upload(rows: list[dict], run_id: str):
    from snowflake.connector.pandas_tools import write_pandas
    df = pd.DataFrame(rows, columns=COLUMNS)
    df["INGESTED_AT"] = pd.Timestamp.utcnow().isoformat()
    df["_SOURCE_RUN_ID"] = run_id
    df = df.astype(object).where(pd.notna(df), None)
    for attempt in range(2):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cols_sql = ", ".join(f'"{c}" VARCHAR' for c in df.columns)
            cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{TABLE}" ({cols_sql})')
            cur.close()
            write_pandas(conn, df, TABLE, database=bulk.LANDING_DB,
                         schema=bulk.LANDING_SCHEMA, quote_identifiers=False,
                         auto_create_table=False)
            return
        except Exception as e:
            if attempt == 1 or ("390114" not in str(e) and "expired" not in str(e).lower()):
                raise
            global _conn
            _conn = None


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------
def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text())
    return {"zips_done": {}}


def save_checkpoint(cp: dict):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_FILE.write_text(json.dumps(cp, indent=1))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="land rows; default is a 20-return dry run")
    ap.add_argument("--years", nargs="*", help="only these zip years, e.g. 2024 2025")
    ap.add_argument("--refresh-targets", action="store_true")
    args = ap.parse_args()

    targets = load_targets(args.refresh_targets)
    wanted_years = sorted({o[:4] for o in targets})
    print(f"hospital slice: {len(targets):,} returns, "
          f"{len({t['ein'] for t in targets.values()}):,} EINs, "
          f"object-id years {wanted_years[0]}..{wanted_years[-1]}")

    urls = list_zip_urls()
    hosted_years = sorted({zip_year(u) for u in urls})
    unreachable = [y for y in wanted_years if y not in hosted_years]
    if unreachable:
        n = sum(1 for o in targets if o[:4] in unreachable)
        print(f"NOT HOSTED by the IRS: object-id years {unreachable}, {n:,} returns. "
              f"Those cannot be fetched.")
    if args.years:
        urls = [u for u in urls if zip_year(u) in set(args.years)]
    print(f"zips to scan: {len(urls)}")

    cp = load_checkpoint()
    done = landed_object_ids() if args.run else set()
    if done:
        print(f"already landed: {len(done):,} returns (skipped)")
    run_id = str(uuid.uuid4())

    buf: list[dict] = []
    n_returns = n_rows = n_empty = n_err = 0
    dry_left = DRY_RUN_RETURNS
    t0 = time.time()

    for url in urls:
        zname = url.rsplit("/", 1)[1]
        if args.run and zname in cp["zips_done"]:
            continue
        rf = RemoteFile(url)
        try:
            zf = zipfile.ZipFile(rf)
        except zipfile.BadZipFile as e:
            print(f"  [{zname}] unreadable: {e}")
            continue
        members = []
        for info in zf.infolist():
            oid = info.filename.rsplit("/", 1)[-1].split("_")[0]
            if oid in targets and oid not in done:
                members.append((oid, info))
        print(f"  [{zname}] {rf.size/1e9:.2f} GB, {len(zf.infolist()):,} members, "
              f"{len(members):,} hospital returns to pull", flush=True)
        if not members:
            if args.run:
                cp["zips_done"][zname] = 0
                save_checkpoint(cp)
            continue

        if not args.run:
            members = members[:dry_left]

        def work(item):
            oid, info = item
            try:
                return oid, parse_return(fetch_member(url, info), oid, zname), None
            except Exception as e:  # noqa: BLE001
                return oid, [], str(e)[:200]

        with concurrent.futures.ThreadPoolExecutor(FETCH_WORKERS) as ex:
            for oid, rows, err in ex.map(work, members):
                n_returns += 1
                if err:
                    n_err += 1
                    print(f"    ERR {oid}: {err}")
                    continue
                if not rows:
                    n_empty += 1
                buf.extend(rows)
                n_rows += len(rows)
                if not args.run:
                    for r in rows:
                        print(f"    {r['EIN']} {r['TAX_YEAR']} {r['OBJECT_ID']} | "
                              f"{r['PERSON_NAME']} | {r['TITLE']} | hrs {r['AVG_HOURS_PER_WEEK']} | "
                              f"org {r['REPORTABLE_COMP_FROM_ORG']} rel {r['REPORTABLE_COMP_FROM_RELATED_ORGS']} "
                              f"other {r['OTHER_COMPENSATION']}")
                if n_returns % PROGRESS_EVERY == 0:
                    rate = n_returns / (time.time() - t0)
                    print(f"    {n_returns:,} returns, {n_rows:,} rows, "
                          f"{n_empty} empty, {n_err} errors, {rate:.1f} ret/s", flush=True)
                if args.run and len(buf) >= FLUSH_ROWS:
                    upload(buf, run_id)
                    print(f"    flushed {len(buf):,} rows", flush=True)
                    buf = []

        if args.run:
            if buf:
                upload(buf, run_id)
                print(f"    flushed {len(buf):,} rows", flush=True)
                buf = []
            cp["zips_done"][zname] = len(members)
            save_checkpoint(cp)
        else:
            dry_left -= len(members)
            if dry_left <= 0:
                break

    print(f"\n{'dry run' if not args.run else 'run'}: {n_returns:,} returns parsed, "
          f"{n_rows:,} person rows, {n_empty} returns with no Part VII rows, "
          f"{n_err} fetch/parse errors, {time.time()-t0:.0f}s")
    if not args.run:
        print("(dry run -- add --run to land)")
        return

    total_landed = len(landed_object_ids())
    print(f"landed returns now in {TABLE}: {total_landed:,} of {len(targets):,} targets")
    passed, report = bulk.run_quality_gate(
        get_conn(), SOURCE_ID, TABLE, run_id, row_count=n_rows, source_url=DOWNLOADS_PAGE)
    if not passed:
        print(f"QUALITY GATE FAILED {TABLE}: {report}")
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
