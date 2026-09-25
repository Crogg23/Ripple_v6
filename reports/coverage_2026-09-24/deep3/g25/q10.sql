-- EPA informal: Jan-Jul 2022-2026 by statute, program, EPA region (first 2 chars of case number) and action type
select left(ENF_IDENTIFIER, 2) reg, STATUTE, PGM_SYS_ACRNM, ENF_TYPE_DESC,
  count_if(year(ACHIEVED_DATE)=2022 and month(ACHIEVED_DATE)<=7) y22, count_if(year(ACHIEVED_DATE)=2023 and month(ACHIEVED_DATE)<=7) y23,
  count_if(year(ACHIEVED_DATE)=2024 and month(ACHIEVED_DATE)<=7) y24, count_if(year(ACHIEVED_DATE)=2025 and month(ACHIEVED_DATE)<=7) y25,
  count_if(year(ACHIEVED_DATE)=2026 and month(ACHIEVED_DATE)<=7) y26, count(*) n_all
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
where year(ACHIEVED_DATE) between 2022 and 2026
group by 1,2,3,4 having count(*) >= 8 order by y26 desc, n_all desc limit 45
