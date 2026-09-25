-- j6: Las Vegas Sands in Texas, join pass 2026-09-24
-- Door: Python (connect/db.py). Every connection opened with:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24';
-- Read-only. Statements numbered in the order run.

-- [1] TX client lines naming Sands/Adelson/Kleinheinz/Success Academy, by filer
-- Sands reports: all TX filers with a Sands client line, report counts, years; plus Abboud's report ids
select i.FILERNAME, i.FILER_ID, upper(i.ONBEHALFNAME) client, count(distinct i.REPORT_ID) reports, min(i.APPLICABLEYEAR) y0, max(i.APPLICABLEYEAR) y1
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING i
where upper(i.ONBEHALFNAME) like '%SANDS%' or upper(i.ONBEHALFNAME) like '%ADELSON%' or upper(i.ONBEHALFNAME) like '%KLEINHEINZ%' or upper(i.ONBEHALFNAME) like '%SUCCESS ACAD%'
group by 1,2,3 order by 3,4 desc;

-- [2] Find TX lobby / ethics tables incl. registration and campaign finance
-- Every Texas lobby / Texas ethics table in marts and landing (looking for a registration / compensation table)
select 'MARTS' db, table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike '%TX%LOBBY%' or table_name ilike '%TEC%' or table_name ilike '%TX_ETHIC%' or table_name ilike '%TX_CAMPAIGN%'
union all
select 'RAW', table_schema, table_name, row_count from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_name ilike '%TX%LOBBY%' or table_name ilike '%TX_ETHIC%' or table_name ilike '%TEC_%' or table_name ilike '%TX_CAMPAIGN%' or table_name ilike '%TX_CF%'
order by 1,3;

-- [3] Abboud cover reports joined to SUBJECT_MATTER and DOCKETS
-- Abboud: every cover report (media and other totals) + count of subject-matter and docket lines joined on REPORT_ID = REPORT_INFO_IDENT
with cv as (
 select REPORT_INFO_IDENT rid, FILER_IDENT, FILER_NAME, FORM_TYPE_CD, REPORT_TYPE_CD, APPLICABLE_YEAR, PERIOD_START_DT, PERIOD_END_DT, FILED_DT,
  try_to_number(TOTAL_EXPEND_MEDIA,18,2) media, try_to_number(TOTAL_EXPEND_FOOD,18,2) food, try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) trans,
  try_to_number(TOTAL_EXPEND_ENTERTAINMENT,18,2) ent, try_to_number(TOTAL_EXPEND_EVENT,18,2) evt
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where FILER_NAME ilike 'Abboud%'
), sm as (select REPORT_ID::string rid, count(*) n_subj, listagg(distinct SUBJECTMATTERCODEVALUE, '; ') within group (order by SUBJECTMATTERCODEVALUE) subjects
  from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1),
 dk as (select REPORT_ID::string rid, count(*) n_dk from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS group by 1)
select cv.rid, FILER_IDENT, FORM_TYPE_CD, REPORT_TYPE_CD, APPLICABLE_YEAR, PERIOD_START_DT, PERIOD_END_DT, FILED_DT, media, food, trans, ent, evt, sm.n_subj, dk.n_dk, left(sm.subjects,200) subjects
from cv left join sm on sm.rid = cv.rid::string left join dk on dk.rid = cv.rid::string
order by PERIOD_START_DT, rid;

-- [4] SUBJECT_MATTER/DOCKETS form types, cover land rate, Abboud rows
-- Why the REPORT_ID join misses: SUBJECT_MATTER and DOCKETS by form/report type, year range, land rate on cover, and any Abboud (FILER_ID 85404) rows
with sm as (select 'SUBJ' t, FORMTYPECD, REPORTTYPECD, APPLICABLEYEAR, REPORT_ID::string rid, FILER_ID, FILERNAME from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER
 union all select 'DOCK', FORMTYPECD, REPORTTYPECD, APPLICABLEYEAR, REPORT_ID::string, FILER_ID, FILERNAME from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_DOCKETS),
cv as (select REPORT_INFO_IDENT::string rid from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER)
select t, FORMTYPECD, left(REPORTTYPECD,11) rtype, count(*) lines, count(distinct sm.rid) reports, count(distinct cv.rid) reports_on_cover,
 min(APPLICABLEYEAR) y0, max(APPLICABLEYEAR) y1,
 count_if(ltrim(FILER_ID,'0')='85404' or FILERNAME ilike 'abboud%') abboud_lines
from sm left join cv on cv.rid = sm.rid
group by 1,2,3 order by 1, lines desc limit 40;

-- [5] Gaming-related subject lines 2019-2026, filers and clients
-- Gaming subject lines 2019-2026: which subject codes mention gaming/casino/racing/lottery, filers and reports per year, with client lines on those reports
with s as (select REPORT_ID::string rid, APPLICABLEYEAR y, FILERNAME, SUBJECTMATTERCODEVALUE sv, SUBJECTMATTERDESCR sd
  from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER
  where (SUBJECTMATTERCODEVALUE ilike any ('%gam%','%casino%','%racing%','%lottery%','%wager%') or SUBJECTMATTERDESCR ilike any ('%gaming%','%casino%','%resort%','%wager%'))
    and APPLICABLEYEAR >= '2019'),
 c as (select REPORT_ID::string rid, listagg(distinct upper(ONBEHALFNAME), ' | ') cl from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING group by 1)
select sv, y, count(distinct s.rid) reports, count(distinct FILERNAME) filers, left(listagg(distinct FILERNAME, '; '),250) who, left(listagg(distinct c.cl, ' || '),250) clients
from s left join c on c.rid = s.rid group by 1,2 order by 1,2;

-- [6] Federal LDA filings for Sands / Kleinheinz / Success Academy by year
-- Federal LDA: Las Vegas Sands (and Kleinheinz / Success Academy) as client, by client name and year
select upper(CLIENT_NAME) client, FILING_YEAR, count(*) filings, count(distinct FILING_UUID) uuids, count(distinct REGISTRANT_NAME) registrants,
 left(listagg(distinct upper(REGISTRANT_NAME), '; '),200) regs,
 sum(try_to_number(INCOME,18,2)) income, sum(try_to_number(EXPENSES,18,2)) expenses, count(distinct CLIENT_ID) client_ids
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS
where upper(CLIENT_NAME) like '%LAS VEGAS SANDS%' or upper(CLIENT_NAME) like '%KLEINHEINZ%' or upper(CLIENT_NAME) like '%SUCCESS ACADEMY%' or upper(CLIENT_NAME) like '%ADELSON%'
   or upper(REGISTRANT_NAME) like '%LAS VEGAS SANDS%'
group by 1,2 order by 1,2;

-- [7] LDA Sands 2021-2026 dedup income + issue text
-- LDA Sands 2021-2026: filing types (amendments double-count?), income deduped to latest per registrant+client+year+period, issue text mentioning Texas/gaming/casino
with f as (
 select FILING_UUID, FILING_YEAR, FILING_PERIOD, FILING_TYPE, upper(REGISTRANT_NAME) reg, upper(CLIENT_NAME) cli, try_to_number(INCOME,18,2) inc, DT_POSTED,
  SPECIFIC_ISSUES, LOBBYING_ISSUES
 from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS
 where upper(CLIENT_NAME) like '%LAS VEGAS SANDS%' and FILING_YEAR >= '2021'
), d as (select * from f qualify row_number() over (partition by reg, FILING_YEAR, FILING_PERIOD order by DT_POSTED desc) = 1)
select FILING_YEAR, count(*) raw_filings, count_if(FILING_TYPE ilike '%A%' ) amend_or_reg_rows,
 (select sum(inc) from d where d.FILING_YEAR=f.FILING_YEAR) income_dedup, sum(inc) income_raw,
 count_if(SPECIFIC_ISSUES ilike '%texas%') texas_mentions, count_if(SPECIFIC_ISSUES ilike any ('%gaming%','%casino%','%gambl%')) gaming_mentions,
 left(listagg(distinct LOBBYING_ISSUES, ' ; '),250) issues, left(max(case when SPECIFIC_ISSUES ilike any ('%gaming%','%casino%','%texas%','%sports wager%') then SPECIFIC_ISSUES end),300) sample_issue
from f group by 1 order by 1;

-- [8] LDA lobbyist positions: Abboud and Sands' federal lobbyists
-- LDA lobbyist positions: any ABBOUD, and the named lobbyists on Sands federal filings 2021-2026 with covered positions
select 'ABBOUD anywhere' k, upper(LOBBYIST_FIRST_NAME||' '||LOBBYIST_LAST_NAME) nm, upper(REGISTRANT_NAME) reg, upper(CLIENT_NAME) cli, min(FILING_YEAR) y0, max(FILING_YEAR) y1, count(*) n, max(COVERED_POSITION) covered
from LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS where upper(LOBBYIST_LAST_NAME) = 'ABBOUD' group by 1,2,3,4
union all
select 'SANDS lobbyists', upper(LOBBYIST_FIRST_NAME||' '||LOBBYIST_LAST_NAME), upper(REGISTRANT_NAME), upper(CLIENT_NAME), min(FILING_YEAR), max(FILING_YEAR), count(*), left(max(COVERED_POSITION),120)
from LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS where upper(CLIENT_NAME) like '%LAS VEGAS SANDS%' and FILING_YEAR >= '2021' group by 1,2,3,4
order by 1,3,2;

-- [9] LDA positions coverage check
-- LDA positions table coverage: rows, years, distinct clients; any Sands client in any year; to explain the 0-row miss
select count(*) n, min(FILING_YEAR) y0, max(FILING_YEAR) y1, count(distinct FILING_UUID) filings, count(distinct upper(CLIENT_NAME)) clients,
 count_if(upper(CLIENT_NAME) like '%SANDS%') sands_rows, count_if(upper(LOBBYIST_LAST_NAME) like 'ABB%') abb_rows,
 count(distinct _LOADED_AT::date) load_days
from LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS;

-- [10] FEC indiv: Adelson donors w/ Sands employer or NV address, by cycle
-- FEC itemized individual gifts: donors named ADELSON with a Sands employer or a Las Vegas/NV address (second field), by donor and cycle; memo rows excluded
select upper(DONOR_NAME) donor, CYCLE_FILE, count(*) n, count(distinct CMTE_ID) cmtes, sum(TRANSACTION_AMT) amt,
 mode(upper(EMPLOYER)) emp, mode(upper(CITY)) city, mode(STATE) st
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where upper(DONOR_NAME) like 'ADELSON,%'
  and coalesce(MEMO_CD,'') <> 'X' and coalesce(IS_MEMO_TRANSACTION::string,'false') not in ('true','TRUE','True')
  and (upper(EMPLOYER) like '%SANDS%' or upper(EMPLOYER) like '%ADELSON%' or STATE = 'NV' or upper(CITY) like '%LAS VEGAS%')
group by 1,2 order by 2,5 desc;

-- [11] FEC Adelson -> committees -> candidates, Texas-tied
-- FEC: Sheldon + Miriam Adelson (NV address) gifts, joined CMTE_ID -> committees -> CAND_ID -> candidates; Texas-tied committees (committee in TX or candidate running in TX), all cycles
with g as (
 select CYCLE_FILE cyc, CMTE_ID, sum(TRANSACTION_AMT) amt, count(*) n, min(TRANSACTION_DATE) d0, max(TRANSACTION_DATE) d1,
  count_if(upper(DONOR_NAME) like 'ADELSON, SHELDON%') n_sheldon, count_if(upper(DONOR_NAME) like 'ADELSON, MIRIAM%') n_miriam
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
 where (upper(DONOR_NAME) like 'ADELSON, SHELDON%' or upper(DONOR_NAME) like 'ADELSON, MIRIAM%' or upper(DONOR_NAME) like 'ADELSON, MIRIAN%')
   and (STATE = 'NV' or upper(CITY) like '%LAS VEGAS%')
   and coalesce(MEMO_CD,'') <> 'X'
 group by 1,2),
 cm as (select CMTE_ID, any_value(CMTE_NM) nm, any_value(CMTE_ST) st, any_value(CMTE_TP) tp, any_value(CAND_ID) cand from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES group by 1),
 cd as (select CAND_ID, any_value(CAND_NAME) cnm, any_value(CAND_OFFICE_ST) cst, any_value(CAND_OFFICE) coff from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES group by 1)
select g.cyc, g.CMTE_ID, cm.nm, cm.st, cm.tp, cd.cnm, cd.cst, cd.coff, g.amt, g.n, g.n_sheldon, g.n_miriam, g.d0, g.d1,
 (select count(*) from g) all_rows, (select count(*) from g left join cm using (CMTE_ID) where cm.CMTE_ID is null) unmatched_cmte
from g left join cm on cm.CMTE_ID = g.CMTE_ID left join cd on cd.CAND_ID = cm.cand
where cm.st = 'TX' or cd.cst = 'TX' or upper(cm.nm) like '%TEXAS%'
order by g.cyc, g.amt desc;

-- [12] FEC Adelson per-cycle totals + unmatched committees
-- FEC Adelson: per-cycle totals (Sheldon+Miriam, NV, non-memo) and the committees that did NOT match the committee table (cycles 2018+), to check none are Texas
with g as (
 select CYCLE_FILE cyc, CMTE_ID, sum(TRANSACTION_AMT) amt, count(*) n
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
 where (upper(DONOR_NAME) like 'ADELSON, SHELDON%' or upper(DONOR_NAME) like 'ADELSON, MIRIAM%' or upper(DONOR_NAME) like 'ADELSON, MIRIAN%')
   and (STATE = 'NV' or upper(CITY) like '%LAS VEGAS%') and coalesce(MEMO_CD,'') <> 'X'
 group by 1,2),
 cm as (select CMTE_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES group by 1),
 alt as (select CMTE_ID, any_value(CMTE_NM) nm, any_value(CMTE_ST) st from LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE group by 1)
select 'TOTAL' k, cyc, null CMTE_ID, null nm, null st, sum(amt) amt, sum(n) n from g where cyc >= 2016 group by cyc
union all
select 'UNMATCHED', g.cyc, g.CMTE_ID, alt.nm, alt.st, g.amt, g.n from g left join cm using (CMTE_ID) left join alt using (CMTE_ID)
where cm.CMTE_ID is null and g.cyc >= 2018
order by 1, 2, 6 desc;

-- [13] Adelson-funded committees -> independent expenditures in Texas races
-- Adelson-funded committees (cycles 2022-2026) -> FEC independent expenditures (SPE_ID = CMTE_ID) on Texas races; non-superseded; plus each committee's Adelson $ and total IE $
with g as (
 select CMTE_ID, sum(TRANSACTION_AMT) adelson_amt
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
 where (upper(DONOR_NAME) like 'ADELSON, SHELDON%' or upper(DONOR_NAME) like 'ADELSON, MIRIAM%' or upper(DONOR_NAME) like 'ADELSON, MIRIAN%')
   and (STATE = 'NV' or upper(CITY) like '%LAS VEGAS%') and coalesce(MEMO_CD,'') <> 'X' and CYCLE_FILE >= 2022
 group by 1),
 ie as (select SPE_ID, any_value(SPE_NAM) spe, CAN_OFFICE_STATE st, upper(CAND_NAME) cand, CAN_OFFICE off, SUP_OPP, FEC_ELECTION_YR yr,
   sum(EXP_AMO) ie_amt, count(*) n, min(EXP_DATE) d0, max(EXP_DATE) d1
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
  where SPE_ID in (select CMTE_ID from g) and coalesce(IS_SUPERSEDED::string,'false') in ('false','FALSE','False','0')
  group by 1,3,4,5,6,7)
select g.CMTE_ID, ie.spe, g.adelson_amt, ie.st, ie.cand, ie.off, ie.SUP_OPP, ie.yr, ie.ie_amt, ie.n, ie.d0, ie.d1,
  (select sum(ie_amt) from ie i2 where i2.SPE_ID = g.CMTE_ID) spender_ie_total
from g join ie on ie.SPE_ID = g.CMTE_ID
where ie.st = 'TX'
order by ie.ie_amt desc limit 40;

-- [14] Sands/Adelson-named committees in FEC and IRS 527 registrations
-- Sands corporate PAC search: FEC committees with SANDS / ADELSON in name or connected org; IRS 8871 527 orgs with SANDS / ADELSON in name
select 'FEC' src, CMTE_ID id, any_value(CMTE_NM) nm, any_value(CONNECTED_ORG_NM) conn, any_value(CMTE_ST) st, any_value(CMTE_TP) tp, null ein
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES
where upper(CMTE_NM) like '%LAS VEGAS SANDS%' or upper(CONNECTED_ORG_NM) like '%LAS VEGAS SANDS%' or upper(CMTE_NM) like '%ADELSON%' or upper(CMTE_NM) like '%TEXAS SANDS%' or upper(CONNECTED_ORG_NM) like '%VENETIAN%'
group by 1,2
union all
select 'IRS8871', FORM_ID_NUMBER::string, any_value(ORG_NAME), null, any_value(MAILING_STATE), null, any_value(EIN)
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS
where upper(ORG_NAME) like '%SANDS%' or upper(ORG_NAME) like '%ADELSON%' or upper(ORG_NAME) like '%DESTINATION RESORT%' or upper(ORG_NAME) like '%TEXAS DESTINATION%'
group by 1,2
order by 1,3;
-- [14] FAILED: 000904 (42000): SQL compilation error: error line 6 at position 52
invalid identifier 'ORG_NAME'

-- [15] Rerun of [14] with ORGANIZATION_NAME, grouped by EIN
-- Sands corporate PAC search: FEC committees with SANDS / ADELSON in name or connected org; IRS 8871 527 orgs with SANDS / ADELSON in name
select 'FEC' src, CMTE_ID id, any_value(CMTE_NM) nm, any_value(CONNECTED_ORG_NM) conn, any_value(CMTE_ST) st, any_value(CMTE_TP) tp, null ein
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES
where upper(CMTE_NM) like '%LAS VEGAS SANDS%' or upper(CONNECTED_ORG_NM) like '%LAS VEGAS SANDS%' or upper(CMTE_NM) like '%ADELSON%' or upper(CMTE_NM) like '%TEXAS SANDS%' or upper(CONNECTED_ORG_NM) like '%VENETIAN%'
group by 1,2
union all
select 'IRS8871', EIN::string, any_value(ORGANIZATION_NAME), null, any_value(MAILING_STATE), null, any_value(EIN)
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS
where upper(ORGANIZATION_NAME) like '%SANDS%' or upper(ORGANIZATION_NAME) like '%ADELSON%' or upper(ORGANIZATION_NAME) like '%DESTINATION RESORT%' or upper(ORGANIZATION_NAME) like '%TEXAS DESTINATION%'
group by 1,2
order by 1,3;

-- [16] Texas Sands PAC + Texas Destination Resort Alliance PAC in IRS 527 tables (EIN)
-- Texas Sands PAC (EIN 874310226) and Texas Destination Resort Alliance PAC (862553314): 8871 registration details, 8872 report count, Schedule A and B totals (joined on EIN, padded)
with e as (select column1 ein from values ('874310226'),('862553314'))
select '8871' part, lpad(trim(o.EIN),9,'0') ein, o.ORGANIZATION_NAME nm, o.ESTABLISHED_DATE::string d, o.EXEMPT_8872_IND::string x1, o.MAILING_CITY||' '||o.MAILING_STATE loc, o.CUSTODIAN_NAME||' / '||o.CONTACT_NAME who, left(o.PURPOSE,160) info, null amt, null n
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS o where lpad(trim(o.EIN),9,'0') in (select ein from e)
union all
select '8872', lpad(trim(EIN),9,'0'), any_value(ORGANIZATION_NAME), min(PERIOD_BEGIN_DATE)::string||' to '||max(PERIOD_END_DATE)::string, null, null, null, null, sum(try_to_number(TOTAL_SCHED_A::string,18,2)), count(*)
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS where lpad(trim(EIN),9,'0') in (select ein from e) group by 2
union all
select 'SchA', lpad(trim(EIN::string),9,'0'), upper(CONTRIBUTOR_NAME), min(CONTRIBUTION_DATE)::string||' to '||max(CONTRIBUTION_DATE)::string, null, CONTRIBUTOR_CITY||' '||CONTRIBUTOR_STATE, CONTRIBUTOR_EMPLOYER, null, sum(CONTRIBUTION_AMOUNT), count(*)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS where lpad(trim(EIN::string),9,'0') in (select ein from e) group by 2,3,6,7
union all
select 'SchB', lpad(trim(EIN::string),9,'0'), upper(RECIPIENT_NAME), min(EXPENDITURE_DATE)::string||' to '||max(EXPENDITURE_DATE)::string, null, RECIPIENT_STATE, null, left(any_value(EXPENDITURE_PURPOSE),80), sum(EXPENDITURE_AMOUNT), count(*)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES where lpad(trim(EIN::string),9,'0') in (select ein from e) group by 2,3,6
order by 2,1,9 desc nulls last;

-- [17] Sands PAC federal gifts to candidates, TX share by cycle
-- Sands PAC (C00399642) -> committee-to-candidate gifts, by cycle: total, Texas candidates share, top TX recipients (CAND_ID join to candidates; memo rows excluded)
with t as (
 select c.CYCLE cyc, c.CAND_ID, cd.cnm, cd.cst, cd.coff, sum(c.TRANSACTION_AMT) amt, count(*) n
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE c
 left join (select CAND_ID, any_value(CAND_NAME) cnm, any_value(CAND_OFFICE_ST) cst, any_value(CAND_OFFICE) coff from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES group by 1) cd on cd.CAND_ID = c.CAND_ID
 where c.CMTE_ID = 'C00399642' and coalesce(c.MEMO_CD,'') <> 'X'
 group by 1,2,3,4,5)
select cyc, 'ALL' k, null cnm, sum(amt) amt, sum(n) n, count(distinct CAND_ID) cands, count_if(cst is null) unmatched_cand from t group by cyc
union all
select cyc, 'TX', listagg(cnm||' $'||amt::int, '; ') within group (order by amt desc), sum(amt), sum(n), count(distinct CAND_ID), null from t where cst = 'TX' group by cyc
order by cyc, k;

-- [18] FEC Kleinheinz + Success Academy staff donations
-- FEC: donors named KLEINHEINZ or employed by Kleinheinz Capital, and donors employed by Success Academy; by cycle, plus top recipient committees 2020-2026 (CMTE_ID -> committees)
with g as (
 select case when upper(EMPLOYER) like '%SUCCESS ACAD%' then 'SUCCESS ACADEMY staff' else 'KLEINHEINZ' end grp,
  upper(DONOR_NAME) donor, upper(CITY) city, STATE, CYCLE_FILE cyc, CMTE_ID, TRANSACTION_AMT amt
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
 where (upper(DONOR_NAME) like 'KLEINHEINZ,%' or upper(EMPLOYER) like '%KLEINHEINZ%' or upper(EMPLOYER) like '%SUCCESS ACADEM%')
   and coalesce(MEMO_CD,'') <> 'X'),
 cm as (select CMTE_ID, any_value(CMTE_NM) nm, any_value(CMTE_ST) st from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES group by 1)
select 'BYCYCLE' k, grp, cyc::string c, null nm, null st, sum(amt) amt, count(*) n, count(distinct donor) donors, left(listagg(distinct donor||' ('||city||' '||STATE||')', '; '),220) who
from g group by grp, cyc
union all
select * from (select 'TOPCMTE 2020+', grp, g.CMTE_ID, cm.nm, cm.st, sum(amt) a, count(*), count(distinct donor), null
 from g left join cm using (CMTE_ID) where cyc >= 2020 group by 2,3,4,5 qualify row_number() over (partition by grp order by a desc) <= 12)
order by 1,2,3;

-- [19] IRS 527 Schedule A gifts from Adelson / Sands entities
-- IRS 527 Schedule A: gifts from Adelsons (NV) or Las Vegas Sands / Venetian entities, deduped on EIN+date+contributor+amount (repeat-filing trap), by recipient 527 and year
with a as (
 select distinct lpad(trim(EIN::string),9,'0') ein, ORG_NAME, upper(CONTRIBUTOR_NAME) cn, CONTRIBUTOR_STATE st, CONTRIBUTION_DATE d, CONTRIBUTION_AMOUNT amt
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS
 where (upper(CONTRIBUTOR_NAME) like '%ADELSON%' and (CONTRIBUTOR_STATE = 'NV' or upper(CONTRIBUTOR_CITY) like '%LAS VEGAS%'))
    or upper(CONTRIBUTOR_NAME) like '%LAS VEGAS SANDS%' or upper(CONTRIBUTOR_NAME) like '%VENETIAN%CASINO%' or upper(CONTRIBUTOR_NAME) like 'SANDS %'
)
select ein, any_value(ORG_NAME) org, year(d) y, listagg(distinct cn, '; ') contributors, sum(amt) amt, count(*) n
from a group by ein, y order by amt desc limit 40;

-- [20] 527 Adelson/Sands gifts 2021-2026 by recipient, TX flag
-- IRS 527 Schedule A, Adelson/Sands gifts 2021-2026 (deduped): total by recipient; flag recipients whose 8871 mailing state is TX (EIN join); plus any 527 with 'TEXAS' in name
with a as (
 select distinct lpad(trim(EIN::string),9,'0') ein, ORG_NAME, upper(CONTRIBUTOR_NAME) cn, CONTRIBUTION_DATE d, CONTRIBUTION_AMOUNT amt
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS
 where ((upper(CONTRIBUTOR_NAME) like '%ADELSON%' and (CONTRIBUTOR_STATE = 'NV' or upper(CONTRIBUTOR_CITY) like '%LAS VEGAS%'))
    or upper(CONTRIBUTOR_NAME) like '%LAS VEGAS SANDS%' or upper(CONTRIBUTOR_NAME) like '%VENETIAN%CASINO%' or upper(CONTRIBUTOR_NAME) like 'SANDS %')
   and year(CONTRIBUTION_DATE) between 2021 and 2026),
 o as (select lpad(trim(EIN),9,'0') ein, any_value(MAILING_STATE) st from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS group by 1)
select a.ein, any_value(ORG_NAME) org, o.st, sum(amt) amt, count(*) n, min(d) d0, max(d) d1, count(*) over () recipients, sum(sum(amt)) over () all_amt
from a left join o on o.ein = a.ein group by a.ein, o.st order by amt desc;

-- [21] RGA/RAGA/RSLC Schedule B to Texas recipients 2021-2026
-- IRS 527 Schedule B, 2021-2026 (deduped on EIN+date+recipient+amount): RGA, RAGA, RSLC payments to Texas recipients; top 25 plus each 527's all-state total
with b as (
 select distinct lpad(trim(EIN::string),9,'0') ein, ORG_NAME, upper(trim(RECIPIENT_NAME)) r, RECIPIENT_STATE st, EXPENDITURE_DATE d, EXPENDITURE_AMOUNT amt, left(EXPENDITURE_PURPOSE,60) purp
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES
 where lpad(trim(EIN::string),9,'0') in ('113655877','464501717','050532524') and year(EXPENDITURE_DATE) between 2021 and 2026)
select * from (
 select ein, any_value(ORG_NAME) org, r, st, sum(amt) amt, count(*) n, min(d) d0, max(d) d1, any_value(purp) purp,
  sum(sum(amt)) over (partition by ein) org_all_states_dummy
 from b group by ein, r, st)
where st = 'TX' or r like '%TEXAS%' or r like '%ABBOTT%' or r like '%PAXTON%' or r like '%PATRICK%'
order by amt desc limit 25;

-- [22] Monthly media: Sands vs all others, deduped, by period month
-- Monthly TX lobby media spend by period month, 2021-2026: Abboud (Sands) vs all other filers; deduped to last-filed report per filer + period start (corrections replace originals)
with c as (
 select FILER_IDENT, FILER_NAME, PERIOD_START_DT, PERIOD_END_DT, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media, REPORT_INFO_IDENT, FILED_DT, REPORT_TYPE_CD
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
 where PERIOD_START_DT >= '2021-01-01'
 qualify row_number() over (partition by FILER_IDENT, PERIOD_START_DT, PERIOD_END_DT order by FILED_DT desc, REPORT_INFO_IDENT desc) = 1)
select to_char(date_trunc('month', PERIOD_START_DT::date),'YYYY-MM') m,
 sum(iff(ltrim(FILER_IDENT,'0')='85404', media, 0)) sands, sum(iff(ltrim(FILER_IDENT,'0')<>'85404', media, 0)) others,
 count_if(ltrim(FILER_IDENT,'0')<>'85404' and media > 0) other_filers_w_media,
 count_if(REPORT_TYPE_CD ilike '%ANN%' and media > 0) annual_rows_w_media
from c group by 1 order by 1;

-- [23] Gregg report; name-based 527 miss check; Abboud totals
-- Misc checks: (a) Aaron Gregg's 2024 Sands report on the cover; (b) name-based miss check for Texas Sands PAC / Texas Destination Resort Alliance in 8872, Schedule A, Schedule B; (c) Abboud totals recomputed
select 'GREGG' k, REPORT_INFO_IDENT::string id, FILER_NAME nm, REPORT_TYPE_CD||' '||PERIOD_START_DT::string info, try_to_number(TOTAL_EXPEND_MEDIA,18,2) amt1, try_to_number(TOTAL_EXPEND_FOOD,18,2) amt2, try_to_number(TOTAL_EXPEND_EVENT,18,2) amt3
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where REPORT_INFO_IDENT::string in (select REPORT_ID::string from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING where upper(ONBEHALFNAME) = 'LAS VEGAS SANDS')
union all select '8872 by name', EIN::string, ORGANIZATION_NAME, null, null, null, null from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS where upper(ORGANIZATION_NAME) like '%TEXAS SANDS%' or upper(ORGANIZATION_NAME) like '%DESTINATION RESORT%'
union all select 'SchA by name', EIN::string, any_value(ORG_NAME), null, sum(CONTRIBUTION_AMOUNT), count(*), null from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS where upper(ORG_NAME) like '%TEXAS SANDS%' or upper(ORG_NAME) like '%DESTINATION RESORT%' group by 2
union all select 'SchB by name', EIN::string, any_value(ORG_NAME), null, sum(EXPENDITURE_AMOUNT), count(*), null from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES where upper(ORG_NAME) like '%TEXAS SANDS%' or upper(ORG_NAME) like '%DESTINATION RESORT%' group by 2
union all select 'ABBOUD TOTAL', null, null, count(*)::string||' reports', sum(try_to_number(TOTAL_EXPEND_MEDIA,18,2)), sum(iff(PERIOD_START_DT between '2025-01-01' and '2025-04-01', try_to_number(TOTAL_EXPEND_MEDIA,18,2),0)), sum(iff(month(PERIOD_START_DT::date) in (1,2,3,4,5) and year(PERIOD_START_DT::date) in (2021,2023,2025), try_to_number(TOTAL_EXPEND_MEDIA,18,2),0))
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where ltrim(FILER_IDENT,'0') = '85404';

-- [24] Truth and Courage PAC donors + MAGA Inc TX IE rows
-- (a) Truth and Courage PAC (C00796045) itemized individual receipts by cycle, top 8 donors, Adelson share; (b) the two MAGA Inc $5M Texas IE rows (same line twice?)
with r as (select CYCLE_FILE cyc, upper(DONOR_NAME) d, upper(CITY)||' '||STATE loc, sum(TRANSACTION_AMT) amt, count(*) n
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS where CMTE_ID = 'C00796045' and coalesce(MEMO_CD,'') <> 'X' group by 1,2,3)
select * from (
 select 'T&C donors' k, cyc::string c, d, loc, amt, n, sum(amt) over (partition by cyc) cyc_total from r
 qualify row_number() over (partition by cyc order by amt desc) <= 8)
union all
select 'MAGA IE', TRAN_ID||' / '||IMAGE_NUM||' / '||FILE_NUM::string, upper(CAND_NAME)||' '||SUP_OPP, left(PUR,60)||' | '||left(PAY,40), EXP_AMO, null, AGG_AMO
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where SPE_ID = 'C00892471' and CAN_OFFICE_STATE = 'TX'
order by 1,2,5 desc;

-- [25] Minnehan's reports, clients, subjects
-- Julie Linn Minnehan (filer of the NY jet report): all her cover reports 2019-2026 with any spend, the clients named on each (REPORT_ID join), and subject lines
with cv as (select REPORT_INFO_IDENT::string rid, FORM_TYPE_CD, REPORT_TYPE_CD, APPLICABLE_YEAR, PERIOD_START_DT, FILED_DT,
   try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) trans, try_to_number(TOTAL_EXPEND_FOOD,18,2) food, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media, try_to_number(TOTAL_EXPEND_EVENT,18,2) evt
  from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where FILER_NAME ilike 'Minnehan%'),
 cl as (select REPORT_ID::string rid, listagg(distinct upper(ONBEHALFNAME), ' | ') clients from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING group by 1),
 sm as (select REPORT_ID::string rid, listagg(distinct SUBJECTMATTERCODEVALUE, '; ') subj from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1)
select cv.*, cl.clients, left(sm.subj,150) subj, count(*) over () all_reports
from cv left join cl using (rid) left join sm using (rid)
where coalesce(trans,0)+coalesce(food,0)+coalesce(media,0)+coalesce(evt,0) > 0 or cl.clients is not null
order by PERIOD_START_DT;
