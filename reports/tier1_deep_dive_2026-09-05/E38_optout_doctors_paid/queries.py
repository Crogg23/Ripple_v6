"""E38 — industry money to Medicare opt-out doctors. Every query, logged to queries.log. Results to results.json."""
import json
from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/queries.log")
H = "LIBRARY_MARTS.HEALTH."
OO = H + "HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS"
OP = {2022: H + "HEALTH__FED_CMS_OPEN_PAYMENTS_2022", 2023: H + "HEALTH__FED_CMS_OPEN_PAYMENTS_2023", 2024: H + "HEALTH__FED_CMS_OPEN_PAYMENTS"}
R = {}

# one row per NPI: earliest effective date, latest end date, one specialty
COH = f"""(select NPI, min(OPTOUT_EFFECTIVE_DATE) eff, max(OPTOUT_END_DATE) end_dt, min(SPECIALTY) specialty, min(STATE_CODE) st
           from {OO} where NPI is not null and length(NPI)=10 group by NPI)"""
FIX = f"(select * from {COH} where eff < '2023-01-01')"

# 0. NPI hygiene in Open Payments (id trap) + cohort sizes
R["op_npi_hygiene"] = run(f"""select count(*) n, count(NPI) npi_nonnull, sum(iff(length(NPI)=10,1,0)) len10, count(distinct NPI) dist,
    sum(iff(NPI in ('0000000000',''),1,0)) sentinel from {OP[2023]}""", "op2023 npi hygiene")
R["cohort_sizes"] = run(f"""select (select count(*) from {COH}) all_optout, (select count(*) from {FIX}) fixed_pre2023,
    (select count(*) from {COH} where eff < '2022-01-01') fixed_pre2022""", "cohort sizes")

# 1. First-pass rebuild, two ways: any opt-out NPI x PY2023 (a) join on distinct list (b) EXISTS
R["fp_join"] = run(f"""select count(*) rows_, count(distinct p.NPI) npis, sum(p.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd
    from {OP[2023]} p join {COH} c on c.NPI = p.NPI""", "first-pass rebuild: join")
R["fp_exists"] = run(f"""select count(*) rows_, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd from {OP[2023]} p
    where exists (select 1 from {OO} o where o.NPI = p.NPI)""", "first-pass rebuild: exists")
# raw-row join (shows the duplicate-affidavit inflation a naive join would produce)
R["fp_naive"] = run(f"""select count(*) rows_, sum(p.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd
    from {OP[2023]} p join {OO} o on o.NPI = p.NPI""", "first-pass naive raw-row join (dupes)")

# 2. Fixed cohort across every program year we hold: total, payers, recipients; plus all-recipient base for share
for py, t in OP.items():
    R[f"fixed_py{py}"] = run(f"""select {py} py, count(*) rows_, count(distinct p.NPI) paid_npis, sum(p.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd,
        median(p.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) med_pay, count(distinct p.APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME) payers,
        sum(iff(p.PHYSICIAN_OWNERSHIP_INDICATOR='Yes',p.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) usd_ownership_flag
        from {t} p join {FIX} c on c.NPI = p.NPI""", f"fixed cohort PY{py}")
    R[f"all_py{py}"] = run(f"""select {py} py, count(distinct NPI) npis, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd
        from {t} where COVERED_RECIPIENT_TYPE <> 'Covered Recipient Teaching Hospital'""", f"all recipients PY{py}")
    # loose cohort (anyone on the roster) for the same year, for the trend contrast
    R[f"loose_py{py}"] = run(f"""select {py} py, count(distinct p.NPI) paid_npis, sum(p.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd
        from {t} p join {COH} c on c.NPI = p.NPI""", f"loose cohort PY{py}")

# 3. Nature of payment, fixed cohort, by year
R["nature"] = run(" union all ".join(f"""select {py} py, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE nature, count(*) n, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd
    from {t} p join {FIX} c on c.NPI=p.NPI group by 1,2""" for py, t in OP.items()) + " order by 1, 4 desc", "nature by year")

# 4. Top payers, fixed cohort, 3 years pooled, with per-year split
R["payers"] = run(f"""select payer, sum(usd) usd, sum(n) n, count(distinct npi) npis,
    sum(iff(py=2022,usd,0)) usd22, sum(iff(py=2023,usd,0)) usd23, sum(iff(py=2024,usd,0)) usd24 from (""" +
    " union all ".join(f"""select {py} py, APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME payer, p.NPI npi, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS usd, 1 n
    from {t} p join {FIX} c on c.NPI=p.NPI""" for py, t in OP.items()) + ") group by 1 order by 2 desc limit 15", "top payers pooled")

# 5. Specialty: opt-out roster label, fixed cohort, pooled; with cohort size per specialty for a paid-rate
R["specialty"] = run(f"""with paid as (""" + " union all ".join(f"""select {py} py, c.NPI, c.specialty, p.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS usd
    from {t} p join {FIX} c on c.NPI=p.NPI""" for py, t in OP.items()) + f""")
    select c.specialty, count(distinct c.NPI) cohort, count(distinct paid.NPI) paid_npis, sum(paid.usd) usd,
      sum(iff(paid.py=2022,paid.usd,0)) usd22, sum(iff(paid.py=2023,paid.usd,0)) usd23, sum(iff(paid.py=2024,paid.usd,0)) usd24
    from {FIX} c left join paid on paid.NPI=c.NPI group by 1 order by 4 desc nulls last limit 20""", "specialty pooled")

# 6. Concentration: top recipients, fixed cohort, pooled
R["top_npis"] = run(f"""select npi, min(specialty) specialty, min(st) st, sum(usd) usd, sum(n) n, count(distinct payer) payers,
    sum(iff(nature like 'Compensation for services%',usd,0)) usd_consult, sum(iff(nature like 'Royalty%',usd,0)) usd_royalty from (""" +
    " union all ".join(f"""select p.NPI npi, c.specialty, c.st, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS usd, 1 n,
    APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME payer, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE nature
    from {t} p join {FIX} c on c.NPI=p.NPI""" for py, t in OP.items()) + ") group by 1 order by 4 desc limit 25", "top recipients pooled")
R["concentration"] = run(f"""with x as (select npi, sum(usd) usd from (""" +
    " union all ".join(f"select p.NPI npi, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS usd from {t} p join {FIX} c on c.NPI=p.NPI" for py, t in OP.items()) +
    """) group by 1), r as (select usd, row_number() over (order by usd desc) rk, sum(usd) over () tot from x)
    select count(*) paid_npis, max(tot) tot, sum(iff(rk<=10,usd,0)) top10, sum(iff(rk<=100,usd,0)) top100,
      sum(iff(usd<100,1,0)) under_100, median(usd) med_per_npi from r""", "concentration pooled")

# 7. Sanity: opt-out specialty vs Open Payments' own specialty for the same NPI (is the roster label trustworthy?)
R["spec_xcheck"] = run(f"""select c.specialty roster, p.COVERED_RECIPIENT_SPECIALTY_1 op_spec, count(distinct p.NPI) npis, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd
    from {OP[2023]} p join {FIX} c on c.NPI=p.NPI group by 1,2 order by 4 desc limit 12""", "specialty cross-check PY2023")

json.dump(R, open("reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/results.json", "w"), indent=1, default=str)
for k, v in R.items():
    print("\n##", k)
    for r in v[:25]: print(r)
