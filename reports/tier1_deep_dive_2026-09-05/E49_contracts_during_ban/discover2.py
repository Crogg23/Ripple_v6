from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E49_contracts_during_ban/queries.log")
cols=[r["COLUMN_NAME"] for r in run("""select column_name from LIBRARY_RAW.information_schema.columns
 where table_schema='LANDING' and table_name='FED_USASPENDING_CONTRACTS_FULL_R2' order by ordinal_position""","usa_all_cols")]
print(len(cols)); print(cols)
print(run("select count(*) n, count(distinct RECIPIENT_UEI) uei, count(distinct nullif(trim(RECIPIENT_DUNS),'')) duns from LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2","usa_uei_unquoted"))
print(run("""select count(*) n, count(nullif(trim(UEI),'')) uei_filled, count(distinct nullif(trim(UEI),'')) uei_distinct,
 sum(iff(IS_ENTITY_NOT_INDIVIDUAL,1,0)) entities, count(TERMINATION_DATE) has_term, min(ACTIVATION_DATE), max(ACTIVATION_DATE),
 sum(iff(length(nullif(trim(UEI),''))=12,1,0)) uei_len12
 from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS""","sam_profile"))
print(run("select UEI, count(*) c from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS where nullif(trim(UEI),'') is not null group by 1 order by 2 desc limit 8","sam_uei_top"))
print(run("select TERMINATION_DATE_RAW, count(*) c from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS where TERMINATION_DATE is null group by 1 order by 2 desc limit 5","sam_term_raw"))
print(run("select RECORD_STATUS, count(*) c from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS group by 1","sam_status"))
