"""E57 probe 2: hygiene on both mart tables. Logs to queries.log."""
import json
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
open_log(HERE / "queries.log")
OP = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS"
PB = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER"
def show(r): print(json.dumps(r, indent=1, default=str))

show(run(f"""select program_year, count(*) rows_, count(distinct npi) npis,
  sum(case when npi is null or trim(npi)='' then 1 else 0 end) blank_npi,
  sum(total_amount_of_payment_usdollars) usd, min(date_of_payment) mind, max(date_of_payment) maxd
  from {OP} group by 1""", "op_profile"))
show(run(f"""select sum(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,18,2)) usd, count(*) rows_
  from LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS""", "op_landing_sum_check"))
show(run(f"""select nature_of_payment_or_transfer_of_value nature, count(*) rows_, count(distinct npi) npis,
  sum(total_amount_of_payment_usdollars) usd from {OP} group by 1 order by usd desc""", "op_nature"))
show(run(f"""select covered_recipient_type, count(*) rows_, sum(total_amount_of_payment_usdollars) usd from {OP} group by 1""", "op_recipient_type"))
show(run(f"""select rndrng_prvdr_ent_cd ent, count(*) rows_, count(distinct rndrng_npi) npis,
  sum(tot_mdcr_alowd_amt) allowed, sum(case when tot_mdcr_alowd_amt is null then 1 else 0 end) null_allowed,
  sum(case when rndrng_npi is null or trim(rndrng_npi)='' or rndrng_npi='0000000000' or length(rndrng_npi)<>10 then 1 else 0 end) bad_npi
  from {PB} group by 1""", "pb_profile"))
show(run(f"""select count(*) n_types, sum(case when rndrng_prvdr_type is null or trim(rndrng_prvdr_type)='' then 1 else 0 end) blank
  from (select rndrng_prvdr_type, count(*) c from {PB} where rndrng_prvdr_ent_cd='I' group by 1)""", "pb_types"))
