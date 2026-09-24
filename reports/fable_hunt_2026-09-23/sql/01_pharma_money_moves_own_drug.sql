select NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE nature, count(*) n, round(sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) usd from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022 group by 1 order by usd desc limit 20;
with pay as (
  select NPI,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'novo nordisk%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) novo,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'lilly usa%' or APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'eli lilly%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) lilly,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'janssen%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) janssen,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'e.r. squibb%' or APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'bristol%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) bms,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'pfizer%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) pfizer,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'boehringer%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) bi,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'astrazeneca%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) az,
    sum(iff(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ilike 'merck sharp%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) merck
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022
  where COVERED_RECIPIENT_TYPE <> 'Covered Recipient Teaching Hospital' and NPI is not null
    and NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE not ilike '%ownership%'
  group by 1),
rx as (
  select NPI, PRESCRIBER_TYPE,
    sum(iff(BRAND_NAME ilike 'ozempic%' or BRAND_NAME ilike 'rybelsus%', TOTAL_CLAIMS,0)) ozempic,
    sum(iff(BRAND_NAME ilike 'trulicity%', TOTAL_CLAIMS,0)) trulicity,
    sum(iff(BRAND_NAME ilike 'eliquis%', TOTAL_CLAIMS,0)) eliquis,
    sum(iff(BRAND_NAME ilike 'xarelto%', TOTAL_CLAIMS,0)) xarelto,
    sum(iff(BRAND_NAME ilike 'jardiance%', TOTAL_CLAIMS,0)) jardiance,
    sum(iff(BRAND_NAME ilike 'farxiga%', TOTAL_CLAIMS,0)) farxiga,
    sum(iff(BRAND_NAME ilike 'januvia%', TOTAL_CLAIMS,0)) januvia,
    sum(iff(BRAND_NAME ilike 'tradjenta%', TOTAL_CLAIMS,0)) tradjenta
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS
  where BRAND_NAME ilike any ('ozempic%','rybelsus%','trulicity%','eliquis%','xarelto%','jardiance%','farxiga%','januvia%','tradjenta%')
  group by 1,2)
select 'GLP1 Ozempic(Novo) vs Trulicity(Lilly)' pair,
  case when coalesce(p.novo,0)>0 and coalesce(p.lilly,0)>0 then 'paid both' when coalesce(p.novo,0)>0 then 'paid Novo only' when coalesce(p.lilly,0)>0 then 'paid Lilly only' else 'paid neither' end grp,
  count(*) prescribers, sum(ozempic) a_claims, sum(trulicity) b_claims, round(100*sum(ozempic)/nullif(sum(ozempic)+sum(trulicity),0),1) pct_a,
  round(avg(100*ozempic/nullif(ozempic+trulicity,0)),1) mean_pct_a_per_npi
from rx r left join pay p on p.NPI=r.NPI where ozempic+trulicity >= 50 group by 1,2
union all
select 'DOAC Eliquis(BMS+Pfizer) vs Xarelto(Janssen)',
  case when (coalesce(p.bms,0)+coalesce(p.pfizer,0))>0 and coalesce(p.janssen,0)>0 then 'paid both' when (coalesce(p.bms,0)+coalesce(p.pfizer,0))>0 then 'paid BMS/Pfizer only' when coalesce(p.janssen,0)>0 then 'paid Janssen only' else 'paid neither' end,
  count(*), sum(eliquis), sum(xarelto), round(100*sum(eliquis)/nullif(sum(eliquis)+sum(xarelto),0),1), round(avg(100*eliquis/nullif(eliquis+xarelto,0)),1)
from rx r left join pay p on p.NPI=r.NPI where eliquis+xarelto >= 50 group by 1,2
union all
select 'SGLT2 Jardiance(BI+Lilly) vs Farxiga(AZ)',
  case when (coalesce(p.bi,0)+coalesce(p.lilly,0))>0 and coalesce(p.az,0)>0 then 'paid both' when (coalesce(p.bi,0)+coalesce(p.lilly,0))>0 then 'paid BI/Lilly only' when coalesce(p.az,0)>0 then 'paid AZ only' else 'paid neither' end,
  count(*), sum(jardiance), sum(farxiga), round(100*sum(jardiance)/nullif(sum(jardiance)+sum(farxiga),0),1), round(avg(100*jardiance/nullif(jardiance+farxiga,0)),1)
from rx r left join pay p on p.NPI=r.NPI where jardiance+farxiga >= 50 group by 1,2
union all
select 'DPP4 Januvia(Merck) vs Tradjenta(BI+Lilly)',
  case when coalesce(p.merck,0)>0 and (coalesce(p.bi,0)+coalesce(p.lilly,0))>0 then 'paid both' when coalesce(p.merck,0)>0 then 'paid Merck only' when (coalesce(p.bi,0)+coalesce(p.lilly,0))>0 then 'paid BI/Lilly only' else 'paid neither' end,
  count(*), sum(januvia), sum(tradjenta), round(100*sum(januvia)/nullif(sum(januvia)+sum(tradjenta),0),1), round(avg(100*januvia/nullif(januvia+tradjenta,0)),1)
from rx r left join pay p on p.NPI=r.NPI where januvia+tradjenta >= 50 group by 1,2
order by 1,2;
