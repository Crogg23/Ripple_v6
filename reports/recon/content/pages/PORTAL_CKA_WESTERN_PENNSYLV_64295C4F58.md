# PORTAL_CKA_WESTERN_PENNSYLV_64295C4F58

rows 5.5K  columns 14  scan 4.2s

roles: audit 2, category 1, date 1, other 7, who 4

## when

INGESTED_AT
  2026      5.5K  ##############################

## who

FIRM_NAME by rows
         5  C. L. RUSSELL GROUP
         5  BELLMAX ELECTRIC LLC
         4  INTERDYNAMICS INC
         4  AXIOS SERVICES LLC
         4  STRATEGIC COMMUNITY ENGAGEMENT, LLC
         4  LTU SOLUTIONS, LLC
         4  EDGEALL INC
         4  EGROVE SYSTEMS CORPORATION
         4  ANAVI STRATEGIES
         4  BRITTS INDUSTRIES, INC.
         4  TALANTAGE LLC
         4  SUMMIT HEALTHCARE SOLUTIONS LLC
         4  COLLABRIUM SYSTEMS LLC
         4  CLIMATE CAPITAL STRATEGIES, INC.
         4  Big Jet LLC
         4  HUMMING BIRDS CONSULTING, LLC
         4  PRESENT SOFTWARE INC
         3  MONTAGE TECHNOLOGY PARTNERS, LLC
         3  COLLABORATIVE PLANNING GROUP SYSTEM
         3  DEVELOPMENT COUNSELLORS INTERNATIONAL

OWNERS by rows
         6  Elizabeth Britt
         6  Jennifer Johnson
         6  Sangeetha Kancherla
         5  Nabaneeta Ray
         5  Gerald Mensah
         5  David Simpkins
         5  Donald Crenshaw
         4  Renu Agarwal
         4  Brigette Bethea
         4  Michelle Schrock
         4  Wayne Purville
         4  Keith Searles
         4  Jose Fuertes
         4  Todd Boucher
         4  J. Nicole Lawton
         4  Dana Heller
         4  CHRISTINE MEYER
         4  Brandy Weatherspoon
         4  Juan Williams
         4  Sara Sargent

VENDOR_ID by rows
         6  20271032
         6  20932274
         5  20423999
         4  20990711
         4  20287825
         4  20137147
         4  20043560
         4  21018547
         4  20951959
         4  21332595
         4  20955198
         4  20137158
         4  20710358
         4  20232795
         4  20275656
         4  20233199
         3  20152493
         3  21277322
         3  20401418
         3  20510213

SRC_SHA256 by rows
      5.5K  d2254064d2b911e11df48f9b74ffa7adb0123139974551ab7e0c4f406faed833

## who x when

FIRM_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ANAVI STRATEGIES                          2026:4
  AXIOS SERVICES LLC                        2026:4
  BELLMAX ELECTRIC LLC                      2026:5
  BRITTS INDUSTRIES, INC.                   2026:4
  Big Jet LLC                               2026:4
  C. L. RUSSELL GROUP                       2026:5
  CLIMATE CAPITAL STRATEGIES, INC.          2026:4
  COLLABORATIVE PLANNING GROUP SYSTEM       2026:3
  COLLABRIUM SYSTEMS LLC                    2026:4
  DEVELOPMENT COUNSELLORS INTERNATIONAL     2026:3
  EDGEALL INC                               2026:4
  EGROVE SYSTEMS CORPORATION                2026:4
  HUMMING BIRDS CONSULTING, LLC             2026:4
  INTERDYNAMICS INC                         2026:4
  LTU SOLUTIONS, LLC                        2026:4
  MONTAGE TECHNOLOGY PARTNERS, LLC          2026:3
  PRESENT SOFTWARE INC                      2026:4
  STRATEGIC COMMUNITY ENGAGEMENT, LLC       2026:4
  SUMMIT HEALTHCARE SOLUTIONS LLC           2026:4
  TALANTAGE LLC                             2026:4

OWNERS by INGESTED_AT  LOAD STAMP, not an event date
  Brandy Weatherspoon                       2026:4
  Brigette Bethea                           2026:4
  CHRISTINE MEYER                           2026:4
  Dana Heller                               2026:4
  David Simpkins                            2026:5
  Donald Crenshaw                           2026:5
  Elizabeth Britt                           2026:6
  Gerald Mensah                             2026:5
  J. Nicole Lawton                          2026:4
  Jennifer Johnson                          2026:6
  Jose Fuertes                              2026:4
  Juan Williams                             2026:4
  Keith Searles                             2026:4
  Michelle Schrock                          2026:4
  Nabaneeta Ray                             2026:5
  Renu Agarwal                              2026:4
  Sangeetha Kancherla                       2026:6
  Sara Sargent                              2026:4
  Todd Boucher                              2026:4
  Wayne Purville                            2026:4

## what

CERTIFICATION_TYPE: DBE 46%, WBE 28%, MBE 23%, ACDBE 4%, DBE (FAA Only) 0%, W/DBE 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| VENDOR_ID | who | 4.3K | 0 | 20071633 29; 21332980 29; 20137753 28; 20043382 28 |
| CERTIFICATION_TYPE | category | 6 | 0 | DBE 2.5K; WBE 1.5K; MBE 1.2K; ACDBE 216 |
| FIRM_NAME | who | 4.7K | 0 | Birkdesign Inc. 29; Neff Specialties, LLC 28; Streamline Engineering, I 28; PROSHARE SERVICES LLC 28 |
| OWNERS | who | 4.1K | 0 | JinJa Birkenbeuel 29; Shari Neff 28; Martha Frech 28; Danielle Baughman 28 |
| WORK_DESCRIPTION | other | 4.3K | 82 | Civil engineering 69; Business and corporate ma 46; Temporary personnel servi 31; Hospitality management wi 28 |
| NAICS_CODES | other | 4.0K | 0 | NA 79; 81101500 67; 541330 64; 541611 49 |
| PHYSICAL_ADDRESS | other | 4.7K | 0 | 2012 W. Augusta Chicago,  29; 1505 Main Street Hastings 28; 21 Sunrise Drive Leechbur 28; 113 Hemlock Street Pittsb 28 |
| PHONE_NUMBER | other | 4.3K | 0 | () - 70; (814) 247-8887 28; (724) 594-0326 28; (814) 242-2004 28 |
| FAX_NUMBER | other | 2.2K | 0 | () - 2.7K; (0) 000-0000 59; (312) 227-0208 15; (570) 829-6448 15 |
| EMAIL_ADDRESS | other | 4.5K | 2 | birkdesign@gmail.com 29; shari@neffspecialties.com 28; mfrech@streamlineengineer 28; DANIELLEBAUGHMAN@PROSHARE 28 |
| WEBSITE | other | 539 | 4.7K | http://WWW.WWLLCPROCUREME 7; http://www.cpromgt.com 6; http://www.tristatewaters 6; http://www.birkcreative.c 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:01:31.17649 5.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 012a30c4-9bae-4a69-a4e6-a 5.5K |
| SRC_SHA256 | who | 1 | 0 | d2254064d2b911e11df48f9b7 5.5K |
