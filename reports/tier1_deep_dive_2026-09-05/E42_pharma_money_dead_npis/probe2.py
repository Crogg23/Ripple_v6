from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E42_pharma_money_dead_npis/queries.log")
OP="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS"; NP="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES"
for r in run(f"select DATE_OF_PAYMENT, PROGRAM_YEAR, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS, NPI from {OP} where NPI is not null limit 5","op_sample"): print(r)
for r in run(f"""select count(*) n, count_if(NPI_DEACTIVATION_DATE is not null) deact, count_if(NPI_DEACTIVATION_DATE is not null and NPI_REACTIVATION_DATE is null) deact_never_react,
  count_if(NPI_DEACTIVATION_DATE is not null and NPI_REACTIVATION_DATE is not null) deact_react,
  count_if(NPI_DEACTIVATION_DATE is not null and nullif(trim(NPI_DEACTIVATION_REASON_CODE),'') is not null) reason_filled,
  min(NPI_DEACTIVATION_DATE) mn, max(NPI_DEACTIVATION_DATE) mx, count(distinct NPI) dn from {NP}""","nppes_cohort"): print(r)
for r in run(f"select count(*) n, count(distinct NPI) dn, count_if(NPI is null or trim(NPI)='') blank, count_if(try_to_date(DATE_OF_PAYMENT,'MM/DD/YYYY') is null) bad_date, min(PROGRAM_YEAR) py0, max(PROGRAM_YEAR) py1 from {OP}","op_keys"): print(r)
