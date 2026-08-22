"""Derive shape-signals from the warehouse metadata dump for the Laboratory map.

Pure local CSV crunching over reports/lab_map/ALL_COLUMNS.csv + ALL_TABLES.csv.
No warehouse access. Emits per-shape candidate tables so each technique in
The Laboratory can be scored against what actually exists.
"""
import csv
import json
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "lab_map")

# --- shape signals: name -> regex tested against the COLUMN NAME -------------
SIG = {
    "lat": r"^(.*_)?(LAT|LATITUDE|Y_COORD|YCOORD|LAT_DD|LATDD|DEC_LAT|LATITUDE_MEASURE|LATITUDE83)$",
    "lon": r"^(.*_)?(LON|LNG|LONG|LONGITUDE|X_COORD|XCOORD|LON_DD|LONDD|DEC_LONG|LONGITUDE_MEASURE|LONGITUDE83)$",
    "geom": r"(GEOM|GEOGRAPHY|SHAPE_|WKT|GEOJSON|POLYGON|BOUNDARY)",
    "zip": r"(^|_)(ZIP|ZIPCODE|ZIP_CODE|POSTAL_CODE|POSTALCODE|ZIP5|ZIP4|ZIPCD)(_|$)",
    "fips": r"(FIPS|GEOID|CENSUS_TRACT|TRACT|BLOCK_GROUP|CBSA|MSA_CODE|CONGRESSIONAL_DISTRICT|CD_CODE)",
    "county": r"(^|_)(COUNTY|COUNTY_NAME|COUNTY_CODE|PARISH|BOROUGH)(_|$)",
    "state": r"(^|_)(STATE|STATE_CD|STATE_CODE|STATE_ABBR|STATE_NAME|PROVINCE|ST_ABBR)(_|$)",
    "city": r"(^|_)(CITY|CITY_NAME|TOWN|MUNICIPALITY|LOCALITY|PLACE_NAME)(_|$)",
    "country": r"(^|_)(COUNTRY|COUNTRY_CODE|CTRY|NATION|ISO_COUNTRY|COUNTRY_NAME)(_|$)",
    "address": r"(ADDRESS|ADDR|STREET)",
    "origin": r"(ORIGIN|FROM_|_FROM$|SOURCE_|SHIPPER|DEPART|EXPORTER|SENDER|PAYER|PAYOR|GRANTOR|ASSIGNOR|PRIOR_|PREVIOUS_|OLD_|PARENT_)",
    "dest": r"(DEST|DESTINATION|TO_|_TO$|TARGET_|RECEIVER|RECIPIENT|ARRIV|IMPORTER|PAYEE|GRANTEE|ASSIGNEE|NEW_|SUBSIDIAR|CHILD_)",
    "amount": r"(AMOUNT|AMT|COST|PRICE|DOLLAR|USD|SPEND|REVENUE|PAYMENT|FINE|PENALTY|OBLIGAT|SALARY|COMPENSAT|ASSET|LIABILIT|BALANCE|_FEE|CHARGE|GROSS|NET_)",
    "count_meas": r"(COUNT|NUM_|_NUM$|QTY|QUANTITY|_N$|TOTAL_|FREQ|VOLUME|UNITS|EMPLOYE)",
    "rate_meas": r"(RATE|RATIO|PCT|PERCENT|SCORE|INDEX|PER_|AVG|MEAN|MEDIAN|DENSITY)",
    "severity": r"(SEVERITY|GRADE|RATING|RISK|LEVEL|TIER|CLASS|CATEGORY|STATUS|TYPE|CODE)",
    "entity_id": r"(EIN|NPI|CIK|DUNS|LEI|UEI|CAGE|CCN|FRN|MINE_ID|FACILITY_ID|REGISTRY_ID|COMPANY_NO|DOCKET|CASE_ID|PLAN_NUM|CUSIP|NDC|FEI_NUMBER|BIOGUIDE|FEC_ID|PERMIT|LICENSE)",
    "name_id": r"(^|_)(NAME|LEGAL_NAME|ENTITY_NAME|ORG_NAME|COMPANY_NAME|FIRM_NAME|DBA|OPERATOR|OWNER|SPONSOR|EMPLOYER|REGISTRANT)(_|$)",
    "person": r"(FIRST_NAME|LAST_NAME|MIDDLE_NAME|PERSON|OFFICER|DIRECTOR|EXECUTIVE|PHYSICIAN|PRESCRIBER|INDIVIDUAL|LOBBYIST|CANDIDATE)",
    "naics_sic": r"(NAICS|SIC|INDUSTRY|SECTOR|PSC|NIGP|CPV)",
    "date_col": r"(DATE|_DT$|_DT_|TIME|TIMESTAMP|YEAR|MONTH|QUARTER|PERIOD|_TS$|EFFECTIVE|EXPIR|FILED|ISSUED|BEGIN|END_|START|STOP)",
    "outcome": r"(VIOLATION|PENALT|DEATH|DIED|FATAL|INJUR|ILLNESS|HARM|COMPLAINT|ADVERSE|RECALL|CLOSURE|EVICT|FORECLOS|BANKRUPT|LAYOFF|EXCLUSION|DEBAR|SANCTION|DENIAL|REVOK|SUSPEN|CITATION|ENFORCE)",
    "flag_bool": r"(^|_)(IS_|HAS_|FLAG|_IND$|_YN$|INDICATOR)",
    "seq_order": r"(SEQ|ORDER|RANK|STEP|LINE_NUM|VERSION|REVISION|AMENDMENT)",
}
SIGRE = {k: re.compile(v) for k, v in SIG.items()}

NUMTYPES = {"NUMBER", "FLOAT", "DECIMAL", "INT", "INTEGER", "BIGINT",
            "SMALLINT", "DOUBLE", "REAL"}
DATETYPES = {"DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ",
             "TIME", "DATETIME"}


def as_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


tables = {}
with open(os.path.join(OUT, "ALL_TABLES.csv"), encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        tables[(r["db"], r["schema"], r["table"])] = r

hits = defaultdict(set)
tbl_sig = defaultdict(set)
tbl_numeric = defaultdict(int)
tbl_date = defaultdict(int)
tbl_text = defaultdict(int)
tbl_variant = defaultdict(int)
tbl_cols = defaultdict(int)
sig_cols = defaultdict(list)

with open(os.path.join(OUT, "ALL_COLUMNS.csv"), encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        key = (r["db"], r["schema"], r["table"])
        col = r["column"].upper()
        dt = r["dtype"].upper()
        tbl_cols[key] += 1
        if dt in NUMTYPES:
            tbl_numeric[key] += 1
        elif dt in DATETYPES:
            tbl_date[key] += 1
        elif dt == "VARIANT" or dt.startswith("OBJECT") or dt.startswith("ARRAY"):
            tbl_variant[key] += 1
        else:
            tbl_text[key] += 1
        for name, rx in SIGRE.items():
            if rx.search(col):
                hits[name].add(key)
                tbl_sig[key].add(name)
                if len(sig_cols[name]) < 6000:
                    sig_cols[name].append((key[0], key[1], key[2], col, dt))

os.makedirs(os.path.join(OUT, "signals"), exist_ok=True)
signal_counts = {}
for name in SIG:
    rows = sorted(sig_cols[name])
    signal_counts[name] = len(hits[name])
    with open(os.path.join(OUT, "signals", "SIG_%s.csv" % name), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["db", "schema", "table", "column", "dtype", "row_count"])
        for db, sc, t, col, dt in rows:
            w.writerow([db, sc, t, col, dt,
                        tables.get((db, sc, t), {}).get("row_count", "")])


def inter(*names):
    s = None
    for n in names:
        s = set(hits[n]) if s is None else (s & hits[n])
    return s


COMBOS = {
    "POINT_GEO_latlon": inter("lat", "lon"),
    "AREA_GEO_zip": set(hits["zip"]),
    "AREA_GEO_fips": set(hits["fips"]),
    "AREA_GEO_county": set(hits["county"]),
    "AREA_GEO_state": set(hits["state"]),
    "GEOM_shapes": set(hits["geom"]),
    "OD_flow_origin_dest": inter("origin", "dest"),
    "GEO_plus_TIME": inter("lat", "lon", "date_col"),
    "GEO_plus_MONEY": inter("lat", "lon", "amount"),
    "GEO_plus_OUTCOME": inter("lat", "lon", "outcome"),
    "ZIP_plus_TIME": hits["zip"] & hits["date_col"],
    "ZIP_plus_OUTCOME": hits["zip"] & hits["outcome"],
    "COUNTY_plus_TIME": hits["county"] & hits["date_col"],
    "ENTITY_plus_TIME": hits["entity_id"] & hits["date_col"],
    "ENTITY_plus_MONEY": hits["entity_id"] & hits["amount"],
    "ENTITY_plus_GEO": hits["entity_id"] & (hits["zip"] | hits["lat"]),
    "ENTITY_plus_OUTCOME": hits["entity_id"] & hits["outcome"],
    "MULTIVAR_numeric_ge8": {k for k, v in tbl_numeric.items() if v >= 8},
    "MULTIVAR_numeric_ge20": {k for k, v in tbl_numeric.items() if v >= 20},
    "MULTIVAR_numeric_ge50": {k for k, v in tbl_numeric.items() if v >= 50},
    "WIDE_ge50_cols": {k for k, v in tbl_cols.items() if v >= 50},
    "WIDE_ge150_cols": {k for k, v in tbl_cols.items() if v >= 150},
    "TIME_any": set(hits["date_col"]),
    "OUTCOME_any": set(hits["outcome"]),
    "PERSON_any": set(hits["person"]),
    "NAICS_any": set(hits["naics_sic"]),
    "SEQ_any": set(hits["seq_order"]),
    "BIG_ge1M_rows": {k for k, t in tables.items()
                      if as_int(t.get("row_count")) >= 1_000_000},
    "BIG_ge10M_rows": {k for k, t in tables.items()
                       if as_int(t.get("row_count")) >= 10_000_000},
}

combo_counts = {}
for name, s in COMBOS.items():
    rows = sorted(s, key=lambda k: -as_int(tables.get(k, {}).get("row_count")))
    combo_counts[name] = len(rows)
    with open(os.path.join(OUT, "signals", "COMBO_%s.csv" % name), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["db", "schema", "table", "row_count", "bytes", "n_cols",
                    "n_numeric", "n_date", "signals"])
        for k in rows:
            t = tables.get(k, {})
            w.writerow([k[0], k[1], k[2], t.get("row_count", ""),
                        t.get("bytes", ""), tbl_cols[k], tbl_numeric[k],
                        tbl_date[k], "|".join(sorted(tbl_sig[k]))])

with open(os.path.join(OUT, "TABLE_SHAPES.csv"), "w", newline="",
          encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["db", "schema", "table", "type", "row_count", "bytes",
                "n_cols", "n_numeric", "n_date", "n_text", "n_variant",
                "signals"])
    for k, t in sorted(tables.items(),
                       key=lambda kv: -as_int(kv[1].get("row_count"))):
        w.writerow([k[0], k[1], k[2], t.get("type", ""), t.get("row_count", ""),
                    t.get("bytes", ""), tbl_cols[k], tbl_numeric[k],
                    tbl_date[k], tbl_text[k], tbl_variant[k],
                    "|".join(sorted(tbl_sig[k]))])

by_type = defaultdict(int)
by_db = defaultdict(int)
for k, t in tables.items():
    by_type[t.get("type", "")] += 1
    by_db[k[0]] += 1

out = {"total_tables": len(tables), "by_type": dict(by_type),
       "by_db": dict(by_db), "signal_table_counts": signal_counts,
       "combo_table_counts": combo_counts}
with open(os.path.join(OUT, "SHAPE_SUMMARY.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2)
print(json.dumps(out, indent=2))
