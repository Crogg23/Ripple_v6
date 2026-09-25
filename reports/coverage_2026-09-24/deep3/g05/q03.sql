-- ASM participants: profile, repeated NPIs, biggest practices, small-practice share by cohort
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS),
rep as (select NPI, count(*) n, count(distinct ASM_COHORT) coh, count(distinct ORGANIZATION_LEGAL_NAME) orgs, count(distinct STATE) st from t group by 1 having count(*)>1),
org as (select ORGANIZATION_LEGAL_NAME o, count(*) n, count(distinct NPI) npis, listagg(distinct STATE, ',') sts, listagg(distinct ASM_COHORT, ',') coh,
          max(ASM_CY27_SMALLPRACTICE) sp from t group by 1 order by n desc limit 15)
select 'profile' k, count(*)::text a, count(distinct NPI)::text b, count(distinct ORGANIZATION_LEGAL_NAME)::text c,
  count_if(ASM_CY27_SMALLPRACTICE='Yes')::text d, count_if(ASM_CY27_SMALLPRACTICE='No')::text e,
  (select count(*) from rep)::text || ' repeat npis; ' || (select count_if(coh>1) from rep)::text || ' in both cohorts; ' || (select count_if(orgs>1) from rep)::text || ' in 2+ orgs' f from t
union all select 'cohort', ASM_COHORT, count(*)::text, count(distinct NPI)::text, count_if(ASM_CY27_SMALLPRACTICE='Yes')::text, count(distinct ORGANIZATION_LEGAL_NAME)::text, count(distinct STATE)::text from t group by 2
union all select 'org', o, n::text, npis::text, sts, coh, sp from org
union all select 'cy28vals', ASM_CY28_PARTICIPANT, count(*)::text, null, null, null, null from t group by 2
