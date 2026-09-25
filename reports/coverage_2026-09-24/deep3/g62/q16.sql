-- Enforcement join: coal-running plants by ash-pond group -> CAMD program ID (= EIA plant code) in the combined-emissions table -> FRS registry ID -> ECHO.
-- Peer groups: unlined OP pond with no coal retirement date / unlined OP with dates / lined OP / pond not OP / no pond reported. Land rate at each hop.
with pl as (select PLANT_CODE, STATE, ASH_IMPOUNDMENT ash, ASH_IMPOUNDMENT_LINED lined, ASH_IMPOUNDMENT_STATUS ast from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT),
g as (select PLANT_CODE, sum(NAMEPLATE_CAPACITY_MW) coal_mw, sum(iff(PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0)) dated_mw
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR where STATUS='OP' and ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') group by 1),
grp as (select g.PLANT_CODE, pl.STATE, g.coal_mw,
          case when pl.ash='Y' and pl.lined='N' and pl.ast='OP' and g.dated_mw=0 then 'a unlined OP, no coal ret date'
               when pl.ash='Y' and pl.lined='N' and pl.ast='OP' then 'b unlined OP, some dated'
               when pl.ash='Y' and pl.lined='Y' and pl.ast='OP' then 'c lined OP'
               when pl.ash='Y' then 'd pond not OP' else 'e no pond reported' end grp
        from g join pl on pl.PLANT_CODE=g.PLANT_CODE),
c as (select try_to_number(PGM_SYS_ID) oris, min(to_varchar(REGISTRY_ID)) reg, count(distinct REGISTRY_ID) nreg
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS where PGM_SYS_ACRNM='CAMDBS' group by 1),
e as (select to_varchar(FRS_ID) reg, max(STATE) st, max(QUARTERS_WITH_NONCOMPLIANCE) q, max(FORMAL_ACTION_COUNT) fa, max(TOTAL_PENALTIES) pen,
        max(PENALTY_COUNT) pcount, max(HAS_WATER_PROGRAM::int) water, max(INFORMAL_ACTION_COUNT) ia, count(*) echo_rows
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where to_varchar(FRS_ID) in (select reg from c) group by 1)
select grp.grp, count(*) plants, round(sum(grp.coal_mw)) coal_mw, count(c.reg) with_reg, max(c.nreg) max_nreg, count(e.reg) in_echo, count_if(e.st=grp.STATE) state_agrees,
  max(e.echo_rows) max_echo_rows, round(median(e.q),1) med_q_noncomp, round(avg(e.q),2) avg_q_noncomp, count_if(e.q>=4) q4plus, count_if(e.q>=12) q12,
  count_if(e.fa>0) any_formal_5yr, round(avg(e.ia),2) avg_informal, count_if(e.pen>0) any_penalty, round(sum(e.pen)) penalties_usd, round(median(iff(e.pen>0,e.pen,null))) med_penalty, sum(e.water) water_program
from grp left join c on c.oris=grp.PLANT_CODE left join e on e.reg=c.reg
group by 1 order by 1
