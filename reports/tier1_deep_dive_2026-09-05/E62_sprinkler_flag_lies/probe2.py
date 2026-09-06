from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies/queries.log")
F="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES"
D="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES"
H="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME"
r = run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES' order by ordinal_position","cols fire")
print([(x['COLUMN_NAME'],x['DATA_TYPE']) for x in r])
for q,l in [
 (f"select AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS f, count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) ccns, min(PROCESSING_DATE) mn, max(PROCESSING_DATE) mx from {H} group by 1 order by 2 desc","flag values"),
 (f"select count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) d, min(length(CMS_CERTIFICATION_NUMBER_CCN)) l1, max(length(CMS_CERTIFICATION_NUMBER_CCN)) l2 from {H}","home ccn key"),
 (f"select DEFICIENCY_PREFIX, count(*) n from {D} group by 1 order by 2 desc","health prefix"),
 (f"select DEFICIENCY_PREFIX, count(*) n, min(SURVEY_DATE) mn, max(SURVEY_DATE) mx, min(PROCESSING_DATE) p1, max(PROCESSING_DATE) p2 from {F} group by 1 order by 2 desc","fire prefix"),
 (f"select DEFICIENCY_TAG_NUMBER tag, DEFICIENCY_DESCRIPTION d, count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) homes from {F} where DEFICIENCY_DESCRIPTION ilike '%sprinkler%' group by 1,2 order by 3 desc","sprinkler tags fire"),
 (f"select DEFICIENCY_TAG_NUMBER tag, DEFICIENCY_DESCRIPTION d, count(*) n from {D} where DEFICIENCY_DESCRIPTION ilike '%sprinkler%' group by 1,2 order by 3 desc","sprinkler tags health"),
 (f"select DEFICIENCY_CORRECTED, count(*) n, sum(iff(CORRECTION_DATE is null,1,0)) nulldate from {F} group by 1","corrected values fire"),
 (f"select count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) homes, sum(iff(h.CMS_CERTIFICATION_NUMBER_CCN is null,1,0)) orphans from {F} f left join {H} h using (CMS_CERTIFICATION_NUMBER_CCN)","fire->home orphans"),
]:
    print("==",l)
    for x in run(q,l): print(x)
