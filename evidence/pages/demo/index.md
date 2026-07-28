---
title: "Ripple: The Platform"
---

```sql domain_counts
select
    TABLE_SCHEMA as domain,
    count(*) as tables,
    sum(ROW_COUNT) as total_rows
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where TABLE_SCHEMA not in ('INFORMATION_SCHEMA', '_RESTORE_20260701', 'DBT_CROGERS')
  and ROW_COUNT > 0
group by TABLE_SCHEMA
order by total_rows desc
```

```sql kpis
select
    sum(total_rows) as total_rows,
    sum(tables) as total_tables,
    count(*) as domains
from ${domain_counts}
```

```sql findings
select FINDING, WHAT, WHO_GETS_HURT, ROWS_ as leads
from LIBRARY_MARTS.FINDINGS.CATALOG
order by ROWS_ desc
```

# One lens. Every domain. No targets.

Ripple maps systemic patterns across public data. No favorites. A census, not a subpoena.

<BigValue data={kpis} value=total_rows title="Rows Under Management" fmt="#,##0" />
<BigValue data={kpis} value=total_tables title="Tables" />
<BigValue data={kpis} value=domains title="Domains" />

## Data by domain

<BarChart
    data={domain_counts}
    x=domain
    y=total_rows
    swapXY=true
    fmt="#,##0"
    title="Rows per domain"
/>

## Shipped findings

Each row is a pattern where the data shows someone gets hurt. Human-reviewed, never auto-published.

<DataTable data={findings} rows=10>
    <Column id=FINDING />
    <Column id=WHAT title="Pattern" />
    <Column id=WHO_GETS_HURT title="Who gets hurt" />
    <Column id=leads fmt="#,##0" />
</DataTable>

---

**Explore deeper:**
- [Opioid Prescribers × Industry Money (Map)](/demo/opioid-map)
- [Hospital Closure Risk (Map)](/demo/hospital-risk)
- [84M Political Donations Over Time](/demo/fec-money)
- [PAC Access-Buying: Both Sides](/demo/pac-both-sides)
- [Federal Contractors × EPA Violators](/demo/contractor-polluter)
