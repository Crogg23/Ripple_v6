---
title: Election Administration Survey
---

```sql rows
select * from library.election_administration_survey
```

```sql n
select count(*) as row_count from library.election_administration_survey
```

The EAVS survey: how every US election jurisdiction actually runs voting -- registration, mail ballots, poll workers, provisionals.

Source: `THE_LIBRARY.ELECTIONS.ELECTION_ADMINISTRATION_SURVEY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
