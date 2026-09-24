-- #1
select table_name, listagg(column_name||':'||left(data_type,3), ' ') within group (order by ordinal_position) cols from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS where table_name in ('POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION','PROCUREMENT__FED_SAM_EXCLUSIONS','FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS','HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI','JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST','LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS','HEALTH__FED_FDA_FAERS_DEMO','JUSTICE__FED_COURTLISTENER_POSITIONS','ECONOMICS__FED_DOL_FORM5500','HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER','HEALTH__FED_CMS_MEDICARE_PROVIDER','HEALTH__FED_CMS_NURSING_HOME_PENALTIES','POLITICS__FED_GOVINFO_BILL_COSPONSORS','FINANCE__FED_SENATE_STOCK_WATCHER','HEALTH__FED_CMS_HOME_HEALTH','LABOR__FED_OSHA_ITA_CASE_DETAIL_2023','HEALTH__HOSPITAL_OFFICER_PAY','JUSTICE__FED_COURTLISTENER_JUDGE_RACES','LABOR__FED_DOL_OLMS','LABOR__FED_OSHA_ITA_CASE_DETAIL_2024','ECONOMICS__FED_FDIC_FAILED_BANKS','ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS','HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER','HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL','HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES','JUSTICE__FED_COURTLISTENER_COURTS','JUSTICE__INTL_UCDP_GED','LABOR__FED_OSHA_ITA_CASE_DETAIL_2025','POLITICS__BILL_COSPONSORS','POLITICS__FJC_JUDGE') group by 1;

-- #2
-- NYC CFB 2013: profile AMOUNT + top recipients, schedule mix
with b as (select RECIPIENT_NAME e, SCHEDULE s, try_to_double(AMOUNT::varchar) v, try_to_double(MATCH_AMOUNT::varchar) m from LIBRARY_MARTS.POLITICS.POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION)
select 'prof' k, count(*)::varchar a, count(v)::varchar b, min(v)::varchar c, median(v)::varchar d, max(v)::varchar e, sum(m)::varchar f from b
union all select * from (select 'sched', s, count(*)::varchar, min(v)::varchar, median(v)::varchar, max(v)::varchar, sum(m)::varchar from b group by s order by count(*) desc limit 12)
union all select * from (select 'top', e, count(*)::varchar, sum(v)::varchar, max(v)::varchar, null, sum(m)::varchar from b group by e order by sum(v) desc nulls last limit 12);

-- #3
-- SAM exclusions: type x status x currently-excluded, activation years
select EXCLUSION_TYPE, RECORD_STATUS, IS_CURRENTLY_EXCLUDED::varchar cur, IS_ENTITY_NOT_INDIVIDUAL::varchar ent, count(*) n, min(ACTIVATION_DATE)::varchar mn, max(ACTIVATION_DATE)::varchar mx, count(distinct nullif(UEI,'')) ueis from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS group by 1,2,3,4 order by n desc limit 25;

-- #4
-- UN sanctions: nationality, gender, list type, listed year
select 'nat' k, NATIONALITY v, count(*) n from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST group by 2 qualify row_number() over (order by n desc) <= 12
union all select 'gender', GENDER, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST group by 2
union all select 'list', UN_LIST_TYPE||'/'||RECORD_TYPE, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST group by 2
union all select 'interpol', HAS_INTERPOL_LINK::varchar, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST group by 2
union all select 'yr', left(LISTED_ON::varchar,4), count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST group by 2 order by 1, 3 desc;

-- #5
-- NAAG: money profile + top defendants
with b as (select DEFENDANTS e, YEAR y, try_to_double(regexp_replace(TOTALSETTLEMENTAMOUNT::varchar,'[$,]','')) t, try_to_double(regexp_replace(OTHER_SETTLEMENT_AMOUNT::varchar,'[$,]','')) o, TOTALSETTLEMENTAMOUNT raw from LIBRARY_MARTS.LEGAL_ENFORCEMENT.LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS)
select 'prof' k, count(*)::varchar a, count(t)::varchar b, count(o)::varchar c, median(t)::varchar d, max(t)::varchar e, sum(t)::varchar f, count(nullif(raw::varchar,''))::varchar g from b
union all select * from (select 'top', left(e,60), y::varchar, t::varchar, o::varchar, null,null,null from b order by t desc nulls last limit 15)
union all select * from (select 'rawsample', raw::varchar, null,null,null,null,null,null from b where t is null and nullif(raw::varchar,'') is not null limit 5);

-- #6
-- Senate stock watcher: amount bands and top senators
select 'amt' k, AMOUNT v, count(*) n from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_STOCK_WATCHER group by 2
union all select * from (select 'sen', SENATOR, count(*) n from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_STOCK_WATCHER group by 2 order by n desc limit 12)
union all select 'yr', year(TRANSACTION_DATE)::varchar, count(*) from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_STOCK_WATCHER group by 2 order by 1,3 desc;

-- #7
-- FDIC failed banks: loss profile, top losses
with b as (select BANK_NAME e, STATE_ABBR st, FAIL_DATE d, try_to_double(ESTIMATED_LOSS_THOUSANDS::varchar) l, try_to_double(TOTAL_ASSETS_THOUSANDS::varchar) a, RESOLUTION_TYPE r from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS)
select 'prof' k, count(*)::varchar a, count(l)::varchar b, median(l)::varchar c, max(l)::varchar d, sum(l)::varchar e, min(d)::varchar f from b
union all select * from (select 'top', e||' '||st, d::varchar, l::varchar, a::varchar, (l/nullif(a,0))::varchar, r from b order by l desc nulls last limit 12)
union all select * from (select 'ratio', e||' '||st, d::varchar, l::varchar, a::varchar, (l/nullif(a,0))::varchar, r from b where a>100000 order by l/nullif(a,0) desc nulls last limit 8);;

-- #8
-- NYC CFB: match vs amount per contributor per recipient (6:1 up to $175 = $1,050 cap)
with c as (select RECIPIENT_NAME r, CONTRIBUTOR_NAME n, ZIP z, sum(try_to_double(AMOUNT::varchar)) a, sum(try_to_double(MATCH_AMOUNT::varchar)) m, count(*) k from LIBRARY_MARTS.POLITICS.POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION where SCHEDULE='ABC' group by 1,2,3)
select 'dist' k, count(*)::varchar a, count_if(m>0)::varchar b, count_if(m>1050)::varchar c, count_if(m>6*a+0.01)::varchar d, max(m)::varchar e, sum(iff(m>1050,m-1050,0))::varchar f from c
union all select * from (select 'over', r, n, z, a::varchar, m::varchar, k::varchar from c where m>1050 or m>6*a+0.01 order by m desc limit 15);

-- #9
-- SAM: repeat UEIs, excluding agency, junk dates
with s as (select * from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS)
select 'agency' k, EXCLUDING_AGENCY v, count(*)::varchar n, count(distinct nullif(UEI,''))::varchar u from s group by 2 qualify row_number() over (order by count(*) desc)<=10
union all select * from (select 'repeatUEI', UEI||' '||max(coalesce(ENTITY_NAME,LAST_NAME)), count(*)::varchar, listagg(distinct EXCLUDING_AGENCY,',') from s where nullif(UEI,'') is not null group by UEI having count(*)>=3 order by count(*) desc limit 12)
union all select 'nUEI3plus', null, count(*)::varchar, null from (select UEI from s where nullif(UEI,'') is not null group by 1 having count(*)>=3)
union all select 'baddate', null, count_if(ACTIVATION_DATE > '2026-09-24' or ACTIVATION_DATE<'1975-01-01')::varchar, count_if(ACTIVATION_DATE > '2026-09-24')::varchar from s
union all select 'actyr', year(ACTIVATION_DATE)::varchar, count(*)::varchar, null from s where year(ACTIVATION_DATE) between 2015 and 2026 group by 2;

-- #10
-- FJC judge + CL judge races
select 'fjc_g' k, GENDER v, count(*) n from LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE group by 2
union all select 'fjc_r', RACE_OR_ETHNICITY, count(*) from LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE group by 2
union all select 'fjc_distinct_nid', null, count(distinct NID) from LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE
union all select 'cl_race', RACE_ID, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_RACES group by 2
union all select 'cl_persons', null, count(distinct PERSON_ID) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_RACES
union all select 'cl_multi', null, count(*) from (select PERSON_ID from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_RACES group by 1 having count(*)>1);

-- #11
-- CL courts
select 'jur' k, JURISDICTION v, count(*)::varchar n, count_if(IN_USE::varchar in ('true','True','1'))::varchar b, count_if(HAS_OPINION_SCRAPER::varchar in ('true','True','1'))::varchar c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_COURTS group by 2
union all select 'inuse', IN_USE::varchar, count(*)::varchar, null, null from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_COURTS group by 2
union all select 'cite_dupes', CITATION_STRING, count(*)::varchar, listagg(ID,',') within group (order by ID), null from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_COURTS where nullif(CITATION_STRING,'') is not null group by 2 having count(*)>=3
union all select 'pacer_yr', left(DATE_LAST_PACER_CONTACT::varchar,4), count(*)::varchar, null, null from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_COURTS group by 2;

-- #12
-- HUD PHA: operating fund profile + top, per-unit
with b as (select FORMAL_PARTICIPANT_NAME e, STD_STATE st, try_to_double(OPERATING_FUND_AMOUNT::varchar) o, try_to_double(CAPITAL_FUND_AMOUNT::varchar) c, try_to_double(TOTAL_DWELLING_UNITS::varchar) u, try_to_double(ACC_UNITS::varchar) acc, try_to_double(PUBLIC_HOUSING_OCCUPIED::varchar) occ from LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES)
select 'prof' k, count(*)::varchar a, count(o)::varchar b, count_if(o>0)::varchar c, median(nullif(o,0))::varchar d, max(o)::varchar e, sum(o)::varchar f from b
union all select * from (select 'top', e||' '||st, o::varchar, c::varchar, acc::varchar, occ::varchar, (o/nullif(acc,0))::varchar from b order by o desc nulls last limit 10)
union all select * from (select 'perunit', e||' '||st, o::varchar, c::varchar, acc::varchar, occ::varchar, (o/nullif(acc,0))::varchar from b where acc>=100 order by o/nullif(acc,0) desc nulls last limit 10)
union all select 'median_perunit', null, median(o/nullif(acc,0))::varchar, null,null,null,null from b where acc>=100;;

-- #13
-- IRS527 Sched A: profile + top orgs + amount>YTD rows
with b as (select ORG_NAME e, EIN, try_to_double(CONTRIBUTION_AMOUNT::varchar) v, try_to_double(AGG_CONTRIBUTION_YTD::varchar) y, CONTRIBUTION_DATE d from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS)
select 'prof' k, count(*)::varchar a, count(v)::varchar b, min(v)::varchar c, median(v)::varchar d, max(v)::varchar e, sum(v)::varchar f, count_if(v>y+1)::varchar g, min(d)::varchar h, max(d)::varchar i from b
union all select * from (select 'top', e, count(*)::varchar, sum(v)::varchar, max(v)::varchar, null,null,null,null,null from b group by e order by sum(v) desc nulls last limit 12)
union all select * from (select 'yr', year(d)::varchar, count(*)::varchar, sum(v)::varchar, null,null,null,null,null,null from b group by 2 order by 2);

-- #14
-- FAERS demo: death_dt fill, event years, countries
select 'prof' k, count(*)::varchar a, count(nullif(DEATH_DT::varchar,''))::varchar b, min(SRC_QUARTER)::varchar c, max(SRC_QUARTER)::varchar d, count(distinct CASEID)::varchar e from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO
union all select * from (select 'death_q', SRC_QUARTER::varchar, count(*)::varchar, count(nullif(DEATH_DT::varchar,''))::varchar, null, null from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO group by 2 order by 2)
union all select * from (select 'cty', REPORTER_COUNTRY, count(*)::varchar, count(nullif(DEATH_DT::varchar,''))::varchar, null,null from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO group by 2 order by count(*) desc limit 10);

-- #15
-- CL positions: vote pct + committee action
select 'jca' k, JUDICIAL_COMMITTEE_ACTION v, count(*)::varchar n, null a from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS group by 2
union all select 'vtype', VOTE_TYPE, count(*)::varchar, null from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS group by 2
union all select 'vyp', null, count(try_to_double(VOTES_YES_PERCENT::varchar))::varchar, min(try_to_double(VOTES_YES_PERCENT::varchar))||'/'||median(try_to_double(VOTES_YES_PERCENT::varchar))||'/'||max(try_to_double(VOTES_YES_PERCENT::varchar)) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS
union all select 'infer', HAS_INFERRED_VALUES::varchar, count(*)::varchar, null from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS group by 2
union all select * from (select 'close', PERSON_ID||' '||COURT_ID, VOTES_YES||'-'||VOTES_NO, DATE_CONFIRMATION::varchar from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS where try_to_double(VOTES_YES_PERCENT::varchar) is not null order by try_to_double(VOTES_YES_PERCENT::varchar) asc limit 12);

-- #16
-- Form 5500: participants profile, filing status, top plans by participants
with b as (select PLAN_NAME p, SPONSOR_DFE_NAME s, SPONS_DFE_EIN e, try_to_double(TOT_PARTCP_BOY_CNT::varchar) n, try_to_double(TOT_ACTIVE_PARTCP_CNT::varchar) a, FILING_STATUS f, FORM_YEAR y, try_to_double(TOTAL_ASSETS_BOY_AMT::varchar) ab from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500)
select 'prof' k, count(*)::varchar a, count(n)::varchar b, median(n)::varchar c, max(n)::varchar d, count(ab)::varchar e, count(distinct e)::varchar f from b
union all select 'fs', f, count(*)::varchar, null,null,null,null from b group by 2
union all select 'yr', y, count(*)::varchar, null,null,null,null from b group by 2
union all select * from (select 'top', s, p, n::varchar, a::varchar, e, null from b order by n desc nulls last limit 10)
union all select 'act>tot', null, count_if(a>n*1.5 and n>100)::varchar, null,null,null,null from b;

-- #17
-- Nursing home penalties: FINE_AMOUNT profile, bunching, top homes
with b as (select CMS_CERTIFICATION_NUMBER_CCN c, PROVIDER_NAME||' '||STATE e, try_to_double(FINE_AMOUNT::varchar) v, PENALTY_TYPE t from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES)
select 'prof' k, t a, count(*)::varchar b, count(v)::varchar c, min(v)::varchar d, median(v)::varchar e, max(v)::varchar f, sum(v)::varchar g from b group by t
union all select * from (select 'top', e, count(*)::varchar, sum(v)::varchar, max(v)::varchar, null,null,null from b where v>0 group by e order by sum(v) desc limit 10)
union all select * from (select 'band', floor(v/10000)*10000::varchar, count(*)::varchar, null,null,null,null,null from b where v between 50000 and 160000 group by 2 order by 2)
union all select * from (select 'repeat', v::varchar, count(*)::varchar, null,null,null,null,null from b where v>0 group by v order by count(*) desc limit 8);;

-- #18
-- Nursing home penalties: FINE_AMOUNT profile, bunching, top homes (fixed union types)
with b as (select CMS_CERTIFICATION_NUMBER_CCN c, PROVIDER_NAME||' '||STATE e, try_to_double(FINE_AMOUNT::varchar) v, PENALTY_TYPE::varchar t from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES)
select 'prof' k, t a, count(*)::varchar b, count(v)::varchar c, min(v)::varchar d, median(v)::varchar e, max(v)::varchar f, sum(v)::varchar g from b group by t
union all select * from (select 'top', e, count(*)::varchar, sum(v)::varchar, max(v)::varchar, null,null,null from b where v>0 group by e order by sum(v) desc limit 10)
union all select * from (select 'band', (floor(v/10000)*10000)::varchar, count(*)::varchar, null,null,null,null,null from b where v between 50000 and 160000 group by 2 order by 2)
union all select * from (select 'repeat', v::varchar, count(*)::varchar, null,null,null,null,null from b where v>0 group by v order by count(*) desc limit 8);

-- #19
-- GovInfo cosponsors vs BILL_COSPONSORS: shape, IS_ORIGINAL values, top members, congress range
select 'gov' t, min(CONGRESS)::varchar a, max(CONGRESS)::varchar b, count(*)::varchar c, count(distinct COSPONSOR_BIOGUIDE)::varchar d, count_if(IS_ORIGINAL::varchar in ('true','True','1','t','Y'))::varchar e, count(nullif(SPONSORSHIP_WITHDRAWN_DATE::varchar,''))::varchar f from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILL_COSPONSORS
union all select 'bill', min(CONGRESS)::varchar, max(CONGRESS)::varchar, count(*)::varchar, count(distinct COSPONSOR_BIOGUIDE)::varchar, count_if(IS_ORIGINAL::varchar in ('true','True','1','t','Y'))::varchar, count(nullif(SPONSORSHIP_WITHDRAWN_DATE::varchar,''))::varchar from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS
union all select * from (select 'gov_cong', CONGRESS::varchar, count(*)::varchar, count(distinct BILL_TYPE||BILL_NUMBER)::varchar, null,null,null from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILL_COSPONSORS group by 2 order by 2)
union all select * from (select 'bill_cong', CONGRESS::varchar, count(*)::varchar, count(distinct BILL_TYPE||BILL_NUMBER)::varchar, null,null,null from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS group by 2 order by 2)
union all select 'isorig_vals', IS_ORIGINAL::varchar, count(*)::varchar, null,null,null,null from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILL_COSPONSORS group by 2;

-- #20
-- top cosponsors in 118th (govinfo) and bill_cosponsors, with party
select 'gov' t, * from (select COSPONSOR_NAME||' '||COSPONSOR_PARTY||'-'||COSPONSOR_STATE n, count(*) c from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILL_COSPONSORS where CONGRESS=(select max(CONGRESS) from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILL_COSPONSORS) group by 1 order by 2 desc limit 10)
union all select 'bill', * from (select COSPONSOR_NAME||' '||COSPONSOR_PARTY||'-'||COSPONSOR_STATE n, count(*) c from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS where CONGRESS=(select max(CONGRESS) from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS) group by 1 order by 2 desc limit 10)
union all select 'bill_wd', * from (select COSPONSOR_NAME||' '||COSPONSOR_PARTY||'-'||COSPONSOR_STATE n, count(*) c from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS where IS_WITHDRAWN::varchar in ('true','True','1','t','Y') group by 1 order by 2 desc limit 8);;

-- #21
-- OSHA ITA case detail 2023/24/25: outcome values, deaths, date span, top companies by cases
with u as (
 select '2023' y, COMPANY_NAME c, EIN, INCIDENT_OUTCOME::varchar o, DATE_OF_INCIDENT::varchar d, DATE_OF_DEATH::varchar dd, try_to_double(ANNUAL_AVERAGE_EMPLOYEES::varchar) emp from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023
 union all select '2024', COMPANY_NAME, EIN, INCIDENT_OUTCOME::varchar, DATE_OF_INCIDENT::varchar, DATE_OF_DEATH::varchar, try_to_double(ANNUAL_AVERAGE_EMPLOYEES::varchar) from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024
 union all select '2025', COMPANY_NAME, EIN, INCIDENT_OUTCOME::varchar, DATE_OF_INCIDENT::varchar, DATE_OF_DEATH::varchar, try_to_double(ANNUAL_AVERAGE_EMPLOYEES::varchar) from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2025)
select 'prof' k, y, count(*)::varchar a, min(d) b, max(d) c, count(nullif(dd,''))::varchar e, median(emp)::varchar f, max(emp)::varchar g from u group by y
union all select 'outc', y||':'||o, count(*)::varchar, null,null,null,null,null from u group by y,o
union all select * from (select 'top', y||':'||c, count(*)::varchar, count_if(o='1')::varchar, max(emp)::varchar, null,null,null from u group by y,c qualify row_number() over (partition by y order by count(*) desc)<=6);

-- #22
-- OSHA deaths by company, all three years (INCIDENT_OUTCOME='1'), and per-year date spill
with u as (
 select '2023' y, COMPANY_NAME c, ESTABLISHMENT_NAME e, INCIDENT_OUTCOME::varchar o, DATE_OF_INCIDENT::varchar d from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023
 union all select '2024', COMPANY_NAME, ESTABLISHMENT_NAME, INCIDENT_OUTCOME::varchar, DATE_OF_INCIDENT::varchar from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024
 union all select '2025', COMPANY_NAME, ESTABLISHMENT_NAME, INCIDENT_OUTCOME::varchar, DATE_OF_INCIDENT::varchar from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2025)
select * from (select 'deaths' k, upper(c) n, count(*)::varchar a, listagg(distinct y,',') b from u where o='1' group by 2 order by count(*) desc limit 15)
union all select 'yrspill', y||':'||left(d,4), count(*)::varchar, null from u group by y, left(d,4) having count(*)>100;

-- #23
-- Chip Roy withdrawals: when and on what
select CONGRESS::varchar c, SPONSORSHIP_WITHDRAWN_DATE::varchar wd, count(*) n, min(BILL_TYPE||BILL_NUMBER) ex, min(SPONSORSHIP_DATE)::varchar sd, count_if(IS_ORIGINAL::varchar in ('true','True')) orig from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS where COSPONSOR_NAME like '%Roy, Chip%' and IS_WITHDRAWN::varchar in ('true','True','1','t','Y') group by 1,2 order by n desc limit 10;;

-- #24
-- Chip Roy: distinct bills among 521 withdrawn rows; and dupes in BILL_COSPONSORS
select 'roy' k, count(*)::varchar a, count(distinct BILL_TYPE||BILL_NUMBER)::varchar b, listagg(distinct BILL_TYPE||BILL_NUMBER, ',') within group (order by BILL_TYPE||BILL_NUMBER) c from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS where COSPONSOR_NAME like '%Roy, Chip%' and SPONSORSHIP_WITHDRAWN_DATE::varchar='2023-05-18'
union all select 'gov_roy', count(*)::varchar, count(distinct BILL_TYPE||BILL_NUMBER)::varchar, null from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILL_COSPONSORS where COSPONSOR_NAME like '%Roy, Chip%' and SPONSORSHIP_WITHDRAWN_DATE::varchar='2023-05-18'
union all select 'dupe_rows', count(*)::varchar, sum(n)::varchar, null from (select CONGRESS,BILL_TYPE,BILL_NUMBER,COSPONSOR_BIOGUIDE, count(*) n from LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS group by 1,2,3,4 having count(*)>1);

-- #25
-- OSHA annual average employees: junk outliers per year
with u as (
 select '2023' y, ESTABLISHMENT_NAME e, try_to_double(ANNUAL_AVERAGE_EMPLOYEES::varchar) emp, try_to_double(TOTAL_HOURS_WORKED::varchar) h from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023
 union all select '2024', ESTABLISHMENT_NAME, try_to_double(ANNUAL_AVERAGE_EMPLOYEES::varchar), try_to_double(TOTAL_HOURS_WORKED::varchar) from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024
 union all select '2025', ESTABLISHMENT_NAME, try_to_double(ANNUAL_AVERAGE_EMPLOYEES::varchar), try_to_double(TOTAL_HOURS_WORKED::varchar) from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2025)
select 'cnt' k, y, count_if(emp>=50000)::varchar a, count_if(emp>=1000000)::varchar b, count_if(h/nullif(emp,0)>8760)::varchar c from u group by y
union all select * from (select 'top', y||':'||e, emp::varchar, h::varchar, (h/nullif(emp,0))::varchar from u where emp>=1000000 group by y,e,emp,h order by emp desc limit 10);

-- #26
-- Hospital officer pay: hours outliers, other comp vs total, top by total
with b as (select HOSPITAL_NAME h, PERSON_NAME p, TITLE t, TAX_YEAR y, try_to_double(AVG_HOURS_PER_WEEK::varchar) hr, try_to_double(AVG_HOURS_PER_WEEK_RELATED_ORG::varchar) hr2, try_to_double(OTHER_COMPENSATION::varchar) o, try_to_double(TOTAL_COMPENSATION::varchar) tot, try_to_double(REPORTABLE_COMP_FROM_ORG::varchar) r1, try_to_double(REPORTABLE_COMP_FROM_RELATED_ORGS::varchar) r2 from LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY)
select 'prof' k, count(*)::varchar a, count(tot)::varchar b, median(nullif(tot,0))::varchar c, max(tot)::varchar d, count_if(hr+coalesce(hr2,0)>100)::varchar e, count_if(hr>168)::varchar f, count_if(abs(tot-(r1+coalesce(r2,0)+coalesce(o,0)))>1)::varchar g from b
union all select * from (select 'hours', h, p, t, y::varchar, hr::varchar, hr2::varchar, tot::varchar from b where hr+coalesce(hr2,0)>100 order by hr+coalesce(hr2,0) desc limit 8)
union all select * from (select 'othershare', h, p, t, y::varchar, o::varchar, tot::varchar, (o/nullif(tot,0))::varchar from b where tot>1000000 order by o desc limit 10)
union all select * from (select 'mismatch', h, p, t, y::varchar, (r1+coalesce(r2,0)+coalesce(o,0))::varchar, tot::varchar, null from b where abs(tot-(r1+coalesce(r2,0)+coalesce(o,0)))>1 order by abs(tot-(r1+coalesce(r2,0)+coalesce(o,0))) desc limit 6);;

-- #27
-- OLMS: assets profile, top, shortage amounts (money missing), terminate flag values
with b as (select UNION_NAME||' '||coalesce(DESIGNATION_PREFIX,'')||' '||coalesce(DESIGNATION_NUMBER::varchar,'')||' '||coalesce(STATE,'') e, FILE_NUMBER f, YEAR_COVERED::varchar y, FORM_TYPE ft, try_to_double(TOTAL_ASSETS::varchar) a, try_to_double(TOTAL_RECEIPTS::varchar) r, try_to_double(SHORTAGE_AMOUNT::varchar) s, TERMINATE_FLAG::varchar tf from LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS)
select 'prof' k, count(*)::varchar a, count(a)::varchar b, median(a)::varchar c, max(a)::varchar d, count_if(s>0)::varchar e, sum(s)::varchar f, min(y)||'-'||max(y) g from b
union all select 'tf', tf, count(*)::varchar, null,null,null,null,null from b group by tf
union all select * from (select 'topA', e, y, ft, a::varchar, r::varchar, null,null from b order by a desc nulls last limit 8)
union all select * from (select 'short', e, y, ft, a::varchar, r::varchar, s::varchar, f from b where s>0 order by s desc limit 15)
union all select * from (select 'shortyr', y, count(*)::varchar, null,null,null, sum(s)::varchar, null from b where s>0 group by y order by y);

-- #28
-- RCRA enforcements: penalty profile, top, types
with b as (select ID_NUMBER i, ACTIVITY_LOCATION st, ENFORCEMENT_TYPE t, ENFORCEMENT_DESC dsc, ENFORCEMENT_AGENCY ag, ENFORCEMENT_ACTION_DATE::varchar d, try_to_double(PMP_AMOUNT::varchar) p, try_to_double(FMP_AMOUNT::varchar) f, try_to_double(FSC_AMOUNT::varchar) s, try_to_double(SCR_AMOUNT::varchar) c from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS)
select 'prof' k, count(*)::varchar a, count_if(p>0)::varchar b, median(nullif(p,0))::varchar c, max(p)::varchar d, sum(p)::varchar e, count_if(f>0)::varchar f2, sum(f)::varchar g, min(d)||'..'||max(d) h from b
union all select * from (select 'top', i, st, dsc, ag, d, p::varchar, f::varchar, null from b order by greatest(coalesce(p,0),coalesce(f,0)) desc limit 12)
union all select * from (select 'fac', i, st, count(*)::varchar, sum(f)::varchar, null,null,null,null from b group by i, st order by count(*) desc limit 8)
union all select * from (select 'repeatF', f::varchar, count(*)::varchar, null,null,null,null,null,null from b where f>0 group by f order by count(*) desc limit 6);

-- #29
-- Medicare PROVIDER vs BY_PROVIDER: copies?
select 'prov' t, count(*) n, count(distinct NPI) d, sum(try_to_double(TOT_MDCR_ALOWD_AMT::varchar)) s, sum(try_to_double(TOT_MDCR_PYMT_AMT::varchar)) p, max(try_to_double(TOT_MDCR_ALOWD_AMT::varchar)) mx from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER
union all select 'byprov', count(*), count(distinct RNDRNG_NPI), sum(try_to_double(TOT_MDCR_ALOWD_AMT::varchar)), sum(try_to_double(TOT_MDCR_PYMT_AMT::varchar)), max(try_to_double(TOT_MDCR_ALOWD_AMT::varchar)) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER;;

-- #30
-- Medicare by provider: profile + top 10 + allowed vs paid gap
with b as (select RNDRNG_NPI n, RNDRNG_PRVDR_LAST_ORG_NAME||' '||coalesce(RNDRNG_PRVDR_FIRST_NAME,'') e, RNDRNG_PRVDR_TYPE t, RNDRNG_PRVDR_STATE_ABRVTN st, try_to_double(TOT_MDCR_ALOWD_AMT::varchar) a, try_to_double(TOT_MDCR_PYMT_AMT::varchar) p, try_to_double(DRUG_MDCR_ALOWD_AMT::varchar) d from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER)
select 'prof' k, count(*)::varchar a, count(a)::varchar b, median(a)::varchar c, max(a)::varchar d, (sum(p)/sum(a))::varchar e, count_if(p>a*1.01)::varchar f, null g from b
union all select * from (select 'top', n, e, t, st, a::varchar, p::varchar, (d/nullif(a,0))::varchar from b order by a desc limit 10)
union all select 'top1pct', null, null, null, null, sum(a)::varchar, null, null from (select a from b qualify percent_rank() over (order by a desc) < 0.01);

-- #31
-- Prov x service: avg allowed profile, top by est payment, allowed<paid
with b as (select RNDRNG_NPI n, RNDRNG_PRVDR_LAST_ORG_NAME e, HCPCS_CD h, HCPCS_DESC hd, PLACE_OF_SRVC pos, try_to_double(AVG_MDCR_ALOWD_AMT::varchar) a, try_to_double(AVG_MDCR_PYMT_AMT::varchar) p, try_to_double(TOT_SRVCS::varchar) s, try_to_double(TOT_BENES::varchar) bn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI)
select 'prof' k, count(*)::varchar a, count(a)::varchar b, median(a)::varchar c, max(a)::varchar d, sum(a*s)::varchar e, count_if(p>a*1.01)::varchar f, count_if(s/nullif(bn,0)>100)::varchar g from b
union all select * from (select 'topavg', n, e, h, left(hd,40), a::varchar, s::varchar, bn::varchar from b order by a desc limit 8)
union all select * from (select 'srv_per_bene', n, e, h, left(hd,40), a::varchar, s::varchar, bn::varchar from b where h not like 'J%' and a>50 order by s/nullif(bn,0) desc limit 8);

-- #32
-- DME by referrer: profile + top + suppression flag values
with b as (select RFRG_NPI n, RFRG_PRVDR_LAST_NAME_ORG||' '||coalesce(RFRG_PRVDR_FIRST_NAME,'') e, RFRG_PRVDR_SPCLTY_DESC sp, RFRG_PRVDR_STATE_ABRVTN st, try_to_double(SUPLR_MDCR_ALOWD_AMT::varchar) a, try_to_double(TOT_SUPLR_BENES::varchar) bn, IS_SUPPRESSED::varchar sup from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER)
select 'prof' k, count(*)::varchar a, count(a)::varchar b, median(a)::varchar c, max(a)::varchar d, sum(a)::varchar e, null f from b
union all select 'sup', sup, count(*)::varchar, sum(a)::varchar, null,null,null from b group by sup
union all select * from (select 'top', n, e, sp, st, a::varchar, bn::varchar from b order by a desc nulls last limit 10)
union all select * from (select 'perbene', n, e, sp, st, a::varchar, (a/nullif(bn,0))::varchar from b where bn>=20 order by a/nullif(bn,0) desc nulls last limit 8);;

-- #33
-- Skin substitutes (Q4100-Q4399) in Part B by provider x service: concentration, per-patient
with b as (select RNDRNG_NPI n, RNDRNG_PRVDR_LAST_ORG_NAME||' '||coalesce(RNDRNG_PRVDR_FIRST_NAME,'') e, RNDRNG_PRVDR_TYPE t, RNDRNG_PRVDR_STATE_ABRVTN st, HCPCS_CD h, try_to_double(AVG_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SRVCS::varchar) a, try_to_double(TOT_BENES::varchar) bn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI where HCPCS_CD between 'Q4100' and 'Q4399'),
p as (select n, e, t, st, sum(a) a, max(bn) mb, count(*) codes from b group by 1,2,3,4)
select 'tot' k, count(*)::varchar a, sum(a)::varchar b, median(a)::varchar c, (select sum(a) from (select a from p order by a desc limit 20))::varchar d, null e, null f from p
union all select * from (select 'top', n, e, t, st, a::varchar, mb::varchar from p order by a desc limit 15)
union all select * from (select 'state', st, count(*)::varchar, sum(a)::varchar, null,null,null from p group by st order by sum(a) desc limit 8)
union all select * from (select 'jeng', n, h, a::varchar, bn::varchar, null, null from b where n='1003053851' order by a desc limit 5);

-- #34
-- DME by supplier: profile avg allowed, top suppliers by total allowed (avg*srvcs), rental
with b as (select SUPLR_NPI n, SUPLR_PRVDR_LAST_NAME_ORG e, SUPLR_PRVDR_STATE_ABRVTN st, HCPCS_CD h, left(HCPCS_DESC,40) hd, try_to_double(AVG_SUPLR_MDCR_ALOWD_AMT::varchar) a, try_to_double(TOT_SUPLR_SRVCS::varchar) s, try_to_double(TOT_SUPLR_BENES::varchar) bn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL)
select 'prof' k, count(*)::varchar a, count(a)::varchar b, median(a)::varchar c, max(a)::varchar d, sum(a*s)::varchar e, count(distinct n)::varchar f from b
union all select * from (select 'topsup', n, e, st, sum(a*s)::varchar, count(*)::varchar, null from b group by n,e,st order by sum(a*s) desc nulls last limit 10)
union all select * from (select 'topcode', h, hd, null, sum(a*s)::varchar, count(distinct n)::varchar, null from b group by h,hd order by sum(a*s) desc nulls last limit 8)
union all select * from (select 'topavg', n, e, st, h||' '||hd, a::varchar, bn::varchar from b order by a desc nulls last limit 5);;

-- #35
-- Top DME suppliers: what codes, benes, per-bene
select SUPLR_PRVDR_LAST_NAME_ORG e, SUPLR_PRVDR_CITY c, HCPCS_CD h, left(HCPCS_DESC,35) hd, try_to_double(TOT_SUPLR_BENES::varchar) bn, try_to_double(TOT_SUPLR_SRVCS::varchar) s, round(try_to_double(AVG_SUPLR_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SUPLR_SRVCS::varchar)) a, round(try_to_double(AVG_SUPLR_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SUPLR_SRVCS::varchar)/nullif(try_to_double(TOT_SUPLR_BENES::varchar),0)) per_bene from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where SUPLR_NPI in ('1811518392','1487343505','1245259282','1700889227','1063414571','1588302186') qualify row_number() over (partition by SUPLR_NPI order by a desc) <= 3 order by e, a desc;

-- #36
-- Home health: spending ratio profile, top/bottom, ownership mix, star rating
with b as (select CCN, PROVIDER_NAME||' '||STATE e, STATE st, TYPE_OF_OWNERSHIP o, try_to_double(HOW_MUCH_MEDICARE_SPENDS_ON_AN_EPISODE_OF_CARE_AT_THIS_AGENCY_COMPARED_TO_MEDICARE_SPENDING_ACROSS_ALL_AGENCIES_NATIONALLY::varchar) r, try_to_double(QUALITY_OF_PATIENT_CARE_STAR_RATING::varchar) star, try_to_double(NO_OF_EPISODES_TO_CALC_HOW_MUCH_MEDICARE_SPENDS_PER_EPISODE_OF_CARE_AT_AGENCY_COMPARED_TO_SPENDING_AT_ALL_AGENCIES_NATIONAL::varchar) ep, try_to_double(PPH_RISK_STANDARDIZED_RATE::varchar) pph from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH)
select 'prof' k, count(*)::varchar a, count(r)::varchar b, min(r)::varchar c, median(r)::varchar d, max(r)::varchar e, count(distinct CCN)::varchar f from b
union all select * from (select 'top', e, o, r::varchar, star::varchar, ep::varchar, pph::varchar from b where ep>=50 order by r desc nulls last limit 10)
union all select * from (select 'state', st, count(r)::varchar, avg(r)::varchar, avg(star)::varchar, count_if(r>=1.5)::varchar, null from b group by st order by avg(r) desc nulls last limit 8)
union all select 'own', o, count(r)::varchar, avg(r)::varchar, avg(star)::varchar, count_if(r>=1.5)::varchar, null from b group by o;

-- #37
-- UCDP GED: deaths profile, by year, top conflicts, code_status, active_year values
with b as (select YEAR y, CONFLICT_NAME c, COUNTRY cty, try_to_double(BEST::varchar) best, try_to_double(DEATHS_CIVILIANS::varchar) civ, CODE_STATUS cs, ACTIVE_YEAR::varchar ay, TYPE_OF_VIOLENCE::varchar tv from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_UCDP_GED)
select 'prof' k, count(*)::varchar a, count(best)::varchar b, median(best)::varchar c, max(best)::varchar d, sum(best)::varchar e, (min(y)||'-'||max(y)) f from b
union all select 'cs', cs, count(*)::varchar, sum(best)::varchar, null,null,null from b group by cs
union all select 'ay', ay, count(*)::varchar, sum(best)::varchar, null,null,null from b group by ay
union all select * from (select 'yr', y::varchar, count(*)::varchar, sum(best)::varchar, sum(civ)::varchar, null,null from b group by y order by y desc limit 8)
union all select * from (select 'topc', c, cty, count(*)::varchar, sum(best)::varchar, sum(civ)::varchar, null from b group by c, cty order by sum(best) desc limit 10)
union all select * from (select 'biggest', c, y::varchar, best::varchar, civ::varchar, tv, null from b order by best desc limit 6);;

-- #38
-- Senate: the biggest bands
select SENATOR, TRANSACTION_DATE::varchar d, OWNER, TICKER, left(ASSET_DESCRIPTION,50) a, TYPE, AMOUNT from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_STOCK_WATCHER where AMOUNT in ('Over $50,000,000','$25,000,001 - $50,000,000','$5,000,001 - $25,000,000') order by AMOUNT desc;

-- #39
-- IRS527: biggest single rows
select ORG_NAME, CONTRIBUTOR_NAME, CONTRIBUTOR_CITY||' '||CONTRIBUTOR_STATE w, CONTRIBUTION_DATE::varchar d, try_to_double(CONTRIBUTION_AMOUNT::varchar) v, try_to_double(AGG_CONTRIBUTION_YTD::varchar) y from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS order by v desc nulls last limit 12;;

-- #40
-- IRS527: summary/total rows mixed in with itemized gifts
with b as (select ORG_NAME o, upper(CONTRIBUTOR_NAME) n, try_to_double(CONTRIBUTION_AMOUNT::varchar) v from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS),
f as (select *, (n like '%SUM OF TRANSACTIONS%' or n like '%AGGREGATE BELOW%' or n like 'TOTAL %' or n like '%SCHEDULE A%' or n like '%RECEIPTS FROM%' or n like '%UNITEMIZED%' or n like '%NON-ITEMIZED%' or n like '%NONITEMIZED%') s from b)
select 'all' k, count_if(s)::varchar a, sum(iff(s,v,0))::varchar b, sum(v)::varchar c, (sum(iff(s,v,0))/sum(v))::varchar d from f
union all select * from (select 'byorg', o, count_if(s)::varchar, sum(iff(s,v,0))::varchar, (sum(iff(s,v,0))/sum(v))::varchar from f group by o having sum(iff(s,v,0))>0 order by sum(iff(s,v,0)) desc limit 10)
union all select * from (select 'names', n, count(*)::varchar, sum(v)::varchar, null from f where s group by n order by sum(v) desc limit 10);;

