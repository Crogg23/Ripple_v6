---
title: Provider Facility Links
---

```sql n
select 2260193 as row_count
```

Which doctors work at which facilities -- the NPI-to-CCN crosswalk, 2.2M links.

Source: `THE_LIBRARY.HEALTH.PROVIDER_FACILITY_LINKS` (raw, 2,260,193 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />
