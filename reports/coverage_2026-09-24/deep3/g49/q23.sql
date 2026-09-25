-- Parentheticals: how much of the table sits in the new opinion-ID range (>= 9M) where the cluster join names the wrong case;
-- and, in the old range, the opinions most often described with "overruled", named via OPINION_CLUSTERS
with p as (select try_to_number(DESCRIBED_OPINION_ID::string) did, TEXT from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_PARENTHETICALS),
band as (select 'band' section, iff(did >= 9000000, 'described id >= 9M', 'described id < 9M') k, count(*) n, count(distinct did) n2,
           null::string case_name, null::string date_filed, null::string sample_text from p group by 2),
ov as (select did, count(*) n, any_value(left(TEXT,140)) sample_text from p where TEXT ilike '%overrul%' and did < 9000000 group by 1 order by n desc limit 15)
select * from band
union all
select 'overruled_top', ov.did::string, ov.n, null, c.CASE_NAME, c.DATE_FILED::string, ov.sample_text
from ov left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS c on try_to_number(c.ID::string) = ov.did
order by 1, 3 desc
