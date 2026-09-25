-- # Pending physicians, Florida: do a few addresses or cities carry the established-doctor excess? NPPES last-update year FL vs rest
with p as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, upper(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME) city,
   upper(PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS)||' '||left(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE,5) addr,
   PROVIDER_ENUMERATION_DATE ed, LAST_UPDATE_DATE lu, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p))
select * from (select 'city' k, city v, count(*) n, count_if(ed<'2016-01-01') old_npi, null x from n where st='FL' group by 2 order by 3 desc limit 10)
union all select * from (select 'addr', addr, count(*), count_if(ed<'2016-01-01'), null from n where st='FL' group by 2 order by 3 desc limit 8)
union all select * from (select 'addr_all', st||' '||addr, count(*), count_if(ed<'2016-01-01'), null from n group by 2 order by 3 desc limit 8)
union all select 'upd_year', iff(st='FL','FL',iff(st='PR','PR','rest'))||' '||year(lu), count(*), count_if(ed<'2016-01-01'), null from n where lu is not null group by 2
union all select * from (select 'tax_FL_old', tx, count(*), null, null from n where st='FL' and ed<'2016-01-01' group by 2 order by 3 desc limit 8)
-- # FAERS: the 2014q2 Avandia heart-attack/stroke wave and the 2014q1 Lipitor diabetes wave. Who sent them, event years, lag, deaths
with d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(MFR_SNDR)) snd, EVENT_DT evt,
   coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT) fda, upper(trim(REPT_COD)) rept, upper(trim(OCCP_COD)) occ from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO where SRC_QUARTER between '2012q4' and '2014q2'),
dr as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, iff(upper(DRUGNAME) like 'AVANDIA%' or upper(DRUGNAME) like 'ROSIGLITAZONE%','AVANDIA','LIPITOR') g
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where SRC_QUARTER between '2012q4' and '2014q2' and upper(trim(ROLE_COD))='PS' and (upper(DRUGNAME) like 'AVANDIA%' or upper(DRUGNAME) like 'ROSIGLITAZONE%' or upper(DRUGNAME) like 'LIPITOR%' or upper(DRUGNAME) like 'ATORVASTATIN%')),
r as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, upper(trim(PT)) pt from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC where SRC_QUARTER between '2012q4' and '2014q2'
   and upper(trim(PT)) in ('MYOCARDIAL INFARCTION','CEREBROVASCULAR ACCIDENT','TYPE 2 DIABETES MELLITUS')),
de as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC where SRC_QUARTER between '2012q4' and '2014q2' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
c as (select dr.g, d.q, d.cs, max(d.snd) snd, max(d.rept) rept, max(d.occ) occ, min(d.evt) evt, min(d.fda) fda, max(iff(de.id is not null,1,0)) died
   from d join dr on dr.id=d.id join r on r.id=d.id and ((dr.g='AVANDIA' and r.pt<>'TYPE 2 DIABETES MELLITUS') or (dr.g='LIPITOR' and r.pt='TYPE 2 DIABETES MELLITUS')) left join de on de.id=d.id group by 1,2,3)
select g, q, count(*) cases, mode(snd) top_sender, count_if(snd like '%GLAXO%' or snd like '%GSK%') gsk_sent, count_if(snd like '%PFIZER%') pfizer_sent, mode(occ) top_occ, mode(rept) top_rept,
  count(evt) has_evt, count_if(year(evt)<2008) evt_pre2008, count_if(year(evt) between 2008 and 2010) evt_2008_10, count_if(year(evt)>=2011) evt_2011plus, median(datediff(day,evt,fda)) med_lag_days, sum(died) died
from c group by 1,2 order by 1,2
-- # FAERS INDI: fentanyl mouth/nose sprays for cancer pain only (TIRF class). Why were they taken, by brand and year? Subsys (Insys) vs peers
with t as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, trim(DRUG_SEQ) seq,
   case when upper(DRUGNAME) like 'SUBSYS%' then 'SUBSYS' when upper(DRUGNAME) like 'FENTORA%' then 'FENTORA' when upper(DRUGNAME) like 'ACTIQ%' then 'ACTIQ'
        when upper(DRUGNAME) like 'ABSTRAL%' then 'ABSTRAL' when upper(DRUGNAME) like 'ONSOLIS%' then 'ONSOLIS' when upper(DRUGNAME) like 'LAZANDA%' then 'LAZANDA' end brand
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS')
   and (upper(DRUGNAME) like 'SUBSYS%' or upper(DRUGNAME) like 'FENTORA%' or upper(DRUGNAME) like 'ACTIQ%' or upper(DRUGNAME) like 'ABSTRAL%' or upper(DRUGNAME) like 'ONSOLIS%' or upper(DRUGNAME) like 'LAZANDA%')),
d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(MFR_SNDR)) snd from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
i as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(DRUG_SEQ),''),trim(INDI_DRUG_SEQ)) seq, upper(trim(INDI_PT)) ip from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI
   where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
ic as (select *, case when ip is null or ip like '%UNKNOWN%' then 'unknown'
     when regexp_like(ip,'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO).*') then 'cancer'
     when ip in ('PAIN','BREAKTHROUGH PAIN','ANALGESIC THERAPY','PAIN MANAGEMENT','ANALGESIA','DRUG USE FOR UNKNOWN INDICATION') then 'generic_pain'
     else 'named_noncancer' end cls from i),
j as (select t.brand, d.cs, min(left(d.q,4)) yr, max(d.snd) snd, max(iff(ic.cls='cancer',1,0)) ca, max(iff(ic.cls='named_noncancer',1,0)) nc, max(iff(ic.cls='generic_pain',1,0)) gp, max(iff(ic.cls='unknown',1,0)) uk, count(ic.ip) nind
   from t join d on d.id=t.id left join ic on ic.id=t.id and ic.seq=t.seq group by 1,2)
select 'yr' k, brand, yr v, count(*) cases, count_if(nind>0) with_ind, sum(ca) cancer, sum(nc) named_noncancer, sum(gp) generic_pain, sum(uk) unknown from j group by 2,3
union all select 'all', brand, mode(snd), count(*), count_if(nind>0), sum(ca), sum(nc), sum(gp), sum(uk) from j group by 2
union all select * from (select 'top', t.brand, ic.ip, count(distinct d.cs), null, null, null, null, null from t join d on d.id=t.id join ic on ic.id=t.id and ic.seq=t.seq
   where t.brand in ('SUBSYS','FENTORA','ACTIQ') group by 2,3 qualify row_number() over (partition by t.brand order by count(distinct d.cs) desc) <= 10)
order by 1,2,3
