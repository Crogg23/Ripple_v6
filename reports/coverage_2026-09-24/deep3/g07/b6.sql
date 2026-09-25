-- # FAERS INDI robustness: Actiq + Fentora reasons split by who reported (health professional vs consumer vs lawyer) and by period (pre-REMS legacy, post-REMS legacy, post-REMS new format)
with t as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, trim(DRUG_SEQ) seq
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS') and (upper(DRUGNAME) like 'ACTIQ%' or upper(DRUGNAME) like 'FENTORA%')),
d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(OCCP_COD)) occ
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
i as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(DRUG_SEQ),''),trim(INDI_DRUG_SEQ)) seq, upper(trim(INDI_PT)) ip from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI
   where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
ic as (select *, case when ip is null or ip like '%UNKNOWN%' then 'unknown'
     when regexp_like(ip,'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO).*') then 'cancer'
     when ip in ('PAIN','BREAKTHROUGH PAIN','ANALGESIC THERAPY','PAIN MANAGEMENT','ANALGESIA') then 'generic_pain'
     else 'named_noncancer' end cls from i),
j as (select d.cs, min(d.q) q, max(d.occ) occ, max(iff(ic.cls='cancer',1,0)) ca, max(iff(ic.cls='named_noncancer',1,0)) nc, max(iff(ic.cls='generic_pain',1,0)) gp
   from t join d on d.id=t.id join ic on ic.id=t.id and ic.seq=t.seq group by 1)
select case when q<='2011q4' then '1 2004-2011 pre-REMS' when q<='2012q3' then '2 2012q1-q3 REMS legacy' else '3 2012q4-2014q2 new format' end period,
  case when occ in ('MD','PH','OT','HP') then 'health pro' when occ='CN' then 'consumer' when occ='LW' then 'lawyer' else coalesce(occ,'blank') end who,
  count(*) cases_with_reason, sum(ca) cancer, sum(nc) named_noncancer, sum(gp) generic_pain, round(100*sum(nc)/count(*)) pct_noncancer
from j group by 1,2 order by 1,2
-- # Pending physicians eyeball: 5 organization NPIs on the physician list, and 6 Florida rows with pre-2016 NPIs and NPPES untouched since before 2017
with p as (select distinct trim(NPI) npi, LAST_NAME ln, FIRST_NAME fn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, ENTITY_TYPE_CODE et, PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME org, PROVIDER_LAST_NAME_LEGAL_NAME nl, PROVIDER_FIRST_NAME nf, PROVIDER_CREDENTIAL_TEXT cred,
   PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, upper(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME) city, PROVIDER_ENUMERATION_DATE ed, LAST_UPDATE_DATE lu, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p))
select * from (select 'org' k, p.npi, p.ln||', '||p.fn pending_name, coalesce(n.org,'')||' / '||coalesce(n.nl,'') nppes_name, n.st||' '||n.city place, n.ed::varchar enum_dt, n.lu::varchar last_upd, n.tx from p join n on n.NPI=p.npi where n.et='2' order by p.npi limit 5)
union all
select * from (select 'fl_stale', p.npi, p.ln||', '||p.fn, coalesce(n.nl,'')||', '||coalesce(n.nf,'')||' '||coalesce(n.cred,''), n.st||' '||n.city, n.ed::varchar, n.lu::varchar, n.tx from p join n on n.NPI=p.npi
  where n.st='FL' and n.ed<'2016-01-01' and n.lu<'2017-01-01' order by hash(p.npi) limit 6)
