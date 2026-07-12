---
title: Veteran Mortality Appendix
---

```sql rows
select * from library.veteran_mortality_appendix
```

```sql n
select count(*) as row_count from library.veteran_mortality_appendix
```

VA all-cause death figures for veterans, 2018-2023, as extracted from a report appendix.

Source: `THE_LIBRARY.HEALTH.VETERAN_MORTALITY_APPENDIX` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
