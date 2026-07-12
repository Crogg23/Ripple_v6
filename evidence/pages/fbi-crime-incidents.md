---
title: Fbi Crime Incidents
---

```sql rows
select * from library.fbi_crime_incidents
```

```sql n
select count(*) as row_count from library.fbi_crime_incidents
```

FBI Crime Data Explorer incident schema (1-row stub -- needs a real pour before it's usable).

Source: `THE_LIBRARY.CRIME_SECURITY.FBI_CRIME_INCIDENTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
