# FED_FHFA_SUSPENDED_COUNTERPARTY_PROGRAM

rows 241  columns 11  scan 3.2s

roles: audit 2, category 2, date 2, other 2, who 3

## when

EFFECTIVE_DATESORT_ASCENDING
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
         2  Dadyan
         2  Torgerson
         2  Ober
         2  Deutsch
         2  Johnson
         2  Hernandez
         2  Ross
         2  Ayvazyan
         2  Edrington
         2  Puretz
         2  Masvidal
         2  Hall
         2  Jones
         1  Schaller
         1  Simon
         1  Kelly
         1  Monheiser

FIRST_NAME by rows
         7  Robert
         5  Michael
         3  David
         2  Edward
         2  Aron
         2  Veronica
         2  Mark
         2  Jose
         2  Paul
         2  James E.
         2  Peter
         2  Anthony
         2  Jeffrey
         2  Andrew
         1  Jacob
         1  Desiree Elizabeth
         1  Jacques
         1  Hyeokji Alex
         1  Evelisse
         1  Erick A.

_SRC_SHA256 by rows
       241  8dcc570e9f13675e27f9286f33097d878c47d1aa2679bd4d87f61edb496afcef

## who x when

LAST_NAME by EFFECTIVE_DATESORT_ASCENDING
  Ayvazyan                                  2024:2
  Brown                                     2016:1 2018:1 2023:1
  Dadyan                                    2022:1 2024:1
  Deutsch                                   2023:2
  Edrington                                 2026:2
  Hall                                      2019:2
  Hernandez                                 2020:1 2025:1
  Johnson                                   2017:1 2024:1
  Jones                                     2017:1 2019:1
  Kelly                                     2017:1
  Martinez                                  2018:1 2025:1 2026:1
  Masvidal                                  2018:1 2019:1
  Monheiser                                 2017:1
  Ober                                      2017:2
  Puretz                                    2025:2
  Ross                                      2016:1 2024:1
  Schaller                                  2023:1
  Simon                                     2016:1
  Torgerson                                 2023:2
  Toro                                      2022:3

FIRST_NAME by EFFECTIVE_DATESORT_ASCENDING
  Andrew                                    2019:1 2026:1
  Anthony                                   2022:1 2026:1
  Aron                                      2023:1 2025:1
  David                                     2017:1 2026:2
  Desiree Elizabeth                         2016:1
  Edward                                    2015:1 2019:1
  Erick A.                                  2019:1
  Evelisse                                  2025:1
  Hyeokji Alex                              2017:1
  Jacob                                     2023:1
  Jacques                                   2017:1
  James E.                                  2016:2
  Jeffrey                                   2017:2
  Jose                                      2017:1 2026:1
  Mark                                      2022:1 2026:1
  Michael                                   2016:1 2018:2 2020:1 2023:1
  Paul                                      2017:1 2019:1
  Peter                                     2022:2
  Robert                                    2017:2 2018:1 2019:1 2023:3
  Veronica                                  2022:2

## what

COMPANY: Affiliated Funding Corporation 9%, Seckel Capital LLC 9%, Briser Abstract Co. 9%, At Home Settlements LLC 9%, Amir Properties & Development  9%, Bell Property & Management Inc 9%, Financial & Real Estate Networ 9%, Anchor Mortgage LLC 9%, Synergy Real Estate Holdings L 9%, 3rd Financial Service Corporat 9%, First Mortgage Company LLC 9%

STATE: California 26%, Florida 16%, New York 11%, New Jersey 11%, Texas 6%, Illinois 6%, Ohio 5%, Virginia 4%, Pennsylvania 4%, Georgia 4%, North Carolina 3%, Washington 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIRST_NAME | who | 191 | 31 | Robert 7; Michael 5; David 3; Edward 2 |
| LAST_NAME | who | 192 | 31 | Brown 3; Martinez 3; Toro 3; Ross 2 |
| COMPANY | category | 32 | 210 | Affiliated Funding Corpor 1; Seckel Capital LLC 1; Briser Abstract Co. 1; At Home Settlements LLC 1 |
| CITY | other | 177 | 0 | Miami 6; Brooklyn 6; Encino 5; Philadelphia 4 |
| STATE | category | 38 | 0 | California 46; Florida 28; New York 20; New Jersey 20 |
| EFFECTIVE_DATESORT_ASCENDING | date | 76 | 0 | 12/28/2022 11; 02/28/2023 11; 07/08/2026 11; 02/08/2019 10 |
| SUSPENSION_END_DATE | date | 39 | 0 | Indefinite 159; 12/28/2027 10; 02/28/2033 8; 06/07/2027 4 |
| SUSPENSION_ORDER | other | 241 | 0 | /sites/default/files/Fark 2; /sites/default/files/Hotc 2; /sites/default/files/Guzm 2; /sites/default/files/Wood 2 |
| _INGESTED_AT | audit | 1 | 0 | 1785965103735317 241 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 03c12806-ae24-4442-877c-3 241 |
| _SRC_SHA256 | who | 1 | 0 | 8dcc570e9f13675e27f9286f3 241 |
