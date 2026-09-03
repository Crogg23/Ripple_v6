# FED_CDC_WONDER

rows 880  columns 9  scan 1.9s

roles: amount 1, audit 2, category 4, other 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CRUDE_RATE | 803 | 0 | 20.90 | 306.97 | 359.10 | 37.0K |

## who

_SRC_SHA256 by rows
       880  8203934d4be3465e63ef558b3ca73cf9f519207693000562af6bc14d38f3fb48

_SRC_SHA256 by dollars
       37.0K      880 rows  8203934d4be3465e63ef558b3ca73cf9f519207693000562af6bc14d38f3

## what

YEAR: 2020 8%, 2019 8%, 2018 8%, 2017 8%, 2016 8%, 2015 8%, 2014 8%, 2013 8%, 2012 8%, 2011 8%, 2010 8%, 2009 8%

ICD_CHAPTER: External causes of morbidity a 8%, Codes for special purposes 8%, Symptoms, signs and abnormal c 8%, Congenital malformations, defo 8%, Certain conditions originating 8%, Pregnancy, childbirth and the  8%, Diseases of the genitourinary  8%, Diseases of the musculoskeleta 8%, Diseases of the skin and subcu 8%, Diseases of the digestive syst 8%, Diseases of the respiratory sy 8%, Diseases of the circulatory sy 8%

SEX: Male 50%, Female 50%

POPULATION: 162,256,202 8%, 167,227,921 8%, 161,657,324 8%, 166,582,199 8%, 161,128,679 8%, 166,038,755 8%, 160,408,119 8%, 165,311,059 8%, 159,078,923 8%, 164,048,590 8%, 158,229,297 8%, 163,189,523 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 22 | 0 | 2020 40; 2019 40; 2018 40; 2017 40 |
| ICD_CHAPTER | category | 20 | 0 | External causes of morbid 44; Codes for special purpose 44; Symptoms, signs and abnor 44; Congenital malformations, 44 |
| SEX | category | 2 | 0 | Male 440; Female 440 |
| DEATHS | other | 763 | 0 | 0 54; Suppressed 9; 29 6; 25 6 |
| POPULATION | category | 44 | 0 | 162,256,202 20; 167,227,921 20; 161,657,324 20; 166,582,199 20 |
| CRUDE_RATE | amount | 421 | 0 | 0.0 73; Unreliable 69; 2.8 15; 2.9 15 |
| _INGESTED_AT | audit | 1 | 0 | 1787435566515654 880 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 5e526f3f-65c2-4be5-b766-2 880 |
| _SRC_SHA256 | who | 1 | 0 | 8203934d4be3465e63ef558b3 880 |
