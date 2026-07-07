-- Daily US national debt (Treasury Debt to the Penny), typed mart — no casts needed.
select
    record_date,
    tot_pub_debt_out_amt / 1e12 as total_debt_tn,
    debt_held_public_amt / 1e12 as public_debt_tn,
    intragov_hold_amt / 1e12 as intragov_debt_tn
from THE_LIBRARY.ECONOMY.NATIONAL_DEBT_DAILY
order by record_date
