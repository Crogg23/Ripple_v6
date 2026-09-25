-- FJC 4th Circuit: published appeals (codes 1/2/4) by appeal-type code and fiscal year; argued and consolidated counts
select iff(grouping(APPEAL_TYPE) = 1, 'ALL', APPEAL_TYPE) appeal_type,
  sum(iff(TAPE_YEAR = '2019' and PUBLICATION_STATUS in ('1','2','4'), 1, 0)) pub19,
  sum(iff(TAPE_YEAR = '2020' and PUBLICATION_STATUS in ('1','2','4'), 1, 0)) pub20,
  sum(iff(TAPE_YEAR = '2021' and PUBLICATION_STATUS in ('1','2','4'), 1, 0)) pub21,
  sum(iff(TAPE_YEAR = '2022' and PUBLICATION_STATUS in ('1','2','4'), 1, 0)) pub22,
  sum(iff(TAPE_YEAR = '2023' and PUBLICATION_STATUS in ('1','2','4'), 1, 0)) pub23,
  sum(iff(TAPE_YEAR = '2024' and PUBLICATION_STATUS in ('1','2','4'), 1, 0)) pub24,
  sum(iff(TAPE_YEAR = '2025' and PUBLICATION_STATUS in ('1','2','4'), 1, 0)) pub25,
  sum(iff(TAPE_YEAR = '2020' and PUBLICATION_STATUS in ('1','2','3','4','5'), 1, 0)) merits20,
  sum(iff(TAPE_YEAR = '2025' and PUBLICATION_STATUS in ('1','2','3','4','5'), 1, 0)) merits25,
  sum(iff(TAPE_YEAR = '2019' and DISPOSITION = '1', 1, 0)) argued19,
  sum(iff(TAPE_YEAR = '2020' and DISPOSITION = '1', 1, 0)) argued20,
  sum(iff(TAPE_YEAR = '2025' and DISPOSITION = '1', 1, 0)) argued25,
  sum(iff(TAPE_YEAR = '2020' and PUBLICATION_STATUS in ('1','2','4') and DISPOSITION = '1', 1, 0)) pub_argued20,
  sum(iff(TAPE_YEAR = '2025' and PUBLICATION_STATUS in ('1','2','4') and DISPOSITION = '1', 1, 0)) pub_argued25,
  sum(iff(TAPE_YEAR = '2020' and PUBLICATION_STATUS in ('1','2','4') and CONSOLIDATED_DOCKET not in ('-8','0'), 1, 0)) pub_consol20,
  sum(iff(TAPE_YEAR = '2025' and PUBLICATION_STATUS in ('1','2','4') and CONSOLIDATED_DOCKET not in ('-8','0'), 1, 0)) pub_consol25
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
where CIRCUIT = '4' and TAPE_YEAR between '2019' and '2025'
group by rollup(APPEAL_TYPE)
order by pub25 desc;
