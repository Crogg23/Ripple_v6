# PORTAL_CKA_SAN_JOSE_OPEN_DA_399CADBC5E

rows 10.0K  columns 18  scan 4.8s

roles: audit 2, category 3, date 4, id 3, other 3, who 4

## when

START_DATE
  2021     10.0K  ##############################

REPORT_DATE
  2021     10.0K  ##############################

OFFENSE_DATE
  2021     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## who

CALL_TYPE by rows
      1.1K  DISTURBANCE
       880  VEHICLE STOP
       821  WELFARE CHECK
       567  ALARM, AUDIBLE
       423  PARKING VIOLATION
       394  SUSPICIOUS VEHICLE
       348  STOLEN VEHICLE
       333  DISTURBANCE, FAMILY
       327  RECOVERED STOLEN VEHICLE
       314  UNK TYPE 911 CALL
       309  SUSPICIOUS PERSON
       273  DISTURBANCE, MUSIC
       262  SUSPICIOUS CIRCUMSTANCES
       239  TRESPASSING
       178  RECKLESS DRIVING
       165  WELFARE CHECK (COMBINED EVENT)
       156  MEET THE CITIZEN
       125  THEFT
       125  BURGLARY  REPORT  (460)
       122  VEHICLE ACCIDENT, PROPERTY DAM

ADDRESS by rows
        40  [2100]-[2200] MONTEREY RD
        39  Not a valid geographical locat
        38  [2800]-[2900] STEVENS CREEK BL
        31  [200]-[300] W MISSION ST
        29  [400]-[500] S MARKET ST
        29  [1700]-[1800] AIRPORT BL
        25  [500]-[600] COLEMAN AV
        23  [500]-[600] E ST JOHN ST
        22  [900]-[1000] BLOSSOM HILL RD
        22  [1500]-[1600] N 1ST ST
        22  [1100]-[1200] S 2ND ST
        20  [300]-[400] SANTANA RW
        20  [700]-[800] STORY RD
        19  [2000]-[2100] N 1ST ST
        19  [300]-[400] N CAPITOL AV
        18  TULLY RD & COCONUT DR
        18  [5800]-[5900] CHARLOTTE DR
        16  [900]-[1000] STORY RD
        16  [1600]-[1700] TULLY RD
        16  [400]-[500] BLOSSOM HILL RD

CITY by rows
     10.0K  San Jose

SRC_SHA256 by rows
     10.0K  3ad26f91842f9670719e3682b83e7f799ae261df651c04c838b6b59e0ff9064f

## who x when

CALL_TYPE by REPORT_DATE
  ALARM, AUDIBLE                            2021:567
  BURGLARY  REPORT  (460)                   2021:125
  DISTURBANCE                               2021:1.1K
  DISTURBANCE, FAMILY                       2021:333
  DISTURBANCE, MUSIC                        2021:273
  MEET THE CITIZEN                          2021:156
  PARKING VIOLATION                         2021:423
  RECKLESS DRIVING                          2021:178
  RECOVERED STOLEN VEHICLE                  2021:327
  STOLEN VEHICLE                            2021:348
  SUSPICIOUS CIRCUMSTANCES                  2021:262
  SUSPICIOUS PERSON                         2021:309
  SUSPICIOUS VEHICLE                        2021:394
  THEFT                                     2021:125
  TRESPASSING                               2021:239
  UNK TYPE 911 CALL                         2021:314
  VEHICLE ACCIDENT, PROPERTY DAM            2021:122
  VEHICLE STOP                              2021:880
  WELFARE CHECK                             2021:821
  WELFARE CHECK (COMBINED EVENT)            2021:165

ADDRESS by REPORT_DATE
  Not a valid geographical locat            2021:39
  TULLY RD & COCONUT DR                     2021:18
  [1100]-[1200] S 2ND ST                    2021:22
  [1500]-[1600] N 1ST ST                    2021:22
  [1600]-[1700] TULLY RD                    2021:16
  [1700]-[1800] AIRPORT BL                  2021:29
  [2000]-[2100] N 1ST ST                    2021:19
  [200]-[300] W MISSION ST                  2021:31
  [2100]-[2200] MONTEREY RD                 2021:40
  [2800]-[2900] STEVENS CREEK BL            2021:38
  [300]-[400] N CAPITOL AV                  2021:19
  [300]-[400] SANTANA RW                    2021:20
  [400]-[500] BLOSSOM HILL RD               2021:16
  [400]-[500] S MARKET ST                   2021:29
  [500]-[600] COLEMAN AV                    2021:25
  [500]-[600] E ST JOHN ST                  2021:23
  [5800]-[5900] CHARLOTTE DR                2021:18
  [700]-[800] STORY RD                      2021:20
  [900]-[1000] BLOSSOM HILL RD              2021:22
  [900]-[1000] STORY RD                     2021:16

## what

PRIORITY: 2 34%, 3 31%, 4 13%, 6 11%, 5 8%, 1 3%

FINAL_DISPO_CODE: N 50%, CAN 16%, R 12%, G 6%, O 3%, D 2%, DUPNCAN 2%, A 2%, GD 2%, E 2%, H 1%, U 1%

FINAL_DISPO: No report required; dispatch r 49%, Canceled 16%, Report taken 12%, Gone on Arrival/unable to loca 6%, No Disposition 5%, Supplemental report taken 3%, Traffic Citation Issued, Hazar 2%, Arrest Made 2%, Traffic Citation Issued, Non-H 2%, Courtesy Service/Citizen or ag 1%, Unfounded event 1%, Turned over To (TOT) 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CDTS | id | 10.1K | 0 | 20210114085107PS 50; 20210114095941PS 50; 20210114085047PS 50; 20210114093554PS 50 |
| EID | id | 9.6K | 0 | 8460663 51; 8460434 51; 8460128 51; 8459843 51 |
| START_DATE | date | 1 | 0 | 5/15/2021 12:00:00 AM 10.0K |
| CALL_NUMBER | id | 9.9K | 0 | P210140124 51; P210130917 51; P210130679 51; P210140181 50 |
| PRIORITY | category | 6 | 0 | 2 3.4K; 3 3.1K; 4 1.3K; 6 1.1K |
| REPORT_DATE | date | 14 | 0 | 1/9/2021 12:00:00 AM 881; 1/1/2021 12:00:00 AM 824; 1/4/2021 12:00:00 AM 797; 1/3/2021 12:00:00 AM 781 |
| OFFENSE_DATE | date | 14 | 0 | 1/9/2021 12:00:00 AM 881; 1/1/2021 12:00:00 AM 824; 1/4/2021 12:00:00 AM 797; 1/3/2021 12:00:00 AM 781 |
| OFFENSE_TIME | other | 9.3K | 0 | 07:04:47 51; 22:28:48 51; 16:44:34 51; 08:51:07 50 |
| CALLTYPE_CODE | other | 156 | 0 | 415 1.1K; 1195 880; WELCK 821; 1033A 567 |
| CALL_TYPE | who | 153 | 0 | DISTURBANCE 1.1K; VEHICLE STOP 880; WELFARE CHECK 821; ALARM, AUDIBLE 567 |
| FINAL_DISPO_CODE | category | 20 | 0 | N 4.8K; CAN 1.5K; R 1.2K; G 546 |
| FINAL_DISPO | category | 17 | 0 | No report required; dispa 4.8K; Canceled 1.5K; Report taken 1.2K; Gone on Arrival/unable to 546 |
| ADDRESS | who | 5.1K | 244 | TULLY RD & COCONUT DR 63; [2000]-[2100] N 1ST ST 52; [2700]-[2800] LONE BLUFF  51; [700]-[800] STORY RD 51 |
| CITY | who | 1 | 0 | San Jose 10.0K |
| STATE | other | 1 | 0 | CA 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:51:57.80755 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 825513c7-e43f-478a-83c8-7 10.0K |
| SRC_SHA256 | who | 1 | 0 | 3ad26f91842f9670719e3682b 10.0K |
