from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner/queries.log")
E="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"
P="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
def show(rows): 
    for r in rows: print(r)
# 1 ownership-ish columns anywhere in HEALTH marts
show(run("""select table_name, column_name, data_type from LIBRARY_MARTS.information_schema.columns
 where table_schema='HEALTH' and (column_name ilike '%OWNER%' or column_name ilike '%CHOW%' or column_name ilike '%CHANGE%' or column_name ilike '%INCORPORAT%' or column_name ilike '%FIRST_APPROVED%' or column_name ilike '%CERTIFICATION_DATE%')
 order by 1,2""","ownership-ish cols in HEALTH"))
# 2 key checks
show(run(f"select count(*) n, count(distinct CCN) d_ccn, count(distinct ENROLLMENT_ID) d_enr, count(distinct NPI) d_npi, count(distinct ASSOCIATE_ID) d_assoc, sum(iff(CCN is null or trim(CCN)='',1,0)) blank_ccn, min(length(CCN)) minlen, max(length(CCN)) maxlen from {E}","enroll key check"))
show(run(f"select CCN, ENROLLMENT_ID, NPI, ASSOCIATE_ID, ORGANIZATION_NAME, INCORPORATION_DATE, ORGANIZATION_TYPE_STRUCTURE, PROPRIETARY_NONPROFIT from {E} limit 5","enroll sample"))
show(run(f"select count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) d_ccn, min(PENALTY_DATE) mn, max(PENALTY_DATE) mx, min(length(CMS_CERTIFICATION_NUMBER_CCN)) minlen, max(length(CMS_CERTIFICATION_NUMBER_CCN)) maxlen, count(distinct FINE_ID) d_fine, min(PROCESSING_DATE) mnp, max(PROCESSING_DATE) mxp from {P}","penalty key check"))
show(run(f"select PENALTY_TYPE, count(*) n from {P} group by 1","penalty types"))
# 3 incorporation date profile
show(run(f"select count(*) n, count(INCORPORATION_DATE) filled, min(INCORPORATION_DATE) mn, max(INCORPORATION_DATE) mx, sum(iff(INCORPORATION_DATE>='2023-06-17',1,0)) since_pen_start, sum(iff(INCORPORATION_DATE>=current_date,1,0)) future from {E}","incorp profile"))
show(run(f"select year(INCORPORATION_DATE) y, count(*) n from {E} where INCORPORATION_DATE>='2015-01-01' group by 1 order by 1","incorp by year 2015+"))
# 4 reproduce first pass: incorporated after first penalty
show(run(f"""with pen as (select CMS_CERTIFICATION_NUMBER_CCN ccn, min(PENALTY_DATE) first_pen from {P} group by 1),
 e as (select CCN, INCORPORATION_DATE from {E})
 select count(distinct pen.ccn) penalized_homes, count(distinct iff(e.CCN is not null, pen.ccn, null)) matched,
 count(distinct iff(e.INCORPORATION_DATE is not null, pen.ccn, null)) with_incorp,
 count(distinct iff(e.INCORPORATION_DATE > pen.first_pen, pen.ccn, null)) incorp_after_first_pen,
 count(distinct iff(e.INCORPORATION_DATE >= '2023-06-17', pen.ccn, null)) incorp_since_202306
 from pen left join e on e.CCN=pen.ccn""","reproduce first pass"))
# 5 landing table columns (is there more there?)
show(run("select column_name, data_type from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS' order by ordinal_position","landing enroll cols"))
