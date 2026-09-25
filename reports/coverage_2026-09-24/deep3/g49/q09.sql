-- Oral arguments: court x year, via DOCKET_ID -> DOCKETS.COURT_ID. Count, median length, transcript fill
with oa as (select DOCKET_ID::string did, DURATION, try_to_date(DATE_CREATED::string) dc, STT_STATUS,
              iff(STT_TRANSCRIPT is not null and length(STT_TRANSCRIPT) > 50, 1, 0) has_tx
            from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da
      from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select coalesce(d.COURT_ID,'(no docket)') court, year(coalesce(d.da, oa.dc)) yr, count(*) n,
  median(oa.DURATION) med_sec, sum(oa.has_tx) n_tx, sum(iff(d.da is null,1,0)) no_argued_date
from oa left join d on d.id = oa.did
group by 1,2 order by 1,2
