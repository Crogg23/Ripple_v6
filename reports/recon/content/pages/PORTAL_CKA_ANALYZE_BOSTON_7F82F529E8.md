# PORTAL_CKA_ANALYZE_BOSTON_7F82F529E8

rows 60  columns 33  scan 4.3s

roles: amount 11, audit 2, category 8, date 1, empty 2, other 7, who 3

## when

INGESTED_AT
  2026        60  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NUMSTORIES | 55 | 1 | 4 | 12.46 | 13 | 274.50 |
| COST | 60 | 0 | 7.82M | 465.87M | 522.74M | 2.17B |
| NUMSTUDENT | 60 | 0 | 475.50 | 29.4K | 32.0K | 154.6K |
| LATITUDE | 60 | 0 | 42.35 | 42.38 | 42.38 | 2.4K |
| LONGITUDE | 60 | -71.18 | -71.09 | 0 | 0 | -4.1K |
| X | 57 | 742.7K | 765.5K | 778.5K | 780.8K | 43.68M |

## who

NAME by rows
         2  Kaplan Career Institute (Closed)
         1  The Boston Conservatory
         1  Harvard University of Public Health
         1  Wheelock College
         1  Massachusetts General Hospital Dietetic Internship
         1  Rets Technical Center
         1  Butera School Of Art
         1  Suffolk University
         1  MASCO Colleges of the Fenway
         1  Boston College
         1  Boston University Rental Office
         1  New England School of Law
         1  Boston Baptist College
         1  Boston University School of Medicine
         1  Bunker Hill Community College
         1  University of Massachusetts-Boston
         1  Massachusetts College of Art and Design
         1  Laboure College
         1  Boston University Admissions
         1  Boston University Research

NAME by dollars
     522.74M        1 rows  Harvard Medical School
     426.36M        1 rows  Northeastern University
     195.58M        1 rows  University of Massachusetts-Boston
     106.84M        1 rows  Massachusetts General Hospital Dietetic Internship
      99.37M        1 rows  Emmanuel College
      87.53M        1 rows  MCPHS University
      72.05M        1 rows  Boston University School of Medicine
      66.94M        1 rows  Boston University
      65.80M        1 rows  Massachusetts College of Art and Design
      55.55M        1 rows  Simmons
      51.94M        1 rows  Laboure College
      37.26M        1 rows  MASCO Colleges of the Fenway
      31.13M        1 rows  Tufts University School of Medicine
      30.89M        1 rows  Roxbury Community College
      26.81M        1 rows  Harvard Business School
      21.82M        1 rows  Simmons College
      21.67M        1 rows  Suffolk University
      20.81M        2 rows  Kaplan Career Institute (Closed)
      19.40M        1 rows  Boston University Sargent College
      18.01M        1 rows  Boston University Trustees

BACKUPPOWE by rows
        60  0.000000000000000

BACKUPPOWE by dollars
       2.17B       60 rows  0.000000000000000

SRC_SHA256 by rows
        60  25926db77c08f144d9b96d025d7b1d7bb70f5bc4a1a11c74f8c4dd460508507f

SRC_SHA256 by dollars
       2.17B       60 rows  25926db77c08f144d9b96d025d7b1d7bb70f5bc4a1a11c74f8c4dd460508

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = COST
  Boston Baptist College                    2026:3.33M
  Boston College                            2026:0
  Boston University                         2026:66.94M
  Boston University Admissions              2026:2.62M
  Boston University Rental Office           2026:82.8K
  Boston University Research                2026:1.48M
  Boston University School of Medicine      2026:72.05M
  Bunker Hill Community College             2026:17.18M
  Butera School Of Art                      2026:594.7K
  Emmanuel College                          2026:99.37M
  Harvard Business School                   2026:26.81M
  Harvard Medical School                    2026:522.74M
  Harvard University of Public Health       2026:0
  Kaplan Career Institute (Closed)          2026:20.81M
  Laboure College                           2026:51.94M
  MASCO Colleges of the Fenway              2026:37.26M
  MCPHS University                          2026:87.53M
  Massachusetts College of Art and Design   2026:65.80M
  Massachusetts General Hospital Dietetic   2026:106.84M
  New England School of Law                 2026:8.71M
  Northeastern University                   2026:426.36M
  Rets Technical Center                     2026:0
  Roxbury Community College                 2026:30.89M
  Simmons                                   2026:55.55M
  Simmons College                           2026:21.82M
  Suffolk University                        2026:21.67M
  The Boston Conservatory                   2026:4.90M
  Tufts University School of Medicine       2026:31.13M
  University of Massachusetts-Boston        2026:195.58M
  Wheelock College                          2026:11.61M

BACKUPPOWE by INGESTED_AT  LOAD STAMP, not an event date, dollars = COST
  0.000000000000000                         2026:2.17B

## what

MATCH_TYPE: NCES & Consortium 49%, Consortium 28%, NCES 23%

ID1: 300 The Fenway, Boston, Massac 18%, 950 Metropolitan Ave, Boston,  9%, One Wells Avenue, Newton, Mass 9%, 400 Heath St, Chestnut Hill, M 9%, 127 Lake Street, Brighton, Mas 9%, 1505 Commonwealth Ave, Brighto 9%, 303 Adams Street, Milton, Mass 9%, 537 Commonwealth Ave, Boston,  9%, 1140 Boylston St, Boston, Mass 9%, 550 Huntington Ave, Boston, Ma 9%

SCHOOLID: 0 56%, 167543 7%, 164845 7%, 164614 4%, 166717 4%, 167455 4%, 167677 4%, 167020 4%, 165264 4%, 16645201 4%, 167224 4%

CITY: Fenway/Kenmore 46%, Back Bay 12%, Allston/Brighton 10%, Boston 6%, Charlestown 6%, Financial District 6%, South End 6%, Beacon Hill 4%, Hyde Park 2%, West Roxbury 2%, Jamaica Plain 2%

CONTACT: HARVARD COLLEGE 18%, BOSTON UNIVERSITY TRSTS OF 18%, BOSTON UNIVERSITY TRSTS 14%, CITY OF BOSTON 9%, COMMWLTH OF MASS 9%, COMMONWEALTH OF MASS 9%, BOSTON BAPTIST COLLEGE 5%, BACK OF THE HILL CONDO TRUST 5%, TRUSTEES OF BOSTON COLLEGE 5%, COMMEX LLC 5%, NEW CARITAS CHRISTI HOSPITAL 5%

YEARBUILT: 1899 51%, 0 11%, 1920 9%, 1900 6%, 1975 4%, 1964 4%, 1925 4%, 1960 4%, 1999 2%, 1923 2%, 1917 2%

CAMPUSHOUS: 40% 17%, 48% 17%, 73.5% 8%, 100% 8%, 27% 8%, 20% 8%, 41% 8%, 17% 8%, 28% 8%, 19% 8%

URL: http://www.hsph.harvard.edu/ 10%, http://www.retstech.com 10%, http://www.blainebeautyschools 10%, http://www.boston.edu 10%, http://www.mspp.edu 10%, http://www.pmc.edu 10%, http://www.sjs.edu 10%, http://www.bryman-institute.co 10%, http://www.laboure.edu 10%, http://www.aiboston.edu 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MATCH_TYPE | category | 4 | 3 | NCES & Consortium 28; Consortium 16; NCES 13 |
| REF_ID | other | 1 | 0 | 0 60 |
| ID1 | category | 40 | 21 | 300 The Fenway, Boston, M 2; 950 Metropolitan Ave, Bos 1; One Wells Avenue, Newton, 1; 400 Heath St, Chestnut Hi 1 |
| ID | other | 59 | 1 | 167543 1; 164845 1; 62594 1; 41509 1 |
| SCHOOLID | category | 43 | 1 | 0 15; 167543 2; 164845 2; 164614 1 |
| NAME | who | 58 | 0 | Kaplan Career Institute ( 2; Harvard University of Pub 1; Rets Technical Center 1; Blaine The Beauty Career  1 |
| ADDRESS | other | 60 | 0 | 677 Huntington Ave 1; 965 Commonwealth Ave 1; 530 Commonwealth Ave 1; 950 Metropolitan Ave, Bos 1 |
| CITY | category | 19 | 1 | Fenway/Kenmore 24; Back Bay 6; Allston/Brighton 5; Boston 3 |
| ZIPCODE | other | 53 | 2 | 0 5; 02215 2; 02115 1; 35206 1 |
| CONTACT | category | 47 | 3 | HARVARD COLLEGE 4; BOSTON UNIVERSITY TRSTS O 4; BOSTON UNIVERSITY TRSTS 3; CITY OF BOSTON 2 |
| PHONENUMBE | other | 55 | 5 | (617) 432-1031 1; (617) 783-1197 1; (508) 370-7447 1; (617) 364-3510 1 |
| YEARBUILT | category | 22 | 3 | 1899 24; 0 5; 1920 4; 1900 3 |
| NUMSTORIES | amount | 15 | 5 | 3 13; 5 11; 4 10; 6 6 |
| COST | amount | 55 | 0 | 0.000000000000000 5; 3326900.000000000000000 1; 5477000.000000000000000 1; 1265300.000000000000000 1 |
| NUMSTUDENT | amount | 42 | 0 | 0.000000000000000 19; 147.000000000000000 1; 448.000000000000000 1; 484.000000000000000 1 |
| BACKUPPOWE | who | 1 | 0 | 0.000000000000000 60 |
| SHELTERCAP | empty | 1 | 60 |  |
| LATITUDE | amount | 58 | 0 | 0.000000000000000 3; 42.253999989999997 1; 42.278892259999999 1; 42.328789989999997 1 |
| LONGITUDE | amount | 58 | 0 | 0.000000000000000 3; -71.110259990000003 1; -71.180351290000004 1; -71.110219990000004 1 |
| COMMENT | other | 58 | 3 | 0401895001 1; 1810945000 1; 2009228000 1; 1001487000 1 |
| X | amount | 57 | 3 | 761679.207870439975522 1; 742669.813146520056762 1; 761565.489593939972110 1; 747258.000164350029081 1 |
| Y | amount | 57 | 3 | 2947900.000126770231873 2; 2917825.673136440105736 1; 2926817.873327849898487 1; 2945080.340083689894527 1 |
| NUMSTUDENT12 | amount | 39 | 22 | 103.000000000000000 1; 558.000000000000000 1; 343.000000000000000 1; 183.000000000000000 1 |
| CAMPUSHOUS | category | 18 | 42 | 40% 2; 48% 2; 73.5% 1; 100% 1 |
| NUMSTUDENTS13 | amount | 43 | 0 | 0.000000000000000 17; 502.000000000000000 2; 96.000000000000000 1; 652.000000000000000 1 |
| URL | category | 48 | 14 | http://www.hsph.harvard.e 1; http://www.retstech.com 1; http://www.blainebeautysc 1; http://www.boston.edu 1 |
| ADDRESS2013 | empty | 1 | 60 |  |
| SHAPE_WKT | other | 60 | 0 | POINT (-71.10352994999993 1; POINT (-71.11921047899994 1; POINT (-71.09639762699998 1; POINT (-71.11025999999998 1 |
| POINT_X | amount | 59 | 0 | -71.103529949999938 1; -71.119210478999946 1; -71.096397626999988 1; -71.110259999999982 1 |
| POINT_Y | amount | 59 | 0 | 42.335066455000060 1; 42.352005221000070 1; 42.348599133000050 1; 42.254000000000076 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:28:48.97315 60 |
| SOURCE_RUN_ID | audit | 1 | 0 | f9877401-755d-4f15-b78a-8 60 |
| SRC_SHA256 | who | 1 | 0 | 25926db77c08f144d9b96d025 60 |
