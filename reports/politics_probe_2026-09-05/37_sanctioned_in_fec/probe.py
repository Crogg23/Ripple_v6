"""Hunch 37: sanctioned individuals (OFAC/UN/UK) whose SURNAME+FIRSTNAME appears in FEC individual contributions.
Multi-word only: key = SURNAME + first given name, both required."""
from _shared.q import open_log, run
from pathlib import Path
open_log(Path(__file__).with_name("probe.log"))
R = "LIBRARY_RAW.LANDING"
def show(sql, l):
    rows = run(sql, l)
    for r in rows: print(l, r)
    return rows

# one normalized key per source. FEC/OFAC are 'LAST, FIRST MIDDLE'; UK is NAME_6=surname NAME_1=first; UN is FIRST_NAME + last non-empty of 2nd/3rd/4th.
KEY_LF = lambda col: f"regexp_replace(upper(trim(split_part({col},',',1))),'[^A-Z ]','') || '|' || split_part(regexp_replace(upper(trim(split_part({col},',',2))),'[^A-Z ]',''),' ',1)"
SANC = f"""
select * from (
  select 'OFAC' src, program list, {KEY_LF('sdn_name')} k from {R}.FED_OFAC_SDN where sdn_type='individual' and sdn_name like '%,%'
  union all
  select 'UK', regime_name, regexp_replace(upper(trim(name_6)),'[^A-Z ]','') || '|' || split_part(regexp_replace(upper(trim(name_1)),'[^A-Z ]',''),' ',1)
    from {R}.INTL_UK_SANCTIONS_LIST where coalesce(type_of_entity,'')='' and coalesce(name_1,'')<>'' and coalesce(name_6,'')<>''
  union all
  select 'UN', un_list_type, regexp_replace(upper(trim(coalesce(nullif(fourth_name,''),nullif(third_name,''),second_name))),'[^A-Z ]','') || '|' || split_part(regexp_replace(upper(trim(first_name)),'[^A-Z ]',''),' ',1)
    from {R}.INTL_UN_CONSOLIDATED_SANCTIONS where record_type='INDIVIDUAL' and coalesce(second_name,'')<>''
) s0 where split_part(k,'|',1)<>'' and split_part(k,'|',2)<>''
"""
show(f"with s as ({SANC}) select src, count(*) rows_, count(distinct k) keys from s group by 1", "sanc_keys")
show(f"with s as ({SANC}) select * from s limit 5", "sanc_sample")

# the one big scan: FEC 84M rows, aggregated per sanctioned key
HIT = f"""
with s as ({SANC}), sk as (select k, min(src) src, listagg(distinct src,'+') srcs, any_value(list) list from s group by 1),
f as (select {KEY_LF('name')} k, transaction_amt::number amt, state, employer, city from {R}.FED_FEC_INDIV_CONTRIBUTIONS where entity_tp='IND' and name like '%,%')
select sk.k, sk.srcs, sk.list, count(*) fec_rows, sum(amt) dollars, count(distinct f.state) states, count(distinct f.employer) employers, any_value(f.city) a_city, any_value(f.state) a_state, any_value(f.employer) a_employer
from f join sk on f.k = sk.k group by 1,2,3
"""
tot = show(f"with h as ({HIT}) select count(*) keys_hit, sum(fec_rows) fec_rows, sum(dollars) dollars, sum(iff(fec_rows<=20,1,0)) keys_le20_rows, sum(iff(fec_rows<=20,fec_rows,0)) rows_le20 from h", "hit_total")
show(f"with h as ({HIT}) select * from h order by fec_rows desc limit 10", "hit_top_noisy")
show(f"with h as ({HIT}) select * from h where fec_rows<=20 order by fec_rows desc, dollars desc limit 15", "hit_rare")
