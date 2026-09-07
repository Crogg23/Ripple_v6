# Dead ends, build B: Provider Relief Fund landed, matched to nursing homes (2026-09-07)

Docket E75: "Did the worst chains get big pandemic bailout money?"
Scope report said: TAGGS is 45 rows of a website menu; land HRSA's flat PRF file instead, match by name + city + state to NURSINGHOME411, roll up by CHAIN_ID. This is that build.

## The short answer

| thing | number |
|---|---|
| PRF rows landed | 419,846 |
| PRF dollars | $135,063,804,375 |
| nursing homes in NH411 | 14,713 |
| homes with a usable name match | 2,122 (14.4%) |
| dollars on those homes | $2,095,676,877 |
| of which homes in a chain | 982 homes, $939,216,726 |
| chains with at least one hit | 255 of 617 |
| matches thrown out as hospital money | 121 homes, $1,210,818,823 |
| matches thrown out as one-word names | 114 homes, $123,784,360 |

**Bad news, up front.** Chain homes match at 9.7%; independents match at 25%. Chains cash the cheque under the operator or parent name, not the sign on the building, and the file has no EIN or CCN to bridge on. So the chain rollup is a floor with a big, uneven hole under it. Zero in the mart is "no name hit", never "no money".

## What was found on hrsa.gov

hrsa.gov/provider-relief/payments-and-data is the documentation page. It answers 403 to a plain fetch (WebFetch, 2026-09-07) and points at the CDC open-data portal. The actual file:

- dataset `kh8y-3es6`, "HHS Provider Relief Fund", data.cdc.gov
- CSV export: `https://data.cdc.gov/api/views/kh8y-3es6/rows.csv?accessType=DOWNLOAD`
- 20.6 MB, last modified 2025-03-28, four columns: Provider Name, State, City, Payment
- Payment is a `"$113,026"` string. 0 rows fail to parse. 59 state codes (territories included). 7 exact duplicate lines, kept.
- The payee's full-name only. No EIN, NPI, CCN, program phase or date.

## Landing

`scripts/hrsa_prf_load.py`. Dry-run default, `--run` to land. CREATE TABLE IF NOT EXISTS then append; refuses to append onto existing rows without `--append`. No overwrite, no drop.

```
python scripts/hrsa_prf_load.py            # dry run: downloaded, profiled, landed nothing
python scripts/hrsa_prf_load.py --run
  landed 419,846 rows into "LIBRARY_RAW"."LANDING".FED_HRSA_PROVIDER_RELIEF_FUND  run b7f0379a-bafd-41cc-a447-dd611e1a0580
  [DQ OK] fed_hrsa_provider_relief_fund/FED_HRSA_PROVIDER_RELIEF_FUND: 419,846 rows, density 0.4286
```

Table: `LIBRARY_RAW.LANDING.FED_HRSA_PROVIDER_RELIEF_FUND`. Columns PROVIDER_NAME, STATE, CITY, PAYMENT, all VARCHAR, plus `_INGESTED_AT`, `_SOURCE_RUN_ID`, `_SRC_SHA256`. Audit columns carry the underscore, same as senate_lda_load.py. Logged to INGEST_RUNS as source `fed_hrsa_provider_relief_fund`.

## dbt

| model | where | grain | rows |
|---|---|---|---|
| `stg_fed_hrsa_provider_relief_fund__payments` | LIBRARY_STAGING view | one file line, newest run | 419,846 |
| `health__fed_hrsa_provider_relief_fund` | LIBRARY_MARTS.HEALTH table | one file line | 419,846 |
| `int_nursing_home_prf_match` | LIBRARY_STAGING view | one home, one payee, one home per payee | 2,357 |
| `health__nursing_home_relief_by_chain` | LIBRARY_MARTS.HEALTH table | one chain | 617 |

Shared name normalizer: `macros/prf_name_key.sql`. Both sides of the join go through it. Source declared in `models/marts/health/_health__sources.yml`.

```
dbt run  --select stg_fed_hrsa_provider_relief_fund__payments health__fed_hrsa_provider_relief_fund int_nursing_home_prf_match health__nursing_home_relief_by_chain
dbt test --select (same four)      19 tests, 19 pass
```

## The match, and how honest it is

City + state must agree exactly. Names go upper, punctuation to space, trailing legal suffix off (LLC, INC, CORP, CO, LP, LTD, PC, LLP, OPCO, OPERATING, HOLDINGS, THE). Then, in order of trust:

| match_method | usable homes | usable dollars | what it is |
|---|---|---|---|
| exact | 1,649 | $1,557,866,771 | keys identical |
| home_starts_with_prf | 217 | $300,434,404 | payee is a shorter name the home name begins with |
| prf_contains_home | 142 | $138,631,124 | home name sits whole inside the payee name |
| prf_starts_with_home | 114 | $98,744,578 | payee begins with the home name |

Nothing fuzzier. No Levenshtein, no first-12-characters rule.

Fan-out cut twice: a home keeps its best method then biggest payment (32 homes had more than one candidate); a payee still claimed by two homes keeps one (7 payees). No dollar sits under two CCNs.

**Three classes of hit are flagged and kept out of the chain dollars:**

1. **One-word names, 114 homes, $123.8M.** The traps file says single-word matches are 8% real. Eyeballed all 114: this set is better than 8%, because most are `<TOWN> OPERATIONS LLC` in that town ("DUNKIRK OPERATING, LLC" for Dunkirk Rehabilitation, "CASPER OPCO LLC" for Casper Mountain). But it also holds "RIVERVIEW" the home vs "RIVERVIEW ENT CENTER" the ear doctor, and "PANORAMA" in Lacey WA. Kept out. The town-opco pattern is a candidate rule for a later, verified pass.
2. **Home is inside a hospital, NH411 `PROVIDER_RESIDES_IN_HOSPITAL = 'Y'`, 98 homes, $984.7M.** The name match is right and the money is wrong: "JAMAICA HOSPITAL MEDICAL CENTER T C U" lands on "JAMAICA HOSPITAL MEDICAL CENTER", $119.8M, which is the hospital's relief, not the unit's.
3. **Payee name says HOSPITAL / MEDICAL CENTER / HEALTH SYSTEM / HEALTH NETWORK, 23 more homes, $226.1M.** The NH411 flag under-catches: "THE METHODIST HOSPITAL SNF" in Houston is 'N' and took $133.2M under the hospital's name.

Class 2 and 3 together: 121 homes, $1.21B. That is 37% of all matched dollars, sitting on 5% of matched homes. Without the guard, ADVENTIST HEALTH ($82.4M, two hospital units) and COMMONSPIRIT were the top two chains.

**Still leaking after the guards:** "ORLANDO HEALTH, INC." $69.5M on Orlando Health and Rehabilitation Center. A hospital system whose name lacks the words the regex looks for. It has no chain id, so the chain mart is clean of it, but the usable total carries it. Any single home over about $10M deserves a look before it is quoted.

Spread on usable matches: median $808,900 per home, mean $987,595.

## Top 10 chains by matched relief

Multi-word, free-standing homes only. Floor, not total.

| chain | homes | matched | share | matched $ | per home | avg rating | fines/bed | SFF |
|---|---|---|---|---|---|---|---|---|
| NATIONAL HEALTHCARE CORPORATION | 64 | 44 | 69% | $66,042,214 | $1,500,959 | 3.8 | $155 | 0 |
| SABER HEALTHCARE GROUP | 126 | 33 | 26% | $28,855,712 | $874,416 | 3.0 | $230 | 3 |
| NHS MANAGEMENT | 43 | 30 | 70% | $26,098,354 | $869,945 | 2.6 | $93 | 0 |
| ERICKSON SENIOR LIVING | 17 | 9 | 53% | $22,731,364 | $2,525,707 | 4.4 | $386 | 0 |
| DIVERSICARE HEALTHCARE | 47 | 27 | 57% | $21,281,335 | $788,198 | 2.6 | $263 | 3 |
| CIENA HEALTHCARE/LAUREL HEALTH CARE | 84 | 20 | 24% | $19,410,979 | $970,549 | 2.8 | $348 | 2 |
| CLINICAL SERVICES, INC. | 48 | 18 | 38% | $16,701,144 | $927,841 | 3.7 | $101 | 1 |
| INFINITY HEALTHCARE CONSULTING | 74 | 13 | 18% | $14,293,377 | $1,099,491 | 2.2 | $445 | 3 |
| HAVEN HEALTH | 20 | 17 | 85% | $13,962,744 | $821,338 | 2.8 | $71 | 0 |
| ARCHCARE | 7 | 3 | 43% | $13,074,436 | $4,358,145 | 3.7 | $0 | 0 |

NHC at the top is a name effect as much as a money effect: it brands every home "NHC HEALTHCARE, <TOWN>" and pays under that name, so 69% of its homes hit. Ensign, Genesis, Life Care Centers and the other giants are near zero here because they pay under opcos.

## The question, answered as far as the data allows

"Worst chains" that did take visible money, chains with 5+ matched homes, sorted by chain average rating:

| chain | homes | matched | matched $ | 1-star homes | SFF | abuse icon | avg rating | fines/bed |
|---|---|---|---|---|---|---|---|---|
| RELIANT CARE MANAGEMENT | 28 | 12 | $8,588,105 | 24 | 4 | 14 | 1.2 | $1,085 |
| ICARE CONSULTING SERVICES | 7 | 6 | $7,424,786 | 5 | 0 | 6 | 1.3 | $2,034 |
| CHAMPION CARE | 20 | 5 | $9,764,893 | 9 | 4 | 4 | 1.7 | $732 |
| JUCKETTE FAMILY HOMES | 6 | 5 | $3,021,973 | 4 | 0 | 2 | 1.7 | $683 |
| SOL HEALTHCARE | 5 | 5 | $4,625,609 | 2 | 0 | 2 | 1.8 | $187 |
| DAVID MARX | 10 | 10 | $7,473,099 | 5 | 0 | 0 | 2.0 | $237 |

Reliant Care: 24 of 28 homes one-star, 14 with the abuse icon, and $8.6M of relief visible on 12 of them. That is the shape of the story E75 asked for, at a floor. The fines are 2023-06 onward and the ratings are a 2025-12 snapshot; the money is 2020-2022. Nothing here says the home was bad when it was paid.

## Traps found today

- The PRF payee for a hospital-based SNF unit is the hospital. NH411's `PROVIDER_RESIDES_IN_HOSPITAL` catches 98 of them and misses at least 23 more whose payee name says HOSPITAL or MEDICAL CENTER. Both guards are in the mart; a system named like "ORLANDO HEALTH, INC." still gets through.
- Chain homes name-match at 9.7%, independents at 25%. The gap is the opco naming pattern, not bad data. Any chain-vs-chain comparison off this mart compares name hygiene as much as money.
- One-word name hits are not all 8% real: `<TOWN> OPERATING LLC` in the same town is a real pattern. Still excluded, still needs a verified rule.

## Files

- `scripts/hrsa_prf_load.py`
- `library-onboarding/ripple_dbt/macros/prf_name_key.sql`
- `library-onboarding/ripple_dbt/models/staging/fed_hrsa_provider_relief_fund/` (model + schema.yml)
- `library-onboarding/ripple_dbt/models/intermediate/nursing_home_relief/int_nursing_home_prf_match.sql`
- `library-onboarding/ripple_dbt/models/marts/health/health__fed_hrsa_provider_relief_fund.sql`
- `library-onboarding/ripple_dbt/models/marts/health/health__nursing_home_relief_by_chain.sql`
- `library-onboarding/ripple_dbt/models/marts/health/schema_nursing_home_relief.yml`
- `library-onboarding/ripple_dbt/models/marts/health/_health__sources.yml` (source row added)

Not done: `economics__fed_hhs_taggs` is still listed disabled at dbt_project.yml line 165; left alone. No timeline view for the new marts. Nothing committed.

## Skeptic pass, 2026-09-07

Verdict AGREE: every number reproduced live, 10 of 10 sampled matches are the same entity. Four notes, applied:

| note | fix |
|---|---|
| $135.06B is not the whole program; CDC metadata says $178B, the file has no phase column, so what is missing is unknown | said here; the mart header will carry it |
| loader docstring named ARP Rural, a separate appropriation | docstring corrected |
| int header said 1,733 / 1,717 / $3.31B; table holds 2,357 / 2,243 / $3.43B; chain mart said 14.3%, is 14.4% | comments refreshed |
| the $10M eyeball caveat sits above the leak: WHITE OAK MANOR $8.3M on one home inside the chain mart, NHC Franklin $18.0M is 27% of NHC's total; `home_starts_with_prf` attributes a shorter, more corporate payee to one building by construction | caveat lowered to $5M here; flag `payee_shorter_than_home` left as the next fix |

Blind spot to keep loud: city+state must match exactly, so chain payments made under an HQ town are invisible. The miss is correlated with being a chain, the very thing E75 asks about.
