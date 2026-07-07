---
title: Fatal Police Shootings
---

```sql by_year
select * from library.fatal_force
```

The Washington Post's **Fatal Force** database — every fatal shooting by an
on-duty police officer in the United States since 2015. Source:
`xc_wapo_fatal_force` (raw view; dates cast at extraction).

<BarChart
    data={by_year}
    x=year
    y=deaths
    series=armed_with
    title="Fatal police shootings per year, by armed status"
    type=stacked
/>
