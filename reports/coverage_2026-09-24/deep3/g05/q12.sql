-- Hospital REH conversions: old CCN (CAH_OR_HOSPITAL_CCN) -> FINDINGS.HOSPITAL_CLOSURE_RISK margins, vs rural hospitals in the same states that did not convert
with reh as (select ENROLLMENT_STATE st, REH_CONVERSION_DATE dt, CAH_OR_HOSPITAL_CCN raw_old, lpad(trim(split_part(CAH_OR_HOSPITAL_CCN,'|',1)),6,'0') old_ccn,
               lpad(trim(CCN),6,'0') new_ccn, ORGANIZATION_NAME, PROPRIETARY_NONPROFIT pnp
             from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS where REH_CONVERSION_FLAG='Y' or PROVIDER_TYPE_CODE='00-24'),
r as (select lpad(trim(CCN),6,'0') ccn, STATE, IS_RURAL, OPERATING_MARGIN_PCT m, NEGATIVE_OPERATING_MARGIN neg, RISK_TIER, FY_END, NET_PATIENT_REVENUE npr, MEDICAID_DEPENDENCE_PCT mcd
      from LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK),
conv as (select reh.*, r.m, r.neg, r.RISK_TIER, r.FY_END, r.npr, r.IS_RURAL, (select count(*) from r r2 where r2.ccn=reh.new_ccn) new_ccn_in_r from reh left join r on r.ccn=reh.old_ccn),
peer as (select r.* from r where r.IS_RURAL and r.STATE in (select st from reh) and r.ccn not in (select old_ccn from reh where old_ccn is not null))
select 'sum_conv' k, count(*)::text a, count(m)::text b, round(median(m),1)::text c, count_if(neg)::text d, round(median(npr)/1e6,1)::text e, sum(new_ccn_in_r)::text f, null g, null h from conv
union all select 'sum_peer', count(*)::text, count(m)::text, round(median(m),1)::text, count_if(neg)::text, round(median(npr)/1e6,1)::text, null, null, null from peer
union all select 'conv_row', st, dt::text, raw_old, left(ORGANIZATION_NAME,34), pnp, round(m,1)::text, RISK_TIER, FY_END from conv
union all select 'conv_year', year(dt)::text, count(*)::text, null, null, null, null, null, null from conv group by 2
order by 1, 2
