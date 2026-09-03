# FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS

rows 6.6K  columns 18  scan 3.1s

roles: audit 2, category 2, date 1, id 2, other 9, state 1, who 3

## when

_INGESTED_AT
  2026      6.6K  ##############################

## who

LAST_NAME by rows
        80  PATEL
        32  KHAN
        31  SMITH
        26  NGUYEN
        26  LEE
        25  SINGH
        25  KIM
        23  SHAH
        17  JOHNSON
        16  PARK
        16  SHARMA
        16  CHEN
        14  MILLER
        14  JONES
        13  DAVIS
        12  PHILLIPS
        12  WILLIAMS
        12  ANDERSON
        11  MOORE
        11  ALI

ORGANIZATION_LEGAL_NAME by rows
        42  INOVA HEALTH CARE SERVICES
        42  HEALTHTEXAS PROVIDER NETWORK
        36  LEHIGH VALLEY PHYSICIAN GROUP
        35  ORTHOLONESTAR PLLC
        34  TMH PHYSICIAN ASSOCIATES PLLC
        33  BAPTIST HEALTH MEDICAL GROUP INC
        32  ST LUKES PHYSICIAN GROUP INC
        27  ST DAVIDS HEART & VASCULAR PLLC
        27  PROVIDENCE MEDICAL FOUNDATION
        26  THE EMORY CLINIC INC
        26  ORTHONJ LLC
        25  HEALTH FIRST MEDICAL GROUP LLC
        25  SUTTER VALLEY MEDICAL FOUNDATION
        24  SUTTER BAY MEDICAL FOUNDATION
        23  SOUTHCOAST PHYSICIANS GROUP INC
        22  HH HEART CENTER LLC
        22  STEWARD MEDICAL GROUP INC
        21  PIEDMONT CARDIOLOGY OF ATLANTA, LLC
        21  CAPITAL CARDIOLOGY ASSOCIATES PLLC
        20  SETON FAMILY OF DOCTORS

FIRST_NAME by rows
       188  MICHAEL
       176  JOHN
       174  DAVID
       116  JAMES
       107  ROBERT
        91  WILLIAM
        76  MARK
        72  DANIEL
        69  JOSEPH
        67  MATTHEW
        67  RICHARD
        66  CHRISTOPHER
        63  JEFFREY
        62  THOMAS
        61  STEVEN
        60  BRIAN
        53  ANDREW
        52  PETER
        51  PAUL
        44  STEPHEN

## who x when

LAST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  ALI                                       2026:11
  ANDERSON                                  2026:12
  CHEN                                      2026:16
  DAVIS                                     2026:13
  JOHNSON                                   2026:17
  JONES                                     2026:14
  KHAN                                      2026:32
  KIM                                       2026:25
  LEE                                       2026:26
  MILLER                                    2026:14
  MOORE                                     2026:11
  NGUYEN                                    2026:26
  PARK                                      2026:16
  PATEL                                     2026:80
  PHILLIPS                                  2026:12
  SHAH                                      2026:23
  SHARMA                                    2026:16
  SINGH                                     2026:25
  SMITH                                     2026:31
  WILLIAMS                                  2026:12

ORGANIZATION_LEGAL_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  BAPTIST HEALTH MEDICAL GROUP INC          2026:33
  CAPITAL CARDIOLOGY ASSOCIATES PLLC        2026:21
  HEALTH FIRST MEDICAL GROUP LLC            2026:25
  HEALTHTEXAS PROVIDER NETWORK              2026:42
  HH HEART CENTER LLC                       2026:22
  INOVA HEALTH CARE SERVICES                2026:42
  LEHIGH VALLEY PHYSICIAN GROUP             2026:36
  ORTHOLONESTAR PLLC                        2026:35
  ORTHONJ LLC                               2026:26
  PIEDMONT CARDIOLOGY OF ATLANTA, LLC       2026:21
  PROVIDENCE MEDICAL FOUNDATION             2026:27
  SETON FAMILY OF DOCTORS                   2026:20
  SOUTHCOAST PHYSICIANS GROUP INC           2026:23
  ST DAVIDS HEART & VASCULAR PLLC           2026:27
  ST LUKES PHYSICIAN GROUP INC              2026:32
  STEWARD MEDICAL GROUP INC                 2026:22
  SUTTER BAY MEDICAL FOUNDATION             2026:24
  SUTTER VALLEY MEDICAL FOUNDATION          2026:25
  THE EMORY CLINIC INC                      2026:26
  TMH PHYSICIAN ASSOCIATES PLLC             2026:34

## where

STATE: TX 1.1K, CA 644, FL 643, GA 349, NJ 298, MI 281, VA 270, NY 251, PA 240, OH 191, LA 162, AL 156

## what

ASM_COHORT: Low Back Pain 61%, Heart Failure 39%

ASM_CY27_SMALLPRACTICE: No 64%, Yes 36%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | id | 6.5K | 0 | 1992971055 34; 1992885297 34; 1992868368 34; 1992867329 34 |
| FIRST_NAME | who | 2.4K | 0 | MICHAEL 188; JOHN 176; DAVID 174; JAMES 116 |
| LAST_NAME | who | 5.0K | 0 | PATEL 80; LEE 37; KIM 35; NGUYEN 35 |
| STATE | state | 49 | 0 | TX 1.1K; CA 644; FL 643; GA 349 |
| ASM_COHORT | category | 2 | 0 | Low Back Pain 4.0K; Heart Failure 2.6K |
| ORGANIZATION_LEGAL_NAME | who | 2.6K | 17 | ORTHOLONESTAR PLLC 47; HEALTHTEXAS PROVIDER NETW 42; INOVA HEALTH CARE SERVICE 42; ORTHONJ LLC 41 |
| ASM_CY27_PARTICIPANT | other | 1 | 0 | Yes 6.6K |
| ASM_CY27_SMALLPRACTICE | category | 2 | 0 | No 4.3K; Yes 2.4K |
| ASM_CY28_PARTICIPANT | other | 1 | 0 | Null 6.6K |
| ASM_CY28_SMALLPRACTICE | other | 1 | 0 | Null 6.6K |
| ASM_CY29_PARTICIPANT | other | 1 | 0 | Null 6.6K |
| ASM_CY29_SMALLPRACTICE | other | 1 | 0 | Null 6.6K |
| ASM_CY30_PARTICIPANT | other | 1 | 0 | Null 6.6K |
| ASM_CY30_SMALLPRACTICE | other | 1 | 0 | Null 6.6K |
| ASM_CY31_PARTICIPANT | other | 1 | 0 | Null 6.6K |
| ASM_CY31_SMALLPRACTICE | other | 1 | 0 | Null 6.6K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 10:56:17.150 6.6K |
| _SOURCE_RUN_ID | audit id | 6.6K | 0 | f386edfc-1bd4-4560-ae33-7 34; 61fbff1d-77bd-4341-aead-2 34; b6c3d2b0-9f0c-4d87-94b9-c 34; 5ccb05ae-ce0a-4ecf-9140-2 34 |
