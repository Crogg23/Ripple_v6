# Five Plotly Studio briefs — 2026-09-03

Each brief is one CSV extract plus one prompt for the Plotly Studio agent.
Plotly Studio takes a flat file and a plain-English ask and builds the Dash app.
So the warehouse does the joining; Studio only charts.
Column names below are verbatim from gen 1's content recon pages.

Rules that apply to every brief:
- One CSV per app, under 200K rows, pre-aggregated where the raw table is >10M rows
- The vintage goes in the CSV filename and the app title, always
- Every dollar column has a sibling `row_is_event` flag or it does not ship
- Names are joined on normalized name only where an ID does not exist; say so in the app

---

## Brief 1 — Paid and pays back

**Question:** does a federal contractor also fund PACs, in the same fiscal year?

**Tables**

| table | rows | role |
|---|---|---|
| FED_USASPENDING_CONTRACTS_FULL_R2 | 93.2M | contracts, one row = one action |
| FED_FEC_INDIV_CONTRIBUTIONS | 84.2M | gifts, NAME + EMPLOYER + AMT |
| FED_FEC_COMMITTEE_TO_COMMITTEE | 28.6M | PAC to PAC, memo trap lives here |

**Extract**

```sql
-- pick one recipient by RECIPIENT_PARENT_NAME, e.g. 'LOCKHEED MARTIN CORPORATION'
with c as (
  select year(to_date(ACTION_DATE)) as fy,
         sum(FEDERAL_ACTION_OBLIGATION) as obligated,
         count(*) as actions
  from FED_USASPENDING_CONTRACTS_FULL_R2
  where RECIPIENT_PARENT_NAME = :org
  group by 1),
g as (
  select year(to_date(TRANSACTION_DT,'MMDDYYYY')) as fy,
         sum(TRANSACTION_AMT) as gifts,
         count(*) as gift_rows
  from FED_FEC_INDIV_CONTRIBUTIONS
  where upper(EMPLOYER) like :org_stem || '%'
    and (MEMO_CD is null or MEMO_CD <> 'X')
  group by 1)
select coalesce(c.fy,g.fy) fy, obligated, actions, gifts, gift_rows
from c full outer join g on c.fy = g.fy order by 1;
```

**CSV columns:** fy, obligated, actions, gifts, gift_rows

**Studio prompt**

> Two-axis line chart, fiscal year on x. Left axis contract dollars obligated, right axis employee political gifts. Add a bar under it for gift_rows. Title includes the org name and "vintage 2006-2026". Add a dropdown to switch org if the CSV has an `org` column.

**Chain**
- checked: same org stem in both tables, same year
- hit: both lines nonzero and move together
- miss: EMPLOYER is free text, stem match fails, or gifts are all memo rows

**Traps**
- TRANSACTION_DT is text MMDDYYYY, not a date
- MEMO_CD 'X' rows are earmark memos, double-count if summed
- EMPLOYER top values are RETIRED and NOT EMPLOYED, so stem match is the only door
- FED_FEC_COMMITTEES columns are C1..C15, unnamed, do not use it for names

---

## Brief 2 — One owner, four agencies

**Question:** stack every federal touch on one company on one timeline.

**Tables**

| table | rows | date column | who column |
|---|---|---|---|
| FED_DOL_OSHA_INSPECTIONS | 5.6M | OPEN_DATE | ESTAB_NAME |
| FED_EPA_ECHO | 3.2M | FAC_DATE_LAST_FORMAL_ACTION | FAC_NAME |
| FED_SAM_EXCLUSIONS_FULL_R2 | 168K | ACTIVE_DATE | NAME |
| FED_USASPENDING_CONTRACTS_FULL_R2 | 93.2M | ACTION_DATE | RECIPIENT_PARENT_NAME |
| FED_OSHA_ITA_300A_SUMMARY_2024 | 399K | YEAR_FILING_FOR | COMPANY_NAME |

**Extract**

```sql
-- :stem = 'WALMART' or 'TENNESSEE VALLEY AUTHORITY'
select 'osha_inspection' src, to_date(OPEN_DATE) d, ESTAB_NAME who, SITE_STATE st, 1 n, null amt
  from FED_DOL_OSHA_INSPECTIONS where upper(ESTAB_NAME) like :stem||'%'
union all
select 'epa_formal_action', to_date(FAC_DATE_LAST_FORMAL_ACTION), FAC_NAME, FAC_STATE, FAC_FORMAL_ACTION_COUNT, FAC_TOTAL_PENALTIES
  from FED_EPA_ECHO where upper(FAC_NAME) like :stem||'%'
union all
select 'sam_exclusion', to_date(ACTIVE_DATE), NAME, STATE_PROVINCE, 1, null
  from FED_SAM_EXCLUSIONS_FULL_R2 where upper(NAME) like :stem||'%'
union all
select 'contract', to_date(ACTION_DATE), RECIPIENT_PARENT_NAME, RECIPIENT_STATE_CODE, 1, FEDERAL_ACTION_OBLIGATION
  from FED_USASPENDING_CONTRACTS_FULL_R2 where upper(RECIPIENT_PARENT_NAME) like :stem||'%'
union all
select 'injury_summary', to_date(YEAR_FILING_FOR||'-01-01'), COMPANY_NAME, STATE, TOTAL_INJURIES, null
  from FED_OSHA_ITA_300A_SUMMARY_2024 where upper(COMPANY_NAME) like :stem||'%';
```

Aggregate to src x year x state before export if over 200K rows.

**CSV columns:** src, d, who, st, n, amt

**Studio prompt**

> Swimlane timeline: one lane per src, dots sized by n, colored by src. Below it, a stacked bar of n per year per src. A US choropleth of st counts as a third tab. Title includes stem and "names matched by prefix, not ID".

**Chain**
- checked: one name stem hits five agency tables
- hit: a violation cluster sits inside a contract run
- miss: stem hits nothing in one table, which still proves the join works

**Traps**
- ECHO date columns are "last" dates, one per facility, not events
- ECHO has 1900 and 1908 dates, filter d >= 1970
- OSHA ITA is one file per year, union 2023-2025 for three years

---

## Brief 3 — Where the money died

**Question:** how much COVID money was promised but never paid out, by program?

**Tables**

| table | rows | obligated col | outlayed col |
|---|---|---|---|
| FED_USASPENDING_ASSISTANCE_FULL | 19.9M | obligated_amount_from_COVID-19_supplementals_for_overall_award | outlayed_amount_from_COVID-19_supplementals_for_overall_award |
| FED_USASPENDING_SUBAWARDS_FULL | 4.7M | PRIME_AWARD_OBLIGATED_AMOUNT_FROM_COVID_19_SUPPLEMENTALS | PRIME_AWARD_OUTLAYED_AMOUNT_FROM_COVID_19_SUPPLEMENTALS |

**The trap first.** Both columns are "for overall award", repeated on every action row.
Summing across actions counts the same award once per row. Dedupe on award key first.

**Extract**

```sql
with one_per_award as (
  select assistance_award_unique_key k,
         max(awarding_agency_name) agency,
         max(cfda_title) program,
         max(action_date_fiscal_year) fy,
         max("obligated_amount_from_COVID-19_supplementals_for_overall_award") obligated,
         max("outlayed_amount_from_COVID-19_supplementals_for_overall_award") outlayed
  from FED_USASPENDING_ASSISTANCE_FULL
  where "obligated_amount_from_COVID-19_supplementals_for_overall_award" > 0
  group by 1)
select agency, program, fy,
       count(*) awards, sum(obligated) obligated, sum(outlayed) outlayed,
       sum(obligated) - sum(outlayed) unspent
from one_per_award group by 1,2,3;
```

**CSV columns:** agency, program, fy, awards, obligated, outlayed, unspent

**Studio prompt**

> Treemap of unspent by agency then program. Second view: dumbbell chart, obligated vs outlayed per program, sorted by gap. Third: fy slider. Title says "one row per award, deduped on award key".

**Chain**
- checked: obligated minus outlayed after one-row-per-award
- hit: a named program with billions unspent
- miss: outlayed equals obligated everywhere, or the column is null pre-2020

**Traps**
- assistance action_date years 2017-2023 sit at exactly 1,000,000 rows, a load cap, not the data
- the column name has a hyphen, quote it

---

## Brief 4 — Lobby before the law

**Question:** does employer lobby spend spike in the quarters before a vote?

**Tables**

| table | rows | what it holds |
|---|---|---|
| CA_LOBBY_EMPLOYER | 1,730 | employer spend by session, QTR_1..QTR_8 |
| CA_LOBBY_COVER | 569K | every filing, FILER, FIRM, RPT_DATE |
| CA_LOBBY_FIRM_EMPLOYER | 170 | firm to employer, PER_TOTAL |
| ST_OPENSTATES_LEGISLATORS | — | people, no bills |

**Honest gap:** there is no bill table in the warehouse today.
So the PoC is spend by quarter only. The vote date is typed in by hand.

**Extract**

```sql
select EMPLOYER_NAME, SESSION_ID, INTEREST_NAME, SESSION_YR_1, SESSION_YR_2,
       QTR_1, QTR_2, QTR_3, QTR_4, QTR_5, QTR_6, QTR_7, QTR_8, SESSION_TOTAL_AMT
from CA_LOBBY_EMPLOYER;
```

Unpivot QTR_1..QTR_8 to long form before export: employer, session, qtr_n, amt.

**CSV columns:** employer, session, interest, qtr_n, amt, session_total

**Studio prompt**

> Small multiples, one line per employer, quarter 1-8 on x, amt on y. Top 20 employers by session_total. A text input for "vote quarter" that draws a vertical line on every panel. Facet by interest.

**Chain**
- checked: spend by quarter, one employer, one session
- hit: a spike in the two quarters before the typed vote date
- miss: flat spend, or 1,730 rows is a 10K-cap sample of a bigger table

**Traps**
- 1,730 rows is suspiciously small for California, check if capped
- CA_LOBBY_COVER has RPT_DATE values in 1860 and 2035, filter 2000-2026

---

## Brief 5 — Dead but still cited

**Question:** which tables stopped in the past, and what does the last real date say?

**Tables**

| table | rows | date col | last real year |
|---|---|---|---|
| FED_DEA_ARCOS_FULL | 178.6M | TRANSACTION_DATE | 2012 |
| FED_FDA_FAERS_DEMO | 5.8M | FDA_DT | 2014 |
| FED_FDA_FAERS_DEMO | 5.8M | INIT_FDA_DT | 2014 |
| FED_DOL_OSHA_INSPECTIONS | 5.6M | OPEN_DATE | 2026 |

**Extract:** zero warehouse queries. Gen 1's json pages already hold rows per year per date column.

```python
# scripts/gen1_when_to_csv.py — reads reports/recon/content/json/*.json
# emits: table, date_col, year, rows
```

Filter to year between 1970 and 2027. Add `last_year` = max year with rows > 1% of table max.

**CSV columns:** table, date_col, year, rows, last_year, vintage_label

**Studio prompt**

> Heatmap: table on y, year on x, cell = rows, log color. Sort tables by last_year ascending so dead ones sit on top. Click a row to see all date columns for that table as lines. Title: "row counts per year, 2,208 tables, from recon 2026-09-03".

**Chain**
- checked: rows per year for every date column, every table
- hit: a table whose last real year is over five years back
- miss: table is current, one date column just lags the other

**Traps**
- FAERS MFR_DT has 2030-2033 rows, garbage, not future
- USAspending assistance has flat 1,000,000-row years, a cap not a fact
- eleven tables carry epoch micros in _INGESTED_AT, skip that column

---

## Build order

| # | brief | queries | why this order |
|---|---|---|---|
| 1 | 5 dead but cited | 0 | free, proves the Studio pipe |
| 2 | 2 one owner | 5 | cheapest real join |
| 3 | 3 money died | 1 | one dedupe query, big number |
| 4 | 1 paid and pays back | 2 | FEC date parsing is the risk |
| 5 | 4 lobby | 1 | no bill table, weakest story |

---

## Addendum 2026-09-03 — Studio dropped, Brief 5 built by hand

Studio was a bust. Brief 5 now ships as one self-contained HTML page, no Dash, no server.
- template: `viz/pages/dead_tables_tpl.html`
- builder: `python scripts/brief5_dead_tables_page.py 2026-09-03` → `outputs/dead_tables_2026-09-03.html`
- live copy: https://claude.ai/code/artifact/bf713bb7-db86-4db3-b586-7fe59f57f992

What it shows, from the CSV alone: 1,910 tables, 4,290 date columns, 327 tables with at least one dead date column, 29 dead on every column, 9 of those with 100K+ rows. The 327 is column grain, the 29 is table grain.
Same recipe works for briefs 1–4: warehouse does the join to a CSV, a page template does the charting.
