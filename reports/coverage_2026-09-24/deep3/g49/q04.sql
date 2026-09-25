-- FJC appeals: every coded outcome-type column, value counts in one pass
select 'OUTCOME' col, OUTCOME::string val, count(*) n from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'PROCEDURAL_TERMINATION', PROCEDURAL_TERMINATION::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'METHOD', METHOD::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'PUBLICATION_STATUS', PUBLICATION_STATUS::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'TERMINATION_TYPE', TERMINATION_TYPE::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'PRO_SE_FILED', PRO_SE_FILED::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'AGENCY', AGENCY::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'DISPOSITION', DISPOSITION::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
order by 1, 3 desc
