# PORTAL_SOC_OPEN_DATA_BR_21BB19A94A

rows 2.0K  columns 15  scan 2.8s

roles: audit 2, category 6, date 1, id 3, other 1, who 3

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

BUSINESS_NAME by rows
        12  AT&T
         7  ALLSTATE INSURANCE CO.
         7  ALL OUT COMMUNITY CARE SERVICES
         5  ALDENS SCHOOL OF COSMETOLOGY
         5  ADVANCE AMERICA CASH ADVANCE
         4  ANYTIME FITNESS
         4  AT&T AUTHORIZED RETAILER #2715
         4  ALLSTATE
         3  BOSLEY PLACE
         3  AAA RENT ALL
         3  BLUE SKIES LANDSCAPE LLC
         3  ALL AROUND CONSTRUCTION
         3  BEAUTY SUPPLY WAREHOUSE
         3  BRASFIELD & GORRIE
         3  AMERICAN GLASS DISTRIBUTORS
         2  3 D CORPORATE CLEANING SERVICES LLC
         2  ASSURANCE FINANCIAL GROUP LLC
         2  BR CONSTRUCTION LLC
         2  A A A ARDVARK STORAGE
         2  ARMSTRONG RELOCATION COMPANY

BUSINESS_NAICS_CODE by rows
       131  541000
       115  815000
       111  238000
       106  453000
        97  454000
        88  811000
        80  812000
        79  nan
        56  621000
        54  722000
        49  561000
        48  236000
        34  441000
        27  448000
        26  445000
        23  524210
        23  423000
        22  532000
        22  339000
        19  454100

SRC_SHA256 by rows
      2.0K  afac5bda0322c3b2a2d7110d741b01f1c13add94984ff750e296c27268d24c84

## who x when

BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date
  3 D CORPORATE CLEANING SERVICES LLC       2026:2
  A A A ARDVARK STORAGE                     2026:2
  AAA RENT ALL                              2026:3
  ADVANCE AMERICA CASH ADVANCE              2026:5
  ALDENS SCHOOL OF COSMETOLOGY              2026:5
  ALL AROUND CONSTRUCTION                   2026:3
  ALL OUT COMMUNITY CARE SERVICES           2026:7
  ALLSTATE                                  2026:4
  ALLSTATE INSURANCE CO.                    2026:7
  AMERICAN GLASS DISTRIBUTORS               2026:3
  ANYTIME FITNESS                           2026:4
  ARMSTRONG RELOCATION COMPANY              2026:2
  ASSURANCE FINANCIAL GROUP LLC             2026:2
  AT&T                                      2026:12
  AT&T AUTHORIZED RETAILER #2715            2026:4
  BEAUTY SUPPLY WAREHOUSE                   2026:3
  BLUE SKIES LANDSCAPE LLC                  2026:3
  BOSLEY PLACE                              2026:3
  BR CONSTRUCTION LLC                       2026:2
  BRASFIELD & GORRIE                        2026:3

BUSINESS_NAICS_CODE by INGESTED_AT  LOAD STAMP, not an event date
  236000                                    2026:48
  238000                                    2026:111
  339000                                    2026:22
  423000                                    2026:23
  441000                                    2026:34
  445000                                    2026:26
  448000                                    2026:27
  453000                                    2026:106
  454000                                    2026:97
  454100                                    2026:19
  524210                                    2026:23
  532000                                    2026:22
  541000                                    2026:131
  561000                                    2026:49
  621000                                    2026:56
  722000                                    2026:54
  811000                                    2026:88
  812000                                    2026:80
  815000                                    2026:115
  nan                                       2026:79

## what

CITY: BATON ROUGE 92%, ZACHARY 3%, BAKER 3%, CENTRAL 1%, GREENWELL SPRINGS 1%, PRIDE 0%, SLAUGHTER 0%, CLINTON 0%

ZIP: 70806 14%, 70816 14%, 70809 11%, 70815 10%, 70810 8%, 70802 8%, 70817 8%, 70808 7%, 70805 7%, 70814 6%, 70791 4%, 70714 3%

WEBSITE: nan 99%, http://albertsons.com/ 0%, http://ymcabr.org/ 0%, http://fmcna.com/fmcna/index.h 0%, http://bayoucommunityhealth.co 0%, http://brcyo.org 0%, http://aka1908.com 0%, http://batonrougealanon.org 0%, http://aarp.org/states/la 0%, http://broadmoorpresbyterian.o 0%, http://thebrightonschool.org/ 0%, http://brec.org 0%

ABC: NO 95%, YES 4%, nan 1%

ADDRESS_AUTHORITY: BATON ROUGE 60%, SAINT GEORGE 19%, PARISH 15%, CENTRAL 2%, BAKER 2%, ZACHARY 2%, SU 0%

HOME_BASED_BUSINESS: NO 93%, YES 7%, nan 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_NAME | who | 1.8K | 0 | AT&T 17; BRASFIELD & GORRIE 12; BOSLEY PLACE 12; BROCK SERVICES LTD 11 |
| FULL_ADDRESS | id | 2.0K | 0 | 9054 SCOTLAND AVE 10; 1337 CHARIOT DR 10; 4512 HIGHLAND RD 10; 9929 GLERMA AVE 10 |
| CITY | category | 8 | 0 | BATON ROUGE 1.8K; ZACHARY 62; BAKER 56; CENTRAL 26 |
| ZIP | category | 24 | 0 | 70806 244; 70816 241; 70809 197; 70815 178 |
| BUSINESS_NAICS_CODE | who | 305 | 0 | 541000 131; 815000 115; 238000 111; 453000 106 |
| PHONE_NUMBER | other | 69 | 0 | nan 1.9K; 225-361-0089 2; 225-275-3200 2; 225-445-0015 2 |
| WEBSITE | category | 48 | 0 | nan 1.9K; http://albertsons.com/ 4; http://ymcabr.org/ 3; http://fmcna.com/fmcna/in 2 |
| ABC | category | 3 | 0 | NO 1.9K; YES 79; nan 25 |
| ADDRESS_AUTHORITY | category | 7 | 0 | BATON ROUGE 1.2K; SAINT GEORGE 376; PARISH 294; CENTRAL 47 |
| ADDRESS_ID | id | 2.0K | 0 | 121983 10; 22839 10; 83966 10; 129396 10 |
| THE_GEOM | id | 2.0K | 0 | {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| HOME_BASED_BUSINESS | category | 3 | 0 | NO 1.9K; YES 137; nan 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:45:26.13263 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 74e31718-60e9-4275-a7b5-d 2.0K |
| SRC_SHA256 | who | 1 | 0 | afac5bda0322c3b2a2d7110d7 2.0K |
