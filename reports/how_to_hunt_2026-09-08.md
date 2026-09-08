# How to hunt in it — the method, measured

2026-09-08. Everything here came back from a live query today, through
the Python door. The chat plug-in door is still dead at 401.

---

## Part 1 — the ocean is not an ocean

You have been told 2,214 tables and 1.37 billion rows. That number is
true and it is useless for hunting, because most of it cannot carry a
story. Here is what happens when you filter for what can.

```
FUNNEL                                          TABLES        ROWS
mart layer, base tables                            704   1.25B
  of those, 100,000 rows or more                   250
  of those, carrying a real date column            165
  of those, also carrying a hard key                46   569.6M

what falls out on the way
  under 10,000 rows                                295   42% of the layer
  big but no date column                            85   no clock, no story
  big and dated but no hard key                    119   cannot be chained
```

**46 tables.** That is the whole huntable warehouse. 569.6 million rows.

A table needs three things before it can carry a wow piece:

| Requirement | Why it is not optional |
|---|---|
| Size | a national claim needs national coverage |
| A real date | no clock means no before, no after, no cause |
| A hard key | no key means no name at the top of the list |

Miss any one and you have a chart, not a story.

Caveat on the 46: the hard-key test used a hand-written list of 18 id
columns. A table keyed on something not on that list was excluded. So
46 is a floor. It is not a ceiling.

Second caveat: FIPS_CODE and COUNTY_FIPS were counted as hard keys for
this pass. The key rules say FIPS is terminal, never a pivot. Some of
the 46 are county-only and cannot chain.

---

## Part 2 — where the deep water actually is

```
SCHEMA               TABLES        ROWS
FINANCE                   4   385,837,060
MARITIME                  1    58,104,610
HEALTH                    8    43,096,928
ENVIRONMENT              15    33,834,231
CORPORATE_REGISTRY        3    23,522,954
ECONOMICS                 4    16,459,844
LABOR                     8     6,447,055
POLITICS                  1     1,689,338
IMMIGRATION               1       422,464
PROCUREMENT               1       168,328
```

ENVIRONMENT has the most huntable tables. FINANCE has the most rows,
and 92% of those rows sit in one file.

### The 25 biggest, in order

| Table | Rows |
|---|---:|
| FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 |
| FINANCE__FED_FEC_INDIV_CONTRIBUTIONS__PREV_20260906 | 84,172,112 |
| MARITIME__FED_NOAA_AIS | 58,104,610 |
| HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUEN… | 31,403,215 |
| CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | 15,804,611 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEM… | 15,432,737 |
| FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS | 9,701,952 |
| HEALTH__FED_CMS_NPPES | 9,606,683 |
| FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES | 8,191,177 |
| ECONOMICS__FED_USASPENDING_CONTRACTS | 6,325,622 |
| CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE | 5,734,780 |
| ECONOMICS__FED_IRS_990_EFILE_INDEX | 5,544,626 |
| ENVIRONMENT__FED_EPA_FRS_FACILITIES | 5,300,149 |
| ECONOMICS__INTL_GLEIF | 3,382,301 |
| ENVIRONMENT__FED_EPA_ECHO | 3,135,554 |
| LABOR__FED_MSHA_VIOLATIONS | 3,087,265 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS | 2,495,249 |
| CORPORATE_REGISTRY__FED_IRS_EO_BMF | 1,983,563 |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS | 1,900,067 |
| POLITICS__FED_FCC_LICENSING | 1,689,338 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES | 1,554,832 |
| ECONOMICS__FED_IRS_AUTO_REVOCATIONS | 1,207,295 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES | 927,415 |
| LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 | 890,934 |
| LABOR__FED_OSHA_ITA_CASE_DETAIL_2024 | 688,649 |

**One duplicate to kill.** `__PREV_20260906` is the old 84.2M snapshot
sitting beside the live 283.8M table. Anything counting FEC has to
name which one it hit, or the number is meaningless.

---

## Part 3 — the five moves that actually found things today

This is not theory. Thirty probes ran this session. Every result worth
keeping came from one of these five shapes, and each is **one query
against one table.** No joins. No chains. No design work.

### Move 1 · The zero hunt
Ask which rows hold a zero or a null where a zero is impossible.

```
Ran on:   ENVIRONMENT__FED_EPA_ECHO, TOTAL_INSPECTION_COUNT
Found:    2,929,890 of 3,135,554 facilities sit at zero
Then:     3,321 of those are active AND classed major
```
- Hit means: the thing exists on paper and nothing ever happened to it
- Miss means: the zero is a loader placeholder, not a real count
- The proof it is real: that column has no nulls at all, while 60,438
  rows in the same table carry a null latitude. The loader can tell
  the difference. So zero is a value.

### Move 2 · The ratio hunt
Take two columns in one table that must agree, and divide them.

```
Ran on:   OSHA ITA, TOTAL_HOURS_WORKED over ANNUAL_AVERAGE_EMPLOYEES
Found:    3,667 establishments report over 4,000 hours per employee
Meaning:  76 hours a week, every week, all year, for every worker
Plus:     196 more report zero employees and non-zero hours
```
- Hit means: one form, one filer, two numbers that cannot both be true
- Miss means: the ratio is explained by contractors or seasonal staff
- No join needed. The contradiction is inside a single row.

### Move 3 · The spread hunt
Group by the administrator instead of the subject.

```
Ran on:   MSHA violations, amount paid over penalty proposed, by state
Found:    KY collects 61.1%. WI collects 85.7%.
Scope:    states with 20,000+ violations only
```
- Hit means: where you are decides what the law actually costs
- Miss means: the spread tracks operator size or bankruptcy, not place
- The tell that it is real: the coal states sit at the bottom together.
  That is a pattern. Scatter would not sort itself by industry.

### Move 4 · The tail hunt
Sort descending. Look at row one. Only row one.

```
Ran on:   UK PSC, companies per postcode plus address line
Row one:  WC2H 9JQ, SHELTON STREET, 141,512 companies
Shape:    16,666 addresses hold 50+ companies each, 3.4M in total
```
- Hit means: one entity is so far out it needs its own explanation
- Miss means: row one is a known aggregator and the answer is boring
- Shelton Street is a known formation agent, so row one alone is not
  the story. The **shape** is: a fifth of the register lives at
  mailboxes. That took one more query.

### Move 5 · The clock hunt
Min and max on the date column, before designing anything.

```
Ran on:   MARITIME__FED_NOAA_AIS
Found:    2024-01-01 to 2024-01-08. Eight days.
Cost of not running it first: a week of design on a dead idea
```
- Hit means: the span supports the question you were about to ask
- Miss means: kill the idea now, before you build anything on it
- This is the cheapest query in the warehouse and it should run first,
  every single time, on every table you are about to touch.

---

## Part 4 — proof the method beats the catalog

The fifteen ideas in the earlier report were written idea-first, from
the tool box. The deep-water query above took twelve seconds and
surfaced four large, dated, keyed sources that **none of the fifteen
ideas mentioned at all**.

| Source | Rows | What it holds |
|---|---:|---|
| SDWA violations and enforcement | 15,432,737 | drinking water, every violation |
| SDWA lead and copper samples | 927,415 | actual lead readings, by system |
| IRS 527 contributions | 9,701,952 | political money outside FEC |
| IRS auto revocations | 1,207,295 | nonprofits stripped of status |

The lead-sample table is the one to stare at. 927,415 individual lead
and copper readings, keyed to a water system, with a date. Nobody has
looked at it. It was not on any list.

That is the argument. A catalog of 934 questions is a way of never
starting. The data raising its own hand is faster and more honest.

---

## Part 5 — what makes a piece wow, mechanically

Three ingredients. A piece missing any one of them lands soft.

| Ingredient | What it looks like | Why it matters |
|---|---|---|
| Scale | a number covering the whole country | nobody can call it an anecdote |
| A name | one facility, person or firm at the top | abstraction does not travel |
| A stake | someone harmed, or money gone | a pattern with no victim is trivia |

Test the never-inspected finding against it:

- **Scale** — 3,135,554 facilities, every state
- **Name** — 3,321 active majors, each with an FRS_ID and an address
- **Stake** — out of compliance, never visited, nobody checking

All three. That is why it is the strongest thing found today.

Now test the cosponsorship-network idea, ranked 45 on the wall:

- Scale — 367,735 cosponsorships, fine
- Name — yes, members of Congress
- **Stake — nobody is harmed by the answer**

Two out of three. That is why it will never wow, no matter how clean
the data is.

---

## Part 6 — the sweep worth building

Run the five moves against all 46 deep-water tables. Let the data
raise its hand instead of picking from a list.

```
SCOPE       46 tables
QUERIES     clock, zero, tail, ratio, spread   ~5 per table
TOTAL       roughly 230 queries
SHAPE       every one is a single-table aggregate, no joins
OUTPUT      one ranked sheet of anomalies, biggest first
```

What comes out is not fifteen ideas. It is a list of places where the
data is already strange, sorted by how strange, with the table and
column named. You pick from findings, not from guesses.

The ratio move is the only one needing per-table thought, since it
must know which two columns should agree. The other four are generic
and can run unattended.

---

## Standing rules this method inherits

- Run the clock first. Always. It is free and it kills bad ideas early.
- A zero is only absence once the loader is proven to write nulls too.
- Row one of a tail is a lead. The shape of the tail is the finding.
- Group by the regulator, not only the regulated.
- No join until a single-table move has already found something.
