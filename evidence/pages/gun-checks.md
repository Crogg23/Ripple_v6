---
title: Gun Background Checks
---

```sql monthly
select * from library.gun_checks
```

FBI **NICS firearm background checks**, all states summed by month. A check is not
a sale — but it's the best public proxy for firearm demand. Source:
`fed_fbi_nics_checks` (raw view; months and counts cast from text at extraction).

<LineChart
    data={monthly}
    x=month
    y=total_checks
    title="NICS background checks per month, national"
    yFmt="#,##0"
/>

<LineChart
    data={monthly}
    x=month
    y={["handgun_checks", "long_gun_checks"]}
    title="Handgun vs long-gun checks"
    yFmt="#,##0"
/>
