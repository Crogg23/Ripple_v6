# FED_FHFA_SUSPENDED_COUNTERPARTY

rows 241  columns 11  scan 3.1s

roles: audit 2, category 2, date 2, other 2, who 3

## when

EFFECTIVE_DATE
  2013         1  #
  2015         3  ##
  2016        10  ########
  2017        23  #################
  2018        18  ##############
  2019        27  ####################
  2020         5  ####
  2021         6  ####
  2022        38  ############################
  2023        35  ##########################
  2024        21  ################
  2025        14  ##########
  2026        40  ##############################

SUSPENSION_END_DATE
  2026         5  ####
  2027        34  ##############################
  2028        14  ############
  2029        10  #########
  2030         4  ####
  2031         2  ##
  2032         3  ###
  2033        10  #########

## who

LAST_NAME by rows
         3  Brown
         3  Martinez
         3  Toro
         2  Ayvazyan
         2  Dadyan
         2  Torgerson
         2  Ober
         2  Johnson
         2  Hernandez
         2  Hall
         2  Masvidal
         2  Puretz
         2  Ross
         2  Deutsch
         2  Edrington
         2  Jones
         1  Behrman
         1  Kelske
         1  Whitehurst
         1  Kang

FIRST_NAME by rows
         7  Robert
         5  Michael
         3  David
         2  Paul
         2  Veronica
         2  Mark
         2  Andrew
         2  Jeffrey
         2  Peter
         2  Anthony
         2  James E.
         2  Jose
         2  Edward
         2  Aron
         1  Ana J.
         1  Karl H.
         1  Samer Nachaat
         1  Dionysius Romero
         1  Emmanuel
         1  Tyler N.

SRC_SHA256 by rows
       241  58a2a232782c9b0da69fd889447a7fd3531409ec19eb1f7bccb948ccaf7293f0

## who x when

LAST_NAME by EFFECTIVE_DATE
  Ayvazyan                                  2024:2
  Behrman                                   2020:1
  Brown                                     2016:1 2018:1 2023:1
  Dadyan                                    2022:1 2024:1
  Deutsch                                   2023:2
  Edrington                                 2026:2
  Hall                                      2019:2
  Hernandez                                 2020:1 2025:1
  Johnson                                   2017:1 2024:1
  Jones                                     2017:1 2019:1
  Kang                                      2019:1
  Kelske                                    2023:1
  Martinez                                  2018:1 2025:1 2026:1
  Masvidal                                  2018:1 2019:1
  Ober                                      2017:2
  Puretz                                    2025:2
  Ross                                      2016:1 2024:1
  Torgerson                                 2023:2
  Toro                                      2022:3
  Whitehurst                                2022:1

FIRST_NAME by EFFECTIVE_DATE
  Ana J.                                    2023:1
  Andrew                                    2019:1 2026:1
  Anthony                                   2022:1 2026:1
  Aron                                      2023:1 2025:1
  David                                     2017:1 2026:2
  Dionysius Romero                          2019:1
  Edward                                    2015:1 2019:1
  Emmanuel                                  2022:1
  James E.                                  2016:2
  Jeffrey                                   2017:2
  Jose                                      2017:1 2026:1
  Karl H.                                   2023:1
  Mark                                      2022:1 2026:1
  Michael                                   2016:1 2018:2 2020:1 2023:1
  Paul                                      2017:1 2019:1
  Peter                                     2022:2
  Robert                                    2017:2 2018:1 2019:1 2023:3
  Samer Nachaat                             2018:1
  Tyler N.                                  2024:1
  Veronica                                  2022:2

## what

COMPANY: Silverstein & Wolf Corp. 9%, MVP Home Solutions LLC 9%, Bolden Pinnacle Group Corporat 9%, Results Home Buyers 2 LLC 9%, Apex Title Agency Incorporated 9%, Rhodium Capital Advisors LLC 9%, Apex Equity Group LLC 9%, Integra Affordable Management  9%, Free Calm and Growing 9%, Phoenix Consultants 9%, Preferred Home Solutions NM, L 9%

STATE: California 26%, Florida 16%, New York 11%, New Jersey 11%, Texas 6%, Illinois 6%, Ohio 5%, Virginia 4%, Pennsylvania 4%, Georgia 4%, Missouri 3%, North Carolina 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIRST_NAME | who | 191 | 31 | Robert 7; Michael 5; David 3; Andrew 2 |
| LAST_NAME | who | 192 | 31 | Martinez 3; Brown 3; Toro 3; Edrington 2 |
| COMPANY | category | 32 | 210 | Silverstein & Wolf Corp. 1; MVP Home Solutions LLC 1; Bolden Pinnacle Group Cor 1; Results Home Buyers 2 LLC 1 |
| CITY | other | 177 | 0 | Brooklyn 6; Miami 6; Encino 5; Newark 4 |
| STATE | category | 38 | 0 | California 46; Florida 28; New York 20; New Jersey 20 |
| EFFECTIVE_DATE | date | 76 | 0 | 2026-07-08 11; 2023-02-28 11; 2022-12-28 11; 2019-02-08 10 |
| SUSPENSION_END_DATE | date | 39 | 0 | indefinite 159; 2027-12-28 10; 2033-02-28 8; 2027-08-15 4 |
| ORDER_LINK | other | 243 | 0 | https://www.fhfa.gov/site 2; https://www.fhfa.gov/site 2; https://www.fhfa.gov/site 2; https://www.fhfa.gov/site 2 |
| INGESTED_AT | audit | 1 | 0 | 1785965513353623 241 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6938fa87-b9d0-49bc-b978-e 241 |
| SRC_SHA256 | who | 1 | 0 | 58a2a232782c9b0da69fd8894 241 |
