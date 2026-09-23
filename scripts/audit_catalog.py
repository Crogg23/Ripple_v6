"""Catalog audit: is the map of the warehouse telling the truth?

Read-only. Grades the MAP of LIBRARY_MARTS, not the data inside it
(that is scripts/score_warehouse.py, the DATA score).

Stages, each cached so later stages re-run without touching the warehouse:

  fetch    inventory from information_schema, a 2,000-row sample of every
           table, COUNT(*) on every view, the timeline registry, word coverage
  links    for every hard-ID column that passes its format check, the full
           list of distinct cleaned values, so table-to-table overlap is exact
  analyze  all checks, local only; writes audit/catalog_audit_<date>.md + .tsv
  catalog  the verified catalog: outputs/catalog/catalog.json and er.json

  python scripts/audit_catalog.py fetch
  python scripts/audit_catalog.py links
  python scripts/audit_catalog.py analyze
  python scripts/audit_catalog.py catalog

Sample caveat: LIMIT reads the first stored blocks, so a sample leans toward
whichever rows were loaded first. Good enough for "is this column an NPI";
not good enough for fill rates on tables loaded in pieces.
"""

from __future__ import annotations

import collections
import csv
import datetime as dt
import glob
import gzip
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from connect import keys  # noqa: E402

CACHE = REPO / "outputs" / "_catalog_audit_cache"
OUT = REPO / "audit"
SKIP = ("INFORMATION_SCHEMA", "TIMELINE", "_RESTORE_20260907", "REVIEW", "PUBLIC")
SAMPLE_N = 2000
TODAY = dt.date.today().isoformat()

# The throwaway regex tagger behind outputs/catalog/catalog.json, copied
# verbatim from session e8dc9438 so its tags can be graded next to the real ones.
REGEX_KEYS = [
    ("NPI", r"^(PRSCRBR_)?NPI$|_NPI$|^NPI_"),
    ("CCN", r"CCN$|^CMS_CERTIFICATION_NUMBER|PROVIDER_CCN|^CCN_"),
    ("EIN", r"^EIN$|_EIN$|^SPONS_DFE_EIN$"),
    ("CIK", r"^CIK$|_CIK$|ISSUER_CIK"),
    ("LEI", r"^LEI$|_LEI$"),
    ("UEI/DUNS", r"^UEI$|_UEI$|DUNS"),
    ("ACCESSION", r"ACCESSION"),
    ("FDIC_CERT", r"^CERT$|FDIC_CERT"),
    ("FEC_ID", r"^CMTE_ID$|^CAND_ID$|^SUB_ID$"),
    ("BIOGUIDE", r"BIOGUIDE"),
    ("IMO", r"IMO_NUMBER"),
    ("FRS/EPA", r"REGISTRY_ID|^FRS_ID|NPDES|^EPA_"),
    ("MINE_ID", r"MINE_ID"),
    ("COUNTY_FIPS", r"FIPS"),
    ("ZIP", r"^ZIP|_ZIP$|ZIP_CODE|POSTAL"),
    ("STATE", r"^STATE$|_STATE$|STATE_CODE|STPR"),
    ("ORG_NAME", r"NAME$|^NAME_|SPONSOR_NAME|ISSUER_NAME|FACILITY"),
]


def regex_tag(col: str) -> str | None:
    for name, pat in REGEX_KEYS:
        if re.search(pat, col):
            return name
    return None


def real_tag(table: str, col: str) -> tuple[str | None, str | None]:
    """The platform tagger as the catalog uses it: engine table keys, catalog-only
    keys, name tokens, then What codes (connect/keys.py catalog_key)."""
    return keys.catalog_key(table, col)


# --------------------------------------------------------------------------- #
# Value shapes. Each returns True when one non-empty value looks like the key.
# --------------------------------------------------------------------------- #
def _luhn_ok(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


def is_npi(v: str) -> bool:
    v = v.strip()
    if v.endswith(".0"):
        v = v[:-2]
    return bool(re.fullmatch(r"[12]\d{9}", v)) and _luhn_ok("80840" + v)


def is_dea(v: str) -> bool:
    v = v.strip().upper()
    m = re.fullmatch(r"[A-Z][A-Z9](\d{7})", v)
    if not m:
        return False
    d = [int(c) for c in m.group(1)]
    return (d[0] + d[2] + d[4] + 2 * (d[1] + d[3] + d[5])) % 10 == d[6]


def is_ein(v: str) -> bool:
    s = re.sub(r"[^0-9]", "", v)
    if v.strip().endswith(".0"):
        s = s[:-1]
    return 7 <= len(s) <= 9 and s.strip("0") != "" and re.fullmatch(r"[0-9\- .]+", v.strip()) is not None


def is_ccn(v: str) -> bool:
    return bool(re.fullmatch(r"\d{2}[0-9A-Z]\d{3}", v.strip().upper().zfill(6)))


def is_fips5(v: str) -> bool:
    s = v.strip()
    if s.endswith(".0"):
        s = s[:-2]
    return bool(re.fullmatch(r"\d{4,5}", s)) and 1 <= int(s.zfill(5)[:2]) <= 78


def fips_level(v: str) -> str | None:
    """State 2, county 5, tract 11, block group 12, block 15 digits."""
    s = v.strip()
    if s.endswith(".0"):
        s = s[:-2]
    if not s.isdigit():
        return None
    return {1: "state", 2: "state", 3: "county part, no state", 4: "county", 5: "county", 10: "tract", 11: "tract",
            12: "block group", 15: "block"}.get(len(s))


def is_any_fips(v: str) -> bool:
    """A usable FIPS on its own. A bare 3-digit county part is not: it repeats in every state."""
    return fips_level(v) not in (None, "county part, no state")


def is_zip(v: str) -> bool:
    return bool(re.fullmatch(r"\d{5}(-?\d{4})?|\d{9}", v.strip()))


def is_cik(v: str) -> bool:
    s = v.strip()
    if s.endswith(".0"):
        s = s[:-2]
    return bool(re.fullmatch(r"\d{1,10}", s)) and int(s) > 0


def is_uei(v: str) -> bool:
    return bool(re.fullmatch(r"[A-HJ-NP-Z1-9][A-HJ-NP-Z0-9]{11}", v.strip().upper()))


def is_duns(v: str) -> bool:
    return bool(re.fullmatch(r"\d{9}", v.strip()))


def is_lei(v: str) -> bool:
    s = v.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{18}\d{2}", s):
        return False
    num = "".join(str(int(c, 36)) for c in s)
    return int(num) % 97 == 1


def is_fec_cmte(v: str) -> bool:
    return bool(re.fullmatch(r"C\d{8}", v.strip().upper()))


def is_fec_cand(v: str) -> bool:
    return bool(re.fullmatch(r"[HSP][0-9][0-9A-Z]{2}\d{5}", v.strip().upper()))


def is_bioguide(v: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]\d{6}", v.strip().upper()))


def is_imo(v: str) -> bool:
    s = re.sub(r"^IMO", "", v.strip().upper())
    if not re.fullmatch(r"\d{7}", s):
        return False
    return sum(int(s[i]) * (7 - i) for i in range(6)) % 10 == int(s[6])


def is_frs(v: str) -> bool:
    return bool(re.fullmatch(r"11\d{10}", v.strip()))


def is_ndc(v: str) -> bool:
    s = v.strip()
    return bool(re.fullmatch(r"\d{4}-\d{4}-\d{2}|\d{5}-\d{3}-\d{2}|\d{5}-\d{4}-\d{1,2}|\d{11}", s))


def is_accession(v: str) -> bool:
    # SEC accession, dashed form only: IRS e-file OBJECT_IDs and FEC image numbers are also 18 bare digits
    return bool(re.fullmatch(r"\d{10}-\d{2}-\d{6}", v.strip()))


US_STATES = set(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK "
    "OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC PR VI GU AS MP AA AE AP FM MH PW UM".split()
)


def is_state(v: str) -> bool:
    return v.strip().upper() in US_STATES


def is_mine_id(v: str) -> bool:
    return bool(re.fullmatch(r'"?\d{5,7}"?', v.strip()))


def is_pwsid(v: str) -> bool:
    return bool(re.fullmatch(r"[A-Z0-9]{2}\d{7}", v.strip().upper()))


# key label (either tagger) -> shape check
SHAPES = {
    "NPI": is_npi, "DEA_NO": is_dea, "EIN": is_ein, "CCN": is_ccn,
    "FIPS": is_any_fips, "COUNTY_FIPS": is_fips5, "ZIP": is_zip, "STATE": is_state,
    "CIK": is_cik, "UEI": is_uei, "DUNS": is_duns, "UEI/DUNS": lambda v: is_uei(v) or is_duns(v),
    "LEI": is_lei, "FEC_CMTE_ID": is_fec_cmte, "FEC_CAND_ID": is_fec_cand,
    "FEC_ID": lambda v: is_fec_cmte(v) or is_fec_cand(v), "BIOGUIDE": is_bioguide,
    "IMO": is_imo, "FRS_ID": is_frs, "FRS/EPA": lambda v: is_frs(v) or is_pwsid(v) or bool(re.fullmatch(r"[A-Z]{2}[0-9A-Z]{7}", v.strip().upper())),
    "MINE_ID": is_mine_id, "PWSID": is_pwsid, "ACCESSION": lambda v: bool(re.fullmatch(r"\d{10}-?\d{2}-?\d{6}", v.strip())),
    "FDA_510K_NO": lambda v: bool(re.fullmatch(r"(K|BK|DEN)\d{6}", v.strip().upper())),
    "FDA_PMA_NO": lambda v: bool(re.fullmatch(r"[PHN]\d{6}", v.strip().upper())),
}

# Shapes distinctive enough to find an untagged key by value alone.
VALUE_ONLY = {"NPI": is_npi, "DEA_NO": is_dea, "FEC_CMTE_ID": is_fec_cmte,
              "LEI": is_lei, "BIOGUIDE": is_bioguide, "NDC": is_ndc, "ACCESSION": is_accession}

# Names that say "I am an ID" for keys neither tagger knows.
NAME_HINTS = [
    ("DEA_NO", r"(^|_)DEA(_|$)"), ("NDC", r"(^|_)NDC(_|$)"), ("NAICS", r"NAICS"),
    ("HCPCS", r"HCPCS|(^|_)CPT(_|$)"), ("CFDA", r"CFDA|ASSISTANCE_LISTING"),
    ("CAS", r"(^|_)CAS(_|$)|CAS_(NO|NUM|NUMBER|RN)"), ("ICD", r"(^|_)ICD"),
    ("SIC", r"(^|_)SIC(_|$)"), ("TIN", r"(^|_)TIN$|TAX_ID"),
]

HARD_KEYS = {"NPI", "DEA_NO", "EIN", "CCN", "CIK", "UEI", "DUNS", "LEI", "FEC_CMTE_ID", "FEC_CAND_ID",
             "BIOGUIDE", "IMO", "FRS_ID", "MINE_ID", "PWSID", "CUSIP", "COMPANY_NO", "NPDES_ID",
             "NCUA_CHARTER", "MSHA_CONTROLLER_ID", "MSHA_OPERATOR_ID", "CL_PERSON_ID", "CL_COURT_ID",
             "ICE_FACILITY", "MMSI", "ICPSR", "PATENT", "ACCESSION", "FDA_510K_NO", "FDA_PMA_NO"}

# What an organization name tends to contain. Used to tell an org-name column
# from a drug, a person, a place or free text.
ORG_WORDS = re.compile(
    r"\b(INC|LLC|L\.L\.C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PC|PA|PLLC|GROUP|HOLDINGS|BANK|TRUST|"
    r"HOSPITAL|PHARMACY|CLINIC|CENTER|CENTRE|HEALTH|MEDICAL|SERVICES|ASSOCIATION|ASSOC|FOUNDATION|"
    r"UNIVERSITY|COLLEGE|SCHOOL|DISTRICT|COUNTY|CITY|DEPARTMENT|DEPT|AUTHORITY|COMMITTEE|PAC|FUND|"
    r"PARTNERS|INTERNATIONAL|INDUSTRIES|ENTERPRISES|CHURCH|SOCIETY|COUNCIL|AGENCY|INSTITUTE|LABS?|"
    r"LABORATORIES|SYSTEMS|SOLUTIONS|NURSING|REHAB|CARE|HOME|WALGREEN|CVS|RITE AID|WAL-MART|WALMART|"
    r"CARDINAL|MCKESSON|AMERISOURCE)\b"
)
PERSON = re.compile(r"^[A-Z][A-Z'\-]+,\s*[A-Z][A-Z'\-]+(\s+[A-Z]\.?)?$|^[A-Z][A-Z'\-]+\s+[A-Z]\.?\s+[A-Z][A-Z'\-]+$")
PERSON_PART = re.compile(r"(^|_)(FIRST|LAST|MIDDLE|SURNAME|GIVEN|FNAME|LNAME|MNAME)(_|$)")
PLACE_WORD = re.compile(r"(^|_)(CITY|STATE|STREET|COUNTY|COUNTRY|NECTA|CBSA|MSA|REGION|TOWN|PLACE|ADDRESS|ADDR)(_|$)")
THING_WORD = re.compile(r"DRUG|PRODUCT|INGREDIENT|GENERIC|BRAND|MEDICATION|CHEMICAL|PROGRAM|INITIATIVE|REGIME|"
                        r"(^|_)(RACE|SEX|GENDER|ETHNICITY|TITLE|FILE|TABLE|FIELD|MEASURE|CATEGORY|TYPE|PREFIX|SUFFIX)(_|$)")

# name-column verdicts that make a usable Who link, graded PROBABILISTIC
NAME_OK = {"organizations", "people", "parts of people's names", "names, org or person unclear"}


def classify_names(vals: list[str], col: str) -> dict:
    """What does a NAME-tagged column actually hold?

    Column-name words decide first, because values alone cannot tell
    'Alabama' from a company. Then the values: org words, 'LAST, FIRST'
    shapes, numbers, one-word codes.
    """
    vals = [v.strip().upper() for v in vals if v and v.strip()]
    if not vals:
        return {"holds": "empty", "org_pct": 0, "person_pct": 0, "numeric_pct": 0}
    n = len(vals)
    org = sum(1 for v in vals if ORG_WORDS.search(v)) / n
    per = sum(1 for v in vals if PERSON.match(v)) / n
    num = sum(1 for v in vals if re.fullmatch(r"[\d.\-/ ]+", v)) / n
    one_word = sum(1 for v in vals if " " not in v and "," not in v) / n
    if num > 0.5:
        holds = "numbers"
    elif THING_WORD.search(col):
        holds = "things, not names"
    elif PLACE_WORD.search(col) and not re.search(r"ORG|COMPANY|BUSINESS|FACILITY", col):
        holds = "places"
    elif PERSON_PART.search(col):
        holds = "parts of people's names"
    elif org >= 0.25:
        holds = "organizations"
    elif per >= 0.25:
        holds = "people"
    elif one_word > 0.7:
        holds = "single words or codes"
    else:
        holds = "names, org or person unclear"
    return {"holds": holds, "org_pct": round(org * 100, 1), "person_pct": round(per * 100, 1),
            "numeric_pct": round(num * 100, 1)}


# --------------------------------------------------------------------------- #
# fetch
# --------------------------------------------------------------------------- #
def _conn():
    from connect.db import connect
    return connect()


def _dicts(conn, sql):
    from connect.db import dicts
    return dicts(conn, sql)


def _sval(v):
    if v is None:
        return None
    s = v if isinstance(v, str) else str(v)
    return s[:200]


def cmd_fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "samples").mkdir(exist_ok=True)
    conn = _conn()
    skip = "(" + ",".join(f"'{s}'" for s in SKIP) + ")"
    tabs = _dicts(conn, f"""
        select table_schema s, table_name t, table_type ty, row_count r, comment cm, created, last_altered
        from LIBRARY_MARTS.information_schema.tables where table_schema not in {skip}""")
    cols = _dicts(conn, f"""
        select table_schema s, table_name t, column_name c, data_type d, ordinal_position o, comment cm
        from LIBRARY_MARTS.information_schema.columns where table_schema not in {skip}
        order by 1, 2, 5""")
    tl = _dicts(conn, """select table_name t, table_type ty from LIBRARY_MARTS.information_schema.tables
                          where table_schema = 'TIMELINE'""")
    fl = _dicts(conn, """select object_fqn, one_liner, comment from LIBRARY_META.REGISTRY.FRIENDLY_LAYER
                          where layer = 'mart'""")
    cc = _dicts(conn, """select fqn, column_name, plain_gloss, gloss_source, detected_key, key_tier
                          from LIBRARY_META.REGISTRY.COLUMN_CATALOG""")
    json.dump({"tabs": tabs, "cols": cols, "timeline": tl, "friendly": fl, "colcat": cc},
              open(CACHE / "inventory.json", "w", encoding="utf-8"), default=str)
    print(f"inventory: {len(tabs)} objects, {len(cols)} columns")

    # a sample of every base table and view
    done = {Path(p).name[:-8] for p in glob.glob(str(CACHE / "samples" / "*.json.gz"))}
    for i, t in enumerate(sorted(tabs, key=lambda x: (x["S"], x["T"]))):
        key = f"{t['S']}.{t['T']}"
        if key in done:
            continue
        try:
            cur = conn.cursor()
            cur.execute("alter session set statement_timeout_in_seconds = 120")
            cur.execute(f'select * from LIBRARY_MARTS."{t["S"]}"."{t["T"]}" limit {SAMPLE_N}')
            names = [d[0] for d in cur.description]
            data = {n: [] for n in names}
            for row in cur.fetchall():
                for n, v in zip(names, row):
                    data[n].append(_sval(v))
            cur.close()
            err = None
        except Exception as e:  # a view that errors is itself a finding
            data, err = {}, str(e)[:300]
        with gzip.open(CACHE / "samples" / f"{key}.json.gz", "wt", encoding="utf-8") as f:
            json.dump({"data": data, "error": err}, f)
        if i % 50 == 0:
            print(f"  sampled {i}/{len(tabs)}", flush=True)

    # retry any sample that failed: every column cast to text, longer timeout.
    # A Python-side conversion error, e.g. a year-0 date, is not the table's fault.
    by_t = collections.defaultdict(list)
    for c in cols:
        by_t[f"{c['S']}.{c['T']}"].append((c["C"], c["D"]))
    for key in sorted(by_t):
        data, err = load_sample(key)
        if not err:
            continue
        s, t = key.split(".", 1)
        sel = ", ".join((f'null as "{c}"' if d in ("GEOGRAPHY", "GEOMETRY", "BINARY") else f'"{c}"::varchar as "{c}"')
                        for c, d in by_t[key])
        try:
            cur = conn.cursor()
            cur.execute("alter session set statement_timeout_in_seconds = 600")
            cur.execute(f'select {sel} from LIBRARY_MARTS."{s}"."{t}" limit {SAMPLE_N}')
            names = [d[0] for d in cur.description]
            data = {n: [] for n in names}
            for row in cur.fetchall():
                for n, v in zip(names, row):
                    data[n].append(_sval(v))
            cur.close()
            err2 = None
        except Exception as e:
            data, err2 = {}, str(e)[:300]
        with gzip.open(CACHE / "samples" / f"{key}.json.gz", "wt", encoding="utf-8") as f:
            json.dump({"data": data, "error": err2, "first_error": err}, f)
        print(f"  resampled {key}: {'ok' if not err2 else err2[:80]}", flush=True)

    # real counts for views, which information_schema reports as NULL
    vc_path = CACHE / "view_counts.json"
    vc = json.load(open(vc_path)) if vc_path.exists() else {}
    for t in tabs:
        key = f"{t['S']}.{t['T']}"
        if t["TY"] != "VIEW" or key in vc:
            continue
        try:
            cur = conn.cursor()
            cur.execute("alter session set statement_timeout_in_seconds = 300")
            cur.execute(f'select count(*) from LIBRARY_MARTS."{t["S"]}"."{t["T"]}"')
            vc[key] = cur.fetchone()[0]
            cur.close()
        except Exception as e:
            vc[key] = f"ERROR {str(e)[:200]}"
        json.dump(vc, open(vc_path, "w"))
        print(f"  view {key}: {vc[key]}", flush=True)
    conn.close()


# --------------------------------------------------------------------------- #
# shared loaders
# --------------------------------------------------------------------------- #
def load_inventory():
    return json.load(open(CACHE / "inventory.json", encoding="utf-8"))


def load_sample(key):
    p = CACHE / "samples" / f"{key}.json.gz"
    if not p.exists():
        return {}, "not sampled"
    with gzip.open(p, "rt", encoding="utf-8") as f:
        d = json.load(f)
    return d["data"], d["error"]


def nonempty(vals):
    return [v for v in vals if v is not None and v.strip() != "" and v.strip().upper() not in ("NAN", "NONE", "NULL")]


def column_rows():
    """One dict per catalog column with both tags and its shape results."""
    inv = load_inventory()
    out = []
    by_table = collections.defaultdict(list)
    for c in inv["cols"]:
        by_table[(c["S"], c["T"])].append(c)
    for (s, t), cs in sorted(by_table.items()):
        data, err = load_sample(f"{s}.{t}")
        for c in cs:
            col = c["C"]
            vals = data.get(col, [])
            ne = nonempty(vals)
            rk = regex_tag(col)
            tk, tier = real_tag(t, col)
            row = {"schema": s, "table": t, "column": col, "type": c["D"], "regex_tag": rk,
                   "real_tag": tk, "real_tier": tier, "sampled": len(vals), "filled": len(ne),
                   "sample_error": err, "distinct": len(set(ne)), "examples": list(dict.fromkeys(ne))[:5]}
            for label, which in (("regex", rk), ("real", tk)):
                fn = SHAPES.get(which) if which else None
                row[f"{label}_shape_pct"] = (round(100 * sum(1 for v in ne if fn(v)) / len(ne), 1)
                                             if fn and ne else None)
            # untagged-by-value scan
            row["value_looks_like"] = None
            if ne and not tk:
                uniq = list(dict.fromkeys(ne))[:500]
                for label, fn in VALUE_ONLY.items():
                    share = sum(1 for v in uniq if fn(v)) / len(uniq)
                    if share >= 0.9 and len(uniq) >= 5:
                        row["value_looks_like"] = f"{label} {round(share * 100)}%"
                        break
            row["name_hint"] = next((lab for lab, pat in NAME_HINTS if re.search(pat, col)), None)
            if (tk == "NAME") or (rk == "ORG_NAME"):
                row.update({f"names_{k}": v for k, v in classify_names(ne, col).items()})
            if tk == "FIPS" and ne:
                lv = collections.Counter(fips_level(v) for v in ne)
                row["fips_level"] = lv.most_common(1)[0][0]
                # a county column holding 1-3 digits is a county part with its zeros
                # stripped ('89' = county 089), not a state (skeptic 2026-09-23)
                if row["fips_level"] in ("state", "county part, no state") and re.search(r"COUNTY|CNTY|CTY|(^|_)CZ(_|$)", col):
                    row["fips_level"] = "county part, no state"
            out.append(row)
    return out


# --------------------------------------------------------------------------- #
# links
# --------------------------------------------------------------------------- #
def cmd_links():
    """Distinct cleaned values of every hard-ID column that passes format."""
    rows = column_rows()
    todo = [r for r in rows if r["real_tag"] in HARD_KEYS and r["filled"] > 0
            and (r["real_shape_pct"] is None or r["real_shape_pct"] >= 50)]
    print(f"hard-ID columns to pull: {len(todo)}")
    (CACHE / "links").mkdir(exist_ok=True)
    conn = _conn()
    cur = conn.cursor()
    cur.execute("alter session set statement_timeout_in_seconds = 600")
    for i, r in enumerate(todo):
        key = f"{r['schema']}.{r['table']}.{r['column']}"
        p = CACHE / "links" / f"{key}.txt.gz"
        if p.exists():
            continue
        col = f'"{r["column"]}"'
        try:
            expr = keys.normalize_sql(r["real_tag"], col)
        except Exception:
            expr = f"upper(regexp_replace({col}::varchar, '[^A-Za-z0-9]', ''))"
        try:
            cur.execute(f'select distinct {expr} v from LIBRARY_MARTS."{r["schema"]}"."{r["table"]}" '
                        f"where v is not null and v <> ''")
            vals = [x[0] for x in cur.fetchall()]
            with gzip.open(p, "wt", encoding="utf-8") as f:
                f.write("\n".join(str(v) for v in vals))
            print(f"  {i + 1}/{len(todo)} {key} {r['real_tag']} {len(vals):,} distinct", flush=True)
        except Exception as e:
            print(f"  {i + 1}/{len(todo)} {key} ERROR {str(e)[:150]}", flush=True)
    conn.close()


# --------------------------------------------------------------------------- #
# profile: full-table value profile for every glossary column, all rows, not a
# first-block sample. One query per table: per column, non-empty count and the
# 8 most common values (APPROX_TOP_K). Feeds the glossary re-check.
#   python scripts/audit_catalog.py profile
# --------------------------------------------------------------------------- #
def cmd_profile(rest: bool = False):
    """rest=False: glossary columns. rest=True: every other column (one-table
    names and names that mean different things per table), for per-table text."""
    import csv as _csv
    gl = REPO / "library-onboarding" / "ripple_dbt" / "seeds" / "plain_english_glossary.csv"
    shared = {r["column_name"] for r in _csv.DictReader(open(gl, encoding="utf-8")) if r["varies"] != "yes"}
    inv0 = load_inventory()
    allnames = {c["C"] for c in inv0["cols"]}
    names = (allnames - shared) if rest else shared
    inv = load_inventory()
    by_t = collections.defaultdict(list)
    for c in inv["cols"]:
        if c["C"] in names and not re.search(r"__PREV|_PREV_", c["T"]) and c["D"] not in ("GEOGRAPHY", "GEOMETRY", "BINARY"):
            by_t[(c["S"], c["T"])].append(c["C"])
    out = CACHE / ("profiles_rest" if rest else "profiles")
    out.mkdir(exist_ok=True)
    conn = _conn()
    cur = conn.cursor()
    cur.execute("alter session set statement_timeout_in_seconds = 1800")
    todo = sorted(by_t.items())
    for i, ((s, t), cols) in enumerate(todo):
        p = out / f"{s}.{t}.json"
        if p.exists():
            continue
        parts = ["count(*) as \"__N\""]
        for j, c in enumerate(cols):
            v = f'nullif(trim(to_varchar("{c}")), \'\')'
            parts.append(f'count({v}) as "F{j}"')
            parts.append(f'approx_top_k({v}, 8) as "K{j}"')
            parts.append(f'approx_count_distinct({v}) as "D{j}"')
        try:
            cur.execute(f'select {", ".join(parts)} from LIBRARY_MARTS."{s}"."{t}"')
            row = cur.fetchone()
            res = {"rows": row[0], "cols": {}}
            for j, c in enumerate(cols):
                top = row[2 + 3 * j]
                top = json.loads(top) if isinstance(top, str) else top
                res["cols"][c] = {"filled": row[1 + 3 * j], "distinct_approx": row[3 + 3 * j],
                                  "top": [[str(a)[:80], b] for a, b in (top or [])]}
            json.dump(res, open(p, "w", encoding="utf-8"))
            print(f"  {i + 1}/{len(todo)} {s}.{t} {len(cols)} cols {row[0]:,} rows", flush=True)
        except Exception as e:
            print(f"  {i + 1}/{len(todo)} {s}.{t} ERROR {str(e)[:150]}", flush=True)
    conn.close()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "analyze"
    if cmd == "fetch":
        cmd_fetch()
    elif cmd == "links":
        cmd_links()
    elif cmd == "profile":
        cmd_profile(rest="--rest" in sys.argv)
    elif cmd == "catalog":
        from audit_catalog_report import cmd_catalog  # noqa: E402
        cmd_catalog()
    elif cmd == "analyze":
        from audit_catalog_report import cmd_analyze  # noqa: E402
        cmd_analyze()
    else:
        sys.exit(f"unknown stage {cmd}")
