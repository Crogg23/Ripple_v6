with ins as (
  select distinct r.OWNER_CIK, r.OWNER_NAME, r.STATE, s.ISSUER_NAME, s.ISSUER_CIK,
    upper(split_part(trim(r.OWNER_NAME),' ',1)) last_nm, upper(regexp_replace(split_part(trim(r.OWNER_NAME),' ',2),'[^A-Za-z]','')) first_nm,
    upper(regexp_replace(split_part(upper(s.ISSUER_NAME),' ',1),'[^A-Z0-9]','')) issuer_w1
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER r
  join LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s on s.ACCESSION_NUMBER = r.ACCESSION_NUMBER
  where s.FILING_DATE between '2021-01-01' and '2025-12-31' and (r.RELATIONSHIP ilike '%officer%' or r.RELATIONSHIP ilike '%director%')
    and r.OWNER_NAME not ilike '%llc%' and r.OWNER_NAME not ilike '%l.p.%' and r.OWNER_NAME not ilike '% lp%' and r.OWNER_NAME not ilike '%trust%' and r.OWNER_NAME not ilike '%fund%' and r.OWNER_NAME not ilike '%capital%' and r.OWNER_NAME not ilike '%partners%' and r.OWNER_NAME not ilike '% inc%' and r.OWNER_NAME not ilike '%corp%'
    and length(split_part(trim(r.OWNER_NAME),' ',2)) >= 3),
fec as (
  select SUB_ID, DONOR_NAME, EMPLOYER, STATE, CMTE_ID, TRANSACTION_AMT, TRANSACTION_DATE, CYCLE_FILE,
    upper(trim(split_part(DONOR_NAME,',',1))) last_nm, upper(regexp_replace(split_part(trim(split_part(DONOR_NAME,',',2)),' ',1),'[^A-Za-z]','')) first_nm,
    upper(regexp_replace(upper(EMPLOYER),'[^A-Z0-9 ]','')) emp
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
  where CYCLE_FILE in ('2022','2024','2026') and TRANSACTION_AMT >= 1000 and ENTITY_TYPE = 'IND' and MEMO_CD is distinct from 'X' and EMPLOYER is not null and length(EMPLOYER) > 3),
m as (
  select distinct ins.OWNER_CIK, fec.SUB_ID, fec.TRANSACTION_AMT, fec.CMTE_ID, fec.CYCLE_FILE
  from ins join fec on fec.last_nm = ins.last_nm and fec.first_nm = ins.first_nm and fec.STATE = ins.STATE and fec.emp like ins.issuer_w1 || '%'
  where length(ins.issuer_w1) >= 4),
cm as (select CMTE_ID, max(CMTE_TP) tp, max(CMTE_PTY_AFFILIATION) pty from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM group by 1)
select count(distinct m.OWNER_CIK) insiders, count(distinct m.SUB_ID) gifts, round(sum(m.TRANSACTION_AMT)/1e6,1) usd_m,
  round(sum(iff(cm.tp='O', m.TRANSACTION_AMT, 0))/1e6,1) super_pac_m, round(sum(iff(cm.pty='REP', m.TRANSACTION_AMT, 0))/1e6,1) rep_m, round(sum(iff(cm.pty='DEM', m.TRANSACTION_AMT, 0))/1e6,1) dem_m
from m left join cm on cm.CMTE_ID = m.CMTE_ID;
with ins as (
  select distinct r.OWNER_CIK, r.OWNER_NAME, r.STATE, s.ISSUER_NAME, s.ISSUER_CIK, r.TITLE,
    upper(split_part(trim(r.OWNER_NAME),' ',1)) last_nm, upper(regexp_replace(split_part(trim(r.OWNER_NAME),' ',2),'[^A-Za-z]','')) first_nm,
    upper(regexp_replace(split_part(upper(s.ISSUER_NAME),' ',1),'[^A-Z0-9]','')) issuer_w1
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER r
  join LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s on s.ACCESSION_NUMBER = r.ACCESSION_NUMBER
  where s.FILING_DATE between '2021-01-01' and '2025-12-31' and (r.RELATIONSHIP ilike '%officer%' or r.RELATIONSHIP ilike '%director%')
    and (s.ISSUER_NAME ilike 'alliance resource%' or s.ISSUER_NAME ilike 'alpha metallurgical%' or s.ISSUER_NAME ilike 'warrior met%' or s.ISSUER_NAME ilike 'peabody%' or s.ISSUER_NAME ilike 'arch resources%' or s.ISSUER_NAME ilike 'arch coal%' or s.ISSUER_NAME ilike 'consol energy%' or s.ISSUER_NAME ilike 'ramaco%' or s.ISSUER_NAME ilike 'coronado%' or s.ISSUER_NAME ilike 'martin marietta%' or s.ISSUER_NAME ilike 'vulcan materials%' or s.ISSUER_NAME ilike 'freeport%' or s.ISSUER_NAME ilike 'cleveland-cliffs%' or s.ISSUER_NAME ilike 'nacco%' or s.ISSUER_NAME ilike 'hallador%' or s.ISSUER_NAME ilike 'core natural%')
    and length(split_part(trim(r.OWNER_NAME),' ',2)) >= 3),
fec as (
  select SUB_ID, DONOR_NAME, EMPLOYER, STATE, CMTE_ID, TRANSACTION_AMT, TRANSACTION_DATE, CYCLE_FILE,
    upper(trim(split_part(DONOR_NAME,',',1))) last_nm, upper(regexp_replace(split_part(trim(split_part(DONOR_NAME,',',2)),' ',1),'[^A-Za-z]','')) first_nm,
    upper(regexp_replace(upper(EMPLOYER),'[^A-Z0-9 ]','')) emp
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
  where CYCLE_FILE in ('2020','2022','2024','2026') and TRANSACTION_AMT >= 200 and ENTITY_TYPE = 'IND' and MEMO_CD is distinct from 'X' and EMPLOYER is not null and length(EMPLOYER) > 3),
m as (
  select distinct ins.ISSUER_NAME, ins.OWNER_NAME, ins.TITLE, fec.SUB_ID, fec.TRANSACTION_AMT, fec.CMTE_ID, fec.CYCLE_FILE, fec.EMPLOYER
  from ins join fec on fec.last_nm = ins.last_nm and fec.first_nm = ins.first_nm and fec.STATE = ins.STATE and (fec.emp like ins.issuer_w1 || '%' or fec.emp like '%COAL%' or fec.emp like '%MINING%' or fec.emp like '%RESOURCE%')
  where length(ins.issuer_w1) >= 4),
cm as (select CMTE_ID, max(CMTE_NM) nm, max(CMTE_TP) tp, max(CMTE_PTY_AFFILIATION) pty from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM group by 1)
select m.ISSUER_NAME, m.OWNER_NAME, any_value(m.TITLE) title, count(distinct m.SUB_ID) gifts, round(sum(m.TRANSACTION_AMT)) usd, round(sum(iff(cm.tp='O',m.TRANSACTION_AMT,0))) super_pac_usd, max_by(cm.nm, m.TRANSACTION_AMT) biggest_recipient, any_value(m.EMPLOYER) employer
from m left join cm on cm.CMTE_ID = m.CMTE_ID group by 1,2 order by usd desc limit 30
