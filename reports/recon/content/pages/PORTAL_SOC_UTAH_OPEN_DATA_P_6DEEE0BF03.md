# PORTAL_SOC_UTAH_OPEN_DATA_P_6DEEE0BF03

rows 2.0K  columns 99  scan 6.8s

roles: amount 5, audit 2, category 37, date 6, id 1, other 5, state 5, who 39

## when

RECEIVED_DATE
  2016         1  
  2017         7  
  2018         9  
  2019       367  #######
  2020      1.6K  ##############################

DECISION_DATE
  2019       370  #######
  2020      1.6K  ##############################

BEGIN_DATE
  2016         1  
  2017         4  
  2018        12  
  2019       204  ####
  2020      1.7K  ##############################
  2021        54  #

END_DATE
  2019         1  
  2020        18  
  2021        77  #
  2022       317  ######
  2023      1.6K  ##############################
  2024        41  #

ORIGINAL_CERT_DATE
  2016         1  #
  2017         7  ####
  2018         9  #####
  2019        15  #########
  2020        51  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| WAGE_RATE_OF_PAY_FROM | 2.0K | 11.61 | 89.0K | 240.0K | 976.7K | 186.89M |
| TOTAL_WORKER_POSITIONS | 2.0K | 1 | 1 | 2 | 30 | 2.2K |
| WAGE_RATE_OF_PAY_TO | 521 | 12 | 112.0K | 255.0K | 380.0K | 59.90M |
| PREVAILING_WAGE | 2.0K | 11.61 | 82.3K | 169.0K | 260.9K | 158.41M |
| TOTAL_WORKSITE_LOCATIONS | 2.0K | 1 | 1 | 4 | 10 | 2.4K |

## who

EMPLOYER_NAME by rows
       176  University of Utah
        68  Overstock.com, Inc.
        63  Ancestry.com Operations, Inc.
        53  CONNVERTEX TECHNOLOGIES INC
        53  ARUP Laboratories
        51  Micron Technology, Inc.
        49  Qualtrics, LLC
        44  Genesys Telecommunications Laboratories, Inc.
        39  Zions Bancorporation, N.A.
        36  Western Governors University
        32  Ally Bank
        30  Micron Technology Utah, LLC
        29  Davis School District
        28  Fatpipe Technologies, Inc.
        26  doTERRA International LLC
        24  IHC Health Services, Inc.
        22  Utah State University
        21  Lucid Software Inc.
        20  Accelerated Engineering
        19  BRIGHAM YOUNG UNIVERSITY

EMPLOYER_NAME by dollars
      15.44M      176 rows  University of Utah
       8.85M       49 rows  Qualtrics, LLC
       7.81M       63 rows  Ancestry.com Operations, Inc.
       7.63M       68 rows  Overstock.com, Inc.
       6.27M       51 rows  Micron Technology, Inc.
       4.81M       44 rows  Genesys Telecommunications Laboratories, Inc.
       4.46M       53 rows  CONNVERTEX TECHNOLOGIES INC
       4.13M       39 rows  Zions Bancorporation, N.A.
       4.02M       32 rows  Ally Bank
       3.90M       36 rows  Western Governors University
       2.99M       30 rows  Micron Technology Utah, LLC
       2.83M       26 rows  doTERRA International LLC
       2.53M       28 rows  Fatpipe Technologies, Inc.
       2.46M       24 rows  IHC Health Services, Inc.
       2.31M       16 rows  Galileo Financial Technologies, Inc.
       2.11M       14 rows  Confluent, Inc.
       1.96M       21 rows  Lucid Software Inc.
       1.87M       13 rows  Finicity Corporation
       1.85M        8 rows  Route App, Inc.
       1.68M       20 rows  Accelerated Engineering

EMPLOYER_POC_LAST_NAME by rows
       134  CARREAU
        85  Burt
        65  Jensen
        57  FLAVELL
        53  KHIRAPATE
        53  BRUCE
        52  Stoddard
        51  Rotter
        43  Allred
        36  Barraco
        34  Hansen
        32  Bazzy
        31  Datta
        30  BALLANTYNE
        30  Ringger
        29  Robbins
        29  Brooks
        23  MORRIS
        20  Dunn
        20  Kalaramadam

EMPLOYER_POC_LAST_NAME by dollars
      11.43M      134 rows  CARREAU
       9.80M       85 rows  Burt
       9.24M       51 rows  Rotter
       7.91M       65 rows  Jensen
       6.18M       57 rows  FLAVELL
       5.72M       52 rows  Stoddard
       4.54M       43 rows  Allred
       4.46M       53 rows  KHIRAPATE
       4.01M       32 rows  Bazzy
       3.90M       29 rows  Brooks
       3.90M       36 rows  Barraco
       3.34M       30 rows  Ringger
       3.33M       34 rows  Hansen
       2.77M       23 rows  MORRIS
       2.68M       30 rows  BALLANTYNE
       2.58M       31 rows  Datta
       2.11M       14 rows  LeBaron
       2.04M       10 rows  Butler
       1.87M       13 rows  Hutchins
       1.84M       20 rows  Dunn

EMPLOYER_POC_FIRST_NAME by rows
       147  Katie
        85  Nate
        63  Jana
        58  STEVEN
        57  Stephen
        53  ROHIT
        53  Amanda
        52  Erin
        44  Patricia
        42  Michele
        41  Mary
        37  Johanna
        32  Tarik
        32  Bryan
        32  Mark
        31  Sanchaita
        29  Traci
        23  WHITNEY
        20  Jeff
        20  Thomas

EMPLOYER_POC_FIRST_NAME by dollars
      12.69M      147 rows  Katie
       9.80M       85 rows  Nate
       9.47M       52 rows  Erin
       7.81M       63 rows  Jana
       6.30M       58 rows  STEVEN
       5.44M       57 rows  Stephen
       4.81M       44 rows  Patricia
       4.46M       53 rows  ROHIT
       4.08M       37 rows  Johanna
       4.06M       32 rows  Bryan
       4.01M       32 rows  Tarik
       3.56M       41 rows  Mary
       3.47M       32 rows  Mark
       3.39M       42 rows  Michele
       2.77M       23 rows  WHITNEY
       2.58M       31 rows  Sanchaita
       2.56M       20 rows  Thomas
       2.51M       20 rows  Jeff
       1.89M        8 rows  Amy
       1.78M       19 rows  Leah

AGENT_ATTORNEY_LAST_NAME by rows
       114  Wheelwright
        85  Davis
        79  Tsai
        69  Young
        65  Wood
        65  Paldino
        63  Bacayan
        56  Olson
        53  CARREAU
        52  Buhler Thomas
        47  Mahmud
        44  Horne
        43  Francis
        37  Graham
        34  Murphy
        25  BUHLER-THOMAS
        25  Gardner
        24  Heckler
        23  TSAI
        20  Kilborn

AGENT_ATTORNEY_LAST_NAME by dollars
       9.80M       85 rows  Davis
       9.56M      114 rows  Wheelwright
       8.37M       79 rows  Tsai
       8.12M       47 rows  Mahmud
       7.81M       63 rows  Bacayan
       7.35M       65 rows  Paldino
       7.27M       69 rows  Young
       5.95M       65 rows  Wood
       4.81M       44 rows  Horne
       4.54M       52 rows  Buhler Thomas
       4.24M       34 rows  Murphy
       4.21M       43 rows  Francis
       3.73M       37 rows  Graham
       3.59M       56 rows  Olson
       2.53M       23 rows  TSAI
       2.13M       25 rows  Gardner
       2.11M       14 rows  Beckerson
       1.96M       25 rows  BUHLER-THOMAS
       1.84M       20 rows  Kilborn
       1.82M       17 rows  Singh

## who x when

EMPLOYER_NAME by DECISION_DATE, dollars = WAGE_RATE_OF_PAY_FROM
  ARUP Laboratories                         2019:153.2K 2020:674.85
  Accelerated Engineering                   2019:1.50M 2020:178.5K
  Ally Bank                                 2019:1.41M 2020:2.62M
  Ancestry.com Operations, Inc.             2019:1.30M 2020:6.51M
  BRIGHAM YOUNG UNIVERSITY                  2019:42.4K 2020:1.58M
  CONNVERTEX TECHNOLOGIES INC               2019:415.3K 2020:4.04M
  Confluent, Inc.                           2020:2.11M
  Davis School District                     2020:1.48M
  Fatpipe Technologies, Inc.                2019:370.0K 2020:2.16M
  Finicity Corporation                      2020:1.87M
  Galileo Financial Technologies, Inc.      2019:1.13M 2020:1.17M
  Genesys Telecommunications Laboratories,  2019:107.0K 2020:4.70M
  IHC Health Services, Inc.                 2019:299.4K 2020:2.16M
  Lucid Software Inc.                       2020:1.96M
  Micron Technology Utah, LLC               2020:2.99M
  Micron Technology, Inc.                   2020:6.27M
  Overstock.com, Inc.                       2019:1.50M 2020:6.13M
  Qualtrics, LLC                            2019:1.34M 2020:7.51M
  Route App, Inc.                           2019:105.0K 2020:1.74M
  University of Utah                        2019:2.71M 2020:12.73M
  Utah State University                     2019:247.0K 2020:1.31M
  Western Governors University              2019:682.5K 2020:3.22M
  Zions Bancorporation, N.A.                2019:1.57M 2020:2.56M
  doTERRA International LLC                 2019:375.5K 2020:2.46M

EMPLOYER_POC_LAST_NAME by DECISION_DATE, dollars = WAGE_RATE_OF_PAY_FROM
  Allred                                    2019:1.98M 2020:2.56M
  BALLANTYNE                                2019:756.4K 2020:1.92M
  BRUCE                                     2019:153.2K 2020:674.85
  Barraco                                   2019:682.5K 2020:3.22M
  Bazzy                                     2019:1.40M 2020:2.62M
  Brooks                                    2019:1.13M 2020:2.77M
  Burt                                      2020:9.80M
  Butler                                    2020:2.04M
  CARREAU                                   2019:1.11M 2020:10.32M
  Datta                                     2019:370.0K 2020:2.21M
  Dunn                                      2020:1.84M
  FLAVELL                                   2019:2.43M 2020:3.76M
  Hansen                                    2019:663.8K 2020:2.66M
  Hutchins                                  2020:1.87M
  Jensen                                    2019:1.30M 2020:6.60M
  KHIRAPATE                                 2019:415.3K 2020:4.04M
  Kalaramadam                               2019:1.50M 2020:178.5K
  LeBaron                                   2020:2.11M
  MORRIS                                    2020:2.77M
  Ringger                                   2019:375.5K 2020:2.96M
  Robbins                                   2020:1.48M
  Rotter                                    2019:1.96M 2020:7.28M
  Stoddard                                  2019:190.9K 2020:5.53M

## where

EMPLOYER_STATE: UT 1.9K, ID 55, CA 17, GA 6, TX 2, CO 1, MI 1, MN 1, NC 1

EMPLOYER_POC_STATE: UT 1.9K, MI 40, CA 9, MA 3, PA 3, TX 2, MN 2, WA 2, GA 1, VT 1, NC 1

AGENT_ATTORNEY_STATE: UT 613, CA 266, TX 161, NY 149, IL 140, CO 128, NJ 27, GA 23, MA 15, WA 12, MD 11

STATE_OF_HIGHEST_COURT: UT 609, NY 257, CO 156, CA 148, TX 142, AZ 67, IL 33, GA 32, NJ 28, MA 21, WI 18

WORKSITE_STATE: UT 1.5K, CA 137, NC 60, WA 56, TX 44, ID 36, AZ 18, VA 14, IN 14, MA 13, IL 12, MI 12

## what

CASE_STATUS: Certified 90%, Certified - Withdrawn 4%, Withdrawn 4%, Denied 2%

VISA_CLASS: H-1B 95%, E-3 Australian 4%, H-1B1 Chile 1%

FULL_TIME_POSITION: True 98%, False 2%

NEW_EMPLOYMENT: 0 60%, 1 39%, 10 0%, 5 0%, 2 0%, 8 0%, 15 0%, 6 0%

CONTINUED_EMPLOYMENT: 0 76%, 1 24%, 10 0%

CHANGE_PREVIOUS_EMPLOYMENT: 0 94%, 1 6%

NEW_CONCURRENT_EMPLOYMENT: 0 100%, 1 0%

CHANGE_EMPLOYER: 0 81%, 1 19%, 2 0%, 10 0%

AMENDED_PETITION: 0 89%, 1 11%, 5 0%

EMPLOYER_COUNTRY: UNITED STATES OF AMERICA 100%, CANADA 0%

EMPLOYER_POC_COUNTRY: UNITED STATES OF AMERICA 99%, CANADA 0%, AUSTRALIA 0%

AGENT_REPRESENTING_EMPLOYER: True 80%, False 20%

AGENT_ATTORNEY_COUNTRY: UNITED STATES OF AMERICA 100%, CANADA 0%

WORKSITE_WORKERS: 1 99%, 10 0%, 5 0%, 2 0%, 8 0%, 15 0%, 30 0%, 6 0%

SECONDARY_ENTITY: False 91%, True 9%

WAGE_UNIT_OF_PAY: Year 92%, Hour 8%, Month 0%

PW_UNIT_OF_PAY: Year 93%, Hour 7%, Month 0%

PW_WAGE_LEVEL: II 44%, IV 21%, III 19%, I 16%, N/A 0%

PW_OES_YEAR: 7/1/2019 - 6/30/2020 81%, 7/1/2020 - 6/30/2021 18%, 2019 1%, 2020 0%, 2018 0%

H_1B_DEPENDENT: N 87%, Y 8%, N/A 5%

WILLFUL_VIOLATOR: N 95%, N/A 5%

SUPPORT_H1B: N/A 91%, Y 8%, NA 1%, N 0%

APPENDIX_A_ATTACHED: N/A 100%

PUBLIC_DISCLOSURE: Disclose Business 93%, Disclose Business and Employme 4%, Disclose Employment 3%, N/A 0%

AGENT_ATTORNEY_PHONE_EXT: 0 68%, 27 14%, 7375 8%, 105 2%, 55 1%, 102 1%, 108 1%, 6938 1%, 227 1%, 5148 1%, 104 1%

PREPARER_MIDDLE_INITIAL: M 22%, H 21%, A 17%, C 9%, G 8%, N/A 7%, F. 6%, R 3%, L 2%, J 2%, X 2%

AGENT_ATTORNEY_PROVINCE: California 35%, NY 34%, CA 20%, N/A 8%, NJ 1%, Colorado 1%, NEW YORK 1%, ONTARIO 1%, TEXAS 1%

EMPLOYER_PHONE_EXT: 0 44%, 3005 31%, 103 17%, 5183 5%, 180 1%, 143 1%, 1126 1%, 5157 1%, 4000 1%, 1338 1%, 1001 1%

EMPLOYER_POC_PHONE_EXT: 3005 51%, 103 28%, 5183 8%, 4456 3%, 108 3%, 701 2%, 151 2%, 180 1%, 143 1%, 118 1%, 1128 1%

EMPLOYER_PROVINCE: UTAH 55%, N/A 34%, NA 4%, CA 4%, UT 2%, argentina 2%

PW_OTHER_SOURCE: CBA 59%, Survey 22%, OES 19%

PW_OTHER_YEAR: 2019 81%, 2020 18%, 2017 1%

PW_TRACKING_NUMBER: P-200-20077-413202 67%, P-100-19054-154992 33%

EMPLOYER_POC_PROVINCE: N/A 48%, Alberta 15%, British Columbia 7%, Queensland 7%, Quebec 7%, QUEBEC 7%, UT 4%, jfksl 4%

PW_SURVEY_PUBLISHER: Radford Global Technology Surv 28%, Radford 20%, RADFORD 12%, Willis Towers Watson Data Serv 12%, Foreign Labor Certificate Data 4%, Payscale Human Capital 4%, Foreign Labor Certification Da 4%, OFLC ONLINE DATA CENTER 4%, D.DIETRICH ASSOCIATES, INC. 4%, Willis Towers Watson 4%, Willis Towers Watson Data Serv 4%

PW_SURVEY_NAME: OFLC ONLINE DATA CENTER 22%, Radford Global Technology Surv 17%, RADFORD GLOBAL TECHNOLOGY SURV 13%, Radford Global Technology Surv 9%, General Industry Professional  9%, 5183 - Software QA Engineer 9%, FLC Wage Results 4%, Payscale Human Capital 4%, All Industries Database - 7-20 4%, DIETRICH SPRING 2019 ENGINEERI 4%, General Industry Middle Manage 4%

STATUTORY_BASIS: WAGE 65%, BOTH 35%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| JOB_TITLE | who | 1.0K | 0 | Software Engineer 95; Software Developer 73; Assistant Professor 46; SOFTWARE DEVELOPER 44 |
| WAGE_RATE_OF_PAY_FROM | amount | 847 | 0 | 83928.00 51; 110000.00 44; 120000.00 36; 100000.00 34 |
| EMPLOYER_NAME | who | 483 | 0 | University of Utah 176; Overstock.com, Inc. 68; Ancestry.com Operations,  63; ARUP Laboratories 55 |
| TRADE_NAME_DBA | who | 116 | 1.6K | University of Utah 100; Ancestry 63; ARUP Laboratories 53; Genesys 24 |
| CASE_NUMBER | id | 2.0K | 0 | I-203-20008-240752 11; I-203-20117-518722 11; I-203-19289-090859 11; I-203-20052-342472 11 |
| CASE_STATUS | category | 4 | 0 | Certified 1.8K; Certified - Withdrawn 83; Withdrawn 74; Denied 38 |
| RECEIVED_DATE | date | 296 | 0 | 2020-05-15T00:00:00.000 41; 2020-03-04T00:00:00.000 29; 2020-06-04T00:00:00.000 27; 2020-02-21T00:00:00.000 26 |
| DECISION_DATE | date | 252 | 0 | 2020-05-22T00:00:00.000 36; 2020-02-28T00:00:00.000 29; 2020-03-11T00:00:00.000 29; 2020-06-11T00:00:00.000 26 |
| VISA_CLASS | category | 3 | 0 | H-1B 1.9K; E-3 Australian 80; H-1B1 Chile 23 |
| SOC_CODE | other | 189 | 0 | 15-1132.00 589; 25-2021.00 90; 15-1133.00 78; 11-3021.00 59 |
| SOC_TITLE | who | 191 | 0 | Software Developers, Appl 603; Elementary School Teacher 90; Software Developers, Syst 79; Computer and Information  59 |
| FULL_TIME_POSITION | category | 2 | 0 | True 2.0K; False 38 |
| BEGIN_DATE | date | 379 | 0 | 2020-10-01T00:00:00.000 237; 2020-07-01T00:00:00.000 90; 2020-08-01T00:00:00.000 53; 2020-08-20T00:00:00.000 28 |
| END_DATE | date | 503 | 0 | 2023-09-30T00:00:00.000 205; 2023-06-30T00:00:00.000 84; 2023-07-31T00:00:00.000 38; 2023-08-20T00:00:00.000 25 |
| TOTAL_WORKER_POSITIONS | amount | 8 | 0 | 1 2.0K; 10 9; 5 5; 2 3 |
| NEW_EMPLOYMENT | category | 8 | 0 | 0 1.2K; 1 780; 10 9; 5 6 |
| CONTINUED_EMPLOYMENT | category | 3 | 0 | 0 1.5K; 1 486; 10 1 |
| CHANGE_PREVIOUS_EMPLOYMENT | category | 2 | 0 | 0 1.9K; 1 123 |
| NEW_CONCURRENT_EMPLOYMENT | category | 2 | 0 | 0 2.0K; 1 10 |
| CHANGE_EMPLOYER | category | 4 | 0 | 0 1.6K; 1 387; 2 1; 10 1 |
| AMENDED_PETITION | category | 3 | 0 | 0 1.8K; 1 223; 5 1 |
| EMPLOYER_ADDRESS1 | who | 479 | 0 | 201 S Presidents Circle 167; 799 West Coliseum Way 73; 1300 West Traverse Parkwa 63; 500 Chipeta Way 55 |
| EMPLOYER_CITY | who | 89 | 0 | Salt Lake City 648; Lehi 173; Midvale 119; Provo 109 |
| EMPLOYER_STATE | state | 9 | 0 | UT 1.9K; ID 55; CA 17; GA 6 |
| EMPLOYER_POSTAL_CODE | who | 103 | 0 | 84043 193; 84112 179; 84047 170; 84095 149 |
| EMPLOYER_COUNTRY | category | 2 | 0 | UNITED STATES OF AMERICA 2.0K; CANADA 1 |
| EMPLOYER_PHONE | who | 462 | 0 | +18015857002 179; +18017057000 63; +18015832787 55; +12083684000 55 |
| NAICS_CODE | other | 213 | 0 | 611310 303; 541511 291; 611110 96; 522110 78 |
| EMPLOYER_POC_LAST_NAME | who | 441 | 0 | CARREAU 134; Burt 85; Jensen 65; FLAVELL 57 |
| EMPLOYER_POC_FIRST_NAME | who | 388 | 0 | Katie 147; Nate 85; Jana 63; STEVEN 58 |
| EMPLOYER_POC_MIDDLE_NAME | who | 85 | 1.4K | A 149; N/A 63; M 55; Felice 36 |
| EMPLOYER_POC_JOB_TITLE | who | 352 | 0 | Associate General Counsel 191; President 92; Coordinator, Immigration  85; Senior Recruiting Special 63 |
| EMPLOYER_POC_ADDRESS1 | who | 500 | 0 | 201 S Presidents Circle 167; 4000 North Flash Drive 85; 799 WEST COLISEUM WAY 79; 1300 West Traverse Parkwa 63 |
| EMPLOYER_POC_CITY | who | 100 | 0 | Salt Lake City 627; Lehi 228; Provo 109; Sandy 82 |
| EMPLOYER_POC_STATE | state | 13 | 10 | UT 1.9K; MI 40; CA 9; MA 3 |
| EMPLOYER_POC_POSTAL_CODE | who | 105 | 0 | 84043 249; 84112 179; 84095 149; 84604 103 |
| EMPLOYER_POC_COUNTRY | category | 3 | 0 | UNITED STATES OF AMERICA 2.0K; CANADA 10; AUSTRALIA 2 |
| EMPLOYER_POC_PHONE | who | 470 | 0 | 18015857002 179; 18017673523 86; 18017057956 63; 18015832787 55 |
| EMPLOYER_POC_EMAIL | who | 499 | 0 | katie.carreau@legal.utah. 148; nburt@micron.com 86; jjensen@ancestry.com 63; SFLAVELL@OVERSTOCK.COM 59 |
| AGENT_REPRESENTING_EMPLOYER | category | 2 | 0 | True 1.6K; False 399 |
| AGENT_ATTORNEY_LAST_NAME | who | 218 | 399 | Wheelwright 114; Davis 85; Tsai 79; Young 69 |
| AGENT_ATTORNEY_FIRST_NAME | who | 202 | 399 | Timothy 116; Lucrecia 85; Roger 79; Elaine 69 |
| AGENT_ATTORNEY_MIDDLE_NAME | who | 103 | 1.1K | M. 138; A 65; Joseph 65; Radler 56 |
| AGENT_ATTORNEY_ADDRESS1 | who | 279 | 399 | 111 South Main Street 114; 555 17th Street 79; 1400 Broadway 65; 551 East South Temple 64 |
| AGENT_ATTORNEY_CITY | who | 109 | 399 | Salt Lake City 403; San Francisco 132; Chicago 124; New York 109 |
| AGENT_ATTORNEY_STATE | state | 27 | 400 | UT 613; CA 266; TX 161; NY 149 |
| AGENT_ATTORNEY_POSTAL_CODE | other | 141 | 399 | 84111 204; 80202 107; 60606 100; 84604 88 |
| AGENT_ATTORNEY_COUNTRY | category | 3 | 399 | UNITED STATES OF AMERICA 1.6K; CANADA 1 |
| AGENT_ATTORNEY_PHONE | who | 189 | 399 | 18012971290 113; 13032958171 102; 13127226300 99; 18016910604 90 |
| AGENT_ATTORNEY_EMAIL_ADDRESS | who | 237 | 399 | twheelwright@djplaw.com 114; gov@giafirm.com 87; immigrationden@hollandhar 79; eyoung@kmclaw.com 69 |
| LAWFIRM_NAME_BUSINESS_NAME | who | 201 | 399 | Durham Jones and Pinegar 108; Berry Appleman & Leiden L 98; Global Immigration Associ 90; Fragomen, Del Rey, Bernse 75 |
| STATE_OF_HIGHEST_COURT | state | 29 | 399 | UT 609; NY 257; CO 156; CA 148 |
| NAME_OF_HIGHEST_STATE_COURT | who | 93 | 399 | Supreme Court 376; Utah Supreme Court 136; Supreme Court of Texas 123; U.S. Supreme Court 114 |
| WORKSITE_WORKERS | category | 9 | 43 | 1 2.0K; 10 9; 5 5; 2 3 |
| SECONDARY_ENTITY | category | 3 | 16 | False 1.8K; True 173 |
| WORKSITE_ADDRESS1 | who | 908 | 0 | 500 Chipeta Way 57; 799 West Coliseum Way 41; 505 1st Avenue South 41; 799 WEST COLISEUM WAY 39 |
| WORKSITE_CITY | who | 240 | 0 | Salt Lake City 545; Lehi 132; South Jordan 66; MIDVALE 66 |
| WORKSITE_COUNTY | who | 119 | 10 | SALT LAKE 967; UTAH 327; DAVIS 61; KING 53 |
| WORKSITE_STATE | state | 32 | 0 | UT 1.5K; CA 137; NC 60; WA 56 |
| WORKSITE_POSTAL_CODE | other | 303 | 0 | 84043 157; 84112 113; 84047 90; 84108 88 |
| WAGE_RATE_OF_PAY_TO | amount | 210 | 1.5K | 140000.00 29; 83929.00 25; 150000.00 16; 130000.00 14 |
| WAGE_UNIT_OF_PAY | category | 3 | 0 | Year 1.9K; Hour 153; Month 4 |
| PREVAILING_WAGE | amount | 830 | 16 | 83928.00 116; 119434.00 49; 101691.00 47; 18.82 33 |
| PW_UNIT_OF_PAY | category | 4 | 16 | Year 1.9K; Hour 145; Month 2 |
| PW_WAGE_LEVEL | category | 6 | 137 | II 821; IV 402; III 360; I 297 |
| PW_OES_YEAR | category | 6 | 137 | 7/1/2019 - 6/30/2020 1.5K; 7/1/2020 - 6/30/2021 339; 2019 19; 2020 7 |
| TOTAL_WORKSITE_LOCATIONS | amount | 10 | 43 | 1 1.7K; 2 250; 10 9; 8 5 |
| AGREE_TO_LC_STATEMENT | other | 1 | 0 | True 2.0K |
| H_1B_DEPENDENT | category | 4 | 3 | N 1.8K; Y 155; N/A 99 |
| WILLFUL_VIOLATOR | category | 3 | 3 | N 1.9K; N/A 99 |
| SUPPORT_H1B | category | 5 | 25 | N/A 1.8K; Y 154; NA 15; N 1 |
| APPENDIX_A_ATTACHED | category | 2 | 43 | N/A 2.0K |
| PUBLIC_DISCLOSURE | category | 4 | 0 | Disclose Business 1.9K; Disclose Business and Emp 78; Disclose Employment 61; N/A 1 |
| PREPARER_LAST_NAME | who | 185 | 1.2K | CARREAU 53; Buhler Thomas 53; HOOD 51; Graham 37 |
| PREPARER_FIRST_NAME | who | 152 | 1.2K | Kim 68; Katie 54; JENNIFER 49; Chad 37 |
| PREPARER_BUSINESS_NAME | who | 140 | 1.2K | Berry Appleman & Leiden L 63; FRAGOMEN, DEL REY, BERNSE 58; Buhler Thomas Law, PC 51; Fragomen, Del Rey, Bernse 44 |
| PREPARER_EMAIL | who | 181 | 1.2K | kim@buhlerthomaslaw.com 66; katie.carreau@legal.utah. 53; cgraham@grahamadair.com 37; ccharles@balglobal.com 30 |
| EMPLOYER_ADDRESS2 | who | 142 | 1.1K | 309 Park Building 175; Suite 600 69; Suite 300 61; SUITE 340 48 |
| EMPLOYER_POC_ADDRESS2 | who | 136 | 1.1K | 309 Park Building 176; Suite 300 56; 500 Chipeta Way 52; SUITE 340 48 |
| AGENT_ATTORNEY_ADDRESS2 | who | 138 | 746 | Suite 200 102; Ste. 2400 90; Suite 3200 88; Suite 2800 88 |
| AGENT_ATTORNEY_PHONE_EXT | category | 15 | 1.9K | 0 66; 27 14; 7375 8; 105 2 |
| WORKSITE_ADDRESS2 | who | 315 | 1.2K | Suite 700 78; Suite 300 48; Suite 200 31; Suite 150 30 |
| PREPARER_MIDDLE_INITIAL | category | 37 | 1.5K | M 91; H 88; A 71; C 37 |
| AGENT_ATTORNEY_PROVINCE | category | 10 | 1.8K | California 68; NY 65; CA 38; N/A 16 |
| EMPLOYER_PHONE_EXT | category | 17 | 1.8K | 0 76; 3005 53; 103 29; 5183 8 |
| EMPLOYER_POC_PHONE_EXT | category | 24 | 1.9K | 3005 53; 103 29; 5183 8; 4456 3 |
| EMPLOYER_PROVINCE | category | 7 | 2.0K | UTAH 31; N/A 19; NA 2; CA 2 |
| SECONDARY_ENTITY_BUSINESS | who | 107 | 1.8K | NC Department of Health a 20; American Express 7; Fidelity Investments 6; Fatpipe, Inc. 5 |
| PW_OTHER_SOURCE | category | 4 | 1.9K | CBA 86; Survey 32; OES 27 |
| PW_OTHER_YEAR | category | 4 | 1.9K | 2019 96; 2020 21; 2017 1 |
| ORIGINAL_CERT_DATE | date | 65 | 1.9K | 2020-01-24T00:00:00.000 10; 2020-04-03T00:00:00.000 3; 2019-11-06T00:00:00.000 3; 2020-05-15T00:00:00.000 2 |
| PW_TRACKING_NUMBER | category | 3 | 2.0K | P-200-20077-413202 2; P-100-19054-154992 1 |
| EMPLOYER_POC_PROVINCE | category | 9 | 2.0K | N/A 13; Alberta 4; British Columbia 2; Queensland 2 |
| PW_SURVEY_PUBLISHER | category | 19 | 2.0K | Radford Global Technology 7; Radford 5; RADFORD 3; Willis Towers Watson Data 3 |
| PW_SURVEY_NAME | category | 25 | 2.0K | OFLC ONLINE DATA CENTER 5; Radford Global Technology 4; RADFORD GLOBAL TECHNOLOGY 3; Radford Global Technology 2 |
| STATUTORY_BASIS | category | 3 | 1.9K | WAGE 100; BOTH 54 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:49:10.48835 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3698ee08-4159-49e5-806c-3 2.0K |
| SRC_SHA256 | who | 1 | 0 | 2cb02e75d8bb3bc8f3a352b8f 2.0K |
