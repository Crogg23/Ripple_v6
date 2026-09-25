-- FEC candidates: one principal campaign committee named by several different candidates; one mailing address used by many candidates
with c as (select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES),
p as (select CAND_PCC, count(distinct CAND_ID) ids, count(distinct CAND_NAME) names, listagg(distinct CAND_NAME, ' / ') within group (order by CAND_NAME) nm,
        listagg(distinct CAND_OFFICE_ST || '-' || CAND_OFFICE, ',') off, min(CAND_ELECTION_YR) y0, max(CAND_ELECTION_YR) y1
      from c where nullif(trim(CAND_PCC),'') is not null group by 1 having count(distinct CAND_ID) > 1),
a as (select upper(trim(CAND_ST1)) || ' | ' || upper(trim(CAND_CITY)) || ' ' || CAND_ST || ' ' || left(CAND_ZIP,5) addr, count(distinct CAND_ID) ids, count(distinct CAND_NAME) names,
        listagg(distinct CAND_OFFICE, ',') offs, count(distinct CAND_OFFICE_ST) sts, min(CAND_ELECTION_YR) y0, max(CAND_ELECTION_YR) y1,
        left(listagg(distinct CAND_NAME, ' / '), 200) nm
      from c where nullif(trim(CAND_ST1),'') is not null group by 1 having count(distinct CAND_NAME) >= 4)
select 'pcc_sum' k, null a, count(*) n1, count_if(names > 1) n2, count_if(ids >= 3) n3, null n4, null n5, null n6, null t from p
union all select 'pcc', CAND_PCC, ids, names, y0, y1, null, null, left(nm || ' || ' || off, 300) from p where names > 1 qualify row_number() over (order by ids desc, names desc) <= 15
union all select 'addr', addr, ids, names, sts, y0, y1, null, offs || ' || ' || nm from a qualify row_number() over (order by names desc) <= 15
order by 1, 3 desc
