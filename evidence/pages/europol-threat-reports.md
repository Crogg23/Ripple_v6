---
title: Europol Threat Reports
---

```sql rows
select * from library.europol_threat_reports
```

```sql n
select count(*) as row_count from library.europol_threat_reports
```

Europol's SOCTA and IOCTA organized-crime and cybercrime threat assessments -- one row per published report.

Source: `THE_LIBRARY.CRIME_SECURITY.EUROPOL_THREAT_REPORTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
