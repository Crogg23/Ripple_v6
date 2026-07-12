---
title: Healthcare Providers
---

```sql n
select 9606683 as row_count
```

Every US healthcare provider with an NPI -- all 9.6M. The backbone of the health data.

Source: `THE_LIBRARY.HEALTH.HEALTHCARE_PROVIDERS` (curated, 9,606,683 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />
