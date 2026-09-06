"""Hunch 88: same person is treasurer of an IRS 527 and an FEC committee. Match = FIRST+LAST tokens (order-free) AND ZIP5."""
from _shared.q import open_log, run
from pathlib import Path
open_log(Path(__file__).with_name("probe.log"))
R = "LIBRARY_RAW.LANDING"; M = "LIBRARY_MARTS"
def show(sql, l):
    rows = run(sql, l)
    for r in rows: print(l, r)
    return rows

show(f"select c1,c2,c3,c6,c7,c8 from {R}.FED_FEC_COMMITTEES limit 3", "cm_landing_sample")
show(f"select count(*) n, count(distinct c1) cmte_ids, count(distinct c1||'|'||c3||'|'||left(c8,5)) id_tres_zip, sum(iff(regexp_like(left(c8,5),'^[0-9]{{5}}$'),1,0)) zip5_ok from {R}.FED_FEC_COMMITTEES", "cm_keys")
show(f"select entity_title, count(*) n from {M}.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS where entity_title ilike '%treas%' group by 1 order by 2 desc limit 5", "t527_titles")
show(f"select count(*) n, count(distinct ein) eins, count(distinct entity_name||'|'||left(entity_zip,5)) name_zip, sum(iff(regexp_like(left(entity_zip,5),'^[0-9]{{5}}$'),1,0)) zip5_ok from {M}.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS where entity_title ilike '%treas%'", "t527_keys")

# order-free 2-token key: sort(first token, last token) of the letters-only name
TOK = lambda col: f"array_to_string(array_sort(array_construct(split_part(regexp_replace(upper(trim({col})),'[^A-Z ]',''),' ',1), split_part(regexp_replace(upper(trim({col})),'[^A-Z ]',''),' ',-1))),'|')"
T527 = f"select distinct ein, org_name, entity_name, {TOK('entity_name')} k, left(entity_zip,5) z, entity_city, entity_state from {M}.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS where entity_title ilike '%treas%' and entity_name like '% %' and regexp_like(left(entity_zip,5),'^[0-9]{{5}}$')"
# FEC: TRES_NM is 'LAST, FIRST M' -> first token = last name, first token after comma = first name; some rows are 'FIRST LAST' with no comma
FEC = f"""select distinct c1 cmte_id, c2 cmte_nm, c3 tres_nm, c10 cmte_tp, c7 st, c6 city,
  iff(c3 like '%,%', array_to_string(array_sort(array_construct(regexp_replace(upper(trim(split_part(c3,',',1))),'[^A-Z ]',''), split_part(regexp_replace(upper(trim(split_part(c3,',',2))),'[^A-Z ]',''),' ',1))),'|'), {TOK('c3')}) k,
  left(c8,5) z from {R}.FED_FEC_COMMITTEES where c3 like '% %' and regexp_like(left(c8,5),'^[0-9]{{5}}$')"""
show(f"with t as ({T527}) select count(*) n, count(distinct k) keys from t", "t527_norm")
show(f"with f as ({FEC}) select count(*) n, count(distinct k) keys, count(distinct cmte_id) cmtes from f", "fec_norm")
J = f"with t as ({T527}), f as ({FEC}) select t.k, t.z, t.entity_name n527, t.org_name org527, t.entity_state st527, f.tres_nm, f.cmte_nm, f.cmte_id, f.cmte_tp, f.st stfec from t join f on t.k=f.k and t.z=f.z"
show(f"with j as ({J}) select count(*) pairs, count(distinct k||z) people, count(distinct org527) orgs527, count(distinct cmte_id) fec_cmtes from j", "hit_total")
show(f"with j as ({J}) select k, z, count(distinct org527) n527, count(distinct cmte_id) nfec from j group by 1,2 order by 3 desc, 4 desc limit 5", "hit_fanout")
show(f"with j as ({J}) select * from j qualify row_number() over (partition by k,z order by cmte_id) = 1 order by random() limit 15", "hit_sample")
# sensitivity: name-only (no zip) to show why zip matters
show(f"with t as ({T527}), f as ({FEC}) select count(distinct t.k) people_name_only from t join f on t.k=f.k", "name_only_ctrl")
# bridge vs mirror: the same committee files an IRS 8871 and an FEC Form 1, so same-name-both-sides is not a bridge. Count people with at least one pair where the org names differ.
NM = lambda c: f"regexp_replace(upper({c}),'[^A-Z]','')"
show(f"""with j as ({J}), p as (select k, z, count(*) pairs, sum(iff({NM('org527')}={NM('cmte_nm')} or {NM('cmte_nm')} like '%'||left({NM('org527')},12)||'%' or {NM('org527')} like '%'||left({NM('cmte_nm')},12)||'%',0,1)) diff_pairs, count(distinct org527) n527 from j group by 1,2)
select count(*) people, sum(iff(diff_pairs>0,1,0)) people_bridging, sum(iff(diff_pairs>0 and n527<=5,1,0)) bridging_not_pro, sum(iff(n527>20,1,0)) pro_treasurers from p""", "bridge_vs_mirror")
show(f"""with j as ({J}) select k, z, n527, org527, tres_nm, cmte_nm, cmte_tp from j where {NM('org527')}<>{NM('cmte_nm')} and {NM('cmte_nm')} not like '%'||left({NM('org527')},12)||'%' and {NM('org527')} not like '%'||left({NM('cmte_nm')},12)||'%'
qualify count(distinct org527) over (partition by k,z) <= 5 order by random() limit 8""", "bridge_sample")
