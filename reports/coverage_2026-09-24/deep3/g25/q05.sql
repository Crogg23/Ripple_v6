-- FEC candidates: per election year x office: rows, candidates, status mix, blank PCC, placeholder ZIP, exact dup rows
select CAND_ELECTION_YR yr, CAND_OFFICE off, count(*) n, count(distinct CAND_ID) cands,
  count_if(CAND_STATUS='C') st_c, count_if(CAND_STATUS='F') st_f, count_if(CAND_STATUS='N') st_n, count_if(CAND_STATUS='P') st_p,
  count_if(CAND_PCC is null or trim(CAND_PCC)='') pcc_blank, count_if(CAND_ZIP like '00000%') zip0,
  count_if(CAND_ST <> CAND_OFFICE_ST and CAND_OFFICE in ('H','S')) mail_out_of_state,
  count(*) - count(distinct hash(CAND_ID, CAND_NAME, CAND_PTY_AFFILIATION, CAND_ELECTION_YR, CAND_OFFICE_ST, CAND_OFFICE, CAND_OFFICE_DISTRICT, CAND_ICI, CAND_STATUS, CAND_PCC, CAND_ST1, CAND_ST2, CAND_CITY, CAND_ST, CAND_ZIP)) exact_dups
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES
group by rollup(1,2) order by 1,2
