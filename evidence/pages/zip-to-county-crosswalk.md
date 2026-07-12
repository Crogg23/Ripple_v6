---
title: Zip To County Crosswalk
---

```sql rows
select * from library.zip_to_county_crosswalk
```

```sql n
select count(*) as row_count from library.zip_to_county_crosswalk
```

A bridge from ZIP code areas to counties -- so ZIP-level data can roll up to the right county.

Source: `THE_LIBRARY.GEOGRAPHY.ZIP_TO_COUNTY_CROSSWALK` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
