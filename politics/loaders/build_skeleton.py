"""Phase 1 -- THE SKELETON: identifier crosswalk + member spine + ideology.

Builds, end to end and ADDITIVELY (new POLITICS schemas only):

  RAW (land via the shared ingest helpers -- first-class, density-gated, logged):
    LIBRARY_RAW.LANDING.FED_CONGRESS_LEGISLATORS   (current+historical+executive, denormalized)
    LIBRARY_RAW.LANDING.FED_VOTEVIEW_MEMBERS       (HSall_members.csv, member-by-congress ideology)

  STAGING (views, LIBRARY_STAGING.POLITICS):
    STG_FED_CONGRESS_LEGISLATORS__MEMBERS
    STG_FED_VOTEVIEW_MEMBERS__IDEOLOGY

  MARTS (tables, LIBRARY_MARTS.POLITICS):
    POLITICS__MEMBER_CROSSWALK   one row per member, keyed on bioguide, every alt ID  [Deliverable #1]
    POLITICS__MEMBER_FEC_ID      one row per (bioguide, fec_id) -- fec is 1:many       [Deliverable #1 bridge]
    POLITICS__MEMBER_SPINE       bioguide-keyed member + DW-NOMINATE ideology          [Deliverable #2]

Safety: only CREATEs new POLITICS schemas + new tables/views + new LANDING tables.
Touches no existing object. CREATE OR REPLACE is scoped to this domain's own objects.

Usage:
  python politics/loaders/build_skeleton.py            # fetch + land + build (idempotent)
  python politics/loaders/build_skeleton.py --skip-fetch  # rebuild marts from existing landing only
"""
from __future__ import annotations
import datetime as dt
import hashlib
import io
import json
import sys
import uuid

import pandas as pd
import requests
import yaml

sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
import ingest  # noqa: E402  (reuse _stringify/_load_landing/_log_run/assess_density)
import snow    # noqa: E402

GH = "https://raw.githubusercontent.com/unitedstates/congress-legislators/main"
LEG_FILES = {
    "current": f"{GH}/legislators-current.yaml",
    "historical": f"{GH}/legislators-historical.yaml",
    "executive": f"{GH}/executive.yaml",
}
VOTEVIEW_URL = "https://voteview.com/static/data/out/members/HSall_members.csv"

# Columns we pull out of each legislator record (the id crosswalk + bio + last term).
_ID_FIELDS = ["bioguide", "icpsr", "thomas", "lis", "govtrack", "opensecrets", "votesmart",
              "cspan", "house_history", "ballotpedia", "maplight", "wikidata", "wikipedia",
              "google_entity_id"]


def _flatten_member(m: dict, setname: str) -> dict:
    idb = m.get("id", {}) or {}
    name = m.get("name", {}) or {}
    bio = m.get("bio", {}) or {}
    terms = m.get("terms", []) or []
    last = terms[-1] if terms else {}
    first = terms[0] if terms else {}
    fec = idb.get("fec", []) or []
    row = {f.upper(): ("" if idb.get(f) is None else str(idb.get(f))) for f in _ID_FIELDS}
    row.update({
        "LEGISLATOR_SET": setname,
        "FEC_IDS": json.dumps([str(x) for x in fec]),  # preserve the 1:many list
        "NAME_FIRST": str(name.get("first", "") or ""),
        "NAME_LAST": str(name.get("last", "") or ""),
        "NAME_OFFICIAL_FULL": str(name.get("official_full", "") or ""),
        "BIRTHDAY": str(bio.get("birthday", "") or ""),
        "GENDER": str(bio.get("gender", "") or ""),
        "TERM_TYPE": str(last.get("type", "") or ""),
        "PARTY": str(last.get("party", "") or ""),
        "STATE": str(last.get("state", "") or ""),
        "DISTRICT": "" if last.get("district") is None else str(last.get("district")),
        "SENATE_CLASS": "" if last.get("class") is None else str(last.get("class")),
        "TERM_START": str(first.get("start", "") or ""),
        "TERM_END": str(last.get("end", "") or ""),
        "N_TERMS": str(len(terms)),
    })
    return row


def fetch_legislators():
    rows, raw_parts = [], []
    for setname, url in LEG_FILES.items():
        r = requests.get(url, timeout=180)
        r.raise_for_status()
        raw_parts.append(r.content)
        data = yaml.safe_load(r.content) or []
        for m in data:
            rows.append(_flatten_member(m, setname))
        print(f"  fetched {setname:<11} {len(data):>6} members ({len(r.content):,} bytes)")
    df = pd.DataFrame(rows)
    return df, b"\n".join(raw_parts)


def fetch_voteview():
    r = requests.get(VOTEVIEW_URL, timeout=180)
    r.raise_for_status()
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, keep_default_na=False)
    df.columns = [c.upper() for c in df.columns]
    print(f"  fetched voteview members {len(df):>6} rows, cols={list(df.columns)[:6]}...")
    return df, r.content


def land(df: pd.DataFrame, source_id: str, url: str, message: str) -> dict:
    """Land a frame exactly like the onboarding agent: TEXT mirror + provenance
    stamps + INGEST_RUNS row + density gate. Snapshot-replace (idempotent)."""
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc)
    table = source_id.upper()
    payload = df.to_csv(index=False).encode("utf-8")
    sha = hashlib.sha256(payload).hexdigest()
    out = ingest._stringify(df.copy())
    out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
    out[ingest.META_SOURCE_RUN_ID] = run_id
    out[ingest.META_SRC_SHA256] = sha
    conn = snow.connect()
    try:
        ingest._load_landing(conn, out, table, overwrite=True)
        ended = dt.datetime.now(dt.timezone.utc)
        density = ingest.assess_density(out)
        status = "empty" if density["empty"] else "success"
        ingest._log_run(conn, source_id, run_id, status, len(out), len(payload), sha, url,
                        started, ended, f"{message} {ingest._density_note(density)}.")
    finally:
        conn.close()
    print(f"  landed {table:<28} {len(out):>6} rows  status={status}  "
          f"density={density['populated_fraction']:.1%}")
    return {"rows": len(out), "status": status, "density": density["populated_fraction"]}


# ---------------------------------------------------------------------------
# Staging views + marts (additive: new POLITICS schemas / objects only)
# ---------------------------------------------------------------------------
DDL = [
("schema staging", "CREATE SCHEMA IF NOT EXISTS LIBRARY_STAGING.POLITICS"),
("schema marts",   "CREATE SCHEMA IF NOT EXISTS LIBRARY_MARTS.POLITICS"),

("stg legislators", """
CREATE OR REPLACE VIEW LIBRARY_STAGING.POLITICS.STG_FED_CONGRESS_LEGISLATORS__MEMBERS AS
SELECT
  NULLIF(TRIM(BIOGUIDE),'')                        AS bioguide,
  TRY_TO_NUMBER(NULLIF(TRIM(ICPSR),''))            AS icpsr,
  NULLIF(TRIM(GOVTRACK),'')                        AS govtrack,
  NULLIF(TRIM(OPENSECRETS),'')                     AS opensecrets,
  NULLIF(TRIM(VOTESMART),'')                       AS votesmart,
  NULLIF(TRIM(LIS),'')                             AS lis,
  NULLIF(TRIM(THOMAS),'')                          AS thomas,
  NULLIF(TRIM(CSPAN),'')                           AS cspan,
  NULLIF(TRIM(WIKIDATA),'')                        AS wikidata,
  NULLIF(TRIM(BALLOTPEDIA),'')                     AS ballotpedia,
  NULLIF(TRIM(WIKIPEDIA),'')                       AS wikipedia,
  NULLIF(TRIM(HOUSE_HISTORY),'')                   AS house_history,
  NULLIF(TRIM(MAPLIGHT),'')                        AS maplight,
  NULLIF(TRIM(GOOGLE_ENTITY_ID),'')                AS google_entity_id,
  TRY_PARSE_JSON(FEC_IDS)                          AS fec_ids,
  NULLIF(TRIM(NAME_FIRST),'')                      AS name_first,
  NULLIF(TRIM(NAME_LAST),'')                       AS name_last,
  COALESCE(NULLIF(TRIM(NAME_OFFICIAL_FULL),''),
           NULLIF(TRIM(NAME_FIRST||' '||NAME_LAST),'')) AS full_name,
  NULLIF(TRIM(BIRTHDAY),'')                        AS birthday,
  NULLIF(TRIM(GENDER),'')                          AS gender,
  NULLIF(TRIM(TERM_TYPE),'')                       AS last_term_type,
  NULLIF(TRIM(PARTY),'')                           AS last_party,
  NULLIF(TRIM(STATE),'')                           AS last_state,
  NULLIF(TRIM(DISTRICT),'')                        AS last_district,
  NULLIF(TRIM(SENATE_CLASS),'')                    AS senate_class,
  NULLIF(TRIM(TERM_START),'')                      AS first_term_start,
  NULLIF(TRIM(TERM_END),'')                        AS last_term_end,
  TRY_TO_NUMBER(NULLIF(TRIM(N_TERMS),''))          AS n_terms,
  LEGISLATOR_SET                                   AS legislator_set
FROM LIBRARY_RAW.LANDING.FED_CONGRESS_LEGISLATORS
"""),

("stg voteview", """
CREATE OR REPLACE VIEW LIBRARY_STAGING.POLITICS.STG_FED_VOTEVIEW_MEMBERS__IDEOLOGY AS
SELECT
  TRY_TO_NUMBER(NULLIF(TRIM(ICPSR),''))            AS icpsr,
  NULLIF(TRIM(BIOGUIDE_ID),'')                     AS bioguide_id,
  TRY_TO_NUMBER(NULLIF(TRIM(CONGRESS),''))         AS congress,
  NULLIF(TRIM(CHAMBER),'')                         AS chamber,
  NULLIF(TRIM(PARTY_CODE),'')                      AS party_code,
  NULLIF(TRIM(STATE_ABBREV),'')                    AS state_abbrev,
  TRY_TO_DOUBLE(NULLIF(TRIM(NOMINATE_DIM1),''))    AS nominate_dim1,
  TRY_TO_DOUBLE(NULLIF(TRIM(NOMINATE_DIM2),''))    AS nominate_dim2,
  NULLIF(TRIM(BIONAME),'')                         AS bioname
FROM LIBRARY_RAW.LANDING.FED_VOTEVIEW_MEMBERS
"""),

("mart crosswalk", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK AS
SELECT
  COALESCE(bioguide, 'gt:'||govtrack, 'os:'||opensecrets, 'name:'||full_name) AS member_key,
  bioguide, icpsr, govtrack, opensecrets, votesmart, lis, thomas, cspan, wikidata,
  ballotpedia, wikipedia, house_history, maplight, google_entity_id,
  fec_ids,
  full_name, name_first, name_last, birthday, gender,
  last_term_type, last_party, last_state, last_district, senate_class,
  first_term_start, last_term_end, n_terms, legislator_set
FROM LIBRARY_STAGING.POLITICS.STG_FED_CONGRESS_LEGISLATORS__MEMBERS
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY COALESCE(bioguide, 'gt:'||govtrack, 'os:'||opensecrets, 'name:'||full_name)
  ORDER BY CASE legislator_set WHEN 'current' THEN 1 WHEN 'historical' THEN 2 ELSE 3 END
) = 1
"""),

("mart fec bridge", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID AS
SELECT
  x.member_key,
  x.bioguide,
  f.value::string        AS fec_id,
  x.full_name,
  x.last_party           AS party,
  x.last_state           AS state,
  x.last_term_type
FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK x,
     LATERAL FLATTEN(input => x.fec_ids) f
WHERE NULLIF(TRIM(f.value::string),'') IS NOT NULL
"""),

("mart spine", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE AS
WITH vv AS (
  SELECT icpsr, bioguide_id, congress, chamber, party_code, state_abbrev,
         nominate_dim1, nominate_dim2, bioname,
         ROW_NUMBER() OVER (PARTITION BY icpsr ORDER BY congress DESC NULLS LAST) AS rn
  FROM LIBRARY_STAGING.POLITICS.STG_FED_VOTEVIEW_MEMBERS__IDEOLOGY
  WHERE icpsr IS NOT NULL
)
SELECT
  x.member_key,
  x.bioguide,
  x.icpsr,
  x.full_name,
  x.last_party        AS party,
  x.last_state        AS state,
  x.last_term_type,
  x.senate_class,
  x.n_terms,
  x.first_term_start,
  x.last_term_end,
  x.legislator_set,
  v.nominate_dim1     AS dw_nominate_dim1,
  v.nominate_dim2     AS dw_nominate_dim2,
  v.congress          AS latest_voteview_congress,
  v.chamber           AS voteview_chamber,
  CASE
    WHEN v.nominate_dim1 IS NULL THEN 'unknown'
    WHEN v.nominate_dim1 < 0     THEN 'left/liberal'
    WHEN v.nominate_dim1 > 0     THEN 'right/conservative'
    ELSE 'centrist'
  END                 AS ideology_label,
  (v.icpsr IS NOT NULL)         AS has_voteview_match,  -- matched a Voteview member row
  (v.nominate_dim1 IS NOT NULL) AS has_ideology         -- carries a USABLE DW-NOMINATE score
FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK x
LEFT JOIN vv v ON v.rn = 1 AND v.icpsr = x.icpsr
"""),
]


def build_models():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        for label, sql in DDL:
            cur.execute(sql)
            print(f"  built {label}")
        conn.commit()
        # quick counts + integrity
        checks = {
            "crosswalk_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK",
            "crosswalk_distinct_bioguide": "SELECT COUNT(DISTINCT bioguide) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK WHERE bioguide IS NOT NULL",
            "crosswalk_null_bioguide": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK WHERE bioguide IS NULL",
            "crosswalk_dupe_bioguide": "SELECT COUNT(*) FROM (SELECT bioguide FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK WHERE bioguide IS NOT NULL GROUP BY bioguide HAVING COUNT(*)>1)",
            "fec_bridge_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID",
            "fec_bridge_members": "SELECT COUNT(DISTINCT member_key) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID",
            "spine_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE",
            "spine_with_ideology": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE WHERE has_ideology",
        }
        print("\nINTEGRITY:")
        for k, q in checks.items():
            cur.execute(q)
            print(f"  {k:<32} {cur.fetchone()[0]:,}")
    finally:
        cur.close()
        conn.close()


def main(skip_fetch: bool):
    if not skip_fetch:
        print("FETCH + LAND:")
        leg_df, _ = fetch_legislators()
        land(leg_df, "fed_congress_legislators", LEG_FILES["current"],
             "unitedstates/congress-legislators (current+historical+executive); one row = one legislator.")
        vv_df, _ = fetch_voteview()
        land(vv_df, "fed_voteview_members", VOTEVIEW_URL,
             "Voteview HSall_members ideology; one row = one member-congress.")
    print("\nBUILD MODELS (staging views + marts):")
    build_models()
    print("\nDONE.")


if __name__ == "__main__":
    main(skip_fetch="--skip-fetch" in sys.argv)
