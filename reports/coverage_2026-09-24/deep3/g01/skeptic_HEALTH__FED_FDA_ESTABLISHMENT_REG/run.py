"""Skeptic pass, g01 FDA_ESTABLISHMENT_REG x EPA EtO. SELECT/WITH only."""
import sys, json
from pathlib import Path
REPO = Path(r"C:/Code/Ripple_v6")
sys.path.insert(0, str(REPO))
from connect import db
HERE = Path(__file__).resolve().parent
CE = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS"
TF = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY"
TB = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023"
FDA = "LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG"
Q = {}
Q["q1_tri_facility_identity"] = f"""
select tri_facility_id, facility_name, street_address, city_name, state_abbr, fac_closed_ind,
       to_varchar(frs_id) frs_id, to_varchar(epa_registry_id) epa_registry_id, parent_co_name, standardized_parent_company
from {TF}
where tri_facility_id in ('37825QLTXT1601H','37825RYLST1135H','78045MDWST121GE')
   or upper(city_name) like 'NEW TAZEWELL%'
   or (state_abbr = 'VA' and facility_name ilike '%STERILIZATION SERV%')
   or (state_abbr = 'PR' and facility_name ilike '%STERI%TECH%')
order by 1"""
Q["q2_tri_eto_2024_rank"] = f"""
with e as (
  select pgm_sys_id, to_varchar(registry_id) reg, reporting_year::int yr, count(*) n, sum(annual_emission) lbs
  from {CE}
  where pgm_sys_acrnm = 'TRIS' and pollutant_name = 'Ethylene oxide' and unit_of_measure = 'Pounds'
  group by 1,2,3
), p as (
  select pgm_sys_id, reg,
    sum(iff(yr=2018,lbs,null)) y2018, sum(iff(yr=2019,lbs,null)) y2019, sum(iff(yr=2020,lbs,null)) y2020,
    sum(iff(yr=2021,lbs,null)) y2021, sum(iff(yr=2022,lbs,null)) y2022, sum(iff(yr=2023,lbs,null)) y2023,
    sum(iff(yr=2024,lbs,null)) y2024, max(n) max_rows_per_yr
  from e group by 1,2
)
select rank() over (order by p.y2024 desc) rk, p.*, t.facility_name, t.street_address, t.city_name, t.state_abbr
from p left join {TF} t on t.tri_facility_id = p.pgm_sys_id
where p.y2024 is not null
order by p.y2024 desc"""
Q["q3_fda_sites"] = f"""
select fei_number, establishment_name, owner_operator_firm_name, address_line_1, city, state_code, iso_country_code,
       establishment_type::string etype, status_code, count(*) n_rows
from {FDA}
where upper(city) like 'NEW TAZEWELL%'
   or establishment_name ilike '%STERILIZATION SERVICES OF V%'
   or establishment_name ilike 'STERI%TECH%'
   or (state_code = 'VA' and establishment_type::string ilike '%contract sterilizer%')
group by 1,2,3,4,5,6,7,8,9 order by 1"""
Q["q4_tri_basic_2023_eto"] = f"""
select c_2_trifd, c_4_facility_name, c_5_street_address, c_6_city, c_8_st, c_30_primary_naics, c_49_form_type,
       c_50_unit_of_measure, c_51_5_1_fugitive_air, c_52_5_2_stack_air, c_65_on_site_release_total,
       count(*) over () n_eto_rows, count(distinct c_2_trifd) over () n_eto_fac,
       sum(c_65_on_site_release_total) over () tot_onsite
from {TB}
where upper(trim(c_37_chemical)) = 'ETHYLENE OXIDE'
qualify row_number() over (order by c_65_on_site_release_total desc nulls last) <= 25
     or c_2_trifd in ('37825QLTXT1601H','37825RYLST1135H')
order by c_65_on_site_release_total desc nulls last"""
Q["q5_tri_eto_completeness"] = f"""
with e as (
  select pgm_sys_id, reporting_year::int yr, count(*) n
  from {CE}
  where pgm_sys_acrnm = 'TRIS' and pollutant_name = 'Ethylene oxide'
  group by 1,2
), f as (
  select pgm_sys_id,
    max(iff(yr=2016,1,0)) h16, max(iff(yr=2017,1,0)) h17, max(iff(yr=2018,1,0)) h18, max(iff(yr=2019,1,0)) h19,
    max(iff(yr=2020,1,0)) h20, max(iff(yr=2021,1,0)) h21, max(iff(yr=2022,1,0)) h22, max(iff(yr=2023,1,0)) h23,
    max(iff(yr=2024,1,0)) h24, max(n) maxn
  from e group by 1
)
select count(*) ids, sum(h16) h16, sum(h18) h18, sum(h22) h22, sum(h23) h23, sum(h24) h24,
  count_if(h16=1 and h22=1 and h17+h18+h19+h20+h21=0) hole_16_to_22,
  count_if(h24=1 and h18=0) in24_not18,
  count_if(maxn > 1) ids_with_dup_rows_in_a_year
from f"""
Q["q6_recall_fda_vs_tri2024"] = f"""
with tri as (
  select distinct e.pgm_sys_id, t.facility_name, t.street_address, upper(trim(t.city_name)) city, t.state_abbr st
  from {CE} e join {TF} t on t.tri_facility_id = e.pgm_sys_id
  where e.pgm_sys_acrnm = 'TRIS' and e.pollutant_name = 'Ethylene oxide' and e.reporting_year::int = 2024
), fda as (
  select fei_number, any_value(establishment_name) est, any_value(address_line_1) addr,
         any_value(upper(trim(city))) city, any_value(state_code) st
  from {FDA}
  where establishment_type::string ilike '%contract sterilizer%' and iso_country_code = 'US'
  group by 1
)
select fda.fei_number, fda.est, fda.addr, fda.city, fda.st, tri.pgm_sys_id, tri.facility_name, tri.street_address, tri.city tri_city,
       iff(regexp_substr(trim(fda.addr),'^[0-9]+') = regexp_substr(trim(tri.street_address),'^[0-9]+'),1,0) num_eq,
       iff(fda.city = tri.city,1,0) city_eq,
       jarowinkler_similarity(upper(fda.est), upper(tri.facility_name)) jw
from fda join tri on fda.st = tri.st
where regexp_substr(trim(fda.addr),'^[0-9]+') = regexp_substr(trim(tri.street_address),'^[0-9]+')
   or jarowinkler_similarity(upper(fda.est), upper(tri.facility_name)) >= 85
order by fda.st, fda.fei_number"""

def main():
    c = db.connect(); cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    for label, sql in Q.items():
        head = sql.lstrip().upper()
        assert head.startswith("SELECT") or head.startswith("WITH"), label
        try:
            cur.execute(sql); cols = [d[0] for d in cur.description]; rows = cur.fetchall(); err = None
        except Exception as ex:
            cols, rows, err = [], [], str(ex)
        out = {"label": label, "sql": sql, "cols": cols, "rows": [[None if v is None else str(v) for v in r] for r in rows], "err": err}
        (HERE / f"{label}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
        print(f"== {label}: {'ERR ' + err if err else str(len(rows)) + ' rows'}")
    cur.close(); c.close()

if __name__ == "__main__":
    main()
