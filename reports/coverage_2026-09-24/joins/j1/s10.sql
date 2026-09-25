-- PPP ($150K+ file): Reliant home legal entities (enrollment ORGANIZATION_NAME, normalized) = BORROWERNAME normalized, state MO/KS; also any borrower name containing RELIANT CARE or DESTEFANE
with rel as (select lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, n.PROVIDER_NAME, upper(n.CITY) city, n.STATE, e.ORGANIZATION_NAME,
   regexp_replace(regexp_replace(upper(e.ORGANIZATION_NAME),'[^A-Z0-9 ]',''),' (L L C|LLC|INC|LP|LLP|CO)$','') k
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME n left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS e on lpad(trim(e.CCN),6,'0')=lpad(trim(n.CMS_CERTIFICATION_NUMBER_CCN),6,'0')
   where n.CHAIN_ID='446'),
ppp as (select BORROWERNAME, BORROWERADDRESS, upper(BORROWERCITY) city, BORROWERSTATE, DATEAPPROVED, CURRENTAPPROVALAMOUNT, FORGIVENESSAMOUNT, JOBSREPORTED, NAICSCODE, LOANNUMBER, SERVICINGLENDERNAME,
   regexp_replace(regexp_replace(upper(BORROWERNAME),'[^A-Z0-9 ]',''),' (L L C|LLC|INC|LP|LLP|CO)$','') k
   from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWERSTATE in ('MO','KS'))
select rel.ccn, rel.PROVIDER_NAME, rel.city home_city, ppp.BORROWERNAME, ppp.city ppp_city, ppp.BORROWERADDRESS, ppp.DATEAPPROVED, ppp.CURRENTAPPROVALAMOUNT, ppp.FORGIVENESSAMOUNT, ppp.JOBSREPORTED, ppp.NAICSCODE, ppp.SERVICINGLENDERNAME, ppp.LOANNUMBER
from ppp left join rel on rel.k=ppp.k
where rel.ccn is not null or ppp.k ilike '%RELIANT CARE%' or ppp.k ilike '%DESTEFANE%' or ppp.k ilike 'MMA HEALTHCARE%' or ppp.k ilike 'BKY HEALTHCARE%'
order by ppp.DATEAPPROVED
