# PORTAL_CKA_IRELAND_NATIONAL_F2EFDE1A8C

rows 1.2K  columns 14  scan 3.6s

roles: audit 2, category 1, date 3, id 3, other 1, who 5

## when

ACTUAL_START_DATE
  2024       359  #################
  2025       643  ##############################
  2026       204  ##########

FINAL_END_DATE
  2024         4  
  2025        61  #####
  2026       378  ##############################
  2027       304  ########################
  2028       212  #################
  2029       174  ##############
  2030        65  #####
  2031         5  
  2033         3  

INGESTED_AT
  2026      1.2K  ##############################

## who

FUNDER_NAME by rows
      1.2K  Research Ireland

LEAD_APPLICANT by rows
         4  Brenda McNally
         4  Kate Robson Brown
         4  Sinéad Ryan
         3  Maeve Liston
         3  Ann Butler
         2  Aaron Lim
         2  Andrew Lindsay
         2  Uri Frank
         2  Daragh Bradshaw
         2  Hugh Geaney
         2  Nigel Flegg
         2  Stephen Gammell
         2  Dawid Maszkiewicz
         2  Maureen O'Sullivan
         2  Rachel Farrell
         2  Andrew Parnell
         2  Brian Walsh
         2  Valesca Lima
         2  Ian Major
         2  Fiona Murphy

AWARD_AMOUNT by rows
       105  € 136,000.00
        89  € 124,000.00
        77  € 112,987.00
        63  € 68,000.00
        63  € 134,149.07
        51  € 102,000.00
        43  € 93,000.00
        43  € 62,000.00
        28  € 34,000.00
        20  € 90,800.00
        15  € 31,000.00
        13  € 66,307.83
        11  € 10,000.00
        11  € 12,000.00
        10  € 55,396.00
         8  € 50,000.00
         7  € 68,100.00
         6  € 102,100.00
         6  € 134,733.46
         6  € 123,020.00

RESEARCH_BODY by rows
       174  Trinity College Dublin
       170  University College Dublin
       126  University of Galway
       125  University College Cork
       100  Dublin City University
        90  University of Limerick
        65  Maynooth University
        49  University College Dublin (UCD)
        35  RCSI University of Medicine and Health Sciences
        32  Trinity College Dublin (TCD)
        22  University College Cork (UCC)
        19  Dublin City University (DCU)
        18  Technological University Dublin
        18  RCSI University of Medicine and Health Science (RCSI)
        16  South East Technological University
        14  Maynooth University (MU)
        13  University of Limerick (UL)
        12  Tyndall National Institute (TNI)
        11  Mary Immaculate College
        10  Atlantic Technological University

## who x when

FUNDER_NAME by FINAL_END_DATE
  Research Ireland                          2024:4 2025:61 2026:378 2027:304 2028:212 2029:174 2030:65 2031:5 2033:3

LEAD_APPLICANT by FINAL_END_DATE
  Aaron Lim                                 2029:2
  Andrew Lindsay                            2029:2
  Andrew Parnell                            2031:2
  Ann Butler                                2026:1 2027:2
  Brenda McNally                            2029:4
  Brian Walsh                               2028:2
  Daragh Bradshaw                           2026:2
  Dawid Maszkiewicz                         2026:1 2027:1
  Fiona Murphy                              2025:1 2027:1
  Hugh Geaney                               2029:2
  Ian Major                                 2026:1 2029:1
  Kate Robson Brown                         2027:4
  Maeve Liston                              2025:1 2026:1 2027:1
  Maureen O'Sullivan                        2028:2
  Nigel Flegg                               2026:2
  Rachel Farrell                            2026:1 2027:1
  Sinéad Ryan                               2027:3 2031:1
  Stephen Gammell                           2026:2
  Uri Frank                                 2025:1 2030:1
  Valesca Lima                              2026:1 2027:1

## what

PROGRAMME_NAME: Government of Ireland Postgrad 41%, Government of Ireland Postdoct 16%, New Foundations (NF) 11%, EPS Postgraduate Application ( 6%, Frontiers for the Future 5%, Discover Programme 4%, Collaborative Alliances for So 4%, Pathway Programme 4%, Industry RD&I Fellowship Progr 3%, EPS Postdoctoral Application ( 2%, Employment-Based Postgraduate  2%, Supplement 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PROJECT_ID | id | 1.2K | 0 | 25/DP/13839(N) 7; 25/DP/13815(N) 7; 25/DP/13894(N) 7; 25/DP/13890(N) 7 |
| PROGRAMME_NAME | category | 36 | 0 | Government of Ireland Pos 455; Government of Ireland Pos 175; New Foundations (NF) 122; EPS Postgraduate Applicat 63 |
| LEAD_APPLICANT | who | 1.2K | 0 | Sinéad Ryan 9; Kate Robson Brown 9; Ann Butler 8; Maeve Liston 8 |
| ORCID_ID | id | 1.1K | 41 | https://orcid.org/0000-00 8; https://orcid.org/0000-00 7; https://orcid.org/0000-00 7; https://orcid.org/0000-00 7 |
| RESEARCH_BODY | who | 60 | 0 | Trinity College Dublin 174; University College Dublin 170; University of Galway 126; University College Cork 125 |
| FUNDER_NAME | who | 1 | 0 | Research Ireland 1.2K |
| FUNDER_ROR_ID | other | 1 | 0 | https://ror.org/010t7sr36 1.2K |
| PROJECT_TITLE | id | 1.2K | 1 | Research Ireland Fellowsh 16; Discover Co-Fund 11; Tackling Climate Misinfor 8; SFI Centre for Research T 7 |
| ACTUAL_START_DATE | date | 62 | 0 | 2025-01-09T00:00:00 382; 2024-01-09T00:00:00 329; 2026-01-03T00:00:00 78; 2025-12-31T00:00:00 63 |
| FINAL_END_DATE | date | 137 | 0 | 2027-08-31T00:00:00 176; 2028-08-31T00:00:00 155; 2029-08-31T00:00:00 150; 2026-08-31T00:00:00 146 |
| AWARD_AMOUNT | who | 497 | 0 | € 136,000.00 105; € 124,000.00 89; € 112,987.00 77; € 68,000.00 63 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:25:10.74691 1.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | fb5e0825-d97c-4ff2-8e1a-c 1.2K |
| SRC_SHA256 | who | 1 | 0 | 5bcfd5b99db0130a6b40f73fc 1.2K |
