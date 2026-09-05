# THE_LIBRARY shelf survey — 2026-09-05

Queries through the Python door, `connect/db.py`. Scripts: `scratchpad/hunt23.py`,
`hunt24.py`.

**Headline: `THE_LIBRARY` holds zero finished investigative products. 253 of its
254 views are single-table renames with a plain-English comment. It is a naming
and documentation layer, not a product layer.**

**The finished products are in a different database. `LIBRARY_MARTS.FINDINGS`
holds 13 views, and one of them —
`EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION` — is the hunt we spent this session
building by hand.**

---

## Two corrections to the query as written

| In the draft | Actual |
|---|---|
| `WHERE TABLE_SCHEMA = 'THE_LIBRARY'` | `THE_LIBRARY` is a **database**, not a schema |
| `SPLIT_PART(TABLE_NAME,'_',1)` as bucket | the bucket is the **schema**, not a name prefix |

There is no `CORP_` / `HEALTH_` / `ENV_` prefix convention. Subject is carried by
the schema, and view names are bare nouns like `HOSPITALS` or `EARTHQUAKES`.

---

## 1. The 25 buckets

| Schema | Views | Schema | Views |
|---|---|---|---|
| HEALTH | 44 | GOVERNMENT | 31 |
| JUSTICE | 22 | CAMPAIGN_FINANCE | 19 |
| COMPANIES | 14 | ECONOMY | 13 |
| ENERGY_ENVIRONMENT | 12 | CRIME_SECURITY | 11 |
| GOVERNMENT_SPENDING | 11 | GEOGRAPHY | 11 |
| HISTORY | 8 | IMMIGRATION | 8 |
| INVESTIGATIONS | 7 | SCIENCE | 6 |
| MONEY | 6 | OPEN_DATA | 6 |
| TRANSPORT | 5 | HOUSING | 5 |
| ELECTIONS | 5 | SANCTIONS | 4 |
| PROCUREMENT | 2 | SPENDING | 1 |
| MISC | 1 | EDUCATION | 1 |
| PUBLIC | 1 | | |

**254 views. Every one carries a comment — 254 of 254.** That is unusual and
worth saying: the documentation layer is complete.

### Name prefixes, since it was asked

`FEDERAL` 11, `FEC` 10, `CONGRESS` 8, `MEMBER` 6, `FED` 5, `DOJ` 4, `PHARMA` 4,
`FOREIGN` 4, `MEDICARE` 4, `DRUG` 4, `SEC` 4, `NONPROFIT` 3, `GLOBAL` 3,
`SCOTUS` 3, `EPSTEIN` 3, `HOSPITAL` 3, `SUPREME` 3.

These are topic words, not a taxonomy. `SPENDING` and `GOVERNMENT_SPENDING` are
separate schemas, as are `MONEY` and `ECONOMY` — the shelf has drifted.

---

## 2. The complexity test — and it fails

Definition length was the obvious proxy for "finished product." It is the wrong
proxy. The longest views are the **widest**, not the most worked:

| Chars | View | What it is |
|---|---|---|
| 44,391 | `IMMIGRATION.BORDER_ENFORCEMENT_MONTHLY` | one DHS file, many columns |
| 33,446 | `ELECTIONS.ELECTION_ADMINISTRATION_SURVEY` | one EAVS file |
| 25,628 | `HEALTH.MEDICARE_FACILITIES` | one CMS POS file |
| 20,047 | `HISTORY.FED_SLAVEVOYAGES_TRANSATLANTIC` | one dataset |
| 19,672 | `JUSTICE.INCARCERATION_TRENDS_BY_COUNTY` | one Vera file |

A 44,000-character definition is a column list, not a join.

### So I tested the definitions directly

Parsed all 254 `VIEW_DEFINITION` bodies for source tables, `JOIN`, and
aggregation:

```
total views                      254
views referencing >1 table         1
views containing a JOIN            1
views with GROUP BY / RANK / OVER  0
```

**Zero aggregations. Zero rankings. One join in the entire shelf.**

The single multi-table view is `PUBLIC.START_HERE`, the card catalog, which joins
`CATALOG` to `FRIENDLY_LAYER`. It is documentation about the shelf, not a finding.

### What this means, plainly

`THE_LIBRARY` renames one landing table per view, picks readable column names, and
attaches a sentence explaining what the data is. That is real work and it makes
the warehouse navigable. **It is not analysis.** Nothing here flags, ranks,
scores or cross-references.

Anyone briefed to expect finished stories on this shelf will not find one.

---

## 3. Where the finished products actually are

`LIBRARY_MARTS` holds 426 views. Parsed the same way: **43 join, aggregate, or
touch more than one table.** The real work lives here.

### `LIBRARY_MARTS.FINDINGS` — 13 views, all labelled as leads

Every comment opens with the same phrase: **"FINDING CANDIDATE (lead, needs human
review)."** Someone built these with the right epistemics already attached.

| View | Rows | What it screens for |
|---|---|---|
| `OPIOID_PRESCRIBER_PAID_HIGH_RX` | **6,020** | high opioid rate + industry payments + overdose county |
| **`EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION`** | **287** | LEIE providers paid after their exclusion date |
| `EXCLUDED_PROVIDER_AT_FACILITY` | **39** | LEIE providers still listed at a facility |
| `EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION_IN_SHORTAGE` | — | the same, inside a shortage area |
| `FEDERAL_CONTRACTOR_EPA_VIOLATOR` | — | federal contractors with EPA violations |
| `MEMBER_MONEY_VS_OUTPUT` | — | Congress ranked by money against output |
| `PAC_FUNDS_BOTH_SIDES` | — | PACs funding opposing candidates |
| `REVOKED_BUT_DEDUCTIBLE` | — | IRS-revoked orgs still listed as deductible |
| `HOSPITAL_CLOSURE_RISK` | — | forward-looking closure risk |
| `REVOKED_BUT_DEDUCTIBLE_BY_STATE` | — | map layer |
| `HOSPITAL_CLOSURE_RISK_BY_STATE` | — | map layer |
| `OPIOID_PRESCRIBER_PAID_HIGH_RX_BY_STATE` | — | map layer |
| `CATALOG` | — | index of the other twelve |

`OPIOID_PRESCRIBER_PAID_HIGH_RX` carries 18 columns including
`RATE_PCTILE_IN_SPECIALTY`, `IN_HIGH_OVERDOSE_COUNTY_2015` and a `REVIEW_TIER`.
That is a scored, tiered screen — a finished investigative product.

### We rebuilt one of these by hand

`EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION` holds **287 rows** with columns
`NPI`, `LAST_NAME`, `FIRST_NAME`, `EXCLUSION_TYPE`, `EXCLUSION_YEAR`,
`POST_EXCLUSION_PAYMENTS`, `TOTAL_PAID_AFTER_EXCLUSION`, `FIRST_PAID_YEAR`,
`LAST_PAID_YEAR`, `DISTINCT_PAYERS`.

That is the query from `reports/pharma_paid_excluded_2026-09-05.md`, already
built, with the date test already in the name.

| | Our hand-built run | The existing view |
|---|---|---|
| Rows | 137 NPIs | **287** |
| Window | 2022 only | `FIRST_PAID_YEAR` to `LAST_PAID_YEAR`, multi-year |

**The gap is almost certainly the year window.** We tested one Open Payments
table; the view appears to span all of them. **Not verified** — the two have not
been reconciled row by row.

`EXCLUDED_PROVIDER_AT_FACILITY` at 39 rows is the Miranda-hospital query,
already built.

---

## The five most interesting things on the shelf

Since `THE_LIBRARY` has no finished products, these are the views most likely to
carry a story with one more query:

| View | Why |
|---|---|
| `HEALTH.PHARMA_PAYMENTS_TO_DOCTORS` | 15.4M payments, the table this session ran on |
| `HOUSING.MORTGAGE_APPLICATIONS` | HMDA with lender LEI and census tract |
| `IMMIGRATION.FOREIGN_WORKER_VISA_APPLICATIONS` | employer, job, wage, visa class, case-level |
| `GOVERNMENT_SPENDING.FEDERAL_CONTRACTS` | 6.3M transactions with UEI |
| `ECONOMY.RETIREMENT_PLAN_FILINGS` | Form 5500 with sponsor **and its EIN** |

The last one matters for the earlier bridge work — Form 5500 carries EIN, and
`FED_FAC_SINGLE_AUDIT` maps EIN to UEI at 95.9% one-to-one.

---

## What is supported

| Statement | Supported? |
|---|---|
| `THE_LIBRARY` has 254 views across 25 schemas | **yes** |
| All 254 carry a comment | **yes** |
| 253 of 254 are single-table, no join, no aggregation | **yes, parsed** |
| The only join is the card catalog | **yes** |
| `LIBRARY_MARTS.FINDINGS` holds 13 built screens | **yes** |
| The excluded-provider screen already existed | **yes, 287 rows** |
| Our 137 and its 287 describe the same population | **not verified** |

---

## Not checked

1. Reconciling our 137 against the view's 287. One query would settle it.
2. The 30 non-`FINDINGS` views in `LIBRARY_MARTS` that join or aggregate.
3. Whether `FINDINGS` views are tables or live views, and how stale they are.
4. `LIBRARY_MARTS.REVIEW.CASE_QUEUE`, which joins six tables and aggregates.
5. `TIMELINE.TIMELINE__WAREHOUSE`, which touches 34 tables.

## Cost

Two scripts plus two ad-hoc queries. All `INFORMATION_SCHEMA` metadata except
three `count(*)` calls on `FINDINGS` views. Cheap. No prior run of this pattern
in the query log to price against.
