"""Row 15: live spot-check of pass-1 families pass 2 never re-touched. 2026-08-31.

Read-only. Dumps reports/row1/row15_pass1_spotcheck.json.
Each check re-measures one falsifiable pass-1 claim.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "reports", "row1", "row15_pass1_spotcheck.json")
DB = "LIBRARY_RAW.LANDING"


def main():
    conn = connect()
    cur = conn.cursor()
    out = {}

    # claim: DEA_NO real ID, 148.6K distinct, one-sided
    cur.execute(f"""select count(distinct REPORTER_DEA_NO), count(distinct BUYER_DEA_NO)
                    from {DB}.FED_DEA_ARCOS_FULL""")
    r = cur.fetchone()
    out["dea_no"] = dict(claim="148.6K distinct, one-sided",
                         reporter_distinct=r[0], buyer_distinct=r[1])
    print("DEA_NO:", out["dea_no"])

    # claim: MINE_ID solid, 100% median, quote-wrapped values handled
    cur.execute(f"""
        with v as (select distinct nullif(trim(replace(MINE_ID,'"','')),'') as k
                   from {DB}.FED_MSHA_VIOLATIONS),
             m as (select distinct nullif(trim(replace(MINE_ID,'"','')),'') as k
                   from {DB}.FED_MSHA_MINES)
        select count(*), count_if(k in (select k from m)) from v where k is not null""")
    tot, hit = cur.fetchone()
    out["mine_id"] = dict(claim="violations->mines ~100%",
                          distinct=tot, matched=hit, pct=round(100*hit/tot, 1))
    print("MINE_ID:", out["mine_id"])

    # claim: PWSID 99.3% median
    cur.execute(f"""
        with v as (select distinct nullif(trim(PWSID),'') as k
                   from {DB}.FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT sample (10)),
             s as (select distinct nullif(trim(PWSID),'') as k
                   from {DB}.FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS)
        select count(*), count_if(k in (select k from s)) from v where k is not null""")
    tot, hit = cur.fetchone()
    out["pwsid"] = dict(claim="violations->systems ~99%",
                        distinct_sampled=tot, matched=hit, pct=round(100*hit/tot, 1))
    print("PWSID:", out["pwsid"])

    # claim: CL_COURT 100% on 71.7M dockets
    cur.execute(f"""
        with d as (select distinct nullif(trim(COURT_ID),'') as k
                   from {DB}.FED_COURTLISTENER_DOCKETS),
             c as (select distinct nullif(trim(ID),'') as k
                   from {DB}.FED_COURTLISTENER_COURTS)
        select count(*), count_if(k in (select k from c)) from d where k is not null""")
    tot, hit = cur.fetchone()
    out["cl_court"] = dict(claim="dockets->courts 100%",
                           distinct=tot, matched=hit, pct=round(100*hit/tot, 1))
    print("CL_COURT:", out["cl_court"])

    # claim: IMO 8.7K distinct indexed, 0 edges (pass-2 later measured 33.4%)
    cur.execute(f"""select count(distinct nullif(trim(IMO_NUMBER),''))
                    from {DB}.FED_USCG_VESSEL_DOCUMENTATION""")
    out["imo_uscg"] = dict(claim="8.7K distinct", distinct=cur.fetchone()[0])
    print("IMO:", out["imo_uscg"])

    # discrepancy probe: pass-1 COMPANY_NO 97% vs pass-2 ukch 85.7%
    cur.execute(f"""
        with g as (select distinct LPAD(NULLIF(TRIM("Entity.RegistrationAuthority.RegistrationAuthorityEntityID"),''),8,'0') as k
                   from {DB}.INTL_GLEIF
                   where "Entity.RegistrationAuthority.RegistrationAuthorityID"='RA000585'),
             u as (select distinct LPAD(NULLIF(TRIM("CompanyNumber"),''),8,'0') as k
                   from {DB}.INT_UK_COMPANIES_HOUSE)
        select count(*), count_if(k in (select k from u)) from g where k is not null""")
    tot, hit = cur.fetchone()
    out["uk_company_no"] = dict(claim="pass-1 said 97, pass-2 said 85.7",
                                distinct=tot, matched=hit, pct=round(100*hit/tot, 1))
    print("UK COMPANY_NO:", out["uk_company_no"])

    conn.close()
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
