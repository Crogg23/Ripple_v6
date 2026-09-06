"""E38 round 2 — first-pass variants, payer-name normalization, the $41M royalty recipient, cohort-time-correct join."""
import json
from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/queries.log")
H = "LIBRARY_MARTS.HEALTH."
OO = H + "HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS"
OP = {2022: H + "HEALTH__FED_CMS_OPEN_PAYMENTS_2022", 2023: H + "HEALTH__FED_CMS_OPEN_PAYMENTS_2023", 2024: H + "HEALTH__FED_CMS_OPEN_PAYMENTS"}
COH = f"(select NPI, min(OPTOUT_EFFECTIVE_DATE) eff, max(OPTOUT_END_DATE) end_dt, min(SPECIALTY) specialty, min(STATE_CODE) st from {OO} where NPI is not null and length(NPI)=10 group by NPI)"
FIX = f"(select * from {COH} where eff < '2023-01-01')"
R = json.load(open("reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/results.json"))

# first-pass variants on PY2023: cutoff at end of 2023; opted out on/before the payment date
R["fp_variants"] = run(f"""select
  sum(iff(c.eff < '2024-01-01', usd, 0)) eff_before_2024,
  sum(iff(c.eff <= try_to_date(p.DATE_OF_PAYMENT,'MM/DD/YYYY'), usd, 0)) eff_on_or_before_payment,
  sum(iff(c.eff < '2023-07-01', usd, 0)) eff_before_mid2023,
  sum(usd) any_roster
  from (select NPI, DATE_OF_PAYMENT, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS usd from {OP[2023]}) p join {COH} c on c.NPI=p.NPI""", "first-pass variants PY2023")

# payer names normalized: upper + strip punctuation; top 12 pooled over the fixed cohort
R["payers_norm"] = run(f"""select payer, sum(usd) usd, count(*) n, count(distinct npi) npis, count(distinct raw) spellings,
    sum(iff(py=2022,usd,0)) usd22, sum(iff(py=2023,usd,0)) usd23, sum(iff(py=2024,usd,0)) usd24,
    sum(iff(nature like 'Royalty%',usd,0)) usd_royalty from (""" +
    " union all ".join(f"""select {py} py, upper(regexp_replace(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME,'[^A-Za-z0-9 ]','')) payer,
    APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME raw, p.NPI npi, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS usd, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE nature
    from {t} p join {FIX} c on c.NPI=p.NPI""" for py, t in OP.items()) + ") group by 1 order by 2 desc limit 12", "top payers normalized")

# the $41M plastic surgeon: who pays, what nature, which year; plus roster row
R["top1_detail"] = run(" union all ".join(f"""select {py} py, APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME payer, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE nature,
    count(*) n, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd from {t} where NPI='1295737930' group by 1,2,3""" for py, t in OP.items()) + " order by 5 desc", "top1 detail")
R["top1_roster"] = run(f"select NPI, SPECIALTY, STATE_CODE, OPTOUT_EFFECTIVE_DATE, OPTOUT_END_DATE, ELIGIBLE_TO_ORDER_AND_REFER from {OO} where NPI='1295737930'", "top1 roster")

# cohort by paid-any-year status: how many of the 27,547 got anything in any of the 3 years; how many all 3
R["paid_persistence"] = run(f"""with y as (""" + " union all ".join(f"select distinct {py} py, p.NPI from {t} p join {FIX} c on c.NPI=p.NPI" for py, t in OP.items()) + f""")
    select count(distinct NPI) paid_any, sum(iff(k=3,1,0)) paid_all3, sum(iff(k=1,1,0)) paid_one from (select NPI, count(distinct py) k from y group by 1)""", "paid persistence")

# cohort composition: what share is mental health / dental (who almost never gets industry money)
R["cohort_mix"] = run(f"""select case when specialty in ('Clinical Psychologist','Mental Health Counselor','Clinical Social Worker','Marriage And Family Therapist') then 'therapists'
    when specialty in ('Dentist','Oral Surgery','Maxillofacial Surgery') then 'dental' when specialty='Psychiatry' then 'psychiatry'
    when specialty in ('Orthopedic Surgery','Plastic And Reconstructive Surgery','Neurosurgery') then 'ortho/plastics/neurosurg' else 'other' end grp,
    count(*) cohort from {FIX} group by 1 order by 2 desc""", "cohort mix")

json.dump(R, open("reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/results.json", "w"), indent=1, default=str)
for k in ["fp_variants","payers_norm","top1_detail","top1_roster","paid_persistence","cohort_mix"]:
    print("\n##", k)
    for r in R[k][:15]: print(r)
print("\n## nature 2024"); [print(r) for r in R["nature"] if r["PY"]==2024]
