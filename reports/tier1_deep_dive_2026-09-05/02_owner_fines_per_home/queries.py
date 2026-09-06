"""Hunch 2 - owner fines per home. Every query, through the Python door. Run from repo root:
PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/02_owner_fines_per_home/queries.py
Writes results.json next to this file; build_story.py reads it."""
import json
from _shared.q import run, open_log
D="reports/tier1_deep_dive_2026-09-05/02_owner_fines_per_home"
open_log(f"{D}/queries.log")
NH="LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411"
DF="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES"
PN="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
out={}
for t in ["HEALTH__FED_NURSINGHOME411","HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES","HEALTH__FED_CMS_NURSING_HOME_PENALTIES"]:
    out[f"cols_{t}"]=run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='{t}' order by ordinal_position", f"cols {t}")
out['nh_shape']=run(f"""select count(*) rows_, count(distinct CMS_CERTIFICATION_NUMBER_CCN) ccns,
 count(distinct CHAIN_ID) chain_ids, count(distinct CHAIN_NAME) chain_names,
 sum(iff(CHAIN_ID is null or trim(CHAIN_ID)='',1,0)) no_chain_id, sum(iff(CHAIN_NAME is null or trim(CHAIN_NAME)='',1,0)) no_chain_name,
 count(distinct PROCESSING_DATE) proc_dates, min(PROCESSING_DATE) pd_min, max(PROCESSING_DATE) pd_max from {NH}""","nh shape")
out['chain_id_sample']=run(f"""select CHAIN_ID, CHAIN_NAME, NUMBER_OF_FACILITIES_IN_CHAIN, count(*) homes_here from {NH}
 where CHAIN_ID is not null group by 1,2,3 order by homes_here desc limit 15""","chain id sample")
out['id_name_xwalk']=run(f"""select
 (select count(*) from (select CHAIN_ID from {NH} where CHAIN_ID is not null group by 1 having count(distinct CHAIN_NAME)>1)) ids_with_many_names,
 (select count(*) from (select CHAIN_NAME from {NH} where CHAIN_NAME is not null group by 1 having count(distinct CHAIN_ID)>1)) names_with_many_ids,
 (select count(*) from (select CHAIN_ID from {NH} where CHAIN_ID is not null group by 1 having count(distinct NUMBER_OF_FACILITIES_IN_CHAIN)>1)) ids_with_many_facility_counts,
 (select count(*) from (select CHAIN_ID, max(NUMBER_OF_FACILITIES_IN_CHAIN) n, count(*) c from {NH} where CHAIN_ID is not null group by 1 having n<>c)) ids_where_count_disagrees""","id/name crosswalk")
out['chain_id_format']=run(f"""select length(CHAIN_ID) len, regexp_like(CHAIN_ID,'^[0-9]+$') numeric, count(*) n, min(CHAIN_ID) lo, max(CHAIN_ID) hi from {NH} where CHAIN_ID is not null group by 1,2 order by n desc""","chain id format")
out['pen_shape']=run(f"""select count(*) rows_, count(distinct FINE_ID) fine_ids, count(distinct CMS_CERTIFICATION_NUMBER_CCN) ccns,
 min(PENALTY_DATE) d_min, max(PENALTY_DATE) d_max, sum(iff(PENALTY_DATE<'2023-06-17',1,0)) before_window,
 count(distinct PROCESSING_DATE) proc_dates from {PN}""","penalties shape")
out['pen_types']=run(f"""select PENALTY_TYPE, count(*) n, count(distinct FINE_ID) fine_ids, sum(FINE_AMOUNT) dollars, sum(iff(FINE_ID is null or trim(FINE_ID)='',1,0)) blank_id from {PN} group by 1 order by n desc""","penalty types")
out['pen_dupes']=run(f"""select count(*) dupe_groups, sum(c-1) extra_rows from (select CMS_CERTIFICATION_NUMBER_CCN, PENALTY_DATE, PENALTY_TYPE, FINE_AMOUNT, count(*) c from {PN} group by 1,2,3,4 having c>1)""","penalty dupes")
out['pen_ccn_in_nh']=run(f"""select count(distinct p.CMS_CERTIFICATION_NUMBER_CCN) pen_ccns, count(distinct n.CMS_CERTIFICATION_NUMBER_CCN) matched from {PN} p left join {NH} n on n.CMS_CERTIFICATION_NUMBER_CCN=p.CMS_CERTIFICATION_NUMBER_CCN""","penalty ccn coverage")
out['def_shape']=run(f"""select count(*) rows_, count(distinct CMS_CERTIFICATION_NUMBER_CCN) ccns, min(SURVEY_DATE) d_min, max(SURVEY_DATE) d_max,
 count(distinct DEFICIENCY_TAG_NUMBER) tags, count(distinct PROCESSING_DATE) proc_dates from {DF}""","deficiency shape")
out['def_by_year']=run(f"""select year(SURVEY_DATE) y, count(*) n from {DF} group by 1 order by 1""","deficiencies by year")
out['pen_by_month']=run(f"""select date_trunc('month',PENALTY_DATE) m, count(*) n, sum(iff(PENALTY_TYPE ilike 'fine%',FINE_AMOUNT,0)) dollars from {PN} group by 1 order by 1""","penalties by month")
# main chain table: fines since 2023-06-17 (Fine rows only, distinct FINE_ID), beds, homes
CHAIN_SQL=f"""
with homes as (
  select CMS_CERTIFICATION_NUMBER_CCN ccn, nullif(trim(CHAIN_ID),'') chain_id, nullif(trim(CHAIN_NAME),'') chain_name,
         NUMBER_OF_CERTIFIED_BEDS beds, NUMBER_OF_FINES cms_fines, TOTAL_AMOUNT_OF_FINES_IN_DOLLARS cms_fine_dollars, NUMBER_OF_PAYMENT_DENIALS cms_denials
  from {NH}),
fines as (
  select CMS_CERTIFICATION_NUMBER_CCN ccn, count(distinct FINE_ID) fines, sum(FINE_AMOUNT) dollars
  from (select distinct CMS_CERTIFICATION_NUMBER_CCN, FINE_ID, FINE_AMOUNT from {PN} where PENALTY_TYPE='Fine' and PENALTY_DATE>='2023-06-17')
  group by 1),
denials as (
  select CMS_CERTIFICATION_NUMBER_CCN ccn, count(*) denials from (select distinct CMS_CERTIFICATION_NUMBER_CCN, PAYMENT_DENIAL_START_DATE, PAYMENT_DENIAL_LENGTH_IN_DAYS from {PN} where PENALTY_TYPE='Payment Denial') group by 1)
select coalesce(h.chain_id,'(none)') chain_id, coalesce(h.chain_name,'(no chain)') chain_name,
  count(*) homes, sum(h.beds) beds,
  sum(coalesce(f.fines,0)) fines, sum(coalesce(f.dollars,0)) dollars,
  sum(iff(f.fines>0,1,0)) homes_fined,
  sum(coalesce(d.denials,0)) denials,
  sum(coalesce(h.cms_fines,0)) cms_fines, sum(coalesce(h.cms_fine_dollars,0)) cms_dollars, sum(coalesce(h.cms_denials,0)) cms_denials,
  round(sum(coalesce(f.fines,0))/count(*),2) fines_per_home,
  round(sum(coalesce(f.dollars,0))/count(*)) dollars_per_home,
  round(100*sum(coalesce(f.fines,0))/nullif(sum(h.beds),0),2) fines_per_100_beds,
  round(sum(coalesce(f.dollars,0))/nullif(sum(h.beds),0)) dollars_per_bed
from homes h left join fines f on f.ccn=h.ccn left join denials d on d.ccn=h.ccn
group by 1,2"""
out['chains']=run(CHAIN_SQL+" order by fines_per_home desc","chain rollup all")
# totals check
out['totals']=run(f"""select count(distinct FINE_ID) fines, sum(FINE_AMOUNT) dollars from (select distinct FINE_ID, FINE_AMOUNT from {PN} where PENALTY_TYPE='Fine')""","fine totals distinct id")
out['fine_id_dupes']=run(f"""select count(*) ids_with_2plus_rows, sum(c) rows_ from (select FINE_ID, count(*) c from {PN} where PENALTY_TYPE='Fine' group by 1 having c>1)""","fine id dupes")
out['fine_id_amount_conflict']=run(f"""select count(*) n from (select FINE_ID from {PN} where PENALTY_TYPE='Fine' group by 1 having count(distinct FINE_AMOUNT)>1 or count(distinct CMS_CERTIFICATION_NUMBER_CCN)>1)""","fine id amount/ccn conflict")
out['denial_dupes']=run(f"""select count(*) rows_, count(distinct CMS_CERTIFICATION_NUMBER_CCN||'|'||PAYMENT_DENIAL_START_DATE||'|'||PAYMENT_DENIAL_LENGTH_IN_DAYS) distinct_ from {PN} where PENALTY_TYPE='Payment Denial'""","denial dupes")
# repeat tag: per chain, (ccn,tag) pairs cited on 2+ distinct survey dates, deficiencies 2017+ AND a separate 2023-06-17+ cut
out['repeat']=run(f"""
with d as (select CMS_CERTIFICATION_NUMBER_CCN ccn, DEFICIENCY_TAG_NUMBER tag, SURVEY_DATE sd from {DF} where SURVEY_DATE is not null),
pairs as (select ccn, tag, count(distinct sd) n_dates, count(distinct iff(sd>='2023-06-17',sd,null)) n_dates_pw from d group by 1,2),
homes as (select CMS_CERTIFICATION_NUMBER_CCN ccn, coalesce(nullif(trim(CHAIN_ID),''),'(none)') chain_id, coalesce(nullif(trim(CHAIN_NAME),''),'(no chain)') chain_name from {NH})
select h.chain_id, h.chain_name, count(distinct h.ccn) homes,
  count(p.tag) pairs, sum(iff(p.n_dates>=2,1,0)) repeat_pairs, round(100*sum(iff(p.n_dates>=2,1,0))/nullif(count(p.tag),0),1) repeat_pct,
  sum(p.n_dates) citations,
  sum(iff(p.n_dates_pw>=1,1,0)) pairs_pw, sum(iff(p.n_dates_pw>=2,1,0)) repeat_pairs_pw,
  round(100*sum(iff(p.n_dates_pw>=2,1,0))/nullif(sum(iff(p.n_dates_pw>=1,1,0)),0),1) repeat_pct_pw
from homes h left join pairs p on p.ccn=h.ccn group by 1,2""","repeat tag by chain")
out['repeat_all']=run(f"""
with d as (select CMS_CERTIFICATION_NUMBER_CCN ccn, DEFICIENCY_TAG_NUMBER tag, SURVEY_DATE sd from {DF}),
pairs as (select ccn, tag, count(distinct sd) n_dates from d group by 1,2)
select count(*) pairs, sum(iff(n_dates>=2,1,0)) repeat_pairs, round(100*sum(iff(n_dates>=2,1,0))/count(*),1) repeat_pct, max(n_dates) max_dates from pairs""","repeat tag overall")
out['def_type_by_year']=run(f"""select year(SURVEY_DATE) y, sum(iff(STANDARD_DEFICIENCY='Y',1,0)) standard, sum(iff(COMPLAINT_DEFICIENCY='Y',1,0)) complaint, count(distinct CMS_CERTIFICATION_NUMBER_CCN) ccns, count(*) n from {DF} group by 1 order by 1""","deficiency type by year")
out['bria_homes']=run(f"""
select h.CMS_CERTIFICATION_NUMBER_CCN ccn, h.PROVIDER_NAME, h.STATE, h.NUMBER_OF_CERTIFIED_BEDS beds, h.OVERALL_RATING, h.SPECIAL_FOCUS_STATUS, h.ABUSE_ICON,
  h.NUMBER_OF_FINES cms_fines, h.TOTAL_AMOUNT_OF_FINES_IN_DOLLARS cms_dollars,
  (select count(distinct FINE_ID) from {PN} p where p.CMS_CERTIFICATION_NUMBER_CCN=h.CMS_CERTIFICATION_NUMBER_CCN and PENALTY_TYPE='Fine') fines,
  (select sum(FINE_AMOUNT) from (select distinct FINE_ID, FINE_AMOUNT, CMS_CERTIFICATION_NUMBER_CCN from {PN} where PENALTY_TYPE='Fine') p where p.CMS_CERTIFICATION_NUMBER_CCN=h.CMS_CERTIFICATION_NUMBER_CCN) dollars
from {NH} h where CHAIN_NAME='BRIA HEALTH SERVICES' order by dollars desc nulls last""","bria homes")
out['pen_dupe_kind']=run(f"""select PENALTY_TYPE, count(*) groups_, sum(c-1) extra, count(distinct ids) distinct_id_groups from (select CMS_CERTIFICATION_NUMBER_CCN, PENALTY_DATE, PENALTY_TYPE, FINE_AMOUNT, count(*) c, count(distinct FINE_ID) ids from {PN} group by 1,2,3,4 having c>1) group by 1""","penalty dupe kind")
out['bria_tags']=run(f"""
with d as (select CMS_CERTIFICATION_NUMBER_CCN ccn, DEFICIENCY_TAG_NUMBER tag, max(DEFICIENCY_DESCRIPTION) descr, count(distinct SURVEY_DATE) n_dates
  from {DF} where SURVEY_DATE>='2023-06-17' and CMS_CERTIFICATION_NUMBER_CCN in (select CMS_CERTIFICATION_NUMBER_CCN from {NH} where CHAIN_NAME='BRIA HEALTH SERVICES') group by 1,2)
select tag, min(descr) descr, count(*) homes_cited, sum(iff(n_dates>=2,1,0)) homes_repeat, sum(n_dates) citations from d group by 1 order by homes_repeat desc, citations desc limit 12""","bria repeat tags")
out['cohort']=run(f"""
with homes as (select CMS_CERTIFICATION_NUMBER_CCN ccn, nullif(trim(CHAIN_ID),'') chain_id, NUMBER_OF_CERTIFIED_BEDS beds from {NH}),
fines as (select CMS_CERTIFICATION_NUMBER_CCN ccn, count(distinct FINE_ID) fines, sum(FINE_AMOUNT) dollars from (select distinct CMS_CERTIFICATION_NUMBER_CCN, FINE_ID, FINE_AMOUNT from {PN} where PENALTY_TYPE='Fine') group by 1),
sz as (select chain_id, count(*) n from homes where chain_id is not null group by 1)
select case when h.chain_id is null then 'no chain' when s.n>=10 then 'chain 10+ homes' else 'chain under 10' end grp,
  count(distinct h.chain_id) chains, count(*) homes, sum(h.beds) beds, sum(coalesce(f.fines,0)) fines, sum(coalesce(f.dollars,0)) dollars,
  round(sum(coalesce(f.fines,0))/count(*),2) fines_per_home, round(100*sum(coalesce(f.fines,0))/sum(h.beds),2) fines_per_100_beds, round(sum(coalesce(f.dollars,0))/sum(h.beds)) dollars_per_bed
from homes h left join fines f on f.ccn=h.ccn left join sz s on s.chain_id=h.chain_id group by 1 order by 1""","cohort by chain size")

# --- skeptic round: survey frequency, Illinois peers ---
out['surveys']=run(f"""
with homes as (select CMS_CERTIFICATION_NUMBER_CCN ccn, coalesce(nullif(trim(CHAIN_ID),''),'(none)') chain_id, coalesce(nullif(trim(CHAIN_NAME),''),'(no chain)') chain_name from {NH}),
sv as (select CMS_CERTIFICATION_NUMBER_CCN ccn, count(distinct SURVEY_DATE) dates from {DF} where SURVEY_DATE>='2023-06-17' group by 1),
d as (select CMS_CERTIFICATION_NUMBER_CCN ccn, DEFICIENCY_TAG_NUMBER tag, count(distinct SURVEY_DATE) n from {DF} where SURVEY_DATE>='2023-06-17' group by 1,2),
rp as (select ccn, sum(iff(n>=2,1,0)) repeat_pairs from d group by 1)
select h.chain_id, h.chain_name, count(distinct h.ccn) homes, sum(coalesce(s.dates,0)) survey_dates,
  round(sum(coalesce(s.dates,0))/count(distinct h.ccn),2) dates_per_home, sum(coalesce(r.repeat_pairs,0)) repeat_pairs
from homes h left join sv s on s.ccn=h.ccn left join rp r on r.ccn=h.ccn group by 1,2""","survey dates per home by chain")
out['il_chains']=run(CHAIN_SQL.replace(f"from {NH})",f"from {NH} where STATE='IL')").replace("group by 1,2","group by 1,2 having count(*)>=10")+" order by dollars_per_bed desc","Illinois-only chains 10+ IL homes")
out['state_bed']=run(f"""
with fines as (select CMS_CERTIFICATION_NUMBER_CCN ccn, count(distinct FINE_ID) fines, sum(FINE_AMOUNT) dollars from (select distinct CMS_CERTIFICATION_NUMBER_CCN, FINE_ID, FINE_AMOUNT from {PN} where PENALTY_TYPE='Fine') group by 1)
select iff(STATE='IL','IL','rest of US') grp, count(*) homes, sum(NUMBER_OF_CERTIFIED_BEDS) beds, sum(coalesce(f.fines,0)) fines, sum(coalesce(f.dollars,0)) dollars,
  round(sum(coalesce(f.fines,0))/count(*),2) fines_per_home, round(sum(coalesce(f.dollars,0))/sum(NUMBER_OF_CERTIFIED_BEDS)) dollars_per_bed
from {NH} h left join fines f on f.ccn=h.CMS_CERTIFICATION_NUMBER_CCN group by 1""","IL vs rest per bed")
json.dump(out, open(f"{D}/results.json","w"), default=str, indent=1)
print({k:len(v) for k,v in out.items()})
