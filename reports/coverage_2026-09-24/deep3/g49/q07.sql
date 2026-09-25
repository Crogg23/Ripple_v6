-- Parentheticals: whole-table shape. Duplicates, blank text, score spread, how many rows say overruled/abrogated
select count(*) n, count(distinct ID) n_id, count(distinct DESCRIBED_OPINION_ID) n_described,
  count(distinct DESCRIBING_OPINION_ID) n_describing, count(distinct GROUP_ID) n_groups,
  count(distinct DESCRIBED_OPINION_ID||'|'||DESCRIBING_OPINION_ID||'|'||TEXT) n_distinct_triples,
  sum(iff(TEXT is null or trim(TEXT)='',1,0)) blank_text, median(length(TEXT)) med_len,
  min(try_to_double(SCORE)) min_score, max(try_to_double(SCORE)) max_score, sum(iff(try_to_double(SCORE) is null,1,0)) score_not_num,
  sum(iff(TEXT ilike '%overrul%',1,0)) says_overrul, sum(iff(TEXT ilike '%abrogat%',1,0)) says_abrogat,
  min(ID) min_id, max(ID) max_id
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_PARENTHETICALS
