# FED_FHFA_SUSPENDED_COUNTERPARTIES

rows 241  columns 11  scan 2.8s

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
         3  Martinez
         3  Toro
         3  Brown
         2  Edrington
         2  Torgerson
         2  Dadyan
         2  Ayvazyan
         2  Masvidal
         2  Ober
         2  Hall
         2  Puretz
         2  Hernandez
         2  Ross
         2  Jones
         2  Deutsch
         2  Johnson
         1  Puccio Jr.
         1  Parker
         1  Tapia
         1  Michno

FIRST_NAME by rows
         7  Robert
         5  Michael
         3  David
         2  Anthony
         2  Edward
         2  James E.
         2  Jeffrey
         2  Andrew
         2  Paul
         2  Veronica
         2  Mark
         2  Aron
         2  Peter
         2  Jose
         1  Jose Bautista
         1  Erick A.
         1  Brandon J.
         1  Sung M.
         1  Tyler N.
         1  Dessalines F.

SRC_SHA256 by rows
       241  e2ab1b98bf5d6cada05873cdf111bc83fc4e6d187b0a67df5714de8459b309a3

## who x when

LAST_NAME by EFFECTIVE_DATE
  Ayvazyan                                  2024:2
  Brown                                     2016:1 2018:1 2023:1
  Dadyan                                    2022:1 2024:1
  Deutsch                                   2023:2
  Edrington                                 2026:2
  Hall                                      2019:2
  Hernandez                                 2020:1 2025:1
  Johnson                                   2017:1 2024:1
  Jones                                     2017:1 2019:1
  Martinez                                  2018:1 2025:1 2026:1
  Masvidal                                  2018:1 2019:1
  Michno                                    2022:1
  Ober                                      2017:2
  Parker                                    2019:1
  Puccio Jr.                                2022:1
  Puretz                                    2025:2
  Ross                                      2016:1 2024:1
  Tapia                                     2023:1
  Torgerson                                 2023:2
  Toro                                      2022:3

FIRST_NAME by EFFECTIVE_DATE
  Andrew                                    2019:1 2026:1
  Anthony                                   2022:1 2026:1
  Aron                                      2023:1 2025:1
  Brandon J.                                2026:1
  David                                     2017:1 2026:2
  Dessalines F.                             2024:1
  Edward                                    2015:1 2019:1
  Erick A.                                  2019:1
  James E.                                  2016:2
  Jeffrey                                   2017:2
  Jose                                      2017:1 2026:1
  Jose Bautista                             2019:1
  Mark                                      2022:1 2026:1
  Michael                                   2016:1 2018:2 2020:1 2023:1
  Paul                                      2017:1 2019:1
  Peter                                     2022:2
  Robert                                    2017:2 2018:1 2019:1 2023:3
  Sung M.                                   2019:1
  Tyler N.                                  2024:1
  Veronica                                  2022:2

## what

COMPANY: Silverstein & Wolf Corp. 8%, MVP Home Solutions LLC 8%, Bolden Pinnacle Group Corporat 8%, Results Home Buyers 2 LLC 8%, Apex Title Agency Incorporated 8%, Rhodium Capital Advisors LLC 8%, Apex Equity Group LLC 8%, Integra Affordable Management  8%, Free Calm and Growing 8%, Phoenix Consultants 8%, Preferred Home Solutions NM, L 8%, Complete Escrow Services LLC 8%

STATE: California 26%, Florida 16%, New York 11%, New Jersey 11%, Texas 6%, Illinois 6%, Ohio 5%, Virginia 4%, Pennsylvania 4%, Georgia 4%, Missouri 3%, North Carolina 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIRST_NAME | who | 190 | 31 | Robert 7; Michael 5; David 3; Andrew 2 |
| LAST_NAME | who | 191 | 31 | Martinez 3; Brown 3; Toro 3; Edrington 2 |
| COMPANY | category | 31 | 210 | Silverstein & Wolf Corp. 1; MVP Home Solutions LLC 1; Bolden Pinnacle Group Cor 1; Results Home Buyers 2 LLC 1 |
| CITY | other | 177 | 0 | Brooklyn 6; Miami 6; Encino 5; Newark 4 |
| STATE | category | 38 | 0 | California 46; Florida 28; New York 20; New Jersey 20 |
| EFFECTIVE_DATE | date | 76 | 0 | 2026-07-08 11; 2023-02-28 11; 2022-12-28 11; 2019-02-08 10 |
| SUSPENSION_END_DATE | date | 39 | 0 | indefinite 159; 2027-12-28 10; 2033-02-28 8; 2027-08-15 4 |
| ORDER_LINK | other | 243 | 0 | https://www.fhfa.gov/site 2; https://www.fhfa.gov/site 2; https://www.fhfa.gov/site 2; https://www.fhfa.gov/site 2 |
| INGESTED_AT | audit | 1 | 0 | 1786129703672998 241 |
| SOURCE_RUN_ID | audit | 1 | 0 | 14579d11-8d3d-4903-82a3-b 241 |
| SRC_SHA256 | who | 1 | 0 | e2ab1b98bf5d6cada05873cdf 241 |
