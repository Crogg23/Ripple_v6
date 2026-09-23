# Catalog audit — 2026-09-23

Read-only. Grades the MAP of LIBRARY_MARTS: is each table what the catalog says,
is each key tag true, do links match, is there plain English. Script: scripts/audit_catalog.py.

## MAP parts

```
Tags true                        556 of     619    89.8%
  (labeled key columns empty in sample, not graded)      81 of      81   100.0%
Hard links work                  234 of     250    93.6%
Tables with a summary            320 of     651    49.2%
Columns described                362 of  20,585     1.8%
Inventory clean                  651 of     651   100.0%
```

## Inventory

```
objects in catalog         651
  base tables              629
  views                     22
backup copies                0
exact duplicate groups       0
objects that error           0
schemas                     36
  with 4 or fewer           17
```

Views and their real row counts:

- ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL: 128155142
- ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL: 20000000
- ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2: 93119582
- FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM: 44398
- FINANCE.FINANCE__FED_SEC_13F_HOLDINGS: 101261252
- FINDINGS.CATALOG: 9
- FINDINGS.EXCLUDED_PROVIDER_AT_FACILITY: 39
- FINDINGS.EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION: 287
- FINDINGS.EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION_IN_SHORTAGE: 287
- FINDINGS.FEDERAL_CONTRACTOR_EPA_VIOLATOR: 57
- FINDINGS.HOSPITAL_CLOSURE_RISK: 4210
- FINDINGS.HOSPITAL_CLOSURE_RISK_BY_STATE: 55
- FINDINGS.MEMBER_MONEY_VS_OUTPUT: 635
- FINDINGS.OPIOID_PRESCRIBER_PAID_HIGH_RX: 6020
- FINDINGS.OPIOID_PRESCRIBER_PAID_HIGH_RX_BY_STATE: 51
- FINDINGS.PAC_FUNDS_BOTH_SIDES: 2680
- FINDINGS.REVOKED_BUT_DEDUCTIBLE: 22512
- FINDINGS.REVOKED_BUT_DEDUCTIBLE_BY_STATE: 59
- HEALTH.HEALTH__FED_FDA_FAERS_DRUG: 20914284
- HEALTH.HEALTH__FED_FDA_FAERS_REAC: 20621386
- JUSTICE.JUSTICE__FED_COURTLISTENER_CITATIONS: 18123788
- JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS: 71677647

Backup copies:


Schemas by size:

```
HEALTH                            106
POLITICS                           83
ENVIRONMENT                        70
JUSTICE                            67
FINANCE                            61
ECONOMICS                          45
REFERENCE                          34
ENERGY                             29
HOUSING                            18
EDUCATION                          16
IMMIGRATION                        15
FINDINGS                           13
LABOR                              12
OPEN_DATA                          11
CORPORATE_REGISTRY                 11
TRANSPORT                          11
CORE                                7
SCIENCE_RESEARCH                    6
SCIENCE                             5
CONSUMER_SAFETY                     4
HISTORY                             4
PROCUREMENT                         4
EPSTEIN                             3
INVESTIGATIONS                      3
GOVERNMENT_RECORDS                  2
CONSUMER_PROTECTION                 1
LEGAL_ENFORCEMENT                   1
MONEY_FINANCE                       1
MARITIME                            1
HISTORICAL_RECORDS                  1
LAND_AND_TERRITORY                  1
FOREIGN_INFLUENCE                   1
REGULATORY                          1
JUDICIARY                           1
CRIMINAL_JUSTICE                    1
GOVERNANCE                          1
```

## Tag truth

Verdict per tag. PASS = 90%+ of sampled values fit the key's shape.
Name tags PASS only when the values read as organizations.

### Platform tagger, connect/keys.py

```
tag             cols  PASS  WEAK  FAIL EMPTY NOTEST
NAME            1392   830     0   452   110      0
STATE            450   321     2    68    59      0
ZIP              225   183    12    14    16      0
ADDRESS          200     0     0     0    13    187
COUNTRY          147     0     0     0    20    127
FIPS             128    90     6    13    19      0
LATLON           119     0     0     0     8    111
EIN               56    36    10     0    10      0
NPI               46    41     0     1     4      0
DOCKET            38     0     0     0     3     35
CCN               37    30     4     0     3      0
NAICS             32     0     0     0     1     31
SIC               25     0     0     0     6     19
CIK               24    24     0     0     0      0
BIOGUIDE          22    22     0     0     0      0
ACCESSION         21    21     0     0     0      0
FRS_ID            21    19     0     0     2      0
UEI               18    16     0     1     1      0
FEC_CMTE_ID       18    17     1     0     0      0
LEI               15    14     0     1     0      0
FEC_CAND_ID       13    13     0     0     0      0
DUNS              12     8     0     0     4      0
EIA_UTILITY_ID    12     0     0     0     0     12
GEOM              12     0     0     0     3      9
EIA_PLANT_ID      10     0     0     0     0     10
NPDES_ID          10     0     0     0     0     10
PWSID             10     9     0     0     1      0
CL_PERSON_ID       9     0     0     0     0      9
PECOS_PAC_ID       8     0     0     0     0      8
PECOS_ENRLMT_ID     7     0     0     0     0      7
ICPSR              6     0     0     0     0      6
NCUA_CHARTER       5     0     0     0     0      5
IMO                5     4     0     0     1      0
CFDA               4     0     0     0     0      4
CAS                4     0     0     0     0      4
CL_COURT_ID        4     0     0     0     0      4
ICE_FACILITY       3     0     0     0     0      3
MINE_ID            3     3     0     0     0      0
MSHA_CONTROLLER_ID     3     0     0     0     0      3
COMPANY_NO         2     0     0     0     0      2
FDIC_CERT          2     0     0     0     0      2
CUSIP              2     0     0     0     0      2
HCPCS              2     0     0     0     0      2
DEA_NO             2     2     0     0     0      0
FDA_510K_NO        2     2     0     0     0      0
FDA_PMA_NO         2     2     0     0     0      0
MSHA_OPERATOR_ID     2     0     0     0     0      2
AWARD_KEY          1     0     0     0     0      1
CAGE               1     0     0     0     0      1
RSSD               1     0     0     0     0      1
NDC                1     0     0     0     0      1
PATENT             1     0     0     0     0      1
MMSI               1     0     0     0     0      1
```

### Catalog regex, catalog.json

```
tag             cols  PASS  WEAK  FAIL EMPTY NOTEST
ORG_NAME        1163   761     0   328    74      0
STATE            376   311     2    41    22      0
ZIP              231   176    18    16    21      0
COUNTY_FIPS      120    35     5    61    19      0
EIN               56    36    10     0    10      0
NPI               49    40     0     5     4      0
FRS/EPA           47    27     0    18     2      0
CCN               36    27     4     2     3      0
UEI/DUNS          30    24     0     1     5      0
CIK               24    23     0     1     0      0
FEC_ID            21    19     0     2     0      0
BIOGUIDE          19    19     0     0     0      0
ACCESSION         13    11     0     2     0      0
LEI                9     8     0     1     0      0
FDIC_CERT          6     0     0     0     0      6
IMO                4     3     0     0     1      0
MINE_ID            3     3     0     0     0      0
```

### Why platform tags fail, by the extra word in the column name

The tagger fires on one word, like NPI, and ignores what else the name says.

```
no extra word      96
NAME                1
4                   1
```

### What NAME-tagged columns hold

```
organizations                      444
names, org or person unclear       219
places                             164
numbers                            128
parts of people's names            122
empty                              110
single words or codes              107
things, not names                   53
people                              45
```

### FIPS columns by level

```
state               50
county              42
None                22
county part, no state    12
tract                1
block group          1
```

## Links

A link works when 5.0%+ of table A's distinct IDs, and 50+ IDs, appear in B.

```
key              columns  pairs working
EIN                   46   2062     391
NPI                   41   1638     401
CCN                   34   1100     228
CIK                   24    552     293
BIOGUIDE              22    456     387
ACCESSION             21    420      34
FRS_ID                19    342     249
FEC_CMTE_ID           18    302     240
UEI                   16    230     111
LEI                   14    168      70
FEC_CAND_ID           13    156     156
NPDES_ID              10     90      81
CL_PERSON_ID           9     72      56
PWSID                  9     72      72
DUNS                   8     52      27
ICPSR                  6     30      27
NCUA_CHARTER           5     18       9
CL_COURT_ID            4     12      12
IMO                    4     10       2
ICE_FACILITY           3      6       6
MSHA_CONTROLLER_ID       3      6       6
MINE_ID                3      6       6
COMPANY_NO             2      2       2
CUSIP                  2      2       2
DEA_NO                 2      0       0
FDA_510K_NO            2      2       2
FDA_PMA_NO             2      2       2
MSHA_OPERATOR_ID       2      2       2
ZIP                    1      0       0
PATENT                 1      0       0
None                   1      0       0
MMSI                   1      0       0
```

## Time

```
catalog tables with a timeline view     403
with date columns, no timeline view      66
no date columns at all                  325
```

Grain of timeline views: day 269, year 120, quarter 7, month 7

## Findings

```
C2 name tag holds something else           551
C2 tag fails its format                    272
C2 catalog regex tag wrong                 150
C5 dates but no timeline view               66
C3 untagged key, by name                    33
C1 view counted as a table                  22
C4 hard ID with no partner                  13
C3 untagged key, by value                    6
C4 hard ID matches nothing                   3
```

By severity: minor 685, moderate 402, severe 29

Every finding: audit/catalog_audit_2026-09-23.tsv. Every column: audit/catalog_audit_columns_2026-09-23.tsv.
Every link pair: audit/catalog_audit_links_2026-09-23.tsv.