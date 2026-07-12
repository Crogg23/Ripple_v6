---
title: Intra American Slave Voyages
---

```sql rows
select * from library.intra_american_slave_voyages
```

```sql n
select count(*) as row_count from library.intra_american_slave_voyages
```

SlaveVoyages Intra-American database -- one row per documented voyage (ship, captain, owners, ports, dates, counts).

Source: `THE_LIBRARY.HISTORY.INTRA_AMERICAN_SLAVE_VOYAGES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
