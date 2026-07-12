---
title: Ransomware Victims
---

```sql rows
select * from library.ransomware_victims
```

```sql n
select count(*) as row_count from library.ransomware_victims
```

Organizations worldwide hit by ransomware gangs -- victim name, gang, sector, country, date.

Source: `THE_LIBRARY.CRIME_SECURITY.RANSOMWARE_VICTIMS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
