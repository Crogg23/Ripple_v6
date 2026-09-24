with h as (
  select RESPONDENT_ID, AGENCY_CODE,
    sum(iff(APPLICANT_RACE_1='3' and ACTION_TAKEN in ('1','2','3'),1,0)) black_apps, sum(iff(APPLICANT_RACE_1='3' and ACTION_TAKEN='3',1,0)) black_denied,
    sum(iff(APPLICANT_RACE_1='5' and ACTION_TAKEN in ('1','2','3'),1,0)) white_apps, sum(iff(APPLICANT_RACE_1='5' and ACTION_TAKEN='3',1,0)) white_denied
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC
  where AS_OF_YEAR = '2017' and LOAN_PURPOSE = '1' and OWNER_OCCUPANCY = '1' and PROPERTY_TYPE = '1' and ACTION_TAKEN in ('1','2','3')
  group by 1,2 having black_apps >= 500 and white_apps >= 2000),
x as (select ARID_2017, max(RESPONDENT_NAME) rname, max(coalesce(LEI_2018, LEI_2019, LEI_2020)) lei from LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF group by 1),
b as (select LEI, max(NAME) bank, max(CERT) cert, max(ASSET) assets from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA where LEI is not null group by 1),
sod as (select FDIC_CERT, sum(BRANCH_DEPOSITS_THOUSANDS) dep_k, count(*) branches from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS where SURVEY_YEAR = 2017 group by 1)
select coalesce(x.rname, h.RESPONDENT_ID) lender, h.AGENCY_CODE, b.bank fdic_bank, h.black_apps, round(100.0*h.black_denied/h.black_apps,1) black_denial_pct, h.white_apps, round(100.0*h.white_denied/h.white_apps,1) white_denial_pct,
  round(100.0*h.black_denied/h.black_apps - 100.0*h.white_denied/h.white_apps,1) gap_pts, round((h.black_denied/h.black_apps)/nullif(h.white_denied/h.white_apps,0),2) ratio, round(sod.dep_k/1e6,1) dep_bn_2017, sod.branches
from h left join x on x.ARID_2017 = h.AGENCY_CODE || ltrim(h.RESPONDENT_ID,'0') or x.ARID_2017 = h.AGENCY_CODE || h.RESPONDENT_ID
left join b on b.LEI = x.lei left join sod on sod.FDIC_CERT = b.cert
order by ratio desc limit 40