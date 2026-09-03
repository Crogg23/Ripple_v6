# PORTAL_CKA_ANALYZE_BOSTON_11B21C9100

rows 41  columns 23  scan 3.9s

roles: amount 2, audit 2, category 12, date 3, empty 1, other 2, who 2

## when

ISSUED
  2023        25  ##############################
  2024         5  ######
  2025         6  #######
  2026         5  ######

EXPIRES
  2026        41  ##############################

INGESTED_AT
  2026        41  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GPSX | 41 | 745.4K | 769.8K | 788.3K | 789.4K | 31.53M |
| GPSY | 41 | 2.92M | 2.95M | 2.97M | 2.97M | 120.76M |

## who

STATUS by rows
        41  Active

STATUS by dollars
      31.53M       41 rows  Active

SRC_SHA256 by rows
        41  a29ce9114ced986cf2b514daab9cee90e26295cc2213c75085aea5a219059d81

SRC_SHA256 by dollars
      31.53M       41 rows  a29ce9114ced986cf2b514daab9cee90e26295cc2213c75085aea5a21905

## who x when

STATUS by ISSUED, dollars = GPSX
  Active                                    2023:19.30M 2024:3.81M 2025:4.61M 2026:3.81M

SRC_SHA256 by ISSUED, dollars = GPSX
  a29ce9114ced986cf2b514daab9cee90e26295cc  2023:19.30M 2024:3.81M 2025:4.61M 2026:3.81M

## what

LICENSE_NUM: CAN526372 14%, CAN525077 14%, CAN524615 7%, CAN524628 7%, CAN524588 7%, CAN524596 7%, CAN524604 7%, CAN524648 7%, CAN524717 7%, CAN524749 7%, CAN524747 7%, CAN524719 7%

LICENSE_TYPE: Recreational Retail Cannabis D 80%, Co-located Recreational and Me 17%, Delivery (operator) 2%

BUSINESS_NAME: Pure Oasis, LLC 13%, Cannabis Healing, LLC 13%, Lowkey 2, LLC 13%, Core Empowerment LLC  7%, Ascend Mass LLC 7%, Berkshire Roots, Inc. 7%, NS AJO Holdings, Inc. 7%, HVV Massachusetts, Inc. 7%, Erba C3 Dorchester LLC 7%, The Heritage Club, LLC 7%, Mayflower Medicinals, Inc. 7%, Sira Naturals, Inc. 7%

DBA_NAME: High Profile X Budega 19%, Pure Oasis 12%, Cannabis Healing 12%, Lowkey Dispensary 12%, Seed 6%, Ascend 6%, Berkshire Roots 6%, Ethos Cannabis 6%, Happy Valley 6%, The Heritage Club 6%, Ayr 6%

COMMENTS: In whole said building 3 607 S 100%

LOCATION_COMMENTS: The premises contains one (1)  17%, The Facility occupies a portio 8%, Retail cannabis establishment  8%, In whole of said building (+/- 8%, The premises consists of the e 8%, Entire first floor of the buil 8%, Overall building area is 13,78 8%, In one floor of single story b 8%, In whole of said building (+/- 8%, In whole of said building (+/- 8%, Approximately 4,665 square fee 8%

APPLICANT: Kobie Evans 12%, Kyle Teevens 12%, Brian Jones II 12%, Jeff Similien 12%, Jasmine Alvarez 6%, Jorge Castillo, Jr. 6%, Guillermo Erazo 6%, Kevin Bradley 6%, Brendan Collins 6%, Nike John 6%, Andrew Plante 6%, Christina Earl 6%

MANAGER: Kyle Teevens 20%, Kobie Evans 13%, Jasmine Alvarez 7%, Jorge Castillo, Jr. 7%, Guillermo Erazo 7%, Kevin Bradley 7%, Brendan Collins 7%, Nike John 7%, Andrew Plante 7%, Christina Earl 7%, Paulino Flores Yessian 7%, Tito Jackson 7%

DAY_PHONE: (617)792-5644 13%, (248)939-0916 13%, (857)636-4618 13%, (617)894-2266 13%, (857)241-8354 7%, (508)816-5751 7%, (617)380-9955 7%, (617)680-0326 7%, (617)640-4104 7%, (774)406-1530 7%, (458)239-1267 7%

ADDRESS: 4-  Neptune RD 14%, 5252-5270  Washington ST 14%, 401A-  Centre ST 7%, 268-274  Friend ST 7%, 430-454  Blue Hill AV 7%, 253-  Meridian ST 7%, 50-  Clapp ST 7%, 220-  William F McClellan HW 7%, 43-  Freeport ST 7%, 116R-  Cambridge ST 7%, 230-  Harvard AV 7%, 829-  Boylston ST 7%

CITY: Boston 22%, Dorchester 20%, East Boston 15%, Allston 8%, Roslindale 8%, West Roxbury 8%, Jamaica Plain 5%, Roxbury 5%, Charlestown 2%, South Boston 2%, Brighton 2%, Mattapan 2%

ZIP: 02128 20%, 02122 10%, 02134 10%, 02131 10%, 02109 10%, 02132 10%, 02130 7%, 02121 7%, 02125 7%, 02114 3%, 02129 3%, 02116 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LICENSE_NUM | category | 39 | 0 | CAN526372 2; CAN525077 2; CAN524615 1; CAN524628 1 |
| STATUS | who | 1 | 0 | Active 41 |
| LICENSE_CATEGORY | other | 1 | 0 | Misc 41 |
| LICENSE_TYPE | category | 3 | 0 | Recreational Retail Canna 33; Co-located Recreational a 7; Delivery (operator) 1 |
| ISSUED | date | 27 | 0 | 2023-03-31 6; 2023-03-29 5; 2023-04-21 3; 2023-07-03 2 |
| EXPIRES | date | 1 | 0 | 2026-12-31 41 |
| BUSINESS_NAME | category | 38 | 1 | Pure Oasis, LLC 2; Cannabis Healing, LLC 2; Lowkey 2, LLC 2; Core Empowerment LLC  1 |
| DBA_NAME | category | 33 | 4 | High Profile X Budega 3; Pure Oasis 2; Cannabis Healing 2; Lowkey Dispensary 2 |
| COMMENTS | category | 2 | 40 | In whole said building 3  1 |
| LOCATION_COMMENTS | category | 36 | 5 | The premises contains one 2; The Facility occupies a p 1; Retail cannabis establish 1; In whole of said building 1 |
| APPLICANT | category | 37 | 0 | Kobie Evans 2; Kyle Teevens 2; Brian Jones II 2; Jeff Similien 2 |
| MANAGER | category | 38 | 1 | Kyle Teevens 3; Kobie Evans 2; Jasmine Alvarez 1; Jorge Castillo, Jr. 1 |
| DAY_PHONE | category | 27 | 10 | (617)792-5644 2; (248)939-0916 2; (857)636-4618 2; (617)894-2266 2 |
| EVENING_PHONE | empty | 1 | 41 |  |
| ADDRESS | category | 39 | 0 | 4-  Neptune RD 2; 5252-5270  Washington ST 2; 401A-  Centre ST 1; 268-274  Friend ST 1 |
| CITY | category | 13 | 0 | Boston 9; Dorchester 8; East Boston 6; Allston 3 |
| STATE | other | 1 | 0 | MA 41 |
| ZIP | category | 23 | 0 | 02128 6; 02122 3; 02134 3; 02131 3 |
| GPSX | amount | 39 | 0 | 784384.2097043842 2; 748582.8748111427 2; 761532.9545539767 1; 774686.6500312984 1 |
| GPSY | amount | 39 | 0 | 2963958.931263387 2; 2919763.5386832207 2; 2942480.073630646 1; 2958218.5743058026 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:21:14.43059 41 |
| SOURCE_RUN_ID | audit | 1 | 0 | d56ef3a8-92ce-4d2b-93cd-e 41 |
| SRC_SHA256 | who | 1 | 0 | a29ce9114ced986cf2b514daa 41 |
