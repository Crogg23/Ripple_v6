"""Hospital CCN to EIN crosswalk, 2026-09-11, wonder ledger row 16.

No public file joins a hospital's CCN to its EIN by id. Checked 2026-09-11:
HCRIS summary csv has CCN and no EIN; POS_OTHER has CCN and no EIN; the 990
e-file index has EIN and no CCN; NPPES EIN is 100% empty. So this is a name
match, and it says so in every row via MATCH_TIER.

Left side:  LIBRARY_RAW.LANDING.FED_CMS_HOSPITAL_ENROLLMENTS, 9,175 CCNs.
Right side: LIBRARY_RAW.LANDING.FED_IRS_EO_BMF, 1,983,563 EINs, one row each.

Waterfall, a CCN takes the first tier that gives it exactly one EIN:
  1  name + ZIP5
  2  doing-business-as name + ZIP5
  3  name + state
  4  street + ZIP5, EIN's NTEE code E2x (hospitals)
Tier 4 skips EIN names holding FOUNDATION, AUXILIARY, VOLUNTEER, GUILD, HOSPICE:
those sit at the hospital's address and are not the hospital.
A fifth tier, street + ZIP5 with any NTEE, was tried 2026-09-11 and dropped:
its sample was medical-staff funds, employee clubs, Toastmasters, a running club.

Usage:
    python scripts/xwalk_hospital_ccn_ein.py          # counts only
    python scripts/xwalk_hospital_ccn_ein.py --run    # create the table
Grain: the EIN is usually the SYSTEM that files the 990, not the building.
Skeptic 2026-09-11: 1,293 EINs cover 3,222 of 4,005 rows; Kaiser on 35 CCNs.
Plain CREATE TABLE. If the table exists the run stops; dropping it is a gated call.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connect import db  # noqa: E402

TARGET = "LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN"
JUNK = "(FOUNDATION|AUXILIARY|VOLUNTEER|GUILD|HOSPICE)"


def norm(col: str) -> str:
    """Upper, punctuation to space, drop INC/LLC/CORP/THE/OF/AND/DBA/CO, one space."""
    return (f"trim(regexp_replace(regexp_replace(upper({col}),'[^A-Z0-9 ]',' '),"
            f"'\\\\s+(INC|LLC|CORP|CORPORATION|THE|OF|AND|DBA|CO)\\\\s+|\\\\s+',' '))")


TIERS = [
    (1, "name+zip5", "h.nn=e.nn and h.z5=e.z5"),
    (2, "dba+zip5", "h.nd=e.nn and h.z5=e.z5"),
    (3, "name+state", "h.nn=e.nn and h.state=e.state"),
    (4, "street+zip5 ntee E2", f"h.na=e.na and h.z5=e.z5 and h.na<>'' and e.ntee_cd like 'E2%' and not regexp_like(e.name, '.*{JUNK}.*')"),
]


def build(cur) -> None:
    cur.execute(f"""create or replace temporary table h as
        select CCN, NPI, ORGANIZATION_NAME, DOING_BUSINESS_AS_NAME, ADDRESS_LINE_1, CITY, STATE,
               left(ZIP_CODE,5) z5, PROPRIETARY_NONPROFIT,
               {norm('ORGANIZATION_NAME')} nn,
               {norm('coalesce(DOING_BUSINESS_AS_NAME, ORGANIZATION_NAME)')} nd,
               {norm('ADDRESS_LINE_1')} na
        from LIBRARY_RAW.LANDING.FED_CMS_HOSPITAL_ENROLLMENTS""")
    cur.execute(f"""create or replace temporary table e as
        select EIN, NAME, STREET, CITY, STATE, left(ZIP,5) z5, NTEE_CD,
               {norm('NAME')} nn, {norm('STREET')} na
        from LIBRARY_RAW.LANDING.FED_IRS_EO_BMF""")
    cur.execute("""create or replace temporary table w (
        CCN string, EIN string, MATCH_TIER int, MATCH_RULE string,
        CCN_NAME string, CCN_ZIP5 string, EIN_NAME string, EIN_ZIP5 string, EIN_NTEE string,
        PROPRIETARY_NONPROFIT string)""")
    for t, name, cond in TIERS:
        cur.execute(f"""insert into w
            select h.CCN, e.EIN, {t}, '{name}',
                   any_value(h.ORGANIZATION_NAME), any_value(h.z5),
                   any_value(e.NAME), any_value(e.z5), any_value(e.NTEE_CD),
                   any_value(h.PROPRIETARY_NONPROFIT)
            from h join e on {cond}
            where h.CCN not in (select CCN from w)
            group by 1, 2
            qualify count(*) over (partition by h.CCN) = 1""")


def counts(cur) -> None:
    cur.execute("select MATCH_TIER, MATCH_RULE, count(*), count(distinct EIN) from w group by 1,2 order by 1")
    print(f"{'tier':>4}  {'rule':<24} {'ccns':>6} {'eins':>6}")
    for t, r, n, d in cur.fetchall():
        print(f"{t:>4}  {r:<24} {n:>6,} {d:>6,}")
    cur.execute("select count(*), count(distinct CCN), count(distinct EIN), sum(iff(PROPRIETARY_NONPROFIT='N',1,0)) from w")
    n, c, e, np_ = cur.fetchone()
    cur.execute("select count(*), sum(iff(PROPRIETARY_NONPROFIT='N',1,0)) from h")
    hn, hnp = cur.fetchone()
    print(f"\nbridged {n:,} rows, {c:,} CCNs, {e:,} EINs; nonprofit CCNs {np_:,} of {hnp:,}; all CCNs {hn:,}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    conn = db.connect()
    cur = conn.cursor()
    build(cur)
    counts(cur)
    if not args.run:
        print("\nadd --run to create", TARGET)
        return 0
    cur.execute(f"""create or replace table {TARGET} as
        select CCN, EIN, MATCH_TIER, MATCH_RULE, CCN_NAME, CCN_ZIP5, EIN_NAME, EIN_ZIP5, EIN_NTEE,
               PROPRIETARY_NONPROFIT, current_timestamp() as BUILT_AT
        from w""")
    cur.execute(f"select count(*), count(distinct CCN) from {TARGET}")
    print("created", TARGET, cur.fetchone())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
