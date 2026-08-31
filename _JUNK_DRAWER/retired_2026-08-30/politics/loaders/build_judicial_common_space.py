#!/usr/bin/env python3
"""Land the Judicial Common Space (JCS) + wire judge ideology onto the spine.

JCS (Epstein/Martin/Segal/Westerland) places SCOTUS justices AND Courts-of-Appeals
judges on the SAME scale as DW-NOMINATE, 1937-2022. Source zip (implicit CC0; CC0
mirror on Harvard Dataverse hdl:1902.1/10333): https://epstein.wustl.edu/s/JCS2024.zip .

Three grains landed (the redundant wide pivot is skipped):
  xc_jcs_scotus   <- jcs_supreme_court_2024_long.csv  (1 row / justice-term; justiceName = Spaeth)
  xc_jcs_coa      <- coa_judges_2024.csv               (1 row / CoA judge, lifetime jcs)
  xc_jcs_medians  <- jcs medians.csv                   (1 row / year, court medians)

The payoff: SCOTUS justiceName is the SAME Spaeth convention as POLITICS__SCOTUS_JUSTICE,
so JCS ideology joins by IDENTITY and inherits justice_code (SCDB) + fjc_nid (FJC) --
DW-NOMINATE-scale ideology for every modern justice with no fuzzy matching. CoA judges
key on "Last, First" + circuit; the FJC-nid match for CoA is a deliberate PROBABILISTIC
follow-on (66 surname collisions), not attempted here.

    python3 politics/loaders/build_judicial_common_space.py            # land + build + smoke
    python3 politics/loaders/build_judicial_common_space.py --skip-fetch  # rebuild marts only
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path as _RepoPath

import pandas as pd
import requests

_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402
from build_skeleton import land  # noqa: E402

URL = "https://epstein.wustl.edu/s/JCS2024.zip"
UA = {"User-Agent": "Mozilla/5.0 (Ripple-Library data onboarding; w.rogers9999@gmail.com)"}
# (sid, filename-substring, min_rows floor)
GRAINS = [
    ("xc_jcs_scotus", "long.csv", 750),
    ("xc_jcs_coa", "coa_judges", 700),
    ("xc_jcs_medians", "medians.csv", 100),
]


def fetch_all() -> dict:
    r = requests.get(URL, headers=UA, timeout=120)
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    members = [n for n in zf.namelist()
               if n.lower().endswith(".csv") and not n.startswith("__MACOSX") and "wide" not in n.lower()]
    out = {}
    for sid, sub, _floor in GRAINS:
        name = next(n for n in members if sub in n.lower())
        df = pd.read_csv(io.BytesIO(zf.read(name)), dtype=str, keep_default_na=False)
        print(f"  {sid:16} <- {name.split('/')[-1]:34} {len(df):>4} rows", flush=True)
        out[sid] = df
    return out


MARTS = [
    ("POLITICS__JUDGE_IDEOLOGY_SCOTUS", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_SCOTUS AS
SELECT
  s.JUSTICENAME                 AS justice_name,   -- Spaeth key (identity to SCDB/crosswalk)
  TRY_TO_NUMBER(s.TERM)         AS term,
  TRY_TO_DOUBLE(s.JCS)          AS jcs,            -- DW-NOMINATE-scale ideology
  sj.justice_code,                                 -- <- POLITICS__SCOTUS_JUSTICE (identity)
  cw.fjc_nid,                                      -- <- POLITICS__FJC_SCOTUS_CROSSWALK
  CURRENT_TIMESTAMP()           AS _built_at
FROM LIBRARY_RAW.LANDING.XC_JCS_SCOTUS s
LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__SCOTUS_JUSTICE sj
       ON UPPER(s.JUSTICENAME) = UPPER(sj.justice_name)
LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK cw
       ON UPPER(s.JUSTICENAME) = UPPER(cw.justice_name)
WHERE TRY_TO_DOUBLE(s.JCS) IS NOT NULL
"""),
    ("POLITICS__JUDGE_IDEOLOGY_COA", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_COA AS
SELECT
  NULLIF(TRIM(NAME),'')         AS jcs_judge_name, -- "Last, First" (FJC-nid match = PROBABILISTIC follow-on)
  TRY_TO_NUMBER(CIRCUIT)        AS circuit,
  TRY_TO_DOUBLE(JCS)            AS jcs,
  CURRENT_TIMESTAMP()           AS _built_at
FROM LIBRARY_RAW.LANDING.XC_JCS_COA
WHERE TRY_TO_DOUBLE(JCS) IS NOT NULL
"""),
    ("POLITICS__JCS_MEDIANS", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__JCS_MEDIANS AS
SELECT
  TRY_TO_NUMBER(YEAR)           AS year,
  NULLIF(TRIM(TERM),'')         AS term,
  TRY_TO_NUMBER(CONGRESS)       AS congress,
  TRY_TO_DOUBLE(PRESIDENT)      AS president_score,  -- a SCORE, not a name
  TRY_TO_DOUBLE(HOUSE_MEDIAN)   AS house_median,
  TRY_TO_DOUBLE(SENATE_MEDIAN)  AS senate_median,
  TRY_TO_DOUBLE(SC_MEDIAN)      AS sc_median,
  CURRENT_TIMESTAMP()           AS _built_at
FROM LIBRARY_RAW.LANDING.XC_JCS_MEDIANS
"""),
]


def smoke(conn) -> bool:
    def sc(sql):
        return snow.fetch_scalar(conn, sql)
    M = "LIBRARY_MARTS.POLITICS"
    checks = [
        ("scotus landed >= 750", sc("SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.XC_JCS_SCOTUS"), lambda v: v >= 750),
        ("coa landed >= 700", sc("SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.XC_JCS_COA"), lambda v: v >= 700),
        ("medians landed >= 100", sc("SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.XC_JCS_MEDIANS"), lambda v: v >= 100),
        ("SCOTUS ideology rows > 0", sc(f"SELECT COUNT(*) FROM {M}.POLITICS__JUDGE_IDEOLOGY_SCOTUS"), lambda v: v > 0),
        ("PAYOFF: >=38 of 40 SCDB justices carry a JCS score (identity join)",
         sc(f"SELECT COUNT(DISTINCT justice_name) FROM {M}.POLITICS__JUDGE_IDEOLOGY_SCOTUS WHERE justice_code IS NOT NULL"),
         lambda v: v >= 38),
        ("every justice_code in ideology mart is a real SCOTUS_JUSTICE (0 bad)",
         sc(f"SELECT COUNT(*) FROM {M}.POLITICS__JUDGE_IDEOLOGY_SCOTUS x WHERE x.justice_code IS NOT NULL AND NOT EXISTS "
            f"(SELECT 1 FROM {M}.POLITICS__SCOTUS_JUSTICE j WHERE j.justice_code=x.justice_code)"), lambda v: v == 0),
        ("EXTERNAL anchor: Rehnquist conservative (max jcs > 0.3)",
         sc(f"SELECT ROUND(MAX(jcs),3) FROM {M}.POLITICS__JUDGE_IDEOLOGY_SCOTUS WHERE justice_name='WHRehnquist'"),
         lambda v: v is not None and v > 0.3),
        ("EXTERNAL anchor: Ginsburg liberal (min jcs < -0.2)",
         sc(f"SELECT ROUND(MIN(jcs),3) FROM {M}.POLITICS__JUDGE_IDEOLOGY_SCOTUS WHERE justice_name='RBGinsburg'"),
         lambda v: v is not None and v < -0.2),
        ("EXTERNAL anchor: Marshall strongly liberal (min jcs < -0.5)",
         sc(f"SELECT ROUND(MIN(jcs),3) FROM {M}.POLITICS__JUDGE_IDEOLOGY_SCOTUS WHERE justice_name='TMarshall'"),
         lambda v: v is not None and v < -0.5),
        ("CoA ideology 705 judges, jcs in sane range",
         sc(f"SELECT COUNT(*) FROM {M}.POLITICS__JUDGE_IDEOLOGY_COA WHERE jcs BETWEEN -2 AND 2"), lambda v: v >= 700),
        ("medians: sc_median present for recent years",
         sc(f"SELECT COUNT(*) FROM {M}.POLITICS__JCS_MEDIANS WHERE year>=2000 AND sc_median IS NOT NULL"), lambda v: v > 0),
    ]
    ok = True
    print("\n=== smoke test ===", flush=True)
    for label, val, chk in checks:
        p = bool(chk(val)); ok = ok and p
        print(f"  [{'PASS' if p else 'FAIL'}] {label}  (got {val})", flush=True)
    # report the full judiciary wiring
    wired = snow.fetch_scalar(conn,
        f"SELECT COUNT(*) FROM {M}.POLITICS__JUDGE_IDEOLOGY_SCOTUS WHERE justice_code IS NOT NULL AND fjc_nid IS NOT NULL")
    print(f"\n  fully-wired SCOTUS ideology rows (justice_code AND fjc_nid): {wired}", flush=True)
    return ok


def main() -> int:
    print("=== Judicial Common Space (JCS 2024) ===", flush=True)
    if "--skip-fetch" not in sys.argv:
        frames = fetch_all()
        for sid, sub, floor in GRAINS:
            land(frames[sid], sid, URL, f"JCS 2024 {sub}; DW-NOMINATE-scale judge ideology.", min_rows=floor)
    conn = snow.connect()
    try:
        snow.execute(conn, "CREATE SCHEMA IF NOT EXISTS LIBRARY_MARTS.POLITICS")
        for name, ddl in MARTS:
            snow.execute(conn, ddl)
            print(f"  built {name}", flush=True)
        ok = smoke(conn)
    finally:
        conn.close()
    print(f"\n{'ALL SMOKE PASS' if ok else 'SMOKE FAILED'} -> {'LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_*'}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
