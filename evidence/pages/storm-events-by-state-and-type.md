---
title: Storm Events By State And Type
---

```sql rows
select * from library.storm_events_by_state_and_type
```

```sql n
select count(*) as row_count from library.storm_events_by_state_and_type
```

NOAA Storm Events rolled to STATE x EVENT_YEAR x EVENT_TYPE.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.STORM_EVENTS_BY_STATE_AND_TYPE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
