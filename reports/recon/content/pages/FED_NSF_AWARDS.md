# FED_NSF_AWARDS

rows 125  columns 23  scan 3.5s

roles: amount 1, audit 2, category 2, date 3, empty 3, other 8, state 1, who 3

## when

AWARD_DATE
  2026       125  ##############################

START_DATE
  2026       111  ##############################
  2027        14  ####

END_DATE
  2027        11  #####
  2028         7  ###
  2029        65  ##############################
  2030        25  ############
  2031        17  ########

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AWARD_AMOUNT | 125 | 12.0K | 455.9K | 2.26M | 20.00M | 76.68M |

## who

PI_NAME by rows
         2  Vasileios Kemerlis
         2  Sujatha Krishnaswamy
         2  Melanie Williamson
         2  Logan Perry
         2  Hao Yan
         2  Gen Li
         2  James Davis
         2  Huanrui Yang
         2  Wenyao Xu
         2  Dana Reinemann
         1  Jiaxin Huang
         1  Rachel Street
         1  Xiaolong Guo
         1  Andres Contreras Hip
         1  Ali Shojaie
         1  Michael Gubanov
         1  Yuchen Liu
         1  Anna Bergstrom
         1  Dustin Richmond
         1  Takashi Kozai

PI_NAME by dollars
      20.00M        1 rows  Dustin Rubenstein
       2.54M        1 rows  Katarzyna Keahey
       1.50M        2 rows  Hao Yan
       1.37M        2 rows  Gen Li
       1.35M        1 rows  Rachel Street
       1.26M        1 rows  Shashank Shekhar
     1000.0K        1 rows  Brooke Whitworth
      998.8K        2 rows  Sujatha Krishnaswamy
      997.3K        2 rows  Huanrui Yang
      973.1K        1 rows  Erotokritos Katsavounidis
      932.9K        1 rows  Trina Roberts
      929.8K        2 rows  Dana Reinemann
      927.4K        2 rows  Logan Perry
      900.0K        2 rows  Wenyao Xu
      900.0K        1 rows  Charles Cao
      900.0K        1 rows  Aaminah Norris
      899.9K        1 rows  Xiaolong Guo
      888.0K        1 rows  Anna Bergstrom
      838.4K        1 rows  Seth Newsome
      822.5K        1 rows  Robert Dunn

AWARDEE_NAME by rows
         3  University of Nebraska-Lincoln
         3  Maricopa County Community College District
         3  University of Oklahoma Norman Campus
         2  Arizona State University
         2  Brown University
         2  University of Colorado at Boulder
         2  Columbia University
         2  University of Iowa
         2  Purdue University
         2  North Carolina State University
         2  University of New Mexico
         2  University of Texas at Austin
         2  University of Mississippi
         2  University of Arizona
         2  University of Missouri-Columbia
         2  Florida State University
         2  Johns Hopkins University
         2  University of Wisconsin-Madison
         2  SUNY at Buffalo
         2  University of California-Santa Cruz

AWARDEE_NAME by dollars
      20.41M        2 rows  Columbia University
       2.54M        1 rows  University of Chicago
       1.50M        2 rows  Arizona State University
       1.39M        2 rows  University of New Mexico
       1.37M        2 rows  University of California-Santa Barbara
       1.35M        1 rows  Las Cumbres Observatory Global Telescope Network
       1.26M        3 rows  University of Nebraska-Lincoln
       1.26M        1 rows  Emory University
       1.24M        2 rows  University of California-Santa Cruz
       1.20M        3 rows  Maricopa County Community College District
       1.16M        2 rows  University of Wisconsin-Madison
       1.15M        3 rows  University of Oklahoma Norman Campus
       1.09M        2 rows  University of Texas at Austin
     1000.0K        1 rows  University of South Carolina at Columbia
      997.3K        2 rows  University of Arizona
      973.1K        1 rows  Massachusetts Institute of Technology
      932.9K        1 rows  Los Angeles County Museum of Natural History Foundation
      929.8K        2 rows  University of Mississippi
      906.7K        2 rows  University of Iowa
      900.0K        1 rows  University of Tennessee Knoxville

_SRC_SHA256 by rows
       125  9b1900c6ca83df35571da3942fbadac5235acee7095f7904c022bfaf2c211e01

_SRC_SHA256 by dollars
      76.68M      125 rows  9b1900c6ca83df35571da3942fbadac5235acee7095f7904c022bfaf2c21

## who x when

PI_NAME by AWARD_DATE, dollars = AWARD_AMOUNT
  Aaminah Norris                            2026:900.0K
  Ali Shojaie                               2026:249.7K
  Andres Contreras Hip                      2026:190.0K
  Anna Bergstrom                            2026:888.0K
  Brooke Whitworth                          2026:1000.0K
  Charles Cao                               2026:900.0K
  Dana Reinemann                            2026:929.8K
  Dustin Richmond                           2026:743.1K
  Dustin Rubenstein                         2026:20.00M
  Erotokritos Katsavounidis                 2026:973.1K
  Gen Li                                    2026:1.37M
  Hao Yan                                   2026:1.50M
  Huanrui Yang                              2026:997.3K
  James Davis                               2026:820.0K
  Jiaxin Huang                              2026:596.5K
  Katarzyna Keahey                          2026:2.54M
  Logan Perry                               2026:927.4K
  Melanie Williamson                        2026:107.6K
  Michael Gubanov                           2026:430.8K
  Rachel Street                             2026:1.35M
  Robert Dunn                               2026:822.5K
  Seth Newsome                              2026:838.4K
  Shashank Shekhar                          2026:1.26M
  Sujatha Krishnaswamy                      2026:998.8K
  Takashi Kozai                             2026:20.0K
  Trina Roberts                             2026:932.9K
  Vasileios Kemerlis                        2026:800.0K
  Wenyao Xu                                 2026:900.0K
  Xiaolong Guo                              2026:899.9K
  Yuchen Liu                                2026:95.0K

AWARDEE_NAME by AWARD_DATE, dollars = AWARD_AMOUNT
  Arizona State University                  2026:1.50M
  Brown University                          2026:800.0K
  Columbia University                       2026:20.41M
  Emory University                          2026:1.26M
  Florida State University                  2026:802.6K
  Johns Hopkins University                  2026:728.8K
  Las Cumbres Observatory Global Telescope  2026:1.35M
  Los Angeles County Museum of Natural His  2026:932.9K
  Maricopa County Community College Distri  2026:1.20M
  Massachusetts Institute of Technology     2026:973.1K
  North Carolina State University           2026:494.1K
  Purdue University                         2026:820.0K
  SUNY at Buffalo                           2026:900.0K
  University of Arizona                     2026:997.3K
  University of California-Santa Barbara    2026:1.37M
  University of California-Santa Cruz       2026:1.24M
  University of Chicago                     2026:2.54M
  University of Colorado at Boulder         2026:755.3K
  University of Iowa                        2026:906.7K
  University of Mississippi                 2026:929.8K
  University of Missouri-Columbia           2026:875.6K
  University of Nebraska-Lincoln            2026:1.26M
  University of New Mexico                  2026:1.39M
  University of Oklahoma Norman Campus      2026:1.15M
  University of South Carolina at Columbia  2026:1000.0K
  University of Tennessee Knoxville         2026:900.0K
  University of Texas at Austin             2026:1.09M
  University of Wisconsin-Madison           2026:1.16M

## where

STATE: CA 18, NY 11, AZ 7, MO 7, TX 5, IL 5, NC 5, OK 4, NE 3, MS 3, IN 3, OH 3

## what

PROGRAM_NAME: RSCH EXPER FOR UNDERGRAD SITES 28%, Workforce (MSPRF) MathSciPDFel 14%, EWFD-Eng Workforce Development 9%, Info Integration & Informatics 8%, Secure &Trustworthy Cyberspace 8%, Software Institutes 6%, CyberTraining - Training-based 6%, Innov TwoYear College STEM Ed 5%, Org Interaction & Ecology 5%, FET-Fndtns of Emerging Tech 4%, NSF ASTRON & ASTROPHY PSTDC FE 4%, WaLCZ-Water, Land, & Crit Zone 4%

CFDA_NUMBER: 47.070 48%, 47.049 18%, 47.074 15%, 47.041 7%, 47.076 4%, 47.049, 47.070 3%, 47.050 2%, 47.084 1%, 47.083 1%, 47.041, 47.075 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AWARD_ID | other | 116 | 0 | 2544741 2; 2548190 2; 2548104 2; 2547842 2 |
| TITLE | other | 101 | 0 | Collaborative Research: S 5; Collaborative Research: C 3; Collaborative Research: F 3; Collaborative Research: L 3 |
| AWARDEE_NAME | who | 101 | 0 | University of Oklahoma No 3; University of Nebraska-Li 3; Maricopa County Community 3; University of Texas at Au 2 |
| INSTITUTION | other | 101 | 0 | University of Oklahoma No 3; University of Nebraska-Li 3; Maricopa County Community 3; University of Texas at Au 2 |
| PI_NAME | who | 117 | 0 | Gen Li 2; Huanrui Yang 2; Logan Perry 2; Dana Reinemann 2 |
| CO_PI_NAMES | empty | 1 | 125 |  |
| PROGRAM_OFFICER | other | 116 | 0 | Gen Li 2; Huanrui Yang 2; Logan A Perry 2; Dana N Reinemann 2 |
| AWARD_AMOUNT | amount | 95 | 0 | 190000 12; 600000 4; 330000 3; 410000 3 |
| AWARD_DATE | date | 38 | 0 | 06/30/2026 21; 05/19/2026 13; 06/25/2026 6; 06/29/2026 6 |
| START_DATE | date | 9 | 0 | 10/01/2026 96; 09/15/2026 8; 01/01/2027 8; 11/01/2026 3 |
| END_DATE | date | 19 | 0 | 09/30/2029 53; 09/30/2030 19; 09/30/2031 13; 09/30/2027 6 |
| STATUS | empty | 1 | 125 |  |
| ABSTRACT | other | 103 | 1 | This award is made as par 12; Pre-trained AI models sha 5; The Open Radio Access Net 3; Cloud computing is essent 3 |
| PROGRAM_NAME | category | 38 | 0 | RSCH EXPER FOR UNDERGRAD  24; Workforce (MSPRF) MathSci 12; EWFD-Eng Workforce Develo 8; Info Integration & Inform 7 |
| EIN | empty | 1 | 125 |  |
| ZIP | other | 98 | 0 | 730193003 3; 68503 3; 652113020 3; 852816941 3 |
| CITY | other | 87 | 0 | COLUMBIA 4; NORMAN 3; NEW YORK 3; Pasadena 3 |
| STATE | state | 40 | 0 | CA 18; NY 11; AZ 7; MO 7 |
| COUNTRY | other | 1 | 0 | US 125 |
| CFDA_NUMBER | category | 10 | 0 | 47.070 60; 47.049 22; 47.074 19; 47.041 9 |
| _INGESTED_AT | audit | 1 | 0 | 1783013126331353 125 |
| _SOURCE_RUN_ID | audit | 1 | 0 | f097596e-b0a4-4742-b2be-c 125 |
| _SRC_SHA256 | who | 1 | 0 | 9b1900c6ca83df35571da3942 125 |
