"""81 - did executives sell stock before their pension plan collapsed onto PBGC?

Chain, four hops, every one a hard identifier:
  PBGC trusteed plans  --EIN-->  SEC DERA submissions  --CIK-->
  Form 4 submissions   --ACCESSION_NUMBER-->  non-derivative transactions

Windows that bound the answer:
  Form 4 filings loaded:      2016-07 to 2025-03
  PBGC terminations loaded:   1972 to 2026
So only terminations from 2016 onward can be tested at all.
"""
import csv
from connect.db import connect, dicts

PBGC = "LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS"
SUB = "LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION"
OWN = "LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER"
DERIV = "LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS"
TRANS = "LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS"
QUARTERS = ["2024Q1", "2024Q2", "2024Q3", "2024Q4",
            "2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1"]

# EIN widths differ. PBGC drops leading zeros, so 531 of its EINs are
# 8 characters. DERA pads to 9 and uses '000000000' where it has none.
# Both sides get stripped to digits and left-padded to 9.
DERA = " union all ".join(
    f"select EIN, CIK, NAME from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_{q}"
    for q in QUARTERS
)

BRIDGE = f"""
with pbgc as (
  select lpad(regexp_replace(EIN, '[^0-9]', ''), 9, '0') as ein_k,
         SPONSOR_NAME, PLAN_NAME, STATE,
         DATE_OF_PLAN_TERMINATION as term_date,
         DATE_OF_PBGC_TRUSTEESHIP as trustee_date,
         NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION as participants
  from {PBGC}
  where EIN is not null
),
dera as (
  -- NAME is deliberately out of the distinct key. One filer spelled two
  -- ways across quarters would otherwise multiply every transaction.
  select distinct lpad(regexp_replace(EIN, '[^0-9]', ''), 9, '0') as ein_k,
         CIK
  from ({DERA})
  where EIN is not null and CIK is not null
    and regexp_replace(EIN, '[^0-9]', '') <> '000000000'
)
select p.*, d.CIK
from pbgc p join dera d on p.ein_k = d.ein_k
"""

WIDTHS = f"""
select 'pbgc' as side, length(regexp_replace(EIN, '[^0-9]', '')) as ein_len,
       count(*) as n
from {PBGC} group by all
union all
select 'dera', length(regexp_replace(EIN, '[^0-9]', '')), count(*)
from ({DERA}) group by all
union all
select 'dera_placeholder_zeros', 9, count(*)
from ({DERA}) where regexp_replace(EIN, '[^0-9]', '') = '000000000'
order by 1, 2
"""

COVERAGE = f"""
with b as ({BRIDGE})
select count(*) as bridged_rows,
       count(distinct ein_k) as bridged_eins,
       count(distinct CIK) as bridged_ciks,
       count_if(term_date >= '2016-01-01') as testable_rows
from b
"""

# every way an insider turns holdings into cash or hands them back.
#   S open-market sale   D disposition to the issuer
#   F shares withheld for tax   M option exercise
# Derivative transactions are pulled in too, not just common stock.
SALES = f"""
with b as ({BRIDGE}),
sub as (
  select ACCESSION_NUMBER, ISSUER_CIK, ISSUER_NAME, PERIOD_OF_REPORT
  from {SUB}
  where DOCUMENT_TYPE in ('4', '4/A')
),
tx as (
  select ACCESSION_NUMBER, TRANSACTION_SK, 'common' as leg, TRANSACTION_DATE,
         SHARES, PRICE_PER_SHARE, TRANSACTION_VALUE, TRANSACTION_CODE
  from {TRANS}
  where TRANSACTION_CODE in ('S', 'D', 'F', 'M')
    and TRANSACTION_DATE between '2016-01-01' and '2026-12-31'
  union all
  -- the derivative table names every column differently
  select ACCESSION_NUMBER, DERIV_TRANS_SK, 'derivative' as leg, TRANS_DATE,
         TRANS_SHARES, TRANS_PRICEPERSHARE, TRANS_TOTAL_VALUE, TRANS_CODE
  from {DERIV}
  where TRANS_CODE in ('S', 'D', 'F', 'M')
    and TRANS_DATE between '2016-01-01' and '2026-12-31'
),
-- one filing can name several owners. Collapse them so a two-owner
-- filing does not double every dollar on its transactions.
own as (
  select ACCESSION_NUMBER,
         listagg(distinct OWNER_NAME, ' + ') as owner_names,
         listagg(distinct TITLE, ' + ') as titles,
         count(distinct OWNER_CIK) as owner_count
  from {OWN}
  group by ACCESSION_NUMBER
)
select b.SPONSOR_NAME, b.PLAN_NAME, b.STATE, b.participants,
       b.term_date, b.trustee_date, b.CIK, s.ISSUER_NAME,
       o.owner_names, o.titles, o.owner_count, t.leg,
       t.TRANSACTION_CODE, t.TRANSACTION_DATE, t.SHARES, t.PRICE_PER_SHARE, t.TRANSACTION_VALUE,
       datediff('day', t.TRANSACTION_DATE, b.term_date) as days_before_termination
from b
join sub s on try_to_number(s.ISSUER_CIK) = try_to_number(b.CIK)
join tx t on t.ACCESSION_NUMBER = s.ACCESSION_NUMBER
left join own o on o.ACCESSION_NUMBER = s.ACCESSION_NUMBER
where t.TRANSACTION_DATE < b.term_date
order by t.TRANSACTION_VALUE desc nulls last
"""

if __name__ == "__main__":
    conn = connect()
    try:
        print("== EIN widths on both sides")
        for r in dicts(conn, WIDTHS):
            print(r)
        print("== bridge coverage")
        print(dicts(conn, COVERAGE)[0])
        print("== every insider sale before the plan terminated")
        rows = dicts(conn, SALES)
        print("rows:", len(rows))
        if rows:
            out = "outputs/81_insider_sales_before_pension_termination.csv"
            with open(out, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
            print(out)
            for r in rows[:20]:
                print(r["SPONSOR_NAME"], "|", r["OWNER_NAMES"], "|", r["TITLES"],
                      "|", r["TRANSACTION_DATE"], "|", r["TRANSACTION_VALUE"],
                      "|", r["DAYS_BEFORE_TERMINATION"], "days before")
    finally:
        conn.close()
