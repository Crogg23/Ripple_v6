# FED_CDC_LEADING_CAUSES_STATE

rows 10.9K  columns 9  scan 2.4s

roles: amount 1, audit 2, category 3, other 1, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AGE_ADJUSTED_DEATH_RATE | 10.9K | 2.60 | 35.90 | 934.59 | 1.1K | 1.39M |

## who

STATE by rows
       209  Virginia
       209  Massachusetts
       209  District of Columbia
       209  New Hampshire
       209  North Dakota
       209  North Carolina
       209  Tennessee
       209  New York
       209  Texas
       209  California
       209  Nevada
       209  Connecticut
       209  New Mexico
       209  Maryland
       209  Missouri
       209  Kentucky
       209  Louisiana
       209  Indiana
       209  Vermont
       209  Nebraska

STATE by dollars
       33.3K      209 rows  Mississippi
       32.2K      209 rows  West Virginia
       32.0K      209 rows  Alabama
       31.8K      209 rows  Kentucky
       31.7K      209 rows  Oklahoma
       31.5K      209 rows  Louisiana
       31.1K      209 rows  Tennessee
       31.0K      209 rows  Arkansas
       29.3K      209 rows  South Carolina
       28.9K      209 rows  Missouri
       28.8K      209 rows  Georgia
       28.8K      209 rows  Indiana
       28.7K      209 rows  District of Columbia
       28.6K      209 rows  Ohio
       28.0K      209 rows  North Carolina
       28.0K      209 rows  Nevada
       27.7K      209 rows  Michigan
       27.0K      209 rows  Pennsylvania
       26.8K      209 rows  Texas
       26.7K      209 rows  Delaware

_SRC_SHA256 by rows
     10.9K  4e555484405f08d8248d3b5dac3dfa03798a9354545208d15646130adbdb6bdc

_SRC_SHA256 by dollars
       1.39M    10.9K rows  4e555484405f08d8248d3b5dac3dfa03798a9354545208d15646130adbdb

## what

YEAR: 1999 8%, 2000 8%, 2001 8%, 2002 8%, 2003 8%, 2004 8%, 2005 8%, 2006 8%, 2007 8%, 2008 8%, 2009 8%, 2010 8%

C_113_CAUSE_NAME: Nephritis, nephrotic syndrome  9%, Malignant neoplasms (C00-C97) 9%, Intentional self-harm (suicide 9%, Influenza and pneumonia (J09-J 9%, Diseases of heart (I00-I09,I11 9%, Diabetes mellitus (E10-E14) 9%, Chronic lower respiratory dise 9%, Cerebrovascular diseases (I60- 9%, Alzheimer's disease (G30) 9%, All Causes 9%, Accidents (unintentional injur 9%

CAUSE_NAME: Kidney disease 9%, Cancer 9%, Suicide 9%, Influenza and pneumonia 9%, Heart disease 9%, Diabetes 9%, CLRD 9%, Stroke 9%, Alzheimer's disease 9%, All causes 9%, Unintentional injuries 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 19 | 0 | 1999 572; 2000 572; 2001 572; 2002 572 |
| C_113_CAUSE_NAME | category | 11 | 0 | Nephritis, nephrotic synd 988; Malignant neoplasms (C00- 988; Intentional self-harm (su 988; Influenza and pneumonia ( 988 |
| CAUSE_NAME | category | 11 | 0 | Kidney disease 988; Cancer 988; Suicide 988; Influenza and pneumonia 988 |
| STATE | who | 51 | 0 | Wyoming 209; Wisconsin 209; West Virginia 209; Washington 209 |
| DEATHS | other | 6.0K | 0 | 563 56; 30 55; 677 55; 345 55 |
| AGE_ADJUSTED_DEATH_RATE | amount | 2.5K | 0 | 15.0 59; 11.1 58; 10.3 57; 10.5 57 |
| _INGESTED_AT | audit | 1 | 0 | 1786299503310413 10.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 781c8ffb-f621-4812-a70f-e 10.9K |
| _SRC_SHA256 | who | 1 | 0 | 4e555484405f08d8248d3b5da 10.9K |
