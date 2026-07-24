-- Server-side bulk ingestion (move GB-scale pours off the laptop).
-- Snowflake fetches source URLs directly on its own compute (cloud-to-cloud),
-- lands the raw file in an internal stage, then a loader COPYs it into the
-- all-TEXT landing table. Bandwidth stops being the wall.
--
-- Plan: .snowflake/cortex/plans/server-side-bulk-ingest.plan.md
-- Every object here is independently DROP-able (see teardown at the bottom).

-- 1. EGRESS network rule -- egress ONLY to the listed government data hosts.
--    Add a host here (and re-create the integration is NOT needed; the rule is
--    referenced by name) before fetching from a new domain.
CREATE OR REPLACE NETWORK RULE LIBRARY_RAW.LANDING.RIPPLE_BULK_EGRESS
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    'files.consumerfinance.gov',   -- CFPB complaints (1.4 GB zip)
    'leidata.gleif.org',           -- GLEIF LEI golden copy (legacy host)
    'goldencopy.gleif.org',        -- GLEIF golden copy metadata API + file storage
    'www.sec.gov',                 -- SEC EDGAR data sets
    'www.irs.gov',                 -- IRS SOI / EO BMF / revocation
    'apps.irs.gov',                -- IRS apps (revocation download)
    'www.fec.gov',                 -- FEC bulk
    'echo.epa.gov',                -- EPA ECHO
    'download.cms.gov',            -- CMS bulk (NPPES, Part D, etc.)
    'data.cms.gov',                -- CMS provider-data metastore + CSVs
    'static.nhtsa.gov',            -- NHTSA recalls/complaints/FARS flat files (harm)
    'data.transportation.gov',     -- USDOT/NHTSA Socrata flat-file exports (harm)
    'enforcedata.dol.gov',         -- DOL enforcement: OSHA + WHD wage-theft + MSHA (harm)
    'arlweb.msha.gov',             -- MSHA mine safety open data (harm)
    'download.open.fda.gov',       -- openFDA drug/device enforcement + adverse events (harm)
    'files.usaspending.gov',       -- USASpending award archives + subawards (spending)
    's3.amazonaws.com',            -- AWS public datasets (path-style)
    'irs-form-990.s3.amazonaws.com' -- IRS 990 e-file index/returns (virtual-hosted S3; dark money)
  )
  COMMENT = 'Ripple server-side bulk ingest: egress only to listed government data hosts';

-- 2. External Access Integration referencing the egress rule. ACCOUNTADMIN-owned.
--    (A SECRET slot can be added later for keyed sources like SAM.)
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION RIPPLE_BULK_ACCESS
  ALLOWED_NETWORK_RULES = (LIBRARY_RAW.LANDING.RIPPLE_BULK_EGRESS)
  ENABLED = TRUE
  COMMENT = 'Ripple server-side bulk fetch: egress to government data hosts only (scoped by RIPPLE_BULK_EGRESS)';

-- 3. Internal stage the proc streams files into. Directory table on for listing.
CREATE STAGE IF NOT EXISTS LIBRARY_RAW.LANDING.BULK_STAGE
  DIRECTORY = (ENABLE = TRUE)
  COMMENT = 'Server-side bulk ingest landing stage (RIPPLE_FETCH_TO_STAGE)';

-- 3b. Raw-mirror CSV file format: parse the header, keep every value as TEXT, no
--     NA coercion. Used by the loader with MATCH_BY_COLUMN_NAME + INFER_SCHEMA.
CREATE FILE FORMAT IF NOT EXISTS LIBRARY_RAW.LANDING.BULK_CSV_TEXT
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  TRIM_SPACE = FALSE
  REPLACE_INVALID_CHARACTERS = TRUE
  ENCODING = 'UTF8'
  ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
  EMPTY_FIELD_AS_NULL = FALSE
  COMMENT = 'Raw-mirror CSV: parse header, keep everything as text, no NA coercion.';

-- 4. RIPPLE_FETCH_TO_STAGE(url, stage_path): stream a URL into BULK_STAGE on
--    Snowflake's own compute. Downloads to /tmp in bounded 1 MB chunks (peak
--    memory ~one chunk) then PUTs the seekable file. Returns a JSON summary.
--    (put_stream can't take requests' non-seekable raw stream, hence the temp file.)
CREATE OR REPLACE PROCEDURE LIBRARY_RAW.LANDING.RIPPLE_FETCH_TO_STAGE(URL STRING, STAGE_PATH STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  PACKAGES = ('snowflake-snowpark-python', 'requests')
  HANDLER = 'fetch'
  EXTERNAL_ACCESS_INTEGRATIONS = (RIPPLE_BULK_ACCESS)
  COMMENT = 'Stream a source URL directly into LIBRARY_RAW.LANDING.BULK_STAGE (cloud-to-cloud, no laptop hop).'
AS
$$
import json
import gzip
import os
import tempfile
import requests

# A descriptive UA with a contact -- several gov hosts (SEC especially) 403 a
# bare/absent User-Agent. Never spoof a browser we are not.
_UA = {"User-Agent": "Ripple accountability-data ingest (contact w.rogers9999@gmail.com)"}


def fetch(session, url, stage_path):
    # Stream the download to a local temp file in bounded 1 MB chunks (peak memory
    # is ~one chunk, not the whole file) then PUT the seekable file to the stage.
    # (put_stream needs a seekable stream; requests' raw response is not seekable.)
    # If stage_path ends in .gz, gzip ON THE FLY: a big raw CSV (~10GB) overflows the
    # Python /tmp sandbox, but its .gz (~2GB) fits, and COPY reads .gz natively.
    stage_path = str(stage_path).lstrip("/")
    basename = os.path.basename(stage_path) or "download.bin"
    stage_dir = os.path.dirname(stage_path)
    target_dir = "@LIBRARY_RAW.LANDING.BULK_STAGE/" + stage_dir
    compress = basename.endswith(".gz")
    tmpdir = tempfile.mkdtemp()
    local_path = os.path.join(tmpdir, basename)  # keep desired name; PUT preserves basename

    total = 0
    with requests.get(url, headers=_UA, stream=True, timeout=1800, allow_redirects=True) as r:
        r.raise_for_status()
        http_status = r.status_code
        etag = r.headers.get("ETag", "")
        last_modified = r.headers.get("Last-Modified", "")
        fh = gzip.open(local_path, "wb", compresslevel=1) if compress else open(local_path, "wb")
        with fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
                    total += len(chunk)

    res = session.file.put(local_path, target_dir, auto_compress=False, overwrite=True)
    r0 = res[0] if isinstance(res, list) and res else res
    return json.dumps({
        "url": url,
        "target": target_dir.rstrip("/") + "/" + basename,
        "http_status": http_status,
        "bytes_downloaded": total,
        "etag": etag,                 # origin content fingerprint (stable across re-fetch)
        "last_modified": last_modified,
        "target_size": getattr(r0, "target_size", None),
        "put_status": getattr(r0, "status", None),
    })
$$;

-- 5. RIPPLE_UNZIP_MEMBER_TO_STAGE(zip_path, member_pattern, out_path): COPY does
--    NOT read .zip. Read the staged zip via SnowflakeFile (seekable -> zipfile can
--    read the central directory), stream the chosen member recompressed to a .gz
--    (COPY reads .gz natively) back into BULK_STAGE. member_pattern '' => largest
--    member. Reads the zip lazily from the stage, so peak local disk ~= the .gz.
CREATE OR REPLACE PROCEDURE LIBRARY_RAW.LANDING.RIPPLE_UNZIP_MEMBER_TO_STAGE(
  ZIP_STAGE_PATH STRING, MEMBER_PATTERN STRING, OUT_STAGE_PATH STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'unzip'
  COMMENT = 'Read a staged .zip via SnowflakeFile (seekable), stream the chosen member recompressed to .gz back into BULK_STAGE so COPY can read it (COPY does not read .zip).'
AS
$$
import gzip
import json
import os
import re
import shutil
import tempfile
import zipfile
from snowflake.snowpark.files import SnowflakeFile


def unzip(session, zip_stage_path, member_pattern, out_stage_path):
    zip_stage_path = str(zip_stage_path).lstrip("/")
    out_stage_path = str(out_stage_path).lstrip("/")
    if "'" in zip_stage_path or "'" in out_stage_path:
        raise ValueError("stage paths must not contain single quotes")

    scoped = session.sql(
        "SELECT BUILD_SCOPED_FILE_URL(@LIBRARY_RAW.LANDING.BULK_STAGE, '"
        + zip_stage_path + "')").collect()[0][0]

    out_name = os.path.basename(out_stage_path)
    out_dir = "@LIBRARY_RAW.LANDING.BULK_STAGE/" + os.path.dirname(out_stage_path)
    tmpdir = tempfile.mkdtemp()
    local_gz = os.path.join(tmpdir, out_name)

    chosen = None
    member_bytes = 0
    with SnowflakeFile.open(scoped, "rb", require_scoped_url=True) as sf:
        with zipfile.ZipFile(sf) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            if not names:
                raise RuntimeError("zip has no file members")
            cand = names
            if member_pattern:
                rx = re.compile(member_pattern, re.I)
                cand = [n for n in names if rx.search(n)] or names
            chosen = max(cand, key=lambda n: zf.getinfo(n).file_size)
            member_bytes = zf.getinfo(chosen).file_size
            with zf.open(chosen, "r") as src, gzip.open(local_gz, "wb", compresslevel=1) as gz:
                shutil.copyfileobj(src, gz, length=1 << 20)

    gz_bytes = os.path.getsize(local_gz)
    res = session.file.put(local_gz, out_dir, auto_compress=False, overwrite=True)
    r0 = res[0] if isinstance(res, list) and res else res
    return json.dumps({
        "zip": zip_stage_path,
        "chosen_member": chosen,
        "member_uncompressed_bytes": member_bytes,
        "gz_bytes": gz_bytes,
        "target": out_dir.rstrip("/") + "/" + out_name,
        "put_status": getattr(r0, "status", None),
    })
$$;

-- 6. KEYED FETCH (Phase 2): close the auth-key gap for public APIs (e.g. data.gov's
--    free api_key). A GENERIC_STRING secret holds the key; the integration must allow
--    it; the proc injects it as a query param (?PARAM_NAME=key) or a header. To
--    activate: ALTER the secret's SECRET_STRING to a real key, then give the source
--    spec an `auth = {style, param}`. Openflow remains the heavier option for true
--    SaaS/DB CDC; this keyed path covers the common public-API-key case cheaply.
CREATE SECRET IF NOT EXISTS LIBRARY_RAW.LANDING.RIPPLE_API_KEY
  TYPE = GENERIC_STRING
  SECRET_STRING = 'REPLACE_ME'
  COMMENT = 'Shared API key for RIPPLE_FETCH_TO_STAGE_KEYED. Replace REPLACE_ME to activate.';

ALTER EXTERNAL ACCESS INTEGRATION RIPPLE_BULK_ACCESS
  SET ALLOWED_AUTHENTICATION_SECRETS = (LIBRARY_RAW.LANDING.RIPPLE_API_KEY);

CREATE OR REPLACE PROCEDURE LIBRARY_RAW.LANDING.RIPPLE_FETCH_TO_STAGE_KEYED(
  URL STRING, STAGE_PATH STRING, AUTH_STYLE STRING, PARAM_NAME STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  PACKAGES = ('snowflake-snowpark-python', 'requests')
  HANDLER = 'fetch'
  EXTERNAL_ACCESS_INTEGRATIONS = (RIPPLE_BULK_ACCESS)
  SECRETS = ('api_key' = LIBRARY_RAW.LANDING.RIPPLE_API_KEY)
  COMMENT = 'Like RIPPLE_FETCH_TO_STAGE but injects the RIPPLE_API_KEY secret (AUTH_STYLE = query|header).'
AS
$$
import json
import os
import tempfile
import _snowflake
import requests

_UA = {"User-Agent": "Ripple accountability-data ingest (contact w.rogers9999@gmail.com)"}


def fetch(session, url, stage_path, auth_style, param_name):
    key = _snowflake.get_generic_secret_string('api_key')
    headers = dict(_UA)
    if str(auth_style).lower() == 'query':
        sep = '&' if '?' in url else '?'
        url = f"{url}{sep}{param_name}={key}"
    else:
        headers[param_name] = key

    stage_path = str(stage_path).lstrip("/")
    basename = os.path.basename(stage_path) or "download.bin"
    target_dir = "@LIBRARY_RAW.LANDING.BULK_STAGE/" + os.path.dirname(stage_path)
    tmpdir = tempfile.mkdtemp()
    local_path = os.path.join(tmpdir, basename)

    total = 0
    with requests.get(url, headers=headers, stream=True, timeout=1800, allow_redirects=True) as r:
        r.raise_for_status()
        http_status = r.status_code
        with open(local_path, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
                    total += len(chunk)

    res = session.file.put(local_path, target_dir, auto_compress=False, overwrite=True)
    r0 = res[0] if isinstance(res, list) and res else res
    return json.dumps({
        "target": target_dir.rstrip("/") + "/" + basename,
        "http_status": http_status,
        "bytes_downloaded": total,
        "put_status": getattr(r0, "status", None),
    })
$$;

-- Teardown (reversibility):
--   DROP PROCEDURE IF EXISTS LIBRARY_RAW.LANDING.RIPPLE_FETCH_TO_STAGE_KEYED(STRING, STRING, STRING, STRING);
--   DROP SECRET    IF EXISTS LIBRARY_RAW.LANDING.RIPPLE_API_KEY;
--   DROP PROCEDURE IF EXISTS LIBRARY_RAW.LANDING.RIPPLE_UNZIP_MEMBER_TO_STAGE(STRING, STRING, STRING);
--   DROP PROCEDURE IF EXISTS LIBRARY_RAW.LANDING.RIPPLE_FETCH_TO_STAGE(STRING, STRING);
--   DROP FILE FORMAT IF EXISTS LIBRARY_RAW.LANDING.BULK_CSV_TEXT;
--   DROP STAGE     IF EXISTS LIBRARY_RAW.LANDING.BULK_STAGE;
--   DROP INTEGRATION IF EXISTS RIPPLE_BULK_ACCESS;
--   DROP NETWORK RULE IF EXISTS LIBRARY_RAW.LANDING.RIPPLE_BULK_EGRESS;
