---
title: Sec Edgar Filings Api
---

```sql rows
select * from library.sec_edgar_filings_api
```

```sql n
select count(*) as row_count from library.sec_edgar_filings_api
```

```sql trend
select date_trunc('month', "REPORTDATE") as period, count(*) as records
from library.sec_edgar_filings_api
where "REPORTDATE" is not null
group by 1
order by 1
```

Structured SEC filing metadata from the data.sec.gov API -- CIK, EIN, form type, dates (200-row probe).

Source: `THE_LIBRARY.COMPANIES.SEC_EDGAR_FILINGS_API` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Sec Edgar Filings Api over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
