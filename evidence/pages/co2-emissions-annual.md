---
title: Co2 Emissions Annual
---

```sql rows
select * from library.co2_emissions_annual
```

```sql n
select count(*) as row_count from library.co2_emissions_annual
```

Total annual CO2 emissions for every country, going back over two centuries.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.CO2_EMISSIONS_ANNUAL` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
