"""Hunch 87: FARA short-form registrants (individual agents) giving to FEC committees inside their registration window."""
from _shared.q import open_log, run
from pathlib import Path
open_log(Path(__file__).with_name("probe.log"))
R = "LIBRARY_RAW.LANDING"
def show(sql, l):
    rows = run(sql, l)
    for r in rows: print(l, r)
    return rows

show(f"select count(*) n, count(distinct registration_number) regs, count(distinct short_form_name) sfn, count(distinct short_form_last_name||'|'||short_form_first_name) lf, min(short_form_date) mn, max(short_form_date) mx, sum(iff(short_form_termination_date='',1,0)) open_ from {R}.FED_FARA_BULK where document_type='Short-Form'", "sf_shape")
show(f"select short_form_name, short_form_last_name, short_form_first_name, short_form_date, short_form_termination_date, registrant_name, registration_number from {R}.FED_FARA_BULK where document_type='Short-Form' limit 5", "sf_sample")
show(f"select count(*) n, count(distinct registration_number) regs, count(distinct foreign_principal_country) countries from {R}.FED_FARA_BULK where document_type='Exhibit AB'", "fp_shape")

# Short-Form rows carry the person only in SHORT_FORM_NAME ('Last, First'); the LAST/FIRST/DATE columns are blank on every one (checked: 0 of 43,168 filled).
# Window = the agent's own DATE_STAMPED (filing date) to the registrant's TERMINATION_DATE from the blank-DOCUMENT_TYPE registrant rows, else today.
AGENTS = f"""
select regexp_replace(upper(trim(split_part(s.short_form_name,',',1))),'[^A-Z ]','') || '|' || split_part(regexp_replace(upper(trim(split_part(s.short_form_name,',',2))),'[^A-Z ]',''),' ',1) k,
       s.registration_number, s.registrant_name, try_to_date(s.date_stamped,'MM/DD/YYYY') d0,
       coalesce(r.term, current_date) d1
from {R}.FED_FARA_BULK s
left join (select registration_number, max(try_to_date(termination_date,'MM/DD/YYYY')) term from {R}.FED_FARA_BULK where document_type='' group by 1) r using (registration_number)
where s.document_type='Short-Form' and s.short_form_name like '%,%'
"""
show(f"with a as ({AGENTS}) select count(*) n, count(distinct k) keys, count(distinct registration_number) regs, sum(iff(d0 is null,1,0)) null_d0 from a", "agent_keys")

HIT = f"""
with a as ({AGENTS}),
f as (select regexp_replace(upper(trim(split_part(name,',',1))),'[^A-Z ]','') || '|' || split_part(regexp_replace(upper(trim(split_part(name,',',2))),'[^A-Z ]',''),' ',1) k,
             try_to_date(transaction_dt,'MMDDYYYY') dt, transaction_amt::number amt, cmte_id, employer, city, state
      from {R}.FED_FEC_INDIV_CONTRIBUTIONS where entity_tp='IND' and name like '%,%'),
j as (select f.k, f.cmte_id, f.amt, f.employer, f.city, f.state, f.dt, a.registration_number, a.registrant_name, a.d0, a.d1,
             iff(f.dt between a.d0 and a.d1, 1, 0) in_window
      from f join a on f.k = a.k)
select k, any_value(registrant_name) registrant, count(distinct registration_number) regs, count(*) fec_rows, sum(amt) dollars,
       sum(in_window) rows_in_window, sum(iff(in_window=1,amt,0)) dollars_in_window,
       count(distinct employer) employers, any_value(employer) a_employer, any_value(city) a_city, any_value(state) a_state
from (select *, row_number() over (partition by k, cmte_id, amt, dt, registration_number order by in_window desc) rn from j) where rn=1
group by 1
"""
show(f"with h as ({HIT}) select count(*) keys_hit, sum(fec_rows) fec_rows, sum(dollars) dollars, sum(iff(rows_in_window>0,1,0)) keys_in_window, sum(rows_in_window) rows_in_window, sum(dollars_in_window) dollars_in_window, sum(iff(fec_rows<=50,1,0)) keys_le50 from h", "hit_total")
show(f"with h as ({HIT}) select * from h order by fec_rows desc limit 8", "hit_top_noisy")
show(f"with h as ({HIT}) select * from h where rows_in_window>0 and fec_rows<=50 order by dollars_in_window desc limit 15", "hit_in_window")
# employer leg: registrant firm name (multi-word) = FEC EMPLOYER, exact
show(f"""with r as (select distinct regexp_replace(upper(trim(registrant_name)),'[^A-Z0-9 ]','') rn from {R}.FED_FARA_BULK where document_type='Registration Statement' and registrant_name like '% %'),
f as (select regexp_replace(upper(trim(employer)),'[^A-Z0-9 ]','') e, transaction_amt::number amt from {R}.FED_FEC_INDIV_CONTRIBUTIONS where entity_tp='IND')
select count(distinct rn) firms_hit, count(*) fec_rows, sum(amt) dollars from f join r on f.e = r.rn""", "employer_leg")
# identity-confirmed leg: same name AND the FEC EMPLOYER string starts with the same 8 letters as the FARA registrant firm, inside the window.
L8 = lambda c: f"left(regexp_replace(upper({c}),'[^A-Z]',''),8)"
CONF = f"""
with a as ({AGENTS}),
f as (select regexp_replace(upper(trim(split_part(name,',',1))),'[^A-Z ]','') || '|' || split_part(regexp_replace(upper(trim(split_part(name,',',2))),'[^A-Z ]',''),' ',1) k,
             try_to_date(transaction_dt,'MMDDYYYY') dt, transaction_amt::number amt, cmte_id, employer, city, state
      from {R}.FED_FEC_INDIV_CONTRIBUTIONS where entity_tp='IND' and name like '%,%' and length(employer)>=8)
select f.k, a.registrant_name, a.registration_number, f.employer, f.city, f.state, f.amt, f.dt, f.cmte_id
from f join a on f.k=a.k and {L8('f.employer')}={L8('a.registrant_name')} and f.dt between a.d0 and a.d1
qualify row_number() over (partition by f.k, f.cmte_id, f.amt, f.dt order by a.registration_number)=1
"""
show(f"with c as ({CONF}) select count(distinct k) agents, count(distinct registration_number) firms, count(*) fec_rows, sum(amt) dollars, count(distinct cmte_id) cmtes from c", "confirmed_total")
show(f"with c as ({CONF}) select k, any_value(registrant_name) firm, any_value(employer) employer, any_value(city) city, count(*) n, sum(amt) dollars from c group by 1 order by 6 desc limit 10", "confirmed_top")
