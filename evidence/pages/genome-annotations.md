---
title: Genome Annotations
---

```sql rows
select * from library.genome_annotations
```

```sql n
select count(*) as row_count from library.genome_annotations
```

Genome annotation records from Ensembl -- genes, variants, and features across species (643-row probe).

Source: `THE_LIBRARY.SCIENCE.GENOME_ANNOTATIONS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
