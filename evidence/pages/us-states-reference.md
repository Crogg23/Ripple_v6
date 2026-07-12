---
title: Us States Reference
---

```sql rows
select * from library.us_states_reference
```

```sql n
select count(*) as row_count from library.us_states_reference
```

The master list of US states and territories: FIPS code, postal abbreviation, and full name.

Source: `THE_LIBRARY.GEOGRAPHY.US_STATES_REFERENCE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
