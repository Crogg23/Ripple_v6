-- #1 other vintages: any table named like DME / durable medical in raw or marts
select 'RAW' db, table_schema, table_name, row_count from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_name ilike any ('%DURABLE%','%DMEPOS%','%\_DME\_%','%DME\_%','%SUPPLIER%','%ALGINATE%')
union all
select 'MARTS', table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike any ('%DURABLE%','%DMEPOS%','%\_DME\_%','%DME\_%','%SUPPLIER%')
order by 1,3;

-- #2 alginate codes A6196-A6199: whole-file paid, allowed, benes, suppliers; and the two suppliers
with s as (select SUPLR_NPI npi, HCPCS_CD c, try_to_number(TOT_SUPLR_SRVCS) sv, try_to_number(TOT_SUPLR_BENES) b, AVG_SUPLR_MDCR_PYMT_AMT p, AVG_SUPLR_MDCR_ALOWD_AMT a
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where HCPCS_CD in ('A6196','A6197','A6198','A6199'))
select c, count(distinct npi) suppliers, round(sum(sv*p)) paid, round(sum(sv*a)) allowed, sum(b) benes_rowsum, sum(sv) services,
 round(sum(iff(npi='1811518392',sv*p,0))) sunshine_paid, round(sum(iff(npi='1487343505',sv*p,0))) almaz_paid,
 sum(iff(npi in ('1811518392','1487343505'),b,0)) two_benes, count_if(b is null) null_benes
from s group by rollup(c) order by c nulls last;

-- #3 A6197 per supplier: top 12 plus peer median (suppliers with a published bene count)
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_CITY) city, max(SUPLR_PRVDR_STATE_ABRVTN) st,
  sum(try_to_number(TOT_SUPLR_SRVCS)) sv, sum(try_to_number(TOT_SUPLR_BENES)) b, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where HCPCS_CD='A6197' group by 1)
select * from (select 'top' k, npi, org, city, st, sv, b, round(paid) paid, round(paid/nullif(b,0)) paid_per_bene, round(sv/nullif(b,0)) units_per_bene from s order by paid desc limit 12)
union all
select 'peer_median_excl_two', count(*)::varchar, null, null, null, median(sv), median(b), round(median(paid)), round(median(paid/nullif(b,0))), round(median(sv/nullif(b,0))) from s where b is not null and npi not in ('1811518392','1487343505')
union all
select 'peer_top10_excl_two_median', null,null,null,null, median(sv), median(b), round(median(paid)), round(median(ppb)), round(median(upb)) from (select sv,b,paid,paid/nullif(b,0) ppb, sv/nullif(b,0) upb from s where b is not null and npi not in ('1811518392','1487343505') order by paid desc limit 10);

-- #4 every row the two suppliers have in the supplier file
select SUPLR_NPI, SUPLR_PRVDR_LAST_NAME_ORG, SUPLR_PRVDR_ST1, SUPLR_PRVDR_ST2, SUPLR_PRVDR_CITY, SUPLR_PRVDR_STATE_ABRVTN, SUPLR_PRVDR_ZIP5, SUPLR_PRVDR_SPCLTY_DESC, HCPCS_CD, left(HCPCS_DESC,50) d, SUPLR_RENTL_IND,
 TOT_SUPLR_BENES, TOT_SUPLR_CLMS, TOT_SUPLR_SRVCS, AVG_SUPLR_MDCR_PYMT_AMT, round(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where SUPLR_NPI in ('1811518392','1487343505') order by 1, paid desc;

-- #5 NPPES for the two NPIs
select NPI, ENTITY_TYPE_CODE, PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME lbn, PROVIDER_OTHER_ORGANIZATION_NAME dba, PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a1, PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a2,
 PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME city, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE zip, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER tel,
 PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS m1, PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME mcity,
 PROVIDER_ENUMERATION_DATE, LAST_UPDATE_DATE, NPI_DEACTIVATION_DATE, NPI_REACTIVATION_DATE, CERTIFICATION_DATE,
 AUTHORIZED_OFFICIAL_FIRST_NAME aof, AUTHORIZED_OFFICIAL_MIDDLE_NAME aom, AUTHORIZED_OFFICIAL_LAST_NAME aol, AUTHORIZED_OFFICIAL_TITLE_OR_POSITION aot, AUTHORIZED_OFFICIAL_TELEPHONE_NUMBER aotel,
 HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx1, HEALTHCARE_PROVIDER_TAXONOMY_CODE_2 tx2, PROVIDER_LICENSE_NUMBER_1 lic1, PROVIDER_LICENSE_NUMBER_STATE_CODE_1 licst, OTHER_PROVIDER_IDENTIFIER_1 oid1, OTHER_PROVIDER_IDENTIFIER_TYPE_CODE_1 oidt1, IS_ORGANIZATION_SUBPART, PARENT_ORGANIZATION_LBN
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in ('1811518392','1487343505');

-- #6 LEIE and SAM: the two NPIs, or the names
select 'LEIE' src, NPI, BUSINESS_NAME nm, LAST_NAME||', '||FIRST_NAME person, SPECIALTY, EXCLUSION_TYPE, EXCLUSION_DATE::varchar dt, ADDRESS, CITY, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
 where NPI in ('1811518392','1487343505') or BUSINESS_NAME ilike '%SUNSHINE SENIOR%' or BUSINESS_NAME ilike '%ALMAZ%'
union all
select 'SAM', NPI, ENTITY_NAME, LAST_NAME||', '||FIRST_NAME, EXCLUDING_AGENCY, EXCLUSION_TYPE, ACTIVATION_DATE::varchar, CLASSIFICATION, CITY, STATE from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS
 where NPI in ('1811518392','1487343505') or ENTITY_NAME ilike '%SUNSHINE SENIOR%' or ENTITY_NAME ilike '%ALMAZ%';

-- #7 NPPES siblings: same authorized-official surname, same street, or same phone as either supplier
select NPI, ENTITY_TYPE_CODE, coalesce(PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME, PROVIDER_LAST_NAME_LEGAL_NAME||', '||PROVIDER_FIRST_NAME) nm,
 PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a1, PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS a2, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME city, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st,
 PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER tel, PROVIDER_ENUMERATION_DATE enum_dt, NPI_DEACTIVATION_DATE deact,
 AUTHORIZED_OFFICIAL_FIRST_NAME||' '||AUTHORIZED_OFFICIAL_LAST_NAME ao, AUTHORIZED_OFFICIAL_TITLE_OR_POSITION aot, AUTHORIZED_OFFICIAL_TELEPHONE_NUMBER aotel, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx1,
 case when AUTHORIZED_OFFICIAL_LAST_NAME ilike any ('PESSOA','TSOTSKHALASHVILI') or PROVIDER_LAST_NAME_LEGAL_NAME ilike any ('PESSOA','TSOTSKHALASHVILI') then 'name'
      when PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS ilike any ('100 E LINTON BLVD%','4407 69TH ST%') or PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS ilike any ('100 E LINTON BLVD%','4407 69TH ST%') then 'address'
      else 'phone' end why
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
where AUTHORIZED_OFFICIAL_LAST_NAME ilike any ('PESSOA','TSOTSKHALASHVILI')
   or PROVIDER_LAST_NAME_LEGAL_NAME ilike any ('TSOTSKHALASHVILI')
   or (PROVIDER_LAST_NAME_LEGAL_NAME ilike 'PESSOA' and PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME='FL')
   or PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS ilike any ('100 E LINTON BLVD%','4407 69TH ST%')
   or PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS ilike any ('100 E LINTON BLVD%','4407 69TH ST%')
   or PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER in ('5613323898','7185706626','9297033500')
   or AUTHORIZED_OFFICIAL_TELEPHONE_NUMBER in ('5613323898','7185706626','9297033500')
order by why, enum_dt;

-- #8 PECOS enrollment rows for the two NPIs, and anything sharing their PAC id
with me as (select NPI, PECOS_ASCT_CNTL_ID pac from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT where NPI in ('1811518392','1487343505'))
select p.NPI, p.PECOS_ASCT_CNTL_ID, p.ENRLMT_ID, p.PROVIDER_TYPE_CD, p.PROVIDER_TYPE_DESC, p.STATE_CD, p.ORG_NAME, p.LAST_NAME, p.FIRST_NAME, iff(p.NPI in (select NPI from me),'self','shares PAC') rel
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT p where p.NPI in (select NPI from me) or p.PECOS_ASCT_CNTL_ID in (select pac from me);

-- #9 LEIE people by the two officials' surnames; FJC criminal and civil by names; ICIJ officers
select 'LEIE' src, LAST_NAME||', '||FIRST_NAME||' '||coalesce(BUSINESS_NAME,'') nm, SPECIALTY a, EXCLUSION_TYPE b, EXCLUSION_DATE::varchar c, CITY||' '||STATE d from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where LAST_NAME ilike any ('PESSOA','TSOTSKHALASHVILI')
union all
select 'FJC_CRIM', DEFENDANT_NAME, DISTRICT::varchar, DOCKET::varchar, FILE_DATE::varchar, FILING_TITLE_1||'/'||FILING_OFFENSE_CODE_1 from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL
 where DEFENDANT_NAME ilike any ('%PESSOA%','%TSOTSKHALASHVILI%','%SUNSHINE SENIOR%','%ALMAZ MED%')
union all
select 'FJC_CIV', PLAINTIFF||' v '||DEFENDANT, DISTRICT::varchar, DOCKET::varchar, FILE_DATE::varchar, NATURE_OF_SUIT::varchar from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
 where PLAINTIFF ilike any ('%SUNSHINE SENIOR%','%ALMAZ MED%','%TSOTSKHALASHVILI%') or DEFENDANT ilike any ('%SUNSHINE SENIOR%','%ALMAZ MED%','%TSOTSKHALASHVILI%','%PESSOA, DANA%','DANA%PESSOA%')
union all
select 'ICIJ', NAME, COUNTRIES, SOURCE_LEAK, null, null from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS where NAME ilike any ('%TSOTSKHALASHVILI%','%DANA%PESSOA%');

-- #10 PPP (150K+ file): the two names, or their addresses
select BORROWERNAME, BORROWERADDRESS, BORROWERCITY, BORROWERSTATE, DATEAPPROVED::varchar, CURRENTAPPROVALAMOUNT, FORGIVENESSAMOUNT, NAICSCODE, JOBSREPORTED
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
where BORROWERNAME ilike any ('%SUNSHINE SENIOR%','%ALMAZ MED%') or BORROWERADDRESS ilike any ('100 E LINTON BLVD%','4407 69TH ST%')
   or (BORROWERSTATE in ('FL','NY') and BORROWERNAME ilike any ('%MEDICAL SUPPL%','%MED SUPPL%','%DME%') and BORROWERCITY ilike any ('DELRAY BEACH','WOODSIDE'));

-- #11 PECOS coverage check: are big DME suppliers in the PECOS enrollment table at all?
with s as (select SUPLR_NPI npi, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL group by 1),
 r as (select npi, paid, row_number() over (order by paid desc) rk from s),
 p as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT)
select iff(rk<=50,'top50','rest') grp, count(*) suppliers, count(p.NPI) in_pecos,
 listagg(iff(rk<=50 and p.NPI is null, r.npi, null), ',') within group (order by rk) top50_missing
from r left join p on r.npi=p.NPI group by 1;

-- #12 the June-2026 1128Aa DME batch in LEIE: who, where, when, and billing in the supplier file (NPI join)
with l as (select NPI, BUSINESS_NAME, SPECIALTY, EXCLUSION_DATE, CITY, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where EXCLUSION_TYPE='1128Aa' and EXCLUSION_DATE between '2026-06-01' and '2026-06-30'),
 s as (select SUPLR_NPI, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid, sum(iff(HCPCS_CD='A6197',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) alg, sum(iff(HCPCS_CD='A4353',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) cath from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL group by 1)
select l.EXCLUSION_DATE::varchar dt, l.BUSINESS_NAME, l.SPECIALTY, l.CITY, l.STATE, l.NPI, round(s.paid) paid, round(s.alg) alginate, round(s.cath) catheter from l left join s on l.NPI=s.SUPLR_NPI order by dt, l.STATE;

-- #13 other DME suppliers in the two ZIPs (33483 Delray Beach, 11377 Woodside) and the two DME-taxonomy neighbors at 100 E Linton
select SUPLR_NPI, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_ST1) st1, max(SUPLR_PRVDR_ZIP5) zip, count(*) codes, round(sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT)) paid,
 listagg(distinct HCPCS_CD, ',') within group (order by HCPCS_CD) hcpcs
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL
where SUPLR_PRVDR_ZIP5 in ('33483','11377') or SUPLR_NPI in ('1326505710','1083959159') group by 1 order by paid desc;

-- #14 DOJ press-release link text (Wayback replay), FCA settlements, CourtListener dockets: names and alginate
select 'DOJ_LISTING' src, CAPTURED_AT::varchar dt, LINK_TEXT txt, RESOLVED_URL url from LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
 where LINK_TEXT ilike any ('%SUNSHINE SENIOR%','%ALMAZ%','%PESSOA%','%TSOTSKHALASHVILI%','%ALGINATE%','%WOUND DRESSING%','%CATHETER%')
union all
select 'FCA', SETTLEMENT_DATE::varchar, CASE_TITLE||' / '||coalesce(PERSON_NAME,''), PRESS_RELEASE_URL from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_DOJ_FCA_SETTLEMENTS
 where CASE_TITLE ilike any ('%SUNSHINE%','%ALMAZ%') or PERSON_NAME ilike any ('%PESSOA%','%TSOTSKHALASHVILI%')
union all
select 'CL_DOCKET', DATE_FILED::varchar, CASE_NAME||' | '||coalesce(DOCKET_NUMBER,'')||' | court '||coalesce(COURT_ID,''), CAUSE from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
 where CASE_NAME ilike any ('%SUNSHINE SENIOR SOLUTIONS%','%ALMAZ MED%','%TSOTSKHALASHVILI%','%DANA PESSOA%','%PESSOA, DANA%','%V. PESSOA%');

-- #15 top 15 A6197 suppliers: NPPES enumeration date + official, PECOS presence, LEIE presence (all on NPI)
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid, sum(try_to_number(TOT_SUPLR_BENES)) b
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where HCPCS_CD='A6197' group by 1 order by paid desc limit 15)
select s.npi, s.org, s.st, round(s.paid) paid, s.b, n.PROVIDER_ENUMERATION_DATE::varchar enum_dt, n.NPI_DEACTIVATION_DATE::varchar deact, n.AUTHORIZED_OFFICIAL_FIRST_NAME||' '||n.AUTHORIZED_OFFICIAL_LAST_NAME ao,
 (select count(*) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT p where p.NPI=s.npi) pecos_rows,
 (select max(EXCLUSION_DATE)::varchar from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l where l.NPI=s.npi) leie_dt
from s left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi order by s.paid desc;

-- #16 the 13 top-50 suppliers missing from PECOS: name, state, catheter and alginate money, LEIE date, NPPES enumeration; plus PECOS landing ingest stamp
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid,
  sum(iff(HCPCS_CD='A4353',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) cath, sum(iff(HCPCS_CD='A6197',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) alg
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where SUPLR_NPI in ('1811518392','1487343505','1063414571','1588302186','1689457772','1790533503','1528004108','1225009665','1871564211','1578139473','1629247036','1003970260','1881972040') group by 1)
select s.npi, s.org, s.st, round(s.paid) paid, round(s.cath) cath, round(s.alg) alg, n.PROVIDER_ENUMERATION_DATE::varchar enum_dt, n.AUTHORIZED_OFFICIAL_FIRST_NAME||' '||n.AUTHORIZED_OFFICIAL_LAST_NAME ao,
 (select max(EXCLUSION_DATE)::varchar from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l where l.NPI=s.npi) leie_dt,
 (select to_varchar(max(_INGESTED_AT)) from LIBRARY_RAW.LANDING.FED_CMS_PECOS_PROVIDER_ENROLLMENT) pecos_ingest
from s left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi order by s.paid desc;

-- #16b the 13 top-50 suppliers missing from PECOS (rewritten with joins): name, catheter/alginate money, LEIE date, NPPES enumeration; plus PECOS landing ingest stamp
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid,
  sum(iff(HCPCS_CD='A4353',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) cath, sum(iff(HCPCS_CD='A6197',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) alg
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where SUPLR_NPI in ('1811518392','1487343505','1063414571','1588302186','1689457772','1790533503','1528004108','1225009665','1871564211','1578139473','1629247036','1003970260','1881972040') group by 1),
 l as (select NPI, max(EXCLUSION_DATE)::varchar leie_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI in (select npi from s) group by 1),
 g as (select to_varchar(min(_INGESTED_AT)) mi, to_varchar(max(_INGESTED_AT)) ma from LIBRARY_RAW.LANDING.FED_CMS_PECOS_PROVIDER_ENROLLMENT)
select s.npi, s.org, s.st, round(s.paid) paid, round(s.cath) cath, round(s.alg) alg, n.PROVIDER_ENUMERATION_DATE::varchar enum_dt, n.AUTHORIZED_OFFICIAL_FIRST_NAME||' '||n.AUTHORIZED_OFFICIAL_LAST_NAME ao, l.leie_dt, g.mi pecos_ingest_min, g.ma pecos_ingest_max
from s left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi left join l on l.NPI=s.npi cross join g order by s.paid desc;

-- #16c the 13 top-50 suppliers missing from PECOS (rewritten with joins): name, catheter/alginate money, LEIE date, NPPES enumeration; plus PECOS landing ingest stamp
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid,
  sum(iff(HCPCS_CD='A4353',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) cath, sum(iff(HCPCS_CD='A6197',try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT,0)) alg
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL where SUPLR_NPI in ('1811518392','1487343505','1063414571','1588302186','1689457772','1790533503','1528004108','1225009665','1871564211','1578139473','1629247036','1003970260','1881972040') group by 1),
 l as (select NPI, max(EXCLUSION_DATE)::varchar leie_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI in (select npi from s) group by 1),
 g as (select to_varchar(min(INGESTED_AT)) mi, to_varchar(max(INGESTED_AT)) ma from LIBRARY_RAW.LANDING.FED_CMS_PECOS_PROVIDER_ENROLLMENT)
select s.npi, s.org, s.st, round(s.paid) paid, round(s.cath) cath, round(s.alg) alg, n.PROVIDER_ENUMERATION_DATE::varchar enum_dt, n.AUTHORIZED_OFFICIAL_FIRST_NAME||' '||n.AUTHORIZED_OFFICIAL_LAST_NAME ao, l.leie_dt, g.mi pecos_ingest_min, g.ma pecos_ingest_max
from s left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi left join l on l.NPI=s.npi cross join g order by s.paid desc;

-- #17 same product menu: suppliers billing catheters (A4353), alginate (A6197), CGM supplies (A4239) and knee+wrist braces (L1852, L3916) together
with s as (select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT) paid,
  count(distinct iff(HCPCS_CD in ('A4353','A6197','A4239','L1852','L3916'), HCPCS_CD, null)) menu, count(distinct HCPCS_CD) codes,
  sum(iff(HCPCS_CD in ('A4353','A6197'), try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT, 0)) cath_alg
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL group by 1)
select menu, count(*) suppliers, round(sum(paid)) paid, listagg(iff(menu>=4, org||' ('||st||') $'||round(paid/1e6,1)||'M/'||codes||' codes', null), '; ') within group (order by paid desc) who
from s where menu>=3 group by 1 order by 1 desc;

-- #18 the two suppliers' share of each code they bill, nationally (paid and patients-rowsum)
with s as (select SUPLR_NPI npi, HCPCS_CD c, try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT p, try_to_number(TOT_SUPLR_BENES) b
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL
  where HCPCS_CD in ('A4353','A6197','A4239','E2103','L1852','L3916','L0651','L0486'))
select c, count(distinct npi) suppliers, round(sum(p)) paid, round(sum(iff(npi='1811518392',p,0))) sunshine, round(sum(iff(npi='1487343505',p,0))) almaz,
 round(100*sum(iff(npi in ('1811518392','1487343505'),p,0))/sum(p),1) two_pct_paid, sum(b) benes_rowsum, sum(iff(npi in ('1811518392','1487343505'),b,0)) two_benes
from s group by 1 order by paid desc;

-- #19 carbon-date the supplier file: newest NPPES enumeration date among its supplier NPIs, and counts enumerated per year 2023-2026
with s as (select distinct SUPLR_NPI npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL)
select year(n.PROVIDER_ENUMERATION_DATE) yr, count(*) npis, max(n.PROVIDER_ENUMERATION_DATE)::varchar newest
from s join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi where n.PROVIDER_ENUMERATION_DATE >= '2023-01-01' group by 1 order by 1;

-- #20 interpret the court/DOJ misses: FJC criminal name fill, DOJ-listing capture window, and CourtListener for the other unbanned high billers
select 'FJC_CRIM_name_fill' k, count(*)::varchar a, count(nullif(trim(DEFENDANT_NAME),''))::varchar b, max(FILE_DATE)::varchar c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL
union all
select 'DOJ_listing_window', count(*)::varchar, min(CAPTURED_AT)::varchar, max(CAPTURED_AT)::varchar from LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
union all
select 'DOJ_listing_health_fraud_2025_26', count(*)::varchar, min(LINK_TEXT), max(LINK_TEXT) from LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING where CAPTURED_AT >= '2025-01-01' and LINK_TEXT ilike any ('%health care fraud%','%medicare%','%durable medical%')
union all
select 'CL_'||COURT_ID, DATE_FILED::varchar, CASE_NAME, DOCKET_NUMBER from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
 where CASE_NAME ilike any ('%ND MEDICAL SOLUTIONS%','%HAWKEYE MEDICAL%','%MAIN STREET DME%','%JL WEBB DME%','%SOUTHEASTERN MEDEQUIP%','%LIFELINE MEDICAL SUPPLY%','%GUGAVA%');

