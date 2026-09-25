-- g20 deep pass 3, 2026-09-24. Every statement run, in order, numbered.
-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- [1] fjc_appt_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT;

-- [2] freedomhouse_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__INTL_FREEDOMHOUSE;

-- [3] cannabis_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__ST_CANNABIS_POLICY_BUNDLES;

-- [4] voteview_meta_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META;

-- [5] irs527_related_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_RELATED_ENTITIES;

-- [6] lg_8871
select EIN, FORM_ID_NUMBER, ORGANIZATION_NAME, INITIAL_REPORT_IND, AMENDED_REPORT_IND, FINAL_REPORT_IND, ESTABLISHED_DATE,
  MAILING_ADDR1, MAILING_CITY, MAILING_STATE, EMAIL_ADDRESS, CUSTODIAN_NAME, CONTACT_NAME, INSERT_DATETIME, EXEMPT_8872_IND, EXEMPT_990_IND, left(PURPOSE, 300) purpose
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS
where lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') in ('881699022','881721891','881744115','882179007','882818797','884133773','884139189','884145793','920471242','920494414','920514698','920525922')
   or regexp_replace(upper(MAILING_ADDR1),'[^A-Z0-9]','') like '11403RDST%'
order by EIN, FORM_ID_NUMBER;

-- [7] lg_8872
select lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') ein, ORGANIZATION_NAME, FORM_TYPE, FORM_ID_NUMBER, AMENDED_REPORT_IND, FINAL_REPORT_IND,
  PERIOD_BEGIN_DATE, PERIOD_END_DATE, TOTAL_SCHED_A, TOTAL_SCHED_B, CUSTODIAN_NAME, CONTACT_NAME, INSERT_DATETIME
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS
where lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') in ('881699022','881721891','881744115','882179007','882818797','884133773','884139189','884145793','920471242','920494414','920514698','920525922')
order by 1, PERIOD_BEGIN_DATE, FORM_ID_NUMBER;

-- [8] lg_schedA
select lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') ein, CONTRIBUTOR_NAME, CONTRIBUTOR_CITY, CONTRIBUTOR_STATE, CONTRIBUTOR_EMPLOYER,
  count(*) n, count(distinct FORM_ID_NUMBER) forms, sum(CONTRIBUTION_AMOUNT) amt, min(CONTRIBUTION_DATE) d0, max(CONTRIBUTION_DATE) d1
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS
where lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') in ('881699022','881721891','881744115','882179007','882818797','884133773','884139189','884145793','920471242','920494414','920514698','920525922')
group by 1,2,3,4,5 order by amt desc;

-- [9] lg_schedB
select lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') ein, RECIPIENT_NAME, RECIPIENT_CITY, RECIPIENT_STATE, left(EXPENDITURE_PURPOSE,120) purpose,
  count(*) n, count(distinct FORM_ID_NUMBER) forms, sum(EXPENDITURE_AMOUNT) amt, min(EXPENDITURE_DATE) d0, max(EXPENDITURE_DATE) d1
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES
where lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') in ('881699022','881721891','881744115','882179007','882818797','884133773','884139189','884145793','920471242','920494414','920514698','920525922')
group by 1,2,3,4,5 order by amt desc;

-- [10] senate_party_votes_118_119
with mm as (
  select CONGRESS, try_to_double(to_varchar(ICPSR))::number icpsr, PARTY_CODE
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS where CONGRESS in (118,119) and CHAMBER = 'Senate')
select v.CONGRESS, v.ROLLNUMBER, mm.PARTY_CODE,
  sum(iff(v.CAST_CODE between 1 and 3,1,0)) yea, sum(iff(v.CAST_CODE between 4 and 6,1,0)) nay, count(*) n
from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
left join mm on mm.CONGRESS = v.CONGRESS and mm.icpsr = try_to_double(to_varchar(v.ICPSR))::number
where v.CHAMBER = 'Senate' and v.CONGRESS in (118,119)
group by 1,2,3 order by 1,2,3;

-- [11] fjc_service_vs_appointment
select count(*) n, count(distinct NID) nids, count(distinct NID || '-' || SEQUENCE) nid_seq,
  max(try_to_date(CONFIRMATION_DATE)) max_conf, max(try_to_date(NOMINATION_DATE)) max_nom,
  count_if(APPOINTING_PRESIDENT = 'Donald J. Trump' and try_to_date(NOMINATION_DATE) >= '2025-01-20') trump2,
  count_if(AYES_NAYS is not null and trim(AYES_NAYS) <> '') recorded,
  listagg(distinct SENATE_VOTE_TYPE, ' | ') vote_types
from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE;

-- [12] mccauley_8871_all
select lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') ein, FORM_ID_NUMBER, ORGANIZATION_NAME, INITIAL_REPORT_IND, AMENDED_REPORT_IND, FINAL_REPORT_IND,
  ESTABLISHED_DATE, MAILING_ADDR1, MAILING_CITY, MAILING_STATE, CUSTODIAN_NAME, CONTACT_NAME, EXEMPT_8872_IND, EXEMPT_990_IND, INSERT_DATETIME
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS
where upper(CUSTODIAN_NAME) like '%MCCAULEY%' or upper(CONTACT_NAME) like '%MCCAULEY%'
   or regexp_replace(upper(MAILING_ADDR1),'[^A-Z0-9]','') like '122CST%'
   or upper(ORGANIZATION_NAME) like '%RINO HUNTER%' or upper(ORGANIZATION_NAME) like '%LIBERTY GROUP%'
order by ESTABLISHED_DATE, FORM_ID_NUMBER;

-- [13] exempt_base_rate_2022
select year(try_to_date(ESTABLISHED_DATE)) yr, MAILING_STATE = 'DC' is_dc, count(distinct EIN) eins,
  count(distinct iff(EXEMPT_8872_IND = '1', EIN, null)) exempt_eins
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS
where year(try_to_date(ESTABLISHED_DATE)) between 2020 and 2024 and INITIAL_REPORT_IND = '1'
group by 1,2 order by 1,2;

-- [14] lg_money_named
select 'A_contributor' side, lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') ein, ORG_NAME, CONTRIBUTOR_NAME nm, CONTRIBUTOR_CITY city, CONTRIBUTOR_STATE st,
  count(*) n, sum(CONTRIBUTION_AMOUNT) amt, min(CONTRIBUTION_DATE) d0, max(CONTRIBUTION_DATE) d1
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS
where upper(CONTRIBUTOR_NAME) like '%LIBERTY GROUP%' or upper(CONTRIBUTOR_NAME) like '%RINO HUNTER%' or upper(CONTRIBUTOR_NAME) like '%MCCAULEY%'
group by 1,2,3,4,5,6
union all
select 'B_recipient', lpad(regexp_replace(EIN,'[^0-9]',''),9,'0'), ORG_NAME, RECIPIENT_NAME, RECIPIENT_CITY, RECIPIENT_STATE,
  count(*), sum(EXPENDITURE_AMOUNT), min(EXPENDITURE_DATE), max(EXPENDITURE_DATE)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES
where upper(RECIPIENT_NAME) like '%LIBERTY GROUP%' or upper(RECIPIENT_NAME) like '%RINO HUNTER%' or upper(RECIPIENT_NAME) like '%MCCAULEY%'
group by 1,2,3,4,5,6
order by amt desc nulls last;

-- [15] fec_liberty_mccauley
select CYCLE, FEC_CMTE_ID, CMTE_NM, TRES_NM, CMTE_ST1, CMTE_CITY, CMTE_ST, CMTE_TP, CMTE_DSGN, CONNECTED_ORG_NM
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_BULK_COMMITTEES
where upper(CMTE_NM) like '%RINO HUNTER%' or upper(CMTE_NM) like '%LIBERTY GROUP%' or upper(CONNECTED_ORG_NM) like '%LIBERTY GROUP%'
   or upper(TRES_NM) like '%MCCAULEY%' or regexp_replace(upper(CMTE_ST1),'[^A-Z0-9]','') like '11403RDST%'
order by CMTE_NM, CYCLE;

-- [16] officers_12
select lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') ein, ORG_NAME, ENTITY_NAME, ENTITY_TITLE, ENTITY_ADDR1, ENTITY_CITY, ENTITY_STATE
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS
where lpad(regexp_replace(EIN,'[^0-9]',''),9,'0') in ('881699022','881721891','881744115','882179007','882818797','884133773','884139189','884145793','920471242','920494414','920514698','920525922')
   or upper(ENTITY_NAME) like '%MCCAULEY%'
order by 1;

-- [17] schedB_liberty_group_addresses
select upper(RECIPIENT_NAME) nm, upper(RECIPIENT_ADDR1) a1, upper(RECIPIENT_ADDR2) a2, upper(RECIPIENT_CITY) city, RECIPIENT_STATE st,
  count(*) n, count(distinct EIN) eins, count(distinct FORM_ID_NUMBER) forms, sum(EXPENDITURE_AMOUNT) amt, min(EXPENDITURE_DATE) d0, max(EXPENDITURE_DATE) d1,
  listagg(distinct ORG_NAME, ' | ') within group (order by ORG_NAME) payers
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES
where upper(RECIPIENT_NAME) like '%LIBERTY GROUP%'
   or regexp_replace(upper(RECIPIENT_ADDR1),'[^A-Z0-9]','') like '11403RDST%'
group by 1,2,3,4,5 order by amt desc;

-- [18] fec_ie_liberty_group_payee
select SPE_NAM, PAY, count(*) n, sum(EXP_AMO) amt, min(EXP_DATE) d0, max(EXP_DATE) d1, listagg(distinct CAND_NAME, ' | ') cands
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
where upper(PAY) like '%LIBERTY GROUP%' or upper(SPE_NAM) like '%RINO HUNTER%' or upper(SPE_NAM) like '%BRIGHTER FUTURE%'
group by 1,2 order by amt desc;

-- [19] bmf_liberty_group_or_addresses
select EIN, ORG_NAME, IN_CARE_OF, STREET, CITY, STATE, SUBSECTION_CODE, NTEE_CODE, RULING_DATE, REVENUE_AMT, ASSET_AMT, TAX_PERIOD_YYYYMM
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF
where regexp_replace(upper(ORG_NAME),'[^A-Z ]','') in ('LIBERTY GROUP INC','LIBERTY GROUP','THE LIBERTY GROUP','THE LIBERTY GROUP INC','AMERICAN LIBERTY GROUP','AMERICAN LIBERTY GROUP INC')
   or regexp_replace(upper(STREET),'[^A-Z0-9]','') like '11403RDST%'
   or upper(IN_CARE_OF) like '%MCCAULEY%'
order by ORG_NAME;

-- [20] senate_delegation_party_118_119
select CONGRESS, STATE_ABBREV, PARTY_CODE, count(distinct ICPSR) senators, listagg(distinct BIONAME, ' | ') names
from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
where CONGRESS in (118,119) and CHAMBER = 'Senate'
group by 1,2,3 order by 1,2,3;
