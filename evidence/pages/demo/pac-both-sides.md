---
title: "PAC Access-Buying: Both Sides"
---

```sql pacs
select
    CMTE_NAME as pac_name,
    CONNECTED_ORG as org,
    MEMBERS_FUNDED as members,
    DEM_MEMBERS as dems,
    REP_MEMBERS as reps,
    TOTAL_USD as total_usd,
    TOTAL_TO_DEMS as dem_usd,
    TOTAL_TO_REPS as rep_usd,
    BIPARTISAN_BALANCE as balance
from LIBRARY_MARTS.FINDINGS.PAC_FUNDS_BOTH_SIDES
where BOTH_SIDES_FLAG = true
order by TOTAL_USD desc
```

```sql totals
select
    count(*) as total_pacs,
    sum(total_usd) as total_money,
    avg(balance) as avg_balance
from ${pacs}
```

```sql top_20
select * from ${pacs} limit 20
```

```sql balance_dist
select
    case
        when balance >= 0.45 then '0.45-0.50 (near-equal)'
        when balance >= 0.40 then '0.40-0.45'
        when balance >= 0.35 then '0.35-0.40'
        when balance >= 0.30 then '0.30-0.35'
        else '< 0.30'
    end as balance_band,
    count(*) as pacs
from ${pacs}
group by balance_band
order by balance_band desc
```

# Who buys access on both sides?

2,680 PACs fund 10+ members of Congress across both parties. This isn't ideology — it's access-buying. The closer to 50/50, the clearer the signal: they don't care who wins, they want a seat at the table regardless.

<BigValue data={totals} value=total_pacs title="Both-sides PACs" fmt="#,##0" />
<BigValue data={totals} value=total_money title="Total $ distributed" fmt="$#,##0" />
<BigValue data={totals} value=avg_balance title="Avg bipartisan balance" fmt="0.00" />

## $ to Democrats vs $ to Republicans

Each dot is a PAC. The diagonal = perfect 50/50 split.

<ScatterPlot
    data={top_20}
    x=dem_usd
    y=rep_usd
    title="Top 20 PACs: Dem $ vs Rep $"
    xAxisTitle="$ to Democrats"
    yAxisTitle="$ to Republicans"
    xFmt="$#,##0"
    yFmt="$#,##0"
    tooltipTitle=pac_name
/>

## Bipartisan balance distribution

Balance = min(dem_share, rep_share). 0.50 = perfectly split. Higher = more clearly buying access regardless of party.

<BarChart
    data={balance_dist}
    x=balance_band
    y=pacs
    title="How balanced are both-sides PACs?"
    fmt="#,##0"
/>

## Top 20 access-buyers

<DataTable data={top_20} rows=20>
    <Column id=pac_name title="PAC" />
    <Column id=org title="Connected org" />
    <Column id=members fmt="#,##0" title="Members funded" />
    <Column id=dems fmt="#,##0" />
    <Column id=reps fmt="#,##0" />
    <Column id=total_usd fmt="$#,##0" title="Total $" />
    <Column id=balance fmt="0.00" title="Balance" />
</DataTable>
