-- FJC appeals: decode APPEAL_TYPE from what rides with it (offense code, agency code, suit code, US side, fee waiver)
select APPEAL_TYPE, count(*) n,
  sum(iff(OFFENSE::string<>'-9',1,0)) has_offense, sum(iff(AGENCY::string<>'-9',1,0)) has_agency,
  sum(iff(NATURE_OF_SUIT::string<>'-9',1,0)) has_nos,
  sum(iff(US_APPELLANT::string='1',1,0)) us_appellant, sum(iff(US_APPELLEE::string='1',1,0)) us_appellee,
  sum(iff(FILING_FEE_STATUS='FP',1,0)) fp, sum(iff(PRO_SE_FILED::string<>'0' and PRO_SE_FILED::string<>'-8',1,0)) pro_se_any,
  mode(APPELLEE) top_appellee, mode(NATURE_OF_SUIT) top_nos, mode(AGENCY) top_agency, mode(ORIGINATING_PROCEEDING) top_orig
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1 order by n desc
