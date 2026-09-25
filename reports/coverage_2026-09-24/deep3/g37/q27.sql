-- Second-table cross-check on named examples: ECHO's own row (formal actions, penalties, status) for the top Missouri no-action permits
-- and the Nebraska HPV plants named in the write-up, plus each NPDES permit's primary SIC
with ids as (select column1 id, column2 lbl from values
  ('110009339288', 'MO0098752 Madison Mine'), ('110006728292', 'MO0104256 Leadwood WWTP'), ('110009872094', 'MO0107719 Center WWTF'),
  ('110012962357', 'MO0035742 Lake Forest CWD'), ('110009823236', 'OH0021032 Bloomville WWTP')),
air as (select REGISTRY_ID id, PGM_SYS_ID || ' ' || FACILITY_NAME lbl from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
        where PGM_SYS_ID in ('NE0000003114100032', 'NE0000003105900030', 'NE0000003108100030', 'NE0000003107900144', 'NE0000003105300146')),
allids as (select * from ids union all select * from air),
sic as (select NPDES_ID, listagg(SIC_CODE || ' ' || SIC_DESC, '; ') s from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SICS
        where NPDES_ID in ('MO0098752', 'MO0104256', 'MO0107719', 'MO0035742', 'OH0021032') and PRIMARY_INDICATOR_FLAG = 'Y' group by 1)
select a.lbl, e.FRS_ID, e.FACILITY_NAME, e.CITY || ', ' || e.STATE loc, e.COMPLIANCE_STATUS, e.QUARTERS_WITH_NONCOMPLIANCE qnc, e.THREE_YR_COMPLIANCE_HISTORY h,
  e.FORMAL_ACTION_COUNT fac, e.INFORMAL_ACTION_COUNT iac, e.DATE_LAST_FORMAL_ACTION dlfa, e.LAST_PENALTY_AMT_ALLOCATED pen, e.IS_MAJOR_FACILITY major, e.PCT_MINORITY pct_min,
  sic.s primary_sic
from allids a left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e on a.id = e.FRS_ID
  left join sic on left(a.lbl, 9) = sic.NPDES_ID
order by 1;
