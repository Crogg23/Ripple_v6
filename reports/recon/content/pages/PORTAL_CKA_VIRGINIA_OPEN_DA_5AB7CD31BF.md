# PORTAL_CKA_VIRGINIA_OPEN_DA_5AB7CD31BF

rows 3.9K  columns 10  scan 3.6s

roles: amount 1, audit 2, category 2, date 1, other 2, who 3

## when

INGESTED_AT
  2026      3.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| INCIDENCE_RATE | 3.9K | 0 | 1.50 | 451.08 | 1.5K | 95.8K |

## who

GEOGRAPHY_VALUE by rows
        73  Virginia
        54  Northern
        54  Southwest
        54  Eastern
        54  Central
        54  Northwest
        27  Galax
        27  Rappahannock
        27  Caroline
        27  Warren
        27  Hanover
        27  Greene
        27  Essex
        27  Madison
        27  Staunton
        27  Roanoke City
        27  Newport News
        27  Martinsville
        27  Middlesex
        27  Buckingham

GEOGRAPHY_VALUE by dollars
        2.7K       27 rows  Petersburg
        2.6K       27 rows  Nottoway
        2.1K       27 rows  Richmond City
        2.0K       27 rows  Portsmouth
        1.9K       27 rows  Hopewell
        1.9K       27 rows  Norfolk
        1.7K       27 rows  Hampton
        1.6K       27 rows  Newport News
        1.6K       27 rows  Franklin City
        1.6K       27 rows  Roanoke City
        1.5K       27 rows  Danville
        1.2K       27 rows  Harrisonburg
        1.2K       27 rows  Suffolk
        1.2K       27 rows  Emporia
        1.1K       27 rows  Fredericksburg
        1.0K       27 rows  Henrico
        1.0K       27 rows  Charlottesville
        1.0K       27 rows  Alexandria
        1.0K       27 rows  Prince George
      971.20       27 rows  Brunswick

CONDITION by rows
       267  Ehrlichiosis/Anaplasmosis
       134  Chickenpox (Varicella)
       134  Human immunodeficiency virus (HIV)
       134  Chlamydia trachomatis infection
       134  Hepatitis C, chronic
       134  Hepatitis C, acute
       134  Shigellosis
       134  Spotted Fever Rickettsiosis (including RMSF)
       134  Hepatitis A
       134  Salmonellosis
       134  Lyme disease
       134  Vibriosis, non-cholera
       134  Tuberculosis
       134  Hepatitis B, acute
       134  Haemophilus influenzae, invasive
       134  Giardiasis
       134  Pertussis
       134  Streptococcal disease, Group A, invasive or toxic shock
       134  Hepatitis B, chronic
       134  Gonorrhea

CONDITION by dollars
       47.8K      134 rows  Chlamydia trachomatis infection
       15.1K      134 rows  Gonorrhea
       10.4K      134 rows  Hepatitis C, chronic
        4.0K      134 rows  Campylobacteriosis
        3.5K      134 rows  Lyme disease
        2.5K      134 rows  Salmonellosis
        2.0K      134 rows  Syphilis, early
        1.7K      134 rows  Hepatitis B, chronic
        1.4K      134 rows  Pertussis
        1.3K      134 rows  Streptococcal disease, Group A, invasive or toxic shock
        1.0K      134 rows  Human immunodeficiency virus (HIV)
      868.10      134 rows  Shiga toxin-producing Escherichia coli Infection (STEC)
      758.70      267 rows  Ehrlichiosis/Anaplasmosis
      422.80      134 rows  Cryptosporidiosis
      391.10      134 rows  Haemophilus influenzae, invasive
      366.60      134 rows  Giardiasis
      338.90      134 rows  Legionellosis
      322.30      134 rows  Shigellosis
      272.30      134 rows  Chickenpox (Varicella)
      240.30      134 rows  Vibriosis, non-cholera

SRC_SHA256 by rows
      3.9K  b5e22d8131541db9de74162e33c6f1437e70ed3454383b3da34e86c0ec94c85a

SRC_SHA256 by dollars
       95.8K     3.9K rows  b5e22d8131541db9de74162e33c6f1437e70ed3454383b3da34e86c0ec94

## who x when

GEOGRAPHY_VALUE by INGESTED_AT  LOAD STAMP, not an event date, dollars = INCIDENCE_RATE
  Buckingham                                2026:754
  Caroline                                  2026:582.30
  Central                                   2026:12.70
  Danville                                  2026:1.5K
  Eastern                                   2026:8.40
  Essex                                     2026:858.60
  Franklin City                             2026:1.6K
  Galax                                     2026:759.40
  Greene                                    2026:455.50
  Hampton                                   2026:1.7K
  Hanover                                   2026:444.40
  Harrisonburg                              2026:1.2K
  Hopewell                                  2026:1.9K
  Madison                                   2026:353.90
  Martinsville                              2026:930.10
  Middlesex                                 2026:494.60
  Newport News                              2026:1.6K
  Norfolk                                   2026:1.9K
  Northern                                  2026:14.10
  Northwest                                 2026:9.10
  Nottoway                                  2026:2.6K
  Petersburg                                2026:2.7K
  Portsmouth                                2026:2.0K
  Rappahannock                              2026:296.80
  Richmond City                             2026:2.1K
  Roanoke City                              2026:1.6K
  Southwest                                 2026:11.20
  Staunton                                  2026:567.40
  Virginia                                  2026:808
  Warren                                    2026:564.20

CONDITION by INGESTED_AT  LOAD STAMP, not an event date, dollars = INCIDENCE_RATE
  Campylobacteriosis                        2026:4.0K
  Chickenpox (Varicella)                    2026:272.30
  Chlamydia trachomatis infection           2026:47.8K
  Cryptosporidiosis                         2026:422.80
  Ehrlichiosis/Anaplasmosis                 2026:758.70
  Giardiasis                                2026:366.60
  Gonorrhea                                 2026:15.1K
  Haemophilus influenzae, invasive          2026:391.10
  Hepatitis A                               2026:67.70
  Hepatitis B, acute                        2026:135.30
  Hepatitis B, chronic                      2026:1.7K
  Hepatitis C, acute                        2026:98.70
  Hepatitis C, chronic                      2026:10.4K
  Human immunodeficiency virus (HIV)        2026:1.0K
  Legionellosis                             2026:338.90
  Lyme disease                              2026:3.5K
  Pertussis                                 2026:1.4K
  Salmonellosis                             2026:2.5K
  Shiga toxin-producing Escherichia coli I  2026:868.10
  Shigellosis                               2026:322.30
  Spotted Fever Rickettsiosis (including R  2026:235.40
  Streptococcal disease, Group A, invasive  2026:1.3K
  Syphilis, early                           2026:2.0K
  Tuberculosis                              2026:171.60
  Vibriosis, non-cholera                    2026:240.30

## what

YEAR: 2024 96%, 2023 4%

GEOGRAPHY_LEVEL: Locality 91%, Health Planning Region 7%, State 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 2 | 0 | 2024 3.8K; 2023 168 |
| CONDITION | who | 75 | 0 | Ehrlichiosis/Anaplasmosis 267; Vibriosis, non-cholera 134; Tuberculosis 134; Syphilis, early 134 |
| GEOGRAPHY_LEVEL | category | 3 | 0 | Locality 3.6K; Health Planning Region 270; State 73 |
| GEOGRAPHY_VALUE | who | 138 | 0 | Virginia 73; Northern 54; Eastern 54; Northwest 54 |
| FIPS | other | 135 | 0 | NA 343; 51840 27; 51830 27; 51820 27 |
| ANNUAL_CASE_COUNT | other | 201 | 0 | 0 1.7K; 1 602; 2 307; 3 207 |
| INCIDENCE_RATE | amount | 681 | 0 | 0 1.7K; 0.1 50; 1 43; 3 33 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:06:56.69683 3.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | ecd35dd0-c518-4556-9ad1-1 3.9K |
| SRC_SHA256 | who | 1 | 0 | b5e22d8131541db9de74162e3 3.9K |
