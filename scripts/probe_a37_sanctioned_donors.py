"""A37 - do people on sanctions lists show up as FEC donors?

Match is LAST|FIRST on a stripped, uppercased name. Middle names are dropped
on both sides. A hit is a name collision, never a person, until a human checks
date of birth, city, and employer.
"""
import csv
from connect.db import connect, dicts

FEC = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS"
OFAC = "LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN"
UK = "LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_UK_SANCTIONS_LIST"
UN = "LIBRARY_RAW.LANDING.INTL_UN_CONSOLIDATED_SANCTIONS"

# one scrub, used on every name on both sides
SCRUB = "upper(regexp_replace({c}, '[^A-Za-z ]', ''))"

SANCTIONED = """
with ofac as (
  select 'OFAC' as list, PROGRAM as regime, SDN_NAME as raw_name,
         trim(split_part(SDN_NAME, ',', 1)) as last_raw,
         trim(split_part(split_part(SDN_NAME, ',', 2), ' ', 2)) as first_raw
  from {OFAC}
  where IS_INDIVIDUAL and SDN_NAME like '%,%'
),
uk as (
  select 'UK' as list, REGIME_NAME as regime,
         NAME_6 || ', ' || coalesce(NAME_1, '') as raw_name,
         NAME_6 as last_raw, NAME_1 as first_raw
  from {UK}
  where TYPE_OF_ENTITY is null and NAME_6 is not null and NAME_1 is not null
),
un as (
  -- UN lists given names in order, so the surname is the last part filled in
  select 'UN' as list, UN_LIST_TYPE as regime,
         coalesce(FOURTH_NAME, THIRD_NAME, SECOND_NAME) || ', ' || FIRST_NAME as raw_name,
         coalesce(FOURTH_NAME, THIRD_NAME, SECOND_NAME) as last_raw,
         FIRST_NAME as first_raw
  from {UN}
  where RECORD_TYPE = 'INDIVIDUAL'
    and FIRST_NAME is not null and SECOND_NAME is not null
)
select list, regime, raw_name,
       {last_k} as last_k, {first_k} as first_k
from (select * from ofac union all select * from uk union all select * from un)
where len({last_k}) >= 3 and len({first_k}) >= 3
""".format(
    OFAC=OFAC, UK=UK, UN=UN,
    last_k=SCRUB.format(c="last_raw"),
    first_k=SCRUB.format(c="first_raw"),
)

DONORS = f"""
select {SCRUB.format(c="trim(split_part(DONOR_NAME, ',', 1))")} as last_k,
       {SCRUB.format(c="trim(split_part(split_part(DONOR_NAME, ',', 2), ' ', 2))")} as first_k,
       DONOR_NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
       TRANSACTION_DATE, TRANSACTION_AMT, CMTE_ID
from {FEC}
where ENTITY_TYPE = 'IND' and not coalesce(IS_MEMO_TRANSACTION, false)
"""

# how many different donor names in all of FEC carry that same LAST|FIRST key.
# a key held by thousands of people is a collision, not a lead.
RARITY = f"""
with s as ({SANCTIONED}), d as ({DONORS})
select s.list, s.regime, s.raw_name as sanctioned_name,
       count(distinct d.DONOR_NAME) as distinct_donor_spellings,
       count(distinct d.ZIP_CODE) as distinct_zips,
       count(distinct d.STATE) as distinct_states,
       count(*) as gifts,
       sum(d.TRANSACTION_AMT) as total_amt,
       min(d.TRANSACTION_DATE) as first_gift,
       max(d.TRANSACTION_DATE) as last_gift,
       any_value(d.CITY) as a_city,
       any_value(d.EMPLOYER) as an_employer,
       any_value(d.OCCUPATION) as an_occupation
from s join d on s.last_k = d.last_k and s.first_k = d.first_k
group by all
having count(distinct d.ZIP_CODE) <= 3
order by total_amt desc
"""

MATCHES = f"""
with s as ({SANCTIONED}), d as ({DONORS})
select s.list, s.regime, s.raw_name as sanctioned_name,
       d.DONOR_NAME, d.CITY, d.STATE, d.ZIP_CODE, d.EMPLOYER, d.OCCUPATION,
       count(*) as gifts,
       sum(d.TRANSACTION_AMT) as total_amt,
       min(d.TRANSACTION_DATE) as first_gift,
       max(d.TRANSACTION_DATE) as last_gift,
       count(distinct d.CMTE_ID) as committees
from s join d on s.last_k = d.last_k and s.first_k = d.first_k
group by all
order by total_amt desc
"""

COUNTS = f"""
with s as ({SANCTIONED}), d as ({DONORS})
select count(distinct s.raw_name) as sanctioned_people_hit,
       count(*) as donation_rows,
       sum(d.TRANSACTION_AMT) as total_amt
from s join d on s.last_k = d.last_k and s.first_k = d.first_k
"""

if __name__ == "__main__":
    conn = connect()
    try:
        print("== headline count")
        for r in dicts(conn, COUNTS):
            print(r)
        print("== rare keys only, 3 zips or fewer")
        rare = dicts(conn, RARITY)
        with open("outputs/a37_rare_key_candidates.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rare[0].keys()))
            w.writeheader()
            w.writerows(rare)
        print("rare candidates:", len(rare))
        for r in rare[:20]:
            print(r["LIST"], "|", r["SANCTIONED_NAME"], "|", r["A_CITY"], r["DISTINCT_STATES"],
                  "|", r["TOTAL_AMT"], "|", r["GIFTS"], "|", r["AN_OCCUPATION"])
        print("== writing matches")
        rows = dicts(conn, MATCHES)
        out = "outputs/a37_sanctioned_donor_name_matches.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(out, len(rows), "rows")
        for r in rows[:15]:
            print(r["LIST"], "|", r["SANCTIONED_NAME"], "|", r["DONOR_NAME"],
                  "|", r["STATE"], "|", r["TOTAL_AMT"], "|", r["GIFTS"])
    finally:
        conn.close()
