"""Hunch 92: House office money (MRA disbursements) to payees who also donate to that member's campaign.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/92_office_money_to_donors/probe.py
"""
import json, sys
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
open_log(HERE / "probe.log")
out = {}
if (HERE / "results.json").exists():
    out.update(json.load(open(HERE / "results.json")))
def q(k, sql):
    if k in out: return
    out[k] = run(sql, k)
    json.dump(out, open(HERE / "results.json", "w"), default=str, indent=1)

# Detail rows only (subtotal trap), member offices only, AMOUNT via try_to_number.
DETAIL = """LIBRARY_RAW.LANDING.FED_HOUSE_DISBURSEMENTS
 where DESCRIPTION not ilike '%TOTALS%' and C_ORGANIZATION regexp '^[0-9]{4} HON\\\\. .*'"""

# Key checks before any join.
q("leg_keys", """select count(*) n, count(distinct BIOGUIDE) bioguides,
 sum(iff(TERM_TYPE='rep' and TERM_END >= '2016-01-01',1,0)) reps_since_2016
 from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS""")
q("cm_keys", """select count(*) n, count(distinct CMTE_ID) cmtes, count(distinct CAND_ID) cands,
 sum(iff(CMTE_DSGN='P',1,0)) principal_rows from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM""")

# Office name -> legislator (rep, served since 2016) on last name + first initial. Report the match rate.
OFFICES = f"""
offices as (
  select distinct regexp_replace(C_ORGANIZATION, '^[0-9]{{4}} HON\\\\. ', '') office
  from {DETAIL}),
office_names as (
  select office,
    upper(regexp_replace(regexp_replace(office, ' (JR\\\\.?|SR\\\\.?|II|III|IV)$', ''), '[^A-Z ]', '')) clean
  from offices),
office_parts as (
  select office, clean,
    regexp_substr(clean, '[A-Z]+$') last_nm,
    left(clean, 1) first_init
  from office_names),
reps as (
  select BIOGUIDE, upper(regexp_replace(NAME_LAST,'[^A-Za-z]','')) last_nm, upper(left(NAME_FIRST,1)) first_init,
    STATE, DISTRICT, NAME_OFFICIAL_FULL, FEC_IDS
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS
  where TERM_TYPE='rep' and TERM_END >= '2016-01-01'),
matched as (
  select o.office, r.BIOGUIDE, r.STATE, r.DISTRICT, r.NAME_OFFICIAL_FULL, r.FEC_IDS,
    count(*) over (partition by o.office) n_hits
  from office_parts o join reps r on o.last_nm = r.last_nm and o.first_init = r.first_init),
member as (select * from matched where n_hits = 1)
"""
q("office_match", f"""with {OFFICES}
 select (select count(*) from offices) offices,
        (select count(distinct office) from matched) matched_any,
        (select count(*) from member) matched_unique""")

# Member -> principal campaign committees via FEC candidate ids.
CMTES = f"""
member_cmte as (
  select m.office, m.BIOGUIDE, m.STATE, m.DISTRICT, m.NAME_OFFICIAL_FULL, c.CMTE_ID
  from member m, lateral flatten(input => try_parse_json(m.FEC_IDS)) f
  join (select distinct CMTE_ID, CAND_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM
        where CMTE_DSGN in ('P','A') and CAND_ID like 'H%') c on c.CAND_ID = f.value::string)
"""
q("member_cmte", f"""with {OFFICES}, {CMTES}
 select count(distinct office) offices_with_cmte, count(distinct CMTE_ID) cmtes from member_cmte""")

# Payees: person-shaped vendor names (LAST FIRST [MI]), 2+ words, no company words; key = LAST, FIRST.
PAYEES = f"""
pay as (
  select regexp_replace(C_ORGANIZATION, '^[0-9]{{4}} HON\\\\. ', '') office,
    left(C_ORGANIZATION,4) yr,
    upper(regexp_replace(VENDOR_NAME, '[^A-Za-z ]', '')) vn,
    SORT_SUBTOTAL_DESCRIPTION cat, try_to_number(AMOUNT) amt
  from {DETAIL} and try_to_number(AMOUNT) > 0),
pay_person as (
  select office, yr, cat, amt,
    split_part(vn,' ',1) || ', ' || split_part(vn,' ',2) pkey
  from pay
  where regexp_count(vn, ' ') between 1 and 3
    and not vn regexp '.*\\\\b(INC|LLC|CORP|CO|LTD|LP|LLP|SERVICES|SERVICE|GROUP|COMPANY|ASSOC|ASSOCIATES|OFFICE|CITI|PCARD|AIRLINES|AIR|HOTEL|INN|BANK|USPS|POSTAL|VERIZON|ATT|COMCAST|AMAZON|STAPLES|UNITED|AMERICAN|DELTA|SOUTHWEST|PRINTING|MAIL|SYSTEMS|SOLUTIONS|TECHNOLOGIES|MEDIA|COMMUNICATIONS|PROPERTIES|REALTY|MANAGEMENT|PARTNERS|ENTERPRISES|STORE|MARKET|CAFE|RESTAURANT|CATERING|PIZZA|GOVERNMENT|CITY|COUNTY|STATE|UNIVERSITY|SCHOOL|CHURCH|CENTER|CLUB|FOUNDATION|ASSOCIATION|CHAMBER|DEPT|DEPARTMENT|TREASURER|TREASURY|HOUSE|CAO|SAA|CLERK|FEDEX|UPS|GRAINGER|DELL|APPLE|MICROSOFT|GOOGLE|FACEBOOK|WALMART|COSTCO|TARGET|HOME|DEPOT|OFFICEMAX|LEASING|RENTAL|RENTALS|AUTO|CAR|CARS|TAXI|UBER|LYFT|PARKING|ENTERPRISE|HERTZ|AVIS|BUDGET|NATIONAL|MARRIOTT|HILTON|HYATT|HOLIDAY|AMTRAK|ALASKA|JETBLUE|FRONTIER|SPIRIT|EXPRESS|VISA|MASTERCARD|CARD|SHELL|EXXON|CHEVRON|BP|SUNOCO|SPEEDWAY|CIRCLE|WAWA)\\\\b.*'
    and split_part(vn,' ',2) <> '' and len(split_part(vn,' ',1)) >= 2 and len(split_part(vn,' ',2)) >= 2),
donor as (
  select CMTE_ID,
    upper(regexp_replace(split_part(DONOR_NAME, ',', 1), '[^A-Za-z]', '')) || ', ' ||
      upper(regexp_replace(split_part(trim(split_part(DONOR_NAME, ',', 2)), ' ', 1), '[^A-Za-z]', '')) dkey,
    DONOR_NAME, CITY, STATE, TRANSACTION_DATE, TRANSACTION_AMT
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
  where ENTITY_TYPE = 'IND' and TRANSACTION_AMT > 0 and DONOR_NAME like '%,%'
    and CMTE_ID in (select CMTE_ID from member_cmte)),
paid as (
  select office, pkey, cat, sum(amt) paid, count(*) n_pay, min(yr) y0, max(yr) y1
  from pay_person group by 1,2,3),
gave as (
  select mc.office, d.dkey, sum(d.TRANSACTION_AMT) gave, count(*) n_gifts,
    min(d.TRANSACTION_DATE) g0, max(d.TRANSACTION_DATE) g1,
    min(d.DONOR_NAME) donor_name_sample, min(d.CITY || ', ' || d.STATE) donor_city_sample
  from donor d join member_cmte mc on mc.CMTE_ID = d.CMTE_ID
  group by 1,2),
hits as (
  select p.office, p.pkey, p.cat, p.paid, p.n_pay, p.y0, p.y1, g.gave, g.n_gifts, g.g0, g.g1, g.donor_name_sample, g.donor_city_sample
  from paid p join gave g on g.office = p.office and g.dkey = p.pkey)
"""
q("payee_shape", f"""with {OFFICES}, {CMTES}, {PAYEES}
 select count(*) person_rows, count(distinct pkey) person_keys, sum(amt) person_dollars,
   sum(iff(cat='PERSONNEL COMPENSATION',amt,0)) staff_dollars,
   (select sum(amt) from pay) all_detail_dollars
 from pay_person""")
q("headline", f"""with {OFFICES}, {CMTES}, {PAYEES}
 select cat, count(*) pairs, count(distinct office) offices, count(distinct pkey) payees,
   sum(paid) paid, sum(gave) gave, sum(n_gifts) gifts
 from hits group by 1 order by paid desc""")
q("top_nonstaff", f"""with {OFFICES}, {CMTES}, {PAYEES}
 select * from hits where cat <> 'PERSONNEL COMPENSATION' order by paid desc limit 40""")
q("top_staff", f"""with {OFFICES}, {CMTES}, {PAYEES}
 select * from hits where cat = 'PERSONNEL COMPENSATION' order by gave desc limit 15""")
q("per_office_nonstaff", f"""with {OFFICES}, {CMTES}, {PAYEES}
 select office, count(*) payees, sum(paid) paid, sum(gave) gave from hits where cat <> 'PERSONNEL COMPENSATION'
 group by 1 order by paid desc limit 20""")

# Vintage check on the FEC mart, and the real-vendor cut: payees never paid as staff by any office.
q("fec_vintage", """select min(TRANSACTION_DATE) d0, max(TRANSACTION_DATE) d1, count(*) n
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS""")
q("true_vendors", f"""with {OFFICES}, {CMTES}, {PAYEES},
 staff_keys as (select distinct pkey from pay_person where cat = 'PERSONNEL COMPENSATION')
 select h.*, (select count(*) from hits h2 where h2.cat <> 'PERSONNEL COMPENSATION' and h2.pkey not in (select pkey from staff_keys)) n_pairs_total
 from hits h where h.cat <> 'PERSONNEL COMPENSATION' and h.pkey not in (select pkey from staff_keys)
 order by h.paid desc limit 40""")
q("true_vendors_total", f"""with {OFFICES}, {CMTES}, {PAYEES},
 staff_keys as (select distinct pkey from pay_person where cat = 'PERSONNEL COMPENSATION')
 select count(*) pairs, count(distinct office) offices, count(distinct pkey) payees, sum(paid) paid, sum(gave) gave
 from hits where cat <> 'PERSONNEL COMPENSATION' and pkey not in (select pkey from staff_keys)""")
q("fec_years", """select year(TRANSACTION_DATE) y, count(*) n, sum(TRANSACTION_AMT) amt
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS group by 1 order by 1""")
