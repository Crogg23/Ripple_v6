---
title: Part D Prescribing By State And Type
---

```sql rows
select * from library.part_d_prescribing_by_state_and_type
```

```sql n
select count(*) as row_count from library.part_d_prescribing_by_state_and_type
```

CMS Medicare Part D prescribers rolled to prescriber STATE x prescriber TYPE (specialty).

Source: `THE_LIBRARY.HEALTH.PART_D_PRESCRIBING_BY_STATE_AND_TYPE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
