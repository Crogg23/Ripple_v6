---
title: Revolving Door Appointees
---

```sql rows
select * from library.revolving_door_appointees
```

```sql n
select count(*) as row_count from library.revolving_door_appointees
```

406 federal appointees mapped to the industries they came from -- the government-to-industry revolving door.

Source: `THE_LIBRARY.GOVERNMENT.REVOLVING_DOOR_APPOINTEES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
