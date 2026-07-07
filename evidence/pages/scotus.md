---
title: The Supreme Court
---

```sql by_term
select * from library.scotus_by_term
```

Every Supreme Court case since 1946, from the **Supreme Court Database (SCDB)**.
Source: `fed_scdb`, a typed curated mart. The shrinking docket is one of the
clearest long-run trends in American government.

<BarChart
    data={by_term}
    x=term
    y=cases
    series=chief_justice
    title="Cases decided per term, colored by Chief Justice"
    echartsOptions={{animation: false}}
/>
