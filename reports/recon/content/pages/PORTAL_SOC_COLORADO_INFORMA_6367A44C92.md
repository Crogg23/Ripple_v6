# PORTAL_SOC_COLORADO_INFORMA_6367A44C92

rows 2.0K  columns 18  scan 3.0s

roles: audit 2, category 10, date 1, id 1, other 2, who 3

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

BUSINESSNAME1 by rows
         8  INDEPENDENCE PASS FOUNDATION
         6  COLORADO ROCKY MOUNTAIN SCHOOL
         5  Centennial Mental Health Center
         5  COLORADO BASKETBALL CLUB
         4  COLORADO JUNIOR RODEO ASSOCIATION
         4  BIOMEDICAL RESEARCH FOUNDATION OF COLORADO
         4  CARBONDALE COMMUNITY NONPROFIT CENTER
         4  Denver Broncos Charities
         4  Capital Sisters International Inc
         4  UNIVERSAL EDUCATION SUPPORTERS INC
         4  RUSSIAN CHRISTIAN RADIO INC
         4  WILDERNESS WORKSHOP
         4  Special KidsSpecial Families Inc
         4  Battlement Mesa Residence Inc
         4  Park Hill Residence Inc
         4  Falcon Community Builders for Classrooms
         4  COALITION FOR THE UPPER SOUTH PLATTE
         4  THOMPSON SOCCER ASSOCIATION INC
         4  FOUNDATION FOR BIOMEDICAL EDUCATION AND RESEARCH
         4  COLORADO CHILDREN'S CHORALE

BUSINESSNAME2 by rows
      1.8K  nan
        11  INC
         5  FOUNDATION INC
         5  CENTER
         4  Apprenticeship Training Fund
         4  ASSOCIATION FOUNDATION
         4  RESEARCH
         4  DBA STONE CREEK CHARTER SCHOOL
         4  Association (CSAHA)
         3  SOCIETY OF CPAS
         3  D/B/A OPPORTUNITY INTERNATIONAL-US
         3  ATTN TIMOTHY STANDRING
         3  MOUNTAINS - AFFILIATES
         3  C/O TOBIN RUPAREL KONCZAK & MUNDELL PC
         3  VALLEY INC
         3  STUDIES ENDOWMENT FUND INC
         2  CHILDREN
         2  OF THE ROCKIES
         2  COLORADO INC
         2  MEDICAL AND TRAUMA SERVICES ADVISORY CO

SRC_SHA256 by rows
      2.0K  6c693802065a902da4b2664be8b7673b9a10d51b2c4f2b4c18278d87c44a3bac

## who x when

BUSINESSNAME1 by INGESTED_AT  LOAD STAMP, not an event date
  BIOMEDICAL RESEARCH FOUNDATION OF COLORA  2026:4
  Battlement Mesa Residence Inc             2026:4
  CARBONDALE COMMUNITY NONPROFIT CENTER     2026:4
  COALITION FOR THE UPPER SOUTH PLATTE      2026:4
  COLORADO BASKETBALL CLUB                  2026:5
  COLORADO CHILDREN'S CHORALE               2026:4
  COLORADO JUNIOR RODEO ASSOCIATION         2026:4
  COLORADO ROCKY MOUNTAIN SCHOOL            2026:6
  Capital Sisters International Inc         2026:4
  Centennial Mental Health Center           2026:5
  Denver Broncos Charities                  2026:4
  FOUNDATION FOR BIOMEDICAL EDUCATION AND   2026:4
  Falcon Community Builders for Classrooms  2026:4
  INDEPENDENCE PASS FOUNDATION              2026:8
  Park Hill Residence Inc                   2026:4
  RUSSIAN CHRISTIAN RADIO INC               2026:4
  Special KidsSpecial Families Inc          2026:4
  THOMPSON SOCCER ASSOCIATION INC           2026:4
  UNIVERSAL EDUCATION SUPPORTERS INC        2026:4
  WILDERNESS WORKSHOP                       2026:4

BUSINESSNAME2 by INGESTED_AT  LOAD STAMP, not an event date
  ASSOCIATION FOUNDATION                    2026:4
  ATTN TIMOTHY STANDRING                    2026:3
  Apprenticeship Training Fund              2026:4
  Association (CSAHA)                       2026:4
  C/O TOBIN RUPAREL KONCZAK & MUNDELL PC    2026:3
  CENTER                                    2026:5
  CHILDREN                                  2026:2
  COLORADO INC                              2026:2
  D/B/A OPPORTUNITY INTERNATIONAL-US        2026:3
  DBA STONE CREEK CHARTER SCHOOL            2026:4
  FOUNDATION INC                            2026:5
  INC                                       2026:11
  MEDICAL AND TRAUMA SERVICES ADVISORY CO   2026:2
  MOUNTAINS - AFFILIATES                    2026:3
  OF THE ROCKIES                            2026:2
  RESEARCH                                  2026:4
  SOCIETY OF CPAS                           2026:3
  STUDIES ENDOWMENT FUND INC                2026:3
  VALLEY INC                                2026:3
  nan                                       2026:1.8K

## what

TAXYR: 2012 28%, 2011 27%, 2010 23%, 2013 15%, 2009 5%, 2016 1%, 2014 0%, 2015 0%

LOBBYINGACTIVITIESIND: f 95%, t 5%

INDEPENDENTAUDITFINCLSTMTIND: f 66%, t 34%

CONSOLIDATEDAUDITFINCLSTMTIND: f 87%, t 13%

FORM990PROVIDEDTOGVRNBODYIND: t 79%, f 21%

CONFLICTOFINTERESTPOLICYIND: t 68%, f 32%

WHISTLEBLOWERPOLICYIND: f 53%, t 47%

DOCUMENTRETENTIONPOLICYIND: f 50%, t 50%

LICENSEDSTATESCD: nan 94%, CO 5%, WY 0%, WA 0%, WI 0%, TX 0%, WV 0%, NY 0%, VA 0%, GA 0%, MD 0%, NC 0%

ALLSTATESCD: nan 100%, All States 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 2.0K | 0 | 201340089349301004 11; 201333179349306363 11; 201343179349300724 10; 201343169349305129 10 |
| TAXYR | category | 8 | 0 | 2012 553; 2011 545; 2010 466; 2013 308 |
| BUSINESSNAME1 | who | 1.2K | 0 | BAM Swim Team 11; SUMMER SCHOLARS 11; THE EARLY LEARNING CENTER 11; NATIONAL STRENGTH & CONDI 11 |
| EIN | other | 1.1K | 0 | 841505469 11; 841314292 11; 841160185 11; 050524458 11 |
| MISSIONDESC | other | 1.3K | 0 | NONE 28; Support adult fitness swi 11; THE ELC IS A CHILD ENRICH 11; EDUCATIONAL ORGANIZATION  11 |
| LOBBYINGACTIVITIESIND | category | 2 | 0 | f 1.9K; t 92 |
| INDEPENDENTAUDITFINCLSTMTIND | category | 2 | 0 | f 1.3K; t 680 |
| CONSOLIDATEDAUDITFINCLSTMTIND | category | 2 | 0 | f 1.7K; t 254 |
| FORM990PROVIDEDTOGVRNBODYIND | category | 2 | 0 | t 1.6K; f 423 |
| CONFLICTOFINTERESTPOLICYIND | category | 2 | 0 | t 1.3K; f 642 |
| WHISTLEBLOWERPOLICYIND | category | 2 | 0 | f 1.1K; t 927 |
| DOCUMENTRETENTIONPOLICYIND | category | 2 | 0 | f 996; t 993 |
| BUSINESSNAME2 | who | 120 | 0 | nan 1.8K; INC 11; CENTER 5; FOUNDATION INC 5 |
| LICENSEDSTATESCD | category | 15 | 0 | nan 1.9K; CO 103; WY 3; WA 3 |
| ALLSTATESCD | category | 2 | 0 | nan 2.0K; All States 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:45:41.44601 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9b0ec5a0-2463-409a-ad47-b 2.0K |
| SRC_SHA256 | who | 1 | 0 | 6c693802065a902da4b2664be 2.0K |
