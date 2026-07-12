---
title: Environmental Defender Attacks
---

```sql rows
select * from library.environmental_defender_attacks
```

```sql n
select count(*) as row_count from library.environmental_defender_attacks
```

Global Witness records of killings and attacks on land and environmental defenders worldwide, since 2012.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.ENVIRONMENTAL_DEFENDER_ATTACKS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
