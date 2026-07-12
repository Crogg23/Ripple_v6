---
title: Fossil Fuel Energy Share
---

```sql rows
select * from library.fossil_fuel_energy_share
```

```sql n
select count(*) as row_count from library.fossil_fuel_energy_share
```

Share of each country's primary energy that comes from fossil fuels, by year.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.FOSSIL_FUEL_ENERGY_SHARE` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
