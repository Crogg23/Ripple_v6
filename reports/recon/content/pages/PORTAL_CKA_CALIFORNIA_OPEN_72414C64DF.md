# PORTAL_CKA_CALIFORNIA_OPEN_72414C64DF

rows 58  columns 22  scan 2.9s

roles: audit 2, category 14, date 1, other 3, who 3

## when

INGESTED_AT
  2026        58  ##############################

## who

SB_552_CONTACT_NAME by rows
         1  Jason Johnston
         1  Kamie Loeser
         1  Yolo County - Natural Resources Division
         1  David Davis; Terri Mejorado
         1  Baljit Singh
         1  Jorge A. Perez; Felipe Vega
         1  Amy Rutledge
         1  Owen A. Cabo Dal Molin
         1  Tiffany Martinez
         1  Judd Goodman; An Bartlett
         1  Gaylon F. Norwood
         1  Jeff Camp
         1  Amy Irani
         1  Kris Mangano
         1  Mireya Turner
         1  Diana Evensen
         1  Denise England
         1  Xzandrea Fowler
         1  Scott Gharda
         1  Sierra Ryan

STATE by rows
        58  California

SRC_SHA256 by rows
        58  57cbdf4e318e36ff14ac0ac9fe8c204fdd3cb21ad5e419f3f5a9da31cf835999

## who x when

SB_552_CONTACT_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Amy Irani                                 2026:1
  Amy Rutledge                              2026:1
  Baljit Singh                              2026:1
  David Davis; Terri Mejorado               2026:1
  Denise England                            2026:1
  Diana Evensen                             2026:1
  Gaylon F. Norwood                         2026:1
  Jason Johnston                            2026:1
  Jeff Camp                                 2026:1
  Jorge A. Perez; Felipe Vega               2026:1
  Judd Goodman; An Bartlett                 2026:1
  Kamie Loeser                              2026:1
  Kris Mangano                              2026:1
  Mireya Turner                             2026:1
  Owen A. Cabo Dal Molin                    2026:1
  Scott Gharda                              2026:1
  Sierra Ryan                               2026:1
  Tiffany Martinez                          2026:1
  Xzandrea Fowler                           2026:1
  Yolo County - Natural Resources Division  2026:1

STATE by INGESTED_AT  LOAD STAMP, not an event date
  California                                2026:58

## what

ASSISTANCE: Direct Technical Assistance 60%, Financial Assistance 36%, No Response 2%, Considering Direct Technical A 2%

STATUS: Executed 51%, Start Date: 4/1/24 7%, Start Date: 10/21/24 5%, Start Date: 2/19/24 5%, Start Date: 7/15/24 5%, Start Date: 6/10/24 5%, Not Applicable 5%, Start Date: 4/8/24 5%, Start Date: 5/20/24 5%, Start Date: 11/6/23 2%, Start Date: 9/25/23 2%, Start Date: 10/19/23 2%

DROUGHT_WEBPAGE: No drought webpage 54%, https://www.yuba.gov/departmen 4%, https://www.yolocounty.org/gov 4%, https://publicworks.venturacou 4%, https://www.tuolumnecounty.ca. 4%, https://tularecounty.ca.gov/rm 4%, https://tehamacountywater.org/ 4%, https://storymaps.arcgis.com/s 4%, https://stanemergency.com/natu 4%, https://www.sonomawater.org/dr 4%, https://www.solanocounty.gov/g 4%, https://drought.readysiskiyou. 4%

TASK_FORCE_ESTABLISHED: Established 97%, Not applicable 2%, Not Established 2%

LEADING_DEPARTMENT_OR_AGENCY: Environmental Health 34%, Office of Emergency Services 20%, Public Works 12%, Community Development 7%, Office of Emergency Management 5%, Planning and Community Develop 5%, Office of Emergency Services,  5%, Community Services 2%, Resource Management Agency 2%, Office of Emergency Services,  2%, County of San Luis Obispo 2%, Office of Emergency Services,  2%

USING_ALTERNATIVE_PROCESS: No 63%, Yes 35%, Not applicable 2%

MEETING_FREQUENCY: Quarterly 53%, Monthly 9%, Unknown 9%, Bimonthly 6%, Not standing 6%, Ad-hoc but increased frequency 3%, Quarterly during non-drought p 3%, Biannually 3%, Not applicable 3%, As needed 3%, Twice a year during non-drough 3%

FORMALIZED_BY_BOS: No 43%, Yes 29%, Unknown 24%, Not applicable 5%

TASK_FORCE_NOTES: Creating subgroup to develop D 9%, Memo from CAO that designates  9%, TF formalized by BOS 9%, WAC advises the BOS on water-r 9%, Task force members are welcome 9%, Has a standing internal TF and 9%, County staff Working Group rep 9%, Created ad-hoc group to develo 9%, Using established Water Manage 9%, Using the alternative process  9%, Using the Water Plan Small Sys 9%

STAGE_OF_DROUGHT_RESILIENCE_PLAN: Completed 81%, In Progress 17%, Not applicable 2%

BOS_ADOPTED: Yes 77%, Planned 12%, Not applicable 4%, Planned - 4/14 4%, No 4%

DROUGHT_RESILIENCE_PLAN: Not available 52%, https://cadwr.box.com/s/dt3cj0 4%, https://cadwr.box.com/s/ywwr6a 4%, https://cadwr.box.com/s/p5pw8j 4%, https://cadwr.box.com/s/zawdwz 4%, https://cadwr.box.com/s/d3qmtr 4%, https://cadwr.box.com/s/lrowxe 4%, https://cadwr.box.com/s/taxnh0 4%, https://cadwr.box.com/s/khh7ah 4%, https://cadwr.box.com/s/c4irr6 4%, https://cadwr.box.com/s/cllm9t 4%, https://cadwr.box.com/s/o4s9cx 4%

PLAN_DEVELOPMENT: Standalone plan 76%, Not yet in development 10%, Integrated into EOP 2%, Incorporated into different co 2%, Integrated into Safety element 2%, Integrated into Local Hazard M 2%, Not applicable 2%, Incorporated into LHMP 2%, Integrated into Emergency Oper 2%, Integrated into Climate Action 2%

DRP_NOTES: County working closely with Sa 11%, Using and updating existing co 11%, No state smalls or domestic we 11%, No state smalls, only domestic 11%, Developing in parallel with UC 11%, County has an MOU with the El  11%, County has MOU with cities for 11%, County Drought Work Group work 11%, County doesn't permit wells; P 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATE | who | 1 | 0 | California 58 |
| COUNTY | other | 58 | 0 | Yuba 1; Yolo 1; Ventura 1; Tuolumne 1 |
| ASSISTANCE | category | 4 | 0 | Direct Technical Assistan 35; Financial Assistance 21; No Response 1; Considering Direct Techni 1 |
| STATUS | category | 29 | 0 | Executed 21; Start Date: 4/1/24 3; Start Date: 10/21/24 2; Start Date: 2/19/24 2 |
| SB_552_CONTACT_NAME | who | 58 | 1 | Ian Scott 1; Yolo County - Natural Res 1; Ben Fischetti 1; Dore Bietz; Sean Hembree 1 |
| SB_552_CONTACT_EMAIL | other | 57 | 2 | iscott@co.yuba.ca.us 1; naturalresources@yolocoun 1; ben.fischetti@ventura.org 1; dbietz@co.tuolumne.ca.us; 1 |
| SB_552_CONTACT_PHONE | other | 54 | 5 | (530) 749-5481 1; 530-666-8775 1; 805-654-2042 1; 209-533-6395; 209-533-555 1 |
| DROUGHT_WEBPAGE | category | 46 | 0 | No drought webpage 13; https://www.yuba.gov/depa 1; https://www.yolocounty.or 1; https://publicworks.ventu 1 |
| TASK_FORCE_ESTABLISHED | category | 3 | 0 | Established 56; Not applicable 1; Not Established 1 |
| LEADING_DEPARTMENT_OR_AGENCY | category | 29 | 1 | Environmental Health 14; Office of Emergency Servi 8; Public Works 5; Community Development 3 |
| USING_ALTERNATIVE_PROCESS | category | 4 | 6 | No 33; Yes 18; Not applicable 1 |
| MEETING_FREQUENCY | category | 14 | 22 | Quarterly 18; Monthly 3; Unknown 3; Bimonthly 2 |
| FORMALIZED_BY_BOS | category | 5 | 37 | No 9; Yes 6; Unknown 5; Not applicable 1 |
| TASK_FORCE_NOTES | category | 16 | 43 | Creating subgroup to deve 1; Memo from CAO that design 1; TF formalized by BOS 1; WAC advises the BOS on wa 1 |
| STAGE_OF_DROUGHT_RESILIENCE_PLAN | category | 3 | 0 | Completed 47; In Progress 10; Not applicable 1 |
| BOS_ADOPTED | category | 6 | 32 | Yes 20; Planned 3; Not applicable 1; Planned - 4/14 1 |
| DROUGHT_RESILIENCE_PLAN | category | 46 | 0 | Not available 12; https://cadwr.box.com/s/d 1; https://cadwr.box.com/s/y 1; https://cadwr.box.com/s/p 1 |
| PLAN_DEVELOPMENT | category | 10 | 0 | Standalone plan 44; Not yet in development 6; Integrated into EOP 1; Incorporated into differe 1 |
| DRP_NOTES | category | 10 | 49 | County working closely wi 1; Using and updating existi 1; No state smalls or domest 1; No state smalls, only dom 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:13:08.18910 58 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4e1121ea-b7be-449c-a65e-d 58 |
| SRC_SHA256 | who | 1 | 0 | 57cbdf4e318e36ff14ac0ac9f 58 |
