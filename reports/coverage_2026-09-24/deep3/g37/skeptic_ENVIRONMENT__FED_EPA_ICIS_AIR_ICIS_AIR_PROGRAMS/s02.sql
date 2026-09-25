-- s02: re-derive q25 facility by facility. Every operating facility with an HPV that began before 2024-07-01 and has no resolved date,
-- in NE (all 34) or with no formal action ever (national 66). Adds class code, registry ID, address, informal actions, formal action dates.
with v as (select PGM_SYS_ID, min(HPV_DAYZERO_DATE) dz, max(HPV_DAYZERO_DATE) dz_max, count(*) n_rows, count(distinct ACTIVITY_ID) n_act,
             listagg(distinct AGENCY_TYPE_DESC, ',') ag, listagg(distinct STATE_CODE, ',') vst, min(DSCV_PATHWAY_DATE) dscv, min(NFTC_PATHWAY_DATE) nftc
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
           where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_RESOLVED_DATE is null and HPV_DAYZERO_DATE < '2024-07-01' group by 1),
fa as (select PGM_SYS_ID, count(*) n, min(SETTLEMENT_ENTERED_DATE) mn, max(SETTLEMENT_ENTERED_DATE) mx, sum(coalesce(PENALTY_AMOUNT,0)) pen,
         listagg(distinct ENF_TYPE_DESC, ';') typ from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS group by 1),
ia as (select PGM_SYS_ID, count(*) n, max(ACHIEVED_DATE) mx, listagg(distinct ENF_TYPE_DESC, ';') typ
         from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS group by 1),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr,
        listagg(distinct PROGRAM_CODE || ':' || AIR_OPERATING_STATUS_CODE, ',') pg
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, count(*) frows, any_value(STATE) st, any_value(FACILITY_NAME) nm, any_value(CITY) city, any_value(STREET_ADDRESS) addr, any_value(REGISTRY_ID) reg,
        any_value(AIR_POLLUTANT_CLASS_CODE) cls, any_value(CURRENT_HPV) chpv, any_value(AIR_OPERATING_STATUS_CODE) fstat
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1)
select coalesce(f.st,'??') st, v.PGM_SYS_ID, f.nm, f.city, f.addr, f.reg, f.cls, f.fstat, f.frows, p.tv_opr, p.pg, v.dz, v.dz_max, v.n_rows, v.n_act, v.ag, v.vst, v.dscv, v.nftc,
  f.chpv, coalesce(fa.n,0) fa_n, fa.mn fa_first, fa.mx fa_last, fa.pen, fa.typ fa_typ, coalesce(ia.n,0) ia_n, ia.mx ia_last, ia.typ ia_typ
from v join p on v.PGM_SYS_ID = p.PGM_SYS_ID left join f on v.PGM_SYS_ID = f.PGM_SYS_ID left join fa on v.PGM_SYS_ID = fa.PGM_SYS_ID left join ia on v.PGM_SYS_ID = ia.PGM_SYS_ID
where p.any_opr = 1 and (f.st = 'NE' or fa.n is null)
order by (f.st = 'NE') desc, (fa.n is null) desc, f.st, v.dz;
